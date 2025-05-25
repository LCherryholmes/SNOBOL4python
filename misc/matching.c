#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <printf.h>
#include <malloc.h>
#include <assert.h>
#include <stdbool.h>
//======================================================================================================================
// PATTERN data type
//----------------------------------------------------------------------------------------------------------------------
#define ABORT   0 // ABORT
#define ANY     1 // ANY$
#define ARB     2 // ARB
#define ARBNO   3 // ARBNO
#define BAL     4 // BAL
#define BREAK   5 // BREAK$
#define BREAKX  6 // BREAKX
#define FAIL    7 // FAIL
#define FENCE   8 // FENCE
#define LEN     9 // LEN#
#define MARB    10 // MARB
#define MARBNO  11 // MARBNO
#define NOTANY  12 // NOTANY$
#define POS     13 // POS#
#define REM     14 // REM
#define RPOS    15 // RPOS#
#define RTAB    16 // RTAB
#define SPAN    17 // SPAN$
#define SUCCESS 18 // SUCCESS
#define TAB     19 // TAB
#define Shift   20 // Shift
#define Reduce  21 // Reduce
#define Pop     22 // Pop
#define nInc    23 // nInc
#define nPop    24 // nPop
#define nPush   25 // nPush
#define Δ       26 // DELTA // "Δ"
#define Θ       27 // Θ
#define Λ       28 // Λ
#define Π       29 // ALT // "Π"
#define Σ       30 // SEQ // "Σ"
#define Φ       31 // Φ
#define α       32 // α
#define δ       33 // δ
#define ε       34 // epsilon // "ε"
#define ζ       35 // zeta // "ζ"
#define θ       36 // θ
#define λ       37 // lambda // "λ"
#define π       38 // π
#define ρ       39 // ρ
#define σ       40 // LIT$ // "σ"
#define φ       41 // φ
#define ω       42 // ω
//----------------------------------------------------------------------------------------------------------------------
static const char * types[] =
{
    "ABORT", "ANY$", "ARB", "ARBNO", "BAL", "BREAK$", "BREAKX", "FAIL", "FENCE", "LEN#", "MARB", "MARBNO", "NOTANY$",
    "POS#", "REM", "RPOS#", "RTAB", "SPAN$", "SUCCESS", "TAB", "Shift", "Reduce", "Pop", "nInc", "nPop", "nPush",
    "DELTA" /*Δ*/, "Θ", "Λ", "ALT" /*Π*/, "SEQ" /*Σ*/, "Φ", "α", "δ", "epsilon" /*ε*/, "zeta" /*ζ*/, "θ",
    "lambda" /*λ*/, "π", "ρ", "LIT$" /*σ*/, "φ", "ω"
};
//----------------------------------------------------------------------------------------------------------------------
typedef struct PATTERN PATTERN;
typedef struct PATTERN {
    int type;
    union {
        const int       n;         /* POS, RPOS, Σ, Π */
        const char *    s;         /* σ, δ, Δ */
        const char *    t;         /* Shift, Reduce */
    };
    union {
        const PATTERN * AP[30];    /* Δ */
        const char *    N;         /* ζ */
        const char *    command;   /* λ */
        const char *    chars;     /* ANY, NOTANY, SPAN, BREAK */
        const char *    v;         /* Shift, Pop */
        int             x;         /* Reduce */
    };
} PATTERN;
//----------------------------------------------------------------------------------------------------------------------
#include "BEAD_PATTERN.h"
#include "BEARDS_PATTERN.h"
#include "C_PATTERN-calculate.h"
#include "RE_PATTERN.h"
//======================================================================================================================
// Heap memory management
const int HEAP_SIZE_INIT  = 32768;
const int HEAP_SIZE_BUMP  = 32768;
const int HEAP_HEAD_SIZE  = 8;
const int HEAP_ALIGN_SIZE = 16;
const int HEAP_ALIGN_BITS = 4;
#define STAMP_STRING -1
#define STAMP_COMMAND -2
#define STAMP_STATE -3
//----------------------------------------------------------------------------------------------------------------------
typedef struct _address { int offset; } address_t;
typedef struct _heap { int pos; int size; unsigned char * a; } heap_t;
typedef struct _head { short stamp; short refs; int size; } head_t;
//----------------------------------------------------------------------------------------------------------------------
static heap_t heap = {0, 0, NULL};
static void heap_init() { heap.pos = 0; heap.size = 0; heap.a = NULL; }
static void heap_fini() { heap.pos = 0; heap.size = 0; free(heap.a); heap.a = NULL; }
static inline void * pointer(address_t a) { return heap.a + a.offset; }
static inline address_t heap_incref(address_t a) {
    if (a.offset > 0) {
        head_t * h = (head_t *) &heap.a[a.offset];
        h[-1].refs++;
    }
    return a;
}
static inline address_t heap_decref(address_t a) {
    if (a.offset > 0) {
        head_t * h = (head_t *) &heap.a[a.offset];
        assert(h[-1].refs > 0);
        h[-1].refs--;
    }
    return a;
}
//----------------------------------------------------------------------------------------------------------------------
static address_t heap_alloc(short stamp, int size) {
    assert(size < HEAP_SIZE_BUMP);
    size = (size + HEAP_ALIGN_SIZE-1) >> HEAP_ALIGN_BITS << HEAP_ALIGN_BITS;
    if (heap.pos + HEAP_ALIGN_SIZE + size >= heap.size) {
        if (heap.a == NULL) {
            heap.a = (unsigned char *) malloc(HEAP_SIZE_INIT);
            memset(heap.a, 0, HEAP_SIZE_INIT);
            heap.size = HEAP_SIZE_INIT;
        } else {
            heap.a = (unsigned char *) realloc(heap.a, heap.size + HEAP_SIZE_BUMP);
            memset(heap.a + heap.size, 0, HEAP_SIZE_BUMP);
            heap.size += HEAP_SIZE_BUMP;
        }
        if (false) printf("heap_alloc=(0x%08.8X, %d, %d)\n", heap.a, heap.pos, heap.size);
    }
    address_t a = {heap.pos + HEAP_HEAD_SIZE};
    head_t * h = (head_t *) &heap.a[a.offset];
    h[-1] = (head_t) {stamp, 1, size};
    heap.pos = a.offset + size;
    if (false) printf("0x%08.8X: %2d %3d %5d alloc\n", a.offset, h[-1].stamp, h[-1].refs, h[-1].size);
    return a;
}
//----------------------------------------------------------------------------------------------------------------------
static address_t heap_free(address_t a) {
    if (a.offset) {
        head_t * h = (head_t *) &heap.a[a.offset];
        if (false) printf("0x%08.8X: %2d %3d %5d free\n", a.offset, h[-1].stamp, h[-1].refs, h[-1].size);
        heap_decref(a);
    }
}
//======================================================================================================================
static address_t alloc_string(const char * string) {
    address_t address = heap_alloc(STAMP_STRING, strlen(string) + 1);
    char * mem = (char *) pointer(address);
    strcpy(mem, string);
    return address;
}
//----------------------------------------------------------------------------------------------------------------------
typedef struct _command command_t;
typedef struct _command { address_t string; address_t command; } command_t;
//----------------------------------------------------------------------------------------------------------------------
static inline const char * _s_(address_t address) { return (const char *) (heap.a + address.offset); }
static inline command_t * _c_(address_t address)  { return (command_t *) (heap.a + address.offset); }
static address_t alloc_command() { return heap_alloc(STAMP_COMMAND, sizeof(command_t)); }
static address_t push_command(address_t command, const char * string) {
    address_t COMMAND = alloc_command();
    _c_(COMMAND)->string = alloc_string(string);
    _c_(COMMAND)->command = heap_incref(command);
    return COMMAND;
}
static address_t pop_command(address_t command) {
    address_t COMMAND = command;
    if (command.offset) {
        COMMAND = _c_(command)->command;
        heap_free(command);
    }
    return COMMAND;
}
//======================================================================================================================
typedef struct _state state_t;
typedef struct _state {
    const char *    SIGMA;
    int             DELTA;
    int             OMEGA;
    const char *    sigma;
    int             delta;
    const PATTERN * PI;
    int             ctx;
    address_t       psi; // state stack
    address_t       lambda; // command stack
} state_t;
//----------------------------------------------------------------------------------------------------------------------
static inline state_t * _z_(address_t address) { return (state_t *) (heap.a + address.offset); }
static state_t empty_state = {NULL, 0, 0, NULL, 0, NULL, 0, {0}, {0} };
static address_t alloc_state() { return heap_alloc(STAMP_STATE, sizeof(state_t)); }
static int       total_states(address_t psi) { int len = 0; for (; psi.offset; len++, psi = _z_(psi)->psi) /**/; return len; }
static address_t push_state(address_t psi, state_t * z) {
    address_t PSI = alloc_state();
    *(_z_(PSI)) = *z;
    _z_(PSI)->psi = heap_incref(psi);
    return PSI;
}
static address_t pop_state(address_t psi) {
    address_t PSI = psi;
    if (psi.offset) {
        PSI = _z_(psi)->psi;
        heap_free(PSI);
    }
    return PSI;
}
//----------------------------------------------------------------------------------------------------------------------
static int iTracks = 0;
static state_t * aTracks = NULL;
static void init_tracks() { iTracks = 0; aTracks = NULL; }
static void fini_tracks() { iTracks = 0; if (aTracks) free(aTracks); aTracks = NULL; }
static state_t * top_track() { if (iTracks > 0) return &aTracks[iTracks - 1]; else return NULL; }
static void push_track(state_t Z) { aTracks = realloc(aTracks, ++iTracks * sizeof(state_t)); aTracks[iTracks - 1] = Z; }
static void pop_track(state_t * z) {
    if (iTracks > 0) {
        state_t state = aTracks[iTracks - 1];
        aTracks = realloc(aTracks, --iTracks * sizeof(state_t));
        if (z) *z = state;
    } else if (z) *z = empty_state;
}
//----------------------------------------------------------------------------------------------------------------------
static void heap_print(state_t * z) {
    printf("zeta: 0x%8.8X 0x%8.8X %d %s\n\n", z->psi, z->lambda, z->ctx, z->PI ? types[z->PI->type] : "NULL");
    printf("tracks: %d\n", iTracks);
    for (int i = 0; i < iTracks; i++) {
        printf("0x%8.8X 0x%8.8X %d %s\n",
            aTracks[i].psi,
            aTracks[i].lambda,
            aTracks[i].ctx,
            types[aTracks[i].PI->type]
        );
    }
    printf("\n");
    printf("heap: 0x%08.8x %d %d\n", heap.a, heap.pos, heap.size);
    int size = -1;
    for (int offset = HEAP_HEAD_SIZE; size && offset < heap.size; ) {
        void * mem = &heap.a[offset];
        head_t * h = (head_t *) mem;
        printf("0x%08.8X: %2d %3d %5d ", offset, h[-1].stamp, h[-1].refs, h[-1].size);
        switch (h[-1].stamp) {
            case STAMP_STRING:  { const char *      s = (const char *) mem;      printf("%s", s); break; }
            case STAMP_COMMAND: { const command_t * c = (const command_t *) mem; printf("0x%8.8X, 0x%8.8X", c->string, c->command); break; }
            case STAMP_STATE: {
                const state_t * z = (const state_t *) mem;
                printf("0x%8.8X 0x%8.8X %d %s", z->psi, z->lambda, z->ctx, types[z->PI->type]);
                break;
            }
        }
        printf("\n");
        size = h[-1].size;
        if (size) size += HEAP_HEAD_SIZE;
        offset += size;
    }
}
//======================================================================================================================
typedef struct _num { int iN; int * aN; } num_t;
static num_t empty_num = {0, NULL};
//----------------------------------------------------------------------------------------------------------------------
static inline void N_init(num_t * N)    { N->iN = 0; N->aN = NULL; }
static inline void N_push(num_t * N)    { N->aN = realloc(N->aN, ++N->iN * sizeof(int));
                                          N->aN[N->iN - 1] = 0;
                                        }
static inline void N_inc(num_t * N)     { N->aN[N->iN - 1]++; }
static inline int  N_top(num_t * N)     { return N->aN[N->iN - 1]; }
static inline int  N_pop(num_t * N)     { if (N->aN && N->iN > 0) {
                                            int n = N->aN[N->iN - 1];
                                            N->aN = realloc(N->aN, --N->iN * sizeof(int));
                                            return n;
                                          }
                                        }
//======================================================================================================================
// Global variables
//----------------------------------------------------------------------------------------------------------------------
typedef struct entry_t { char * name; const void * value; } entry_t;
typedef struct bucket_t { int count; int capacity; entry_t * entries; } bucket_t;
typedef struct globals_t { int num_buckets; bucket_t * buckets; } globals_t;
static globals_t globals = {0, NULL};
static void globals_init() {
    globals.num_buckets = 4;
    globals.buckets = calloc(globals.num_buckets, sizeof(bucket_t));
}
static void globals_fini() {
    for (int i = 0; i < globals.num_buckets; i++) {
        for (int j = 0; j < globals.buckets[i].count; j++)
            free(globals.buckets[i].entries[j].name);
        free(globals.buckets[i].entries);
    }
    free(globals.buckets);
}
//----------------------------------------------------------------------------------------------------------------------
static unsigned int hash(const char * str, int num_buckets) {
    int c;
    unsigned int h = 5381;
    while ((c = *str++))
        h = ((h << 5) + h) + c; /* h * 33 + c */
    return h % num_buckets;
}
//----------------------------------------------------------------------------------------------------------------------
static const void * globals_lookup(const char * name) {
    unsigned int index = hash(name, globals.num_buckets);
    bucket_t * bucket = &globals.buckets[index];
    int low = 0, high = bucket->count - 1;
    while (low <= high) {
        int mid = (low + high) >> 1;
        int cmp = strcmp(name, bucket->entries[mid].name);
        if (cmp == 0) return bucket->entries[mid].value;
        else if (cmp < 0) high = mid - 1;
        else low = mid + 1;
    }
    return NULL;
}
//----------------------------------------------------------------------------------------------------------------------
static void globals_insert(const char * name, const void * value) {
    unsigned int index = hash(name, globals.num_buckets);
    bucket_t * bucket = &globals.buckets[index];
    int low = 0, high = bucket->count - 1;
    int pos = 0;
    while (low <= high) {
        int mid = (low + high) >> 1;
        int cmp = strcmp(name, bucket->entries[mid].name);
        if (cmp == 0) { bucket->entries[mid].value = value; return; } // using replacement logic
        else if (cmp < 0) high = mid - 1;
        else low = mid + 1;
    }
    pos = low;
    if (bucket->count >= bucket->capacity) {
        int bump_capacity = bucket->capacity == 0 ? 4 : bucket->capacity;
        int new_capacity = bucket->capacity + bump_capacity;
        entry_t * new_entries = realloc(bucket->entries, new_capacity * sizeof(entry_t));
        memset(&new_entries[bucket->capacity], 0, bump_capacity * sizeof(entry_t));
        bucket->entries = new_entries;
        bucket->capacity = new_capacity;
    }
    entry_t new_entry = {strdup(name), value};
    for (int i = bucket->count; i > pos; i--)
        bucket->entries[i] = bucket->entries[i - 1];
    bucket->entries[pos] = new_entry;
    bucket->count++;
}
//======================================================================================================================
#define PROCEED 0
#define SUCCEED 1
#define FAILURE 2
#define RECEDE  3
//----------------------------------------------------------------------------------------------------------------------
static const char * actions[4] = {
    ":proceed", // ↓ →↘
    ":succeed", // → ↑↗
    ":fail",    // ← ↑↙
    ":recede"   // ↑ ←↖
};
//----------------------------------------------------------------------------------------------------------------------
#define MAX_DEPTH 3
void preview(const PATTERN * PI, int depth) {
    int type = PI->type;
    if (depth >= MAX_DEPTH)     { printf("."); return; }
    switch (type) {
    case ε:         { printf("ε()"); break; }
    case σ:         { printf("\"%s\"", PI->s); break; }
    case λ:         { printf("λ(\"%s\")", PI->command); break; }
    case ζ:         { printf("ζ(\"%s\")", PI->N); break; }
    case LEN:       { printf("LEN(%d)", PI->n); break; }
    case POS:       { printf("POS(%d)", PI->n); break; }
    case RPOS:      { printf("RPOS(%d)", PI->n); break; }
    case ANY:       { printf("ANY(\"%s\")", PI->chars); break; }
    case SPAN:      { printf("SPAN(\"%s\")", PI->chars); break; }
    case BREAK:     { printf("BREAK(\"%s\")", PI->chars); break; }
    case NOTANY:    { printf("NOTANY(\"%s\")", PI->chars); break; }
    case ARBNO:     { printf("ARBNO("); preview(PI->AP[0], depth + 1); printf(")"); break; }
    case Δ:         { printf("Δ("); preview(PI->AP[0], depth + 1); printf(", \"%s\")", PI->s); break; }
    case δ:         { printf("δ("); preview(PI->AP[0], depth + 1); printf(", \"%s\")", PI->s); break; }
    case π:         { printf("π("); preview(PI->AP[0], depth + 1); printf(")"); break; }
    case FENCE:     { printf("FENCE("); if (PI->n > 0) preview(PI->AP[0], depth + 1); printf(")"); break; }
    case nPush:     { printf("nPush()"); break; }
    case nInc:      { printf("nInc()"); break; }
    case nPop:      { printf("nPop()"); break; }
    case Shift:     { if (PI->v)
                        printf("Shift(\"%s\", \"%s\")", PI->t, PI->v);
                      else printf("Shift(\"%s\")", PI->t);
                      break;
                    }
    case Reduce:    { if (PI->x)
                        printf("Reduce(\"%s\", %d)", PI->t, PI->x);
                      else printf("Reduce(\"%s\")", PI->t);
                      break;
                    }
    case Pop:       { printf("Pop(\"%s\")", PI->v); break; } // t
    case ARB:       { printf("ARB"); break; }
    case Π:
    case Σ:
    case ρ:         { printf("%s(", types[PI->type]);
                        for (int i = 0; i < PI->n && depth + 1 < MAX_DEPTH; i++) {
                            if (i) printf(" ");
                            preview(PI->AP[i], depth + 1);
                        }
                        printf(")");
                        break;
                    }
    default:        { printf("\n%s\n", types[type]); fflush(stdout); assert(0); break; }
    }
}
//----------------------------------------------------------------------------------------------------------------------
static int min(int x1, int x2) { if (x1 < x2) return x1; else return x2; }
static int max(int x1, int x2) { if (x1 > x2) return x1; else return x2; }
//----------------------------------------------------------------------------------------------------------------------
#define HEAD_WINDOW 16
#define TAIL_WINDOW 12
static void animate(int action, state_t Z, int iteration) {
//  --------------------------------------------------------------------------------------------------------------------
    char head[HEAD_WINDOW+3]; memset(head, 0, sizeof(head));
    char tail[TAIL_WINDOW+3]; memset(tail, 0, sizeof(tail));
    int α_delta = min(Z.DELTA, TAIL_WINDOW);
    int ω_delta = min(Z.OMEGA - Z.DELTA, HEAD_WINDOW);
    const char * sigma = NULL;
    int i;
    i = 0;
    tail[i++] = '"';
    for (sigma = Z.SIGMA - α_delta; sigma < Z.SIGMA;)
        tail[i++] = *(sigma++);
    tail[i++] = '"';
    tail[i++] = 0;
    i = 0;
    head[i++] = '"';
    for (sigma = Z.SIGMA + ω_delta; sigma > Z.SIGMA;)
        head[i++] = *(--sigma);
    head[i++] = '"';
    head[i++] = 0;
//  --------------------------------------------------------------------------------------------------------------------
    char status[20]; sprintf(status, "%s/%d", types[Z.PI->type], Z.ctx + 1);
    printf("%4d %2d %2d %-*s %*s %3d %*s  %-8s  ",
        iteration,
        iTracks,
        total_states(Z.psi),
        12, status,
        TAIL_WINDOW, tail,
        Z.DELTA,
        HEAD_WINDOW, head,
        actions[action]
    );
    preview(Z.PI, 0);
    printf("\n");
    fflush(stdout);
}
//----------------------------------------------------------------------------------------------------------------------
static bool Π_ARB(state_t * z) {
    if (z->DELTA + z->ctx <= z->OMEGA) {
        z->sigma += z->ctx;
        z->delta += z->ctx;
        return true;
    } else return false;
}
//----------------------------------------------------------------------------------------------------------------------
static bool Π_LITERAL(state_t * z, const char * string) {
    for ( z->sigma = z->SIGMA, z->delta = z->DELTA
        ; *string
        ; z->sigma++, z->delta++, string++) {
        if (*z->sigma == 0) return false;
        if (*z->sigma != *string) return false;
    }
    return true;
}
//----------------------------------------------------------------------------------------------------------------------
static bool Π_ANY(state_t * z, const char * chars) {
    z->sigma = z->SIGMA;
    z->delta = z->DELTA;
    if (*z->sigma != 0) {
        const char * c;
        for (c = chars; *c; c++)
            if (*z->sigma == *c)
                break;
        if (*c != 0) {
            z->sigma++;
            z->delta++;
            return true;
        } else return false;
    } else return false;
}
//----------------------------------------------------------------------------------------------------------------------
static bool Π_NOTANY(state_t * z, const char * chars) {
    z->sigma = z->SIGMA;
    z->delta = z->DELTA;
    if (*z->sigma != 0) {
        const char * c;
        for (c = chars; *c; c++)
            if (*z->sigma == *c)
                break;
        if (*c == 0) {
            z->sigma++;
            z->delta++;
            return true;
        } else return false;
    } else return false;
}
//----------------------------------------------------------------------------------------------------------------------
static bool Π_SPAN(state_t * z, const char * chars) {
    for ( z->sigma = z->SIGMA
        , z->delta = z->DELTA
        ; *z->sigma
        ; z->sigma++
        , z->delta++) {
        const char * c;
        for (c = chars; *c; c++)
            if (*z->sigma == *c)
                break;
        if (!*c) break;
    }
    return z->delta > z->DELTA;
}
//----------------------------------------------------------------------------------------------------------------------
static bool Π_BREAK(state_t * z, const char * chars) {
    for ( z->sigma = z->SIGMA
        , z->delta = z->DELTA
        ; *z->sigma
        ; z->sigma++
        , z->delta++) {
        const char * c;
        for (c = chars; *c; c++)
            if (*z->sigma == *c)
                break;
        if (*c) break;
    }
    return *z->sigma != 0;
}
//----------------------------------------------------------------------------------------------------------------------
static inline bool Π_move(state_t * z, int delta) {
    if (delta >= 0 && z->DELTA + delta <= z->OMEGA) {
          z->sigma += delta;
          z->delta += delta;
          return true;
    } else false;
}
static inline bool Π_POS(state_t * z)   { return z->PI->n == z->DELTA; }
static inline bool Π_RPOS(state_t * z)  { return z->PI->n == z->OMEGA - z->DELTA; }
static inline bool Π_alpha(state_t * z) { return z->DELTA == 0 || (z->DELTA > 0 && z->SIGMA[-1] == '\n'); }
static inline bool Π_omega(state_t * z) { return z->DELTA == z->OMEGA || (z->DELTA < z->OMEGA && z->SIGMA[0] == '\n'); }
static inline bool Π_LEN(state_t * z)   { return Π_move(z, z->PI->n); }
static inline bool Π_TAB(state_t * z)   { return Π_move(z, z->PI->n - z->DELTA); }
static inline bool Π_REM(state_t * z)   { return Π_move(z, z->OMEGA - z->DELTA); }
static inline bool Π_RTAB(state_t * z)  { return Π_move(z, z->OMEGA - z->DELTA - z->PI->n); }
//----------------------------------------------------------------------------------------------------------------------
static inline bool Π_nPush(state_t * z)  { z->lambda = push_command(z->lambda, "N = N_push(N)"); return true; }
static inline bool Π_nInc(state_t * z)   { z->lambda = push_command(z->lambda, "N_inc(N)");      return true; }
static inline bool Π_nPop(state_t * z)   { z->lambda = push_command(z->lambda, "N = N_pop(N)");  return true; }
//----------------------------------------------------------------------------------------------------------------------
static inline bool Π_Shift(state_t * z)  {
    char command_text[128];
    if (z->PI->t == NULL)       sprintf(command_text, "shift();");
    else if (z->PI->v == NULL)  sprintf(command_text, "shift(\"%s\");", z->PI->t);
    else                        sprintf(command_text, "shift(\"%s\", \"%s\");", z->PI->t, z->PI->v);
    z->lambda = push_command(z->lambda, command_text);
    return true;
}
//----------------------------------------------------------------------------------------------------------------------
static inline bool Π_Reduce(state_t * z) {
    char top_text[32];
    if      (z->PI->x == -2)    sprintf(top_text, "istack[itop + 1]");
    else if (z->PI->x == -1)    sprintf(top_text, "istack[itop]");
    else                        sprintf(top_text, "%s", z->PI->x);
    char command_text[128];
    sprintf(command_text, "reduce(\"%s\", \"%s\");", z->PI->t, top_text);
    z->lambda = push_command(z->lambda, command_text);
    return true;
}
//----------------------------------------------------------------------------------------------------------------------
static inline bool Π_Pop(state_t * z) {
    char command_text[128];
    if (z->PI->v == NULL)
        sprintf(command_text, "pop();");
    else sprintf(command_text, "pop(\"%s\");", z->PI->v);
    z->lambda = push_command(z->lambda, command_text);
    return true;
}
//----------------------------------------------------------------------------------------------------------------------
static inline bool Π_theta(state_t * z) {
    char command_text[128];
    if (strcmp(z->PI->N, "OUTPUT") == 0)
        sprintf(command_text, "printf(\" %d\");", z->DELTA);
    else sprintf(command_text, "%s = %d;", z->PI->N, z->DELTA);
    z->lambda = push_command(z->lambda, command_text);
    return true;
}
//----------------------------------------------------------------------------------------------------------------------
static inline bool Π_DELTA(state_t * z) {
    char command_text[128];
    if (strcmp(z->PI->N, "OUTPUT") == 0)
        sprintf(command_text, "printf(\"%%s\", subject[%d:%d]);", z->DELTA, z->delta);
    else sprintf(command_text, "%s = subject[%d:%d];", z->PI->N, z->DELTA, z->delta);
    z->lambda = push_command(z->lambda, command_text);
    return true;
}
//----------------------------------------------------------------------------------------------------------------------
static inline bool Π_lambda(state_t * z) {
    z->lambda = push_command(z->lambda, z->PI->command);
    return true;
}
//======================================================================================================================
static inline void ζ_down_context(state_t * z) {
    z->psi = push_state(z->psi, z);
    z->sigma = z->SIGMA;
    z->delta = z->DELTA;
    z->PI = z->PI->AP[z->ctx];
    z->ctx = 0;
}
//----------------------------------------------------------------------------------------------------------------------
static inline void ζ_down_select(state_t * z, const PATTERN * PI) {
    z->psi = push_state(z->psi, z);
    z->sigma = z->SIGMA;
    z->delta = z->DELTA;
    z->PI = PI;
    z->ctx = 0;
}
//----------------------------------------------------------------------------------------------------------------------
static inline void ζ_over(state_t * z, const PATTERN * PI) { z->sigma = z->SIGMA; z->delta = z->DELTA; z->ctx = 0; z->PI = PI; }
static inline void ζ_over_dynamic(state_t * z) { z->sigma = z->SIGMA; z->delta = z->DELTA; z->ctx = 0; z->PI = globals_lookup(z->PI->N); }
//----------------------------------------------------------------------------------------------------------------------
static inline void ζ_stay_next(state_t * z)                { z->sigma = z->SIGMA; z->delta = z->DELTA; z->ctx++; }
static inline void ζ_move_next(state_t * z)                { z->SIGMA = z->sigma; z->DELTA = z->delta; z->ctx++; }
//----------------------------------------------------------------------------------------------------------------------
static void ζ_up_success(state_t * z) {
    if (z->psi.offset) {
        z->PI = _z_(z->psi)->PI;
        z->ctx = _z_(z->psi)->ctx;
        z->psi = pop_state(z->psi);
    } else z->PI = NULL;
}
//----------------------------------------------------------------------------------------------------------------------
static void ζ_up_track_success(state_t * z) {
    state_t * track = top_track();
    track->SIGMA = z->SIGMA;
    track->DELTA = z->DELTA;
    track->sigma = z->sigma;
    track->delta = z->delta;
    if (z->psi.offset) {
        z->PI = _z_(z->psi)->PI;
        z->ctx = _z_(z->psi)->ctx;
        z->psi = pop_state(z->psi);
    } else z->PI = NULL;
}
//----------------------------------------------------------------------------------------------------------------------
static void ζ_up_fail(state_t * z) {
    if (z->psi.offset) {
        z->PI = _z_(z->psi)->PI;
        z->ctx = _z_(z->psi)->ctx;
        z->psi = pop_state(z->psi);
    } else z->PI = NULL;
}
//----------------------------------------------------------------------------------------------------------------------
static void MATCH(const char * pattern_name, const char * subject) {
    heap_init();
    init_tracks();
    int a = PROCEED;
    int iteration = 0;
    num_t num; num = empty_num;
    const PATTERN * pattern = globals_lookup(pattern_name);
    state_t Z = {subject, 0, strlen(subject), NULL, 0, pattern, 0, {0}, {0}};
    while (Z.PI) {
        iteration++; // if (iteration > 64) break;
        animate(a, Z, iteration);
        int t = Z.PI->type;
        switch (t<<2|a) {
//      ----------------------------------------------------------------------------------------------------------------
        case Π<<2|PROCEED:       if (Z.ctx < Z.PI->n)
                                    { a = PROCEED; push_track(Z);   ζ_down_context(&Z); break; }
                               else { a = RECEDE;  pop_track(&Z);                       break; }
        case Π<<2|SUCCEED:          { a = SUCCEED;                  ζ_up_success(&Z);   break; }
        case Π<<2|FAILURE:          { a = PROCEED;                  ζ_stay_next(&Z);    break; }
        case Π<<2|RECEDE:           { a = PROCEED;                  ζ_stay_next(&Z);    break; }
//      ----------------------------------------------------------------------------------------------------------------
        case Σ<<2|PROCEED:       if (Z.ctx < Z.PI->n)
                                    { a = PROCEED;                  ζ_down_context(&Z); break; }
                               else { a = SUCCEED;                  ζ_up_success(&Z);   break; }
        case Σ<<2|SUCCEED:          { a = PROCEED;                  ζ_move_next(&Z);    break; }
        case Σ<<2|FAILURE:          { a = RECEDE;  pop_track(&Z);                       break; }
        case Σ<<2|RECEDE:           { assert(0); }
//      ----------------------------------------------------------------------------------------------------------------
        case ARBNO<<2|PROCEED:   if (Z.ctx == 0)
                                    { a = SUCCEED; push_track(Z);   ζ_up_success(&Z);   break; }
                               else { a = PROCEED; push_track(Z);   ζ_down_select(&Z, Z.PI->AP[0]); break; }
        case ARBNO<<2|SUCCEED:      { a = SUCCEED;                  ζ_up_track_success(&Z); break; }
        case ARBNO<<2|FAILURE:      { a = RECEDE;  pop_track(&Z);                       break; }
        case ARBNO<<2|RECEDE:       { a = PROCEED;                  ζ_move_next(&Z);    break; }
//      ----------------------------------------------------------------------------------------------------------------
        case ARB<<2|PROCEED:     if (Π_ARB(&Z))
                                    { a = SUCCEED; push_track(Z);   ζ_up_success(&Z);   break; }
                               else { a = RECEDE;  pop_track(&Z);                       break; }
        case ARB<<2|RECEDE:         { a = PROCEED;                  ζ_stay_next(&Z);    break; }
//      ----------------------------------------------------------------------------------------------------------------
        case SUCCESS<<2|PROCEED:    { a = SUCCEED; push_track(Z);   ζ_up_success(&Z);   break; }
        case SUCCESS<<2|RECEDE:     { a = PROCEED;                  ζ_stay_next(&Z);    break; }
//      ----------------------------------------------------------------------------------------------------------------
        case π<<2|PROCEED:          { assert(0); break; }
        case ρ<<2|PROCEED:          { assert(0); break; }
        case FENCE<<2|PROCEED:      { assert(0); break; }
//      ----------------------------------------------------------------------------------------------------------------
        case σ<<2|PROCEED:          if (Π_LITERAL(&Z, Z.PI->s))     { a = SUCCEED; ζ_up_success(&Z);    break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);       break; }
        case ANY<<2|PROCEED:        if (Π_ANY(&Z, Z.PI->chars))     { a = SUCCEED; ζ_up_success(&Z);    break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);       break; }
        case NOTANY<<2|PROCEED:     if (Π_NOTANY(&Z, Z.PI->chars))  { a = SUCCEED; ζ_up_success(&Z);    break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);       break; }
        case SPAN<<2|PROCEED:       if (Π_SPAN(&Z, Z.PI->chars))    { a = SUCCEED; ζ_up_success(&Z);    break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);       break; }
        case BREAK<<2|PROCEED:      if (Π_BREAK(&Z, Z.PI->chars))   { a = SUCCEED; ζ_up_success(&Z);    break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);       break; }
        case POS<<2|PROCEED:        if (Π_POS(&Z))                  { a = SUCCEED; ζ_up_success(&Z);    break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);       break; }
        case RPOS<<2|PROCEED:       if (Π_RPOS(&Z))                 { a = SUCCEED; ζ_up_success(&Z);    break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);       break; }
        case LEN<<2|PROCEED:        if (Π_LEN(&Z))                  { a = SUCCEED; ζ_up_success(&Z);    break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);       break; }
        case α<<2|PROCEED:          if (Π_alpha(&Z))                { a = SUCCEED; ζ_up_success(&Z);    break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);       break; }
        case ω<<2|PROCEED:          if (Π_omega(&Z))                { a = SUCCEED; ζ_up_success(&Z);    break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);       break; }
//      ----------------------------------------------------------------------------------------------------------------
        case ζ<<2|PROCEED:          { a = PROCEED; ζ_over_dynamic(&Z);                      break; }
        case Δ<<2|PROCEED:          { a = PROCEED; Π_DELTA(&Z); ζ_over(&Z, Z.PI->AP[0]);    break; }
        case δ<<2|PROCEED:          { a = PROCEED; ζ_over(&Z, Z.PI->AP[0]);                 break; }
        case ε<<2|PROCEED:          { a = SUCCEED; ζ_up_success(&Z);                        break; }
        case λ<<2|PROCEED:          { a = SUCCEED; Π_lambda(&Z); ζ_up_success(&Z);          break; }
        case FAIL<<2|PROCEED:       { a = FAILURE; ζ_up_fail(&Z);                           break; }
        case ABORT<<2|PROCEED:      { a = FAILURE; Z.PI = NULL;                             break; }
        case nPush<<2|PROCEED:      { a = SUCCEED; Π_nPush(&Z); ζ_up_success(&Z);           break; }
        case nInc<<2|PROCEED:       { a = SUCCEED; Π_nInc(&Z); ζ_up_success(&Z);            break; }
        case nPop<<2|PROCEED:       { a = SUCCEED; Π_nPop(&Z); ζ_up_success(&Z);            break; }
        case Shift<<2|PROCEED:      { a = SUCCEED; Π_Shift(&Z); ζ_up_success(&Z);           break; }
        case Reduce<<2|PROCEED:     { a = SUCCEED; Π_Reduce(&Z); ζ_up_success(&Z);          break; }
        case Pop<<2|PROCEED:        { a = SUCCEED; Π_Pop(&Z); ζ_up_success(&Z);             break; }
        default:                    { printf("%s\n", t); fflush(stdout); assert(0);         break; }
        }
    }
    if (false) heap_print(&Z);
    fini_tracks();
    heap_fini();
}
//----------------------------------------------------------------------------------------------------------------------
static const PATTERN ARB_1 = {POS, .n=0};
static const PATTERN ARB_2 = {ARB};
static const PATTERN ARB_3 = {RPOS, .n=0};
static const PATTERN ARB_0 = {Σ, 3, {&ARB_1, &ARB_2, &ARB_3}};

static const PATTERN ARBNO_1 = {POS, .n=0};
static const PATTERN ARBNO_3 = {LEN, .n=1};
static const PATTERN ARBNO_2 = {ARBNO, 1, &ARBNO_3};
static const PATTERN ARBNO_4 = {RPOS, .n=0};
static const PATTERN ARBNO_0 = {Σ, 3, {&ARBNO_1, &ARBNO_2, &ARBNO_4}};

int main() {
    globals_init();
    globals_insert("BEAD",          &BEAD_0);
    globals_insert("BEARDS",        &BEARDS_0);
    globals_insert("C",             &C_0);
    globals_insert("X",             &C_3);
    globals_insert("Arb",           &ARB_0);
    globals_insert("Arbno",         &ARBNO_0);
    globals_insert("Quantifier",    &RE_Quantifier_0);
    globals_insert("Item",          &RE_Item_0);
    globals_insert("Factor",        &RE_Factor_0);
    globals_insert("Term",          &RE_Term_0);
    globals_insert("Expression",    &RE_Expression_0);
    globals_insert("RegEx",         &RE_RegEx_0);
//  MATCH("BEAD",   "READS");
//  MATCH("BEARDS", "ROOSTS");
    MATCH("C",      "x+y*z");
//  MATCH("Arb",    "xyz");
//  MATCH("Arbno",  "xyz");
//  MATCH("RegEx",  "x|yz");
    globals_fini();
}
//----------------------------------------------------------------------------------------------------------------------
