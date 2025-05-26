#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <printf.h>
#include <malloc.h>
#include <assert.h>
#include <stdbool.h>
//----------------------------------------------------------------------------------------------------------------------
#define DEBUG_HEAP false
#define DEBUG_MATCH true
#define DEBUG_COLLECT false
//======================================================================================================================
// PATTERN data type ===================================================================================================
//======================================================================================================================
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
#define SUCCEED 18 // SUCCEED
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
#define ω       42 // ω (omega MUST be last)
//----------------------------------------------------------------------------------------------------------------------
static const char * types[] =
{
    "ABORT", "ANY$", "ARB", "ARBNO", "BAL", "BREAK$", "BREAKX", "FAIL", "FENCE", "LEN#", "MARB", "MARBNO", "NOTANY$",
    "POS#", "REM", "RPOS#", "RTAB", "SPAN$", "SUCCEED", "TAB", "Shift", "Reduce", "Pop", "nInc", "nPop", "nPush",
    "DELTA" /*Δ*/, "Θ", "Λ", "ALT" /*Π*/, "SEQ" /*Σ*/, "Φ", "α", "delta" /*δ*/, "epsilon" /*ε*/, "zeta" /*ζ*/, "θ",
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
#include "C_PATTERN.h"
#include "CALC_PATTERN.h"
#include "TESTS_PATTERN.h"
#include "RE_PATTERN.h"
//======================================================================================================================
// Heap memory management ==============================================================================================
//======================================================================================================================
const int HEAP_SIZE_INIT  = 32768;
const int HEAP_SIZE_BUMP  = 32768;
const int HEAP_HEAD_SIZE  = 4;
const int HEAP_ALIGN_SIZE = 16;
const int HEAP_ALIGN_BITS = 4;
#define STAMP_STRING 1
#define STAMP_COMMAND 2
#define STAMP_STATE 3
//----------------------------------------------------------------------------------------------------------------------
typedef struct _address { int offset; } address_t;
typedef struct _heap { int current; int size; unsigned char * a; } heap_t;
typedef struct _head { unsigned int mark:1; unsigned int stamp:3; int address:14; int size:14; } head_t;
//----------------------------------------------------------------------------------------------------------------------
static head_t empty_head = {0, 0, 0, 0};
static heap_t heap = {0, 0, NULL};
static void heap_init() { heap.current = 0; heap.size = 0; heap.a = NULL; }
static void heap_fini() { heap.current = 0; heap.size = 0; free(heap.a); heap.a = NULL; }
static inline void * pointer(address_t a) { return &heap.a[a.offset]; }
static inline head_t * head_pointer(address_t a) { return &((head_t *) pointer(a))[-1]; }
static inline void heap_mark_set(address_t a)   { head_pointer(a)->mark = true; }
static inline void heap_mark_clear(address_t a) { head_pointer(a)->mark = false; }
//----------------------------------------------------------------------------------------------------------------------
static address_t heap_alloc(short stamp, int size) {
    assert(size < HEAP_SIZE_BUMP);
    size = (size + HEAP_ALIGN_SIZE-1) >> HEAP_ALIGN_BITS << HEAP_ALIGN_BITS;
    if (heap.current + HEAP_ALIGN_SIZE + size >= heap.size) {
        if (heap.a == NULL) {
            heap.a = (unsigned char *) malloc(HEAP_SIZE_INIT);
            memset(heap.a, 0, HEAP_SIZE_INIT);
            heap.size = HEAP_SIZE_INIT;
        } else {
            heap.a = (unsigned char *) realloc(heap.a, heap.size + HEAP_SIZE_BUMP);
            memset(heap.a + heap.size, 0, HEAP_SIZE_BUMP);
            heap.size += HEAP_SIZE_BUMP;
        }
        if (DEBUG_HEAP)
            fprintf(stderr, "heap_alloc=(0x%08.8X: %d, %d)\n", heap.a, heap.current, heap.size);
    }
    address_t a = {heap.current + HEAP_HEAD_SIZE};
    head_t * h = head_pointer(a);
    *h = (head_t) {0, stamp, 0, size};
    heap.current = a.offset + size;
    if (DEBUG_HEAP)
        fprintf(stderr, "0x%08.8X: %1d %3d %6d\n", a.offset, h->mark, h->stamp, h->size);
    return a;
}
//======================================================================================================================
typedef struct _command command_t;
typedef struct _command { address_t string; address_t lambda; } command_t;
//----------------------------------------------------------------------------------------------------------------------
static address_t alloc_string(const char * string) {
    address_t address = heap_alloc(STAMP_STRING, strlen(string) + 1);
    char * mem = (char *) pointer(address);
    strcpy(mem, string);
    return address;
}
//----------------------------------------------------------------------------------------------------------------------
static inline const char * CC(address_t address) { return (const char *) (heap.a + address.offset); }
static inline command_t * C(address_t address)  { return (command_t *) (heap.a + address.offset); }
static address_t alloc_command() { return heap_alloc(STAMP_COMMAND, sizeof(command_t)); }
static address_t push_command(address_t lambda, const char * string) {
    address_t s = alloc_string(string); // addresses always point backward
    address_t LAMBDA = alloc_command();
    C(LAMBDA)->string = s;
    C(LAMBDA)->lambda = lambda;
    return LAMBDA;
}
static address_t pop_command(address_t lambda) {
    address_t LAMBDA = lambda;
    if (lambda.offset) {
        LAMBDA = C(lambda)->lambda;
    }
    return LAMBDA;
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
    unsigned int    fenced:1;
    unsigned int    yielded:1;
    int             ctx:30;
    address_t       psi; // state stack
    address_t       lambda; // command stack
} state_t;
//----------------------------------------------------------------------------------------------------------------------
static inline state_t * S(address_t address) { return (state_t *) (heap.a + address.offset); }
static state_t empty_state = {NULL, 0, 0, NULL, 0, NULL, 0, 0, 0, {0}, {0} };
static address_t alloc_state() { return heap_alloc(STAMP_STATE, sizeof(state_t)); }
static int       total_states(address_t psi) { int len = 0; for (; psi.offset; len++, psi = S(psi)->psi) /**/; return len; }
static address_t push_state(address_t psi, state_t * z) {
    address_t PSI = alloc_state();
    *(S(PSI)) = *z;
    S(PSI)->psi = psi;
    return PSI;
}
static address_t pop_state(address_t psi) {
    address_t PSI = psi;
    if (psi.offset) {
        PSI = S(psi)->psi;
    }
    return PSI;
}
//----------------------------------------------------------------------------------------------------------------------
static int num_tracks = 0;
static state_t * tracks = NULL;
static void Ω_init() { num_tracks = 0; tracks = NULL; }
static void Ω_fini() { num_tracks = 0; if (tracks) free(tracks); tracks = NULL; }
static inline state_t * Ω_top() { if (num_tracks > 0) return &tracks[num_tracks - 1]; else return NULL; }
static void Ω_push(state_t * z) { tracks = realloc(tracks, ++num_tracks * sizeof(state_t)); tracks[num_tracks - 1] = *z; }
static void Ω_pop(state_t * z) {
    if (num_tracks > 0) {
        state_t state = tracks[num_tracks - 1];
        tracks = realloc(tracks, --num_tracks * sizeof(state_t));
        if (z) *z = state;
    } else if (z) *z = empty_state;
}
//----------------------------------------------------------------------------------------------------------------------
static void heap_display_entry(address_t a) {
    void * mem = pointer(a);
    head_t * h = head_pointer(a);
    fprintf(stderr, "0x%8.8X: %1d %2d 0x%08.8X 0x%08.8X: ", a.offset, h->mark, h->stamp, h->address, h->size);
    switch (h->stamp) {
        case STAMP_STRING: {
            const char * s = (const char *) mem;
            fprintf(stderr, "%s", s);
            break;
        }
        case STAMP_COMMAND: {
            const command_t * c = (const command_t *) mem;
            fprintf(stderr, "0x%8.8X 0x%8.8X", c->string, c->lambda);
            break;
        }
        case STAMP_STATE: {
            const state_t * z = (const state_t *) mem;
            fprintf(stderr, "0x%8.8X 0x%8.8X %d %s", z->psi, z->lambda, z->ctx, types[z->PI->type]);
            break;
        }

    }
    fprintf(stderr, "\n");
}
//----------------------------------------------------------------------------------------------------------------------
static void heap_print(state_t * z) {
    address_t source = {HEAP_HEAD_SIZE};
    int size = -1;
    for (; size && source.offset < heap.size; source.offset += size) {
        head_t * s = head_pointer(source);
        size = s->size;
        heap_display_entry(source);
        if (size) size += HEAP_HEAD_SIZE;
    }
    fprintf(stderr, "\n");
}
//======================================================================================================================
// Heap garbage collection =============================================================================================
//======================================================================================================================
static void heap_collect_1_states(address_t psi) {
    for (; psi.offset; psi = S(psi)->psi) {
        heap_mark_set(psi);
        heap_mark_set(S(psi)->lambda);
    }
}
//----------------------------------------------------------------------------------------------------------------------
static void heap_collect_1_commands(address_t lambda) {
    for (; lambda.offset; lambda = C(lambda)->lambda) {
        heap_mark_set(lambda);
        heap_mark_set(C(lambda)->string);
    }
}
//----------------------------------------------------------------------------------------------------------------------
static void heap_collect_1(state_t * z) {
    heap_collect_1_states(z->psi);
    heap_collect_1_commands(z->lambda);
    for (int i = 0; i < num_tracks; i++) {
        heap_collect_1_states(tracks[i].psi);
        heap_collect_1_commands(tracks[i].lambda);
    }
}
//----------------------------------------------------------------------------------------------------------------------
static inline void heap_adjust_entry(address_t a) {
    switch (head_pointer(a)->stamp) {
        case STAMP_STRING: break;
        case STAMP_COMMAND: {
            command_t * c = (command_t *) pointer(a);
            if (c->string.offset) c->string = (address_t) {head_pointer(c->string)->address};
            if (c->lambda.offset) c->lambda = (address_t) {head_pointer(c->lambda)->address};
            break;
        }
        case STAMP_STATE: {
            state_t * z = (state_t *) pointer(a);
            if (z->psi.offset)    z->psi    = (address_t) {head_pointer(z->psi)->address};
            if (z->lambda.offset) z->lambda = (address_t) {head_pointer(z->lambda)->address};
            break;
        }
        default: assert(0); break;
    }
}
//----------------------------------------------------------------------------------------------------------------------
static void heap_collect_2_calculate(state_t * z) {
    address_t destination = {HEAP_HEAD_SIZE};
    address_t source = {HEAP_HEAD_SIZE};
    for (int size = -1; size && source.offset < heap.size; source.offset += size) {
        head_t * s = head_pointer(source);
        size = s->size;
        if (size && s->mark) {
            s->address = destination.offset;
            destination.offset += size + HEAP_HEAD_SIZE;
        } else s->address = 0;
        if (size) size += HEAP_HEAD_SIZE;
    }
}
//----------------------------------------------------------------------------------------------------------------------
static void heap_collect_2_adjust(state_t * z) {
    address_t destination = {HEAP_HEAD_SIZE};
    address_t source = {HEAP_HEAD_SIZE};
    for (int size = -1; size && source.offset < heap.size; source.offset += size) {
        head_t * s = head_pointer(source);
        size = s->size;
        if (size && s->mark) heap_adjust_entry(source);
        if (size) size += HEAP_HEAD_SIZE;
    }
}
//----------------------------------------------------------------------------------------------------------------------
static void heap_collect_2(state_t * z) {
    heap_collect_2_calculate(z);
    heap_collect_2_adjust(z);
}
//----------------------------------------------------------------------------------------------------------------------
static void heap_collect_3(state_t * z) {
    address_t destination = {0};
    address_t source = {HEAP_HEAD_SIZE};
    for (int size = -1; size && source.offset < heap.size; source.offset += size) {
        head_t * s = head_pointer(source);
        size = s->size;
        if (size && s->mark) {
            destination = (address_t) {s->address};
            head_t * d = head_pointer(destination);
            memcpy(d, s, size + HEAP_HEAD_SIZE);
            d->address = 0;
            if (DEBUG_COLLECT)
                heap_display_entry(destination);
        }
        if (size) size += HEAP_HEAD_SIZE;
    }
    *head_pointer(destination) = empty_head;
}
//----------------------------------------------------------------------------------------------------------------------
static void heap_collect(state_t * z) {
    heap_collect_1(z);
    heap_collect_2(z);
    heap_collect_3(z);
}
//======================================================================================================================
// Global variable dictionary ==========================================================================================
//======================================================================================================================
typedef struct entry_t { char * name; const void * value; } entry_t;
typedef struct bucket_t { int count; int capacity; entry_t * entries; } bucket_t;
typedef struct globals_t { int num_buckets; bucket_t * buckets; } globals_t;
//----------------------------------------------------------------------------------------------------------------------
static globals_t globals = {0, NULL};
static void globals_init() {
    globals.num_buckets = 4;
    globals.buckets = calloc(globals.num_buckets, sizeof(bucket_t));
}
//----------------------------------------------------------------------------------------------------------------------
static void globals_fini() {
    for (int i = 0; i < globals.num_buckets; i++) {
        for (int j = 0; j < globals.buckets[i].count; j++) {
            free(globals.buckets[i].entries[j].name);
            free((void *) globals.buckets[i].entries[j].value);
        }
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
static const void * lookup(const char * name) {
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
static void assign(const char * name, const void * value) {
    unsigned int index = hash(name, globals.num_buckets);
    bucket_t * bucket = &globals.buckets[index];
    int low = 0, high = bucket->count - 1;
    int pos = 0;
    while (low <= high) {
        int mid = (low + high) >> 1;
        int cmp = strcmp(name, bucket->entries[mid].name);
        if (cmp == 0) {
            free((void *) bucket->entries[mid].value);
            bucket->entries[mid].value = value;
            return;
        }
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
//----------------------------------------------------------------------------------------------------------------------
static inline void assign_str(const char * name, const char * v) { return assign(name, strdup(v)); }
static inline void assign_int(const char * name, int v) { int * V = malloc(sizeof(int)); *V = v; return assign(name, V); }
static void assign_ptr(const char * name, const void * v) { const void ** V = malloc(sizeof(void *)); *V = v; return assign(name, V); }
//======================================================================================================================
// PATTERN scanners ====================================================================================================
//======================================================================================================================
#define PROCEED 0
#define SUCCESS 1
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
    if (depth >= MAX_DEPTH) { fprintf(stderr, "."); return; }
    int type = PI->type;
    switch (type) {
    case ε:         { fprintf(stderr, "ε"); break; }
    case α:         { fprintf(stderr, "α"); break; }
    case ω:         { fprintf(stderr, "ω"); break; }
    case σ:         { fprintf(stderr, "\"%s\"", PI->s); break; }
    case Λ:         { fprintf(stderr, "Λ(\"%s\")", PI->command); break; }
    case λ:         { fprintf(stderr, "λ(\"%s\")", PI->command); break; }
    case ζ:         { fprintf(stderr, "ζ(\"%s\")", PI->N); break; }
    case Θ:         { fprintf(stderr, "Θ(\"%s\")", PI->N); break; }
    case θ:         { fprintf(stderr, "θ(\"%s\")", PI->N); break; }
    case Φ:         { fprintf(stderr, "Φ(\"%s\")", PI->N); break; }
    case φ:         { fprintf(stderr, "φ(\"%s\")", PI->N); break; }
    case POS:       { fprintf(stderr, "POS(%d)", PI->n); break; }
    case TAB:       { fprintf(stderr, "TAB(%d)", PI->n); break; }
    case LEN:       { fprintf(stderr, "LEN(%d)", PI->n); break; }
    case RTAB:      { fprintf(stderr, "RTAB(%d)", PI->n); break; }
    case RPOS:      { fprintf(stderr, "RPOS(%d)", PI->n); break; }
    case ANY:       { fprintf(stderr, "ANY(\"%s\")", PI->chars); break; }
    case SPAN:      { fprintf(stderr, "SPAN(\"%s\")", PI->chars); break; }
    case BREAK:     { fprintf(stderr, "BREAK(\"%s\")", PI->chars); break; }
    case BREAKX:    { fprintf(stderr, "BREAKX(\"%s\")", PI->chars); break; }
    case NOTANY:    { fprintf(stderr, "NOTANY(\"%s\")", PI->chars); break; }
    case ARBNO:     { fprintf(stderr, "ARBNO("); preview(PI->AP[0], depth + 1); fprintf(stderr, ")"); break; }
    case MARBNO:    { fprintf(stderr, "MARBNO("); preview(PI->AP[0], depth + 1); fprintf(stderr, ")"); break; }
    case Δ:         { fprintf(stderr, "Δ("); preview(PI->AP[0], depth + 1); fprintf(stderr, ", \"%s\")", PI->s); break; }
    case δ:         { fprintf(stderr, "δ("); preview(PI->AP[0], depth + 1); fprintf(stderr, ", \"%s\")", PI->s); break; }
    case π:         { fprintf(stderr, "π("); preview(PI->AP[0], depth + 1); fprintf(stderr, ")"); break; }
    case FENCE:     { if (PI->n > 0) {
                          fprintf(stderr, "FENCE(");
                          preview(PI->AP[0], depth + 1);
                          fprintf(stderr, ")");
                      } else fprintf(stderr, "FENCE");
                      break;
                    }
    case nPush:     { fprintf(stderr, "nPush()"); break; }
    case nInc:      { fprintf(stderr, "nInc()"); break; }
    case nPop:      { fprintf(stderr, "nPop()"); break; }
    case Shift:     { if (PI->v)
                        fprintf(stderr, "Shift(\"%s\", \"%s\")", PI->t, PI->v);
                      else fprintf(stderr, "Shift(\"%s\")", PI->t);
                      break;
                    }
    case Reduce:    { if (PI->x)
                        fprintf(stderr, "Reduce(\"%s\", %d)", PI->t, PI->x);
                      else fprintf(stderr, "Reduce(\"%s\")", PI->t);
                      break;
                    }
    case Pop:       { fprintf(stderr, "Pop(\"%s\")", PI->v); break; } // t
    case ARB:       { fprintf(stderr, "ARB"); break; }
    case BAL:       { fprintf(stderr, "BAL"); break; }
    case REM:       { fprintf(stderr, "REM"); break; }
    case FAIL:      { fprintf(stderr, "FAIL"); break; }
    case MARB:      { fprintf(stderr, "MARB"); break; }
    case ABORT:     { fprintf(stderr, "ABORT"); break; }
    case SUCCEED:   { fprintf(stderr, "SUCCEED"); break; }
    case Π:
    case Σ:
    case ρ:         { fprintf(stderr, "%s(", types[PI->type]);
                        for (int i = 0; i < PI->n && depth + 1 < MAX_DEPTH; i++) {
                            if (i) fprintf(stderr, " ");
                            preview(PI->AP[i], depth + 1);
                        }
                        fprintf(stderr, ")");
                        break;
                    }
    default:        { fprintf(stderr, "\n%s\n", types[type]); fflush(stdout); assert(0); break; }
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
    fprintf(stderr, "%4d %2d %2d %-*s %*s %3d %*s  %-8s  ",
        iteration,
        num_tracks,
        total_states(Z.psi),
        12, status,
        TAIL_WINDOW, tail,
        Z.DELTA,
        HEAD_WINDOW, head,
        actions[action]
    );
    preview(Z.PI, 0);
    fprintf(stderr, "\n");
    fflush(stderr);
}
//======================================================================================================================
static inline bool Π_ARB(state_t * z) {
    if (z->DELTA + z->ctx <= z->OMEGA) {
        z->sigma += z->ctx;
        z->delta += z->ctx;
        return true;
    } else return false;
}
//----------------------------------------------------------------------------------------------------------------------
static inline bool Π_MARB(state_t * z) {
    if (z->OMEGA - z->ctx >= z->DELTA) {
        z->sigma += z->ctx;
        z->delta += z->ctx;
        return true;
    } else return false;
}
//----------------------------------------------------------------------------------------------------------------------
static bool Π_BAL(state_t * z) {
    int nest = 0;
    z->sigma += z->ctx + 1;
    z->delta += z->ctx + 1;
    while (z->delta <= z->OMEGA) {
        char ch = z->sigma[-1];
        switch (ch) {
            case '(': nest += 1; break;
            case ')': nest -= 1; break;
        }
        if (nest < 0) break;
        else if (nest > 0 && z->delta >= z->OMEGA) break;
        else if (nest == 0) { z->ctx = z->delta; return true; }
        z->sigma++;
        z->delta++;
    }
    return false;
}
//----------------------------------------------------------------------------------------------------------------------
static bool Π_LITERAL(state_t * z) {
    const char * string = z->PI->s;
    for (; *string; z->sigma++, z->delta++, string++) {
        if (*z->sigma == 0) return false;
        if (*z->sigma != *string) return false;
    }
    return true;
}
//----------------------------------------------------------------------------------------------------------------------
static bool Π_ANY(state_t * z) {
    const char * chars = z->PI->chars;
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
static bool Π_NOTANY(state_t * z) {
    const char * chars = z->PI->chars;
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
static bool Π_SPAN(state_t * z) {
    const char * chars = z->PI->chars;
    for (; *z->sigma; z->sigma++, z->delta++) {
        const char * c;
        for (c = chars; *c; c++)
            if (*z->sigma == *c)
                break;
        if (!*c) break;
    }
    return z->delta > z->DELTA;
}
//----------------------------------------------------------------------------------------------------------------------
static bool Π_BREAK(state_t * z) {
    const char * chars = z->PI->chars;
    for (; *z->sigma; z->sigma++, z->delta++) {
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
//----------------------------------------------------------------------------------------------------------------------
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
static inline bool Π_delta(state_t * z) {
    if (strcmp(z->PI->s, "OUTPUT") == 0)
        printf("%.*s", z->delta - z->DELTA, z->sigma);
    else ;
    return true;
}
static inline bool Π_DELTA(state_t * z) {
    char command_text[128];
    if (strcmp(z->PI->s, "OUTPUT") == 0)
        sprintf(command_text, "printf(\"%%s\", subject[%d:%d]);", z->DELTA, z->delta);
    else sprintf(command_text, "%s = subject[%d:%d];", z->PI->s, z->DELTA, z->delta);
    z->lambda = push_command(z->lambda, command_text);
    return true;
}
//----------------------------------------------------------------------------------------------------------------------
static inline bool Π_LAMBDA(state_t * z) { return true; }
static inline bool Π_lambda(state_t * z) {
    z->lambda = push_command(z->lambda, z->PI->command);
    return true;
}
//----------------------------------------------------------------------------------------------------------------------
static inline bool Π_THETA(state_t * z) { return true; }
static inline bool Π_theta(state_t * z) {
    char command_text[128];
    if (strcmp(z->PI->N, "OUTPUT") == 0)
        sprintf(command_text, "printf(\" %d\");", z->DELTA);
    else sprintf(command_text, "%s = %d;", z->PI->N, z->DELTA);
    z->lambda = push_command(z->lambda, command_text);
    return true;
}
//----------------------------------------------------------------------------------------------------------------------
static inline bool Π_PHI(state_t * z)   { return true; }
static inline bool Π_phi(state_t * z)   { return true; }
//======================================================================================================================
static inline void ζ_down(state_t * z) {
    z->psi = push_state(z->psi, z);
    z->sigma = z->SIGMA;
    z->delta = z->DELTA;
    z->PI = z->PI->AP[z->ctx];
    z->ctx = 0;
}
//----------------------------------------------------------------------------------------------------------------------
static void ζ_down_single(state_t * z) {
    z->psi = push_state(z->psi, z);
    z->sigma = z->SIGMA;
    z->delta = z->DELTA;
    z->PI = z->PI->AP[0];
    z->ctx = 0;
}
//----------------------------------------------------------------------------------------------------------------------
static inline void ζ_over(state_t * z, const PATTERN * PI) { z->sigma = z->SIGMA; z->delta = z->DELTA; z->ctx = 0; z->PI = PI; }
static inline void ζ_over_dynamic(state_t * z) {
    assert(z->sigma == z->SIGMA); z->sigma = z->SIGMA;
    assert(z->delta == z->DELTA); z->delta = z->DELTA;
    z->ctx = 0;
    z->PI = * (const PATTERN **) lookup(z->PI->N);
}
//----------------------------------------------------------------------------------------------------------------------
static inline void ζ_next(state_t * z)      { z->sigma = z->SIGMA; z->delta = z->DELTA; }
static inline void ζ_stay_next(state_t * z) { z->sigma = z->SIGMA; z->delta = z->DELTA; z->yielded = false; z->ctx++; }
static inline void ζ_move_next(state_t * z) { z->SIGMA = z->sigma; z->DELTA = z->delta; z->yielded = false; z->ctx++; }
//----------------------------------------------------------------------------------------------------------------------
static void ζ_up(state_t * z) {
    if (z->psi.offset) {
        z->PI = S(z->psi)->PI;
        z->ctx = S(z->psi)->ctx;
        z->psi = pop_state(z->psi);
    } else z->PI = NULL;
}
//----------------------------------------------------------------------------------------------------------------------
static void ζ_up_track(state_t * z) {
    state_t * track = Ω_top();
    track->SIGMA = z->SIGMA;
    track->DELTA = z->DELTA;
    track->sigma = z->sigma;
    track->delta = z->delta;
    track->yielded = true;
    if (z->psi.offset) {
        z->PI = S(z->psi)->PI;
        z->ctx = S(z->psi)->ctx;
        z->psi = pop_state(z->psi);
    } else z->PI = NULL;
}
//----------------------------------------------------------------------------------------------------------------------
static void ζ_up_fail(state_t * z) {
    if (z->psi.offset) {
        z->PI = S(z->psi)->PI;
        z->ctx = S(z->psi)->ctx;
        z->psi = pop_state(z->psi);
    } else z->PI = NULL;
}
//----------------------------------------------------------------------------------------------------------------------
typedef struct _num { int iN; int * aN; } num_t;
static num_t empty_num = {0, NULL};
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
static void MATCH(const char * pattern_name, const char * subject) {
    Ω_init();
    heap_init();
    int a = PROCEED;
    int iteration = 0;
    num_t num; num = empty_num;
    const PATTERN * pattern = * (const PATTERN **) lookup(pattern_name);
    state_t Z = {subject, 0, strlen(subject), NULL, 0, pattern, 0, 0, 0, {0}, {0}};
    while (Z.PI) {
        iteration++; // if (iteration > 64) break;
        if (DEBUG_MATCH) animate(a, Z, iteration);
        int t = Z.PI->type;
        switch (t<<2|a) {
//      ----------------------------------------------------------------------------------------------------------------
        case Π<<2|PROCEED:       if (Z.ctx < Z.PI->n)
                                    { a = PROCEED; Ω_push(&Z);      ζ_down(&Z);                     break; }
                               else { a = RECEDE;  Ω_pop(&Z);                                       break; }
        case Π<<2|SUCCESS:          { a = SUCCESS;                  ζ_up(&Z);                       break; }
        case Π<<2|FAILURE:          { a = PROCEED;                  ζ_stay_next(&Z);                break; }
        case Π<<2|RECEDE:        if (!Z.fenced)
                                    { a = PROCEED;                  ζ_stay_next(&Z);                break; }
                               else { a = FAILURE;                  ζ_up_fail(&Z);                  break; }
//      ----------------------------------------------------------------------------------------------------------------
        case Σ<<2|PROCEED:       if (Z.ctx < Z.PI->n)
                                    { a = PROCEED;                  ζ_down(&Z);                     break; }
                               else { a = SUCCESS;                  ζ_up(&Z);                       break; }
        case Σ<<2|SUCCESS:          { a = PROCEED;                  ζ_move_next(&Z);                break; }
        case Σ<<2|FAILURE:          { a = RECEDE;  Ω_pop(&Z);                                       break; }
//      ----------------------------------------------------------------------------------------------------------------
        case ρ<<2|PROCEED:       if (Z.ctx < Z.PI->n)
                                    { a = PROCEED;                  ζ_down(&Z);                     break; }
                               else { a = SUCCESS;                  ζ_up(&Z);                       break; }
        case ρ<<2|SUCCESS:          { a = PROCEED;                  ζ_stay_next(&Z);                break; }
        case ρ<<2|FAILURE:          { a = RECEDE;  Ω_pop(&Z);                                       break; }
//      ----------------------------------------------------------------------------------------------------------------
        case π<<2|PROCEED:       if (Z.ctx == 0)
                                    { a = SUCCESS; Ω_push(&Z);      ζ_up(&Z);                       break; }
                            else if (Z.ctx == 1)
                                    { a = PROCEED; Ω_push(&Z);      ζ_down_single(&Z);              break; }
                               else { a = RECEDE;  Ω_pop(&Z);                                       break; }
        case π<<2|SUCCESS:          { a = SUCCESS;                  ζ_up(&Z);                       break; }
        case π<<2|FAILURE:          { a = FAILURE;                  ζ_up_fail(&Z);                  break; }
        case π<<2|RECEDE:        if (!Z.fenced)
                                    { a = PROCEED;                  ζ_stay_next(&Z);                break; }
                               else { a = FAILURE;                  ζ_up_fail(&Z);                  break; }
//      ----------------------------------------------------------------------------------------------------------------
        case ARBNO<<2|PROCEED:
                                 if (Z.ctx == 0)
                                    { a = SUCCESS; Ω_push(&Z);      ζ_up_track(&Z);                 break; }
                               else { a = PROCEED; Ω_push(&Z);      ζ_down_single(&Z);              break; }
        case ARBNO<<2|SUCCESS:
                                    { a = SUCCESS;                  ζ_up_track(&Z);                 break; }
        case ARBNO<<2|FAILURE:
                                    { a = RECEDE;  Ω_pop(&Z);                                       break; }
        case ARBNO<<2|RECEDE:
                                 if (Z.fenced)
                                    { a = FAILURE;                  ζ_up_fail(&Z);                  break; }
                            else if (Z.yielded)
                                    { a = PROCEED;                  ζ_move_next(&Z);                break; }
                               else { a = FAILURE;                  ζ_up_fail(&Z);                  break; }
//      ----------------------------------------------------------------------------------------------------------------
        case MARBNO<<2|PROCEED:     { assert(0); }
        case MARBNO<<2|RECEDE:      { assert(0); }
        case MARBNO<<2|SUCCESS:     { assert(0); }
        case MARBNO<<2|FAILURE:     { assert(0); }
//      ----------------------------------------------------------------------------------------------------------------
        case ARB<<2|PROCEED:     if (Π_ARB(&Z))
                                    { a = SUCCESS; Ω_push(&Z);      ζ_up(&Z);                       break; }
                               else { a = RECEDE;  Ω_pop(&Z);                                       break; }
        case ARB<<2|RECEDE:      if (!Z.fenced)
                                    { a = PROCEED;                  ζ_stay_next(&Z);                break; }
                               else { a = FAILURE;                  ζ_up_fail(&Z);                  break; }
//      ----------------------------------------------------------------------------------------------------------------
        case MARB<<2|PROCEED:    if (Π_MARB(&Z))
                                    { a = SUCCESS; Ω_push(&Z);      ζ_up(&Z);                       break; }
                               else { a = RECEDE;  Ω_pop(&Z);                                       break; }
        case MARB<<2|RECEDE:      if (!Z.fenced)
                                    { a = PROCEED;                  ζ_stay_next(&Z);                break; }
                               else { a = FAILURE;                  ζ_up_fail(&Z);                  break; }
//      ----------------------------------------------------------------------------------------------------------------
        case BAL<<2|PROCEED:     if (Π_BAL(&Z))
                                    { a = SUCCESS; Ω_push(&Z);      ζ_up(&Z);                       break; }
                               else { a = RECEDE;  Ω_pop(&Z);                                       break; }
        case BAL<<2|RECEDE:      if (!Z.fenced)
                                    { a = PROCEED;                  ζ_next(&Z);                     break; }
                               else { a = FAILURE;                  ζ_up_fail(&Z);                  break; }
//      ----------------------------------------------------------------------------------------------------------------
        case ABORT<<2|PROCEED:      { a = FAILURE;                  Z.PI = NULL;                    break; }
        case SUCCEED<<2|PROCEED:    { a = SUCCESS; Ω_push(&Z);      ζ_up(&Z);                       break; }
        case SUCCEED<<2|RECEDE:  if (!Z.fenced)
                                    { a = PROCEED;                  ζ_stay_next(&Z);                break; }
                               else { a = FAILURE;                  ζ_up_fail(&Z);                  break; }
        case FAIL<<2|PROCEED:       { a = FAILURE;                  ζ_up_fail(&Z);                  break; }
//      ----------------------------------------------------------------------------------------------------------------
        case FENCE<<2|PROCEED:   if (Z.PI->n == 0)
                                    { a = SUCCESS; Ω_push(&Z);      ζ_up(&Z);                       break; }
                            else if (Z.PI->n == 1)
                                    { a = PROCEED; Z.fenced = true; ζ_down_single(&Z);              break; }
        case FENCE<<2|RECEDE:    if (Z.PI->n == 0)
                                    { a = RECEDE;                   Z.PI = NULL;                    break; }
                            else if (Z.PI->n == 1)
                                    { assert(0); /* invalid */ }
        case FENCE<<2|SUCCESS:   if (Z.PI->n == 1)
                                    { a = SUCCESS; Z.fenced = false; ζ_up(&Z);                      break; }
                               else { assert(0); /* invalid */ }
        case FENCE<<2|FAILURE:   if (Z.PI->n == 1)
                                    { a = FAILURE; Z.fenced = false; ζ_up_fail(&Z);                 break; }
                               else { assert(0); /* invalid */ }
//      ----------------------------------------------------------------------------------------------------------------
        case Δ<<2|PROCEED:          { a = PROCEED;                  ζ_down_single(&Z);              break; }
        case Δ<<2|SUCCESS:          { a = SUCCESS; Π_DELTA(&Z);     ζ_up(&Z);                       break; }
        case Δ<<2|FAILURE:          { a = FAILURE;                  ζ_up_fail(&Z);                  break; }
//      ----------------------------------------------------------------------------------------------------------------
        case δ<<2|PROCEED:          { a = PROCEED;                  ζ_down_single(&Z);              break; }
        case δ<<2|SUCCESS:          { a = SUCCESS; Π_delta(&Z);     ζ_up(&Z);                       break; }
        case δ<<2|FAILURE:          { a = FAILURE;                  ζ_up_fail(&Z);                  break; }
//      ----------------------------------------------------------------------------------------------------------------
        case ζ<<2|PROCEED:          { a = PROCEED;                  ζ_over_dynamic(&Z);             break; }
//      ----------------------------------------------------------------------------------------------------------------
        case ε<<2|PROCEED:          { a = SUCCESS;                  ζ_up(&Z);                       break; }
        case Λ<<2|PROCEED:          { a = SUCCESS; Π_LAMBDA(&Z);    ζ_up(&Z);                       break; }
        case λ<<2|PROCEED:          { a = SUCCESS; Π_lambda(&Z);    ζ_up(&Z);                       break; }
        case Θ<<2|PROCEED:          { a = SUCCESS; Π_THETA(&Z);     ζ_up(&Z);                       break; }
        case θ<<2|PROCEED:          { a = SUCCESS; Π_theta(&Z);     ζ_up(&Z);                       break; }
        case Φ<<2|PROCEED:          { a = SUCCESS; Π_PHI(&Z);       ζ_up(&Z);                       break; }
        case φ<<2|PROCEED:          { a = SUCCESS; Π_phi(&Z);       ζ_up(&Z);                       break; }
        case nPush<<2|PROCEED:      { a = SUCCESS; Π_nPush(&Z);     ζ_up(&Z);                       break; }
        case nInc<<2|PROCEED:       { a = SUCCESS; Π_nInc(&Z);      ζ_up(&Z);                       break; }
        case nPop<<2|PROCEED:       { a = SUCCESS; Π_nPop(&Z);      ζ_up(&Z);                       break; }
        case Shift<<2|PROCEED:      { a = SUCCESS; Π_Shift(&Z);     ζ_up(&Z);                       break; }
        case Reduce<<2|PROCEED:     { a = SUCCESS; Π_Reduce(&Z);    ζ_up(&Z);                       break; }
        case Pop<<2|PROCEED:        { a = SUCCESS; Π_Pop(&Z);       ζ_up(&Z);                       break; }
//      ----------------------------------------------------------------------------------------------------------------
        case σ<<2|PROCEED:          if (Π_LITERAL(&Z))              { a = SUCCESS; ζ_up(&Z);        break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);   break; }
        case ANY<<2|PROCEED:        if (Π_ANY(&Z))                  { a = SUCCESS; ζ_up(&Z);        break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);   break; }
        case NOTANY<<2|PROCEED:     if (Π_NOTANY(&Z))               { a = SUCCESS; ζ_up(&Z);        break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);   break; }
        case SPAN<<2|PROCEED:       if (Π_SPAN(&Z))                 { a = SUCCESS; ζ_up(&Z);        break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);   break; }
        case BREAK<<2|PROCEED:      if (Π_BREAK(&Z))                { a = SUCCESS; ζ_up(&Z);        break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);   break; }
        case POS<<2|PROCEED:        if (Π_POS(&Z))                  { a = SUCCESS; ζ_up(&Z);        break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);   break; }
        case RPOS<<2|PROCEED:       if (Π_RPOS(&Z))                 { a = SUCCESS; ζ_up(&Z);        break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);   break; }
        case LEN<<2|PROCEED:        if (Π_LEN(&Z))                  { a = SUCCESS; ζ_up(&Z);        break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);   break; }
        case TAB<<2|PROCEED:        if (Π_TAB(&Z))                  { a = SUCCESS; ζ_up(&Z);        break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);   break; }
        case RTAB<<2|PROCEED:       if (Π_RTAB(&Z))                 { a = SUCCESS; ζ_up(&Z);        break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);   break; }
        case REM<<2|PROCEED:        if (Π_REM(&Z))                  { a = SUCCESS; ζ_up(&Z);        break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);   break; }
        case α<<2|PROCEED:          if (Π_alpha(&Z))                { a = SUCCESS; ζ_up(&Z);        break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);   break; }
        case ω<<2|PROCEED:          if (Π_omega(&Z))                { a = SUCCESS; ζ_up(&Z);        break; }
                                    else                            { a = FAILURE; ζ_up_fail(&Z);   break; }
//      ----------------------------------------------------------------------------------------------------------------
        default:                    { fprintf(stderr, "%d %s\n", t, t <= ω ? types[t] : "");
                                      fflush(stderr);
                                      assert(0);
                                      break;
                                    }
        }
    }
    heap_collect(&Z);
    heap_print(&Z);
    heap_fini();
    Ω_fini();
}
//======================================================================================================================
// Main test program ===================================================================================================
//======================================================================================================================
static const PATTERN ARB_1 = {POS, .n=0};
static const PATTERN ARB_2 = {ARB};
static const PATTERN ARB_3 = {RPOS, .n=0};
static const PATTERN ARB_0 = {Σ, 3, {&ARB_1, &ARB_2, &ARB_3}};

static const PATTERN ARBNO_1 = {POS, .n=0};
static const PATTERN ARBNO_3 = {LEN, .n=1};
static const PATTERN ARBNO_2 = {ARBNO, 1, &ARBNO_3};
static const PATTERN ARBNO_4 = {RPOS, .n=0};
static const PATTERN ARBNO_0 = {Σ, 3, {&ARBNO_1, &ARBNO_2, &ARBNO_4}};

static const PATTERN Bal_1 = {POS, .n=0};
static const PATTERN Bal_3 = {BAL};
static const PATTERN Bal_2 = {δ, .s="OUTPUT", &Bal_3};
static const PATTERN Bal_4 = {RPOS, .n=0};
static const PATTERN Bal_0 = {Σ, 3, {&Bal_1, &Bal_2, &Bal_4}};

int main() {
    globals_init();
    assign_ptr("BEAD",          &BEAD_0);
    assign_ptr("BEARDS",        &BEARDS_0);
    assign_ptr("C",             &C_0);
    assign_ptr("X",             &C_3);
    assign_ptr("CALC",          &CALC_0);
    assign_ptr("EXPR",          &CALC_3);
    assign_ptr("Arb",           &ARB_0);
    assign_ptr("Arbno",         &ARBNO_0);
    assign_ptr("RE_Quantifier", &RE_Quantifier_0);
    assign_ptr("RE_Item",       &RE_Item_0);
    assign_ptr("RE_Factor",     &RE_Factor_0);
    assign_ptr("RE_Term",       &RE_Term_0);
    assign_ptr("RE_Expression", &RE_Expression_0);
    assign_ptr("RE_RegEx",      &RE_RegEx_0);
    assign_ptr("identifier",    &identifier_0);
    assign_ptr("real_number",   &real_number_0);
    assign_ptr("Bal",           &Bal_0);
//  MATCH("BEAD",       "READS");
//  MATCH("BEARDS",     "ROOSTS");
//  MATCH("C",          "x+y*z");
//  MATCH("CALC",       "x+y*z");
//  MATCH("Arb",        "");
//  MATCH("Arb",        "x");
//  MATCH("Arb",        "xy");
//  MATCH("Arb",        "xyz");
//  MATCH("Arbno",      "");
//  MATCH("Arbno",      "x");
//  MATCH("Arbno",      "xy");
//  MATCH("Arbno",      "xyz");
//  MATCH("identifier", "x");
//  MATCH("identifier", "Id_99");
//  MATCH("identifier", "Id+");
//  MATCH("real_number","12.99E+3");
//  MATCH("real_number","12990.0");
//  MATCH("Bal",        ")A+B(");
//  MATCH("Bal",        "A+B)");
//  MATCH("Bal",        "(A+B");
//  MATCH("Bal",        "(A+B)");
    MATCH("RE_RegEx",   "x|yz");
    globals_fini();
}
//======================================================================================================================
