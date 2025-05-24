#include <malloc.h>
#include <assert.h>
#include <string.h>
#include <printf.h>
#include <stdbool.h>
//======================================================================================================================
static const char ABORT[]   = "ABORT";
static const char ANY[]     = "ANY$";
static const char ARBNO[]   = "ARBNO";
static const char ARB[]     = "ARB";
static const char BAL[]     = "BAL";
static const char BREAKX[]  = "BREAKX";
static const char BREAK[]   = "BREAK$";
static const char FAIL[]    = "FAIL";
static const char FENCE[]   = "FENCE";
static const char LEN[]     = "LEN#";
static const char MARBNO[]  = "MARBNO";
static const char MARB[]    = "MARB";
static const char NOTANY[]  = "NOTANY$";
static const char POS[]     = "POS#";
static const char REM[]     = "REM";
static const char RPOS[]    = "RPOS#";
static const char RTAB[]    = "RTAB";
static const char SPAN[]    = "SPAN$";
static const char SUCCESS[] = "SUCCESS";
static const char TAB[]     = "TAB";
static const char Shift[]   = "Shift";
static const char Reduce[]  = "Reduce";
static const char Pop[]     = "Pop";
static const char nInc[]    = "nInc";
static const char nPop[]    = "nPop";
static const char nPush[]   = "nPush";
static const char Δ[]       = "DELTA"; // "Δ";
static const char Θ[]       = "Θ";
static const char Λ[]       = "Λ";
static const char Π[]       = "ALT"; // "Π";
static const char Σ[]       = "SEQ"; // "Σ";
static const char Φ[]       = "Φ";
static const char α[]       = "α";
static const char δ[]       = "δ";
static const char ε[]       = "epsilon"; // "ε";
static const char ζ[]       = "zeta"; // "ζ";
static const char θ[]       = "θ";
static const char λ[]       = "lambda"; // "λ";
static const char π[]       = "π";
static const char ρ[]       = "ρ";
static const char σ[]       = "LIT$"; // "σ";
static const char φ[]       = "φ";
static const char ω[]       = "ω";
//======================================================================================================================
typedef struct PATTERN PATTERN;
typedef struct PATTERN {
    const char * type;
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
//======================================================================================================================
#include "BEAD_PATTERN.h"
#include "BEARDS_PATTERN.h"
#include "C_PATTERN.h"
#include "RE_PATTERN.h"
//======================================================================================================================
#define HEAP_SIZE_INIT 4096
#define HEAP_SIZE_BUMP 4096
#define HEAP_ALIGN_SIZE 8
#define HEAP_ALIGN_BITS 3
#define STAMP_STRING -1
#define STAMP_COMMAND -2
#define STAMP_STATE -3
//----------------------------------------------------------------------------------------------------------------------
typedef struct _address { int offset; } address_t;
typedef struct _heap { int pos; int size; unsigned char * a; } heap_t;
static heap_t heap = {0, 0, NULL};
static heap_t empty_heap = {0, 0, NULL};
static void heap_init() { heap.pos = 0; heap.size = 0; heap.a = NULL; }
static void heap_free() { heap.pos = 0; heap.size = 0; free(heap.a); heap.a = NULL; }
static inline void * pointer(address_t address) { return heap.a + address.offset; }
static address_t heap_alloc(int stamp, int size) {
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
    }
    address_t address = {heap.pos + HEAP_ALIGN_SIZE};
    ((int *) &heap.a[address.offset])[-1] = stamp;
    heap.pos = address.offset + size;
    printf("0x%08.8x = heap_alloc()\n", address.offset);
    return address;
}
//======================================================================================================================
static address_t alloc_string(const char * string) {
    address_t address = heap_alloc(STAMP_STRING, strlen(string) + 1);
    char * mem = (char *) pointer(address);
    strcpy(mem, string);
    return address;
}
static inline const char * _string_(address_t address)  { return (const char *) (heap.a + address.offset); }
//----------------------------------------------------------------------------------------------------------------------
typedef struct _command command_t;
typedef struct _command { address_t string; address_t command; } command_t;
static inline command_t * _c_(address_t address)  { return (command_t *) (heap.a + address.offset); }
//----------------------------------------------------------------------------------------------------------------------
static address_t alloc_command() { return heap_alloc(STAMP_COMMAND, sizeof(command_t)); }
static address_t pop_command(address_t command) { if (command.offset) return _c_(command)->command; else return command; }
static address_t push_command(address_t command, const char * string) {
    address_t COMMAND = alloc_command();
    _c_(COMMAND)->string = alloc_string(string);
    _c_(COMMAND)->command = command;
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
static inline state_t * _s_(address_t address)      { return (state_t *) (heap.a + address.offset); }
//----------------------------------------------------------------------------------------------------------------------
static state_t empty_state = {NULL, 0, 0, NULL, 0, NULL, 0, {0}, {0} };
static address_t alloc_state() { return heap_alloc(STAMP_STATE, sizeof(state_t)); }
static int       total_states(address_t psi) { int len = 0; for (; psi.offset; len++, psi = _s_(psi)->psi) /**/; return len; }
static address_t pop_state(address_t psi) { if (psi.offset) return _s_(psi)->psi; else return psi; }
static address_t push_state(address_t psi, state_t * z) {
    address_t PSI = alloc_state();
    *(_s_(PSI)) = *z;
    _s_(PSI)->psi = psi;
    return PSI;
}
//----------------------------------------------------------------------------------------------------------------------
static int iTracks = 0;
static state_t *aTracks = NULL;
static void init_tracks() { iTracks = 0; aTracks = NULL; }
static void fini_tracks() { iTracks = 0; if (aTracks) free(aTracks); aTracks = NULL; }
static void push_track(state_t Z) { aTracks = realloc(aTracks, ++iTracks * sizeof(state_t)); aTracks[iTracks - 1] = Z; }
static void pop_track(state_t * z) {
    if (iTracks > 0) {
        state_t state = aTracks[iTracks - 1];
        aTracks = realloc(aTracks, --iTracks * sizeof(state_t));
        if (z) *z = state;
    } else if (z) *z = empty_state;
}
//======================================================================================================================
#define PROCEED 0
#define SUCCEED 1
#define FAILURE 2
#define RECEDE 3
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
    const char * type = PI->type;
    if (depth >= MAX_DEPTH)     { printf("."); return; }
    if      (type == ε)         { printf("ε()"); }
    else if (type == σ)         { printf("\"%s\"", PI->s); }
    else if (type == λ)         { printf("λ(\"%s\")", PI->command); }
    else if (type == ζ)         { printf("ζ(\"%s\")", PI->N); }
    else if (type == LEN)       { printf("LEN(%d)", PI->n); }
    else if (type == POS)       { printf("POS(%d)", PI->n); }
    else if (type == RPOS)      { printf("RPOS(%d)", PI->n); }
    else if (type == ANY)       { printf("ANY(\"%s\")", PI->chars); }
    else if (type == SPAN)      { printf("SPAN(\"%s\")", PI->chars); }
    else if (type == BREAK)     { printf("BREAK(\"%s\")", PI->chars); }
    else if (type == NOTANY)    { printf("NOTANY(\"%s\")", PI->chars); }
    else if (type == ARBNO)     { printf("ARBNO("); preview(PI->AP[0], depth + 1); printf(")"); }
    else if (type == Δ)         { printf("Δ("); preview(PI->AP[0], depth + 1); printf(", \"%s\")", PI->s); }
    else if (type == δ)         { printf("δ("); preview(PI->AP[0], depth + 1); printf(", \"%s\")", PI->s); }
    else if (type == π)         { printf("π("); preview(PI->AP[0], depth + 1); printf(")"); }
    else if (type == FENCE)     { printf("FENCE("); if (PI->n > 0) preview(PI->AP[0], depth + 1); printf(")"); }
    else if (type == nPush)     { printf("nPush()"); }
    else if (type == nInc)      { printf("nInc()"); }
    else if (type == nPop)      { printf("nPop()"); }
    else if (type == Shift)     { if (PI->v)
                                    printf("Shift(\"%s\", \"%s\")", PI->t, PI->v);
                                  else printf("Shift(\"%s\")", PI->t);
                                }
    else if (type == Reduce)    { if (PI->v)
                                    printf("Reduce(\"%s\", \"%s\")", PI->t, PI->v);
                                  else printf("Reduce(\"%s\")", PI->t);
                                }
    else if (type == Pop)       { printf("Pop(\"%s\")", PI->v); } // t
    else if (type == ARB)       { printf("ARB"); }
    else if (type == Π
         ||  type == Σ
         ||  type == ρ)         { printf("%s(", PI->type);
                                  for (int i = 0; i < PI->n && depth + 1 < MAX_DEPTH; i++) {
                                      if (i) printf(" ");
                                      preview(PI->AP[i], depth + 1);
                                  }
                                  printf(")");
                                }
    else { printf("\n%s\n", type); fflush(stdout); assert(0); }
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
    char status[20]; sprintf(status, "%s/%d", Z.PI->type, Z.ctx + 1);
    printf("%4d %2d %2d %-*s %*s %3d %*s  %-8s  ",
        iteration,
        total_states(Z.psi),
        iTracks,
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
static void ζ_down_context(state_t * z) {
    z->psi = push_state(z->psi, z);
    z->sigma = z->SIGMA;
    z->delta = z->DELTA;
    z->PI = z->PI->AP[z->ctx];
    z->ctx = 0;
}
//----------------------------------------------------------------------------------------------------------------------
static void ζ_down_select(state_t * z, const PATTERN * PI) {
    z->psi = push_state(z->psi, z);
    z->SIGMA = z->sigma;
    z->DELTA = z->delta;
    z->PI = PI;
    z->ctx = 0;
}
//----------------------------------------------------------------------------------------------------------------------
static void ζ_over(state_t * z, const PATTERN * PI) { z->sigma = z->SIGMA; z->delta = z->DELTA; z->ctx = 0; z->PI = PI; }
static void ζ_stay_next(state_t * z)                { z->sigma = z->SIGMA; z->delta = z->DELTA; z->ctx++; }
static void ζ_move_next(state_t * z)                { z->SIGMA = z->sigma; z->DELTA = z->delta; z->ctx++; }
//----------------------------------------------------------------------------------------------------------------------
static void ζ_up_success(state_t * z) {
    if (z->psi.offset) {
        z->PI = _s_(z->psi)->PI;
        z->ctx = _s_(z->psi)->ctx;
        z->psi = pop_state(z->psi);
    } else z->PI = NULL;
}
//----------------------------------------------------------------------------------------------------------------------
static void ζ_up_fail(state_t * z) {
    if (z->psi.offset) {
        z->PI = _s_(z->psi)->PI;
        z->ctx = _s_(z->psi)->ctx;
        z->psi = pop_state(z->psi);
    } else z->PI = NULL;
}
//----------------------------------------------------------------------------------------------------------------------
static void MATCH(const PATTERN * pattern, const char * subject) {
    heap_init();
    init_tracks();
    int a = PROCEED;
    int iteration = 0;
    num_t num; num = empty_num;
    state_t Z = {subject, 0, strlen(subject), NULL, 0, pattern, 0, {0}, {0}};
    while (Z.PI) {
        iteration++; if (iteration > 512) break;
        animate(a, Z, iteration);
        const char * t = Z.PI->type;
//      ----------------------------------------------------------------------------------------------------------------
        if      (t == Π       && a == PROCEED)   if (Z.ctx < Z.PI->n)
                                                    { a = PROCEED; push_track(Z);   ζ_down_context(&Z); }
                                               else { a = RECEDE;  pop_track(&Z);   }
        else if (t == Π       && a == SUCCEED)      { a = SUCCEED;                  ζ_up_success(&Z); }
        else if (t == Π       && a == FAILURE)      { a = PROCEED;                  ζ_stay_next(&Z); }
        else if (t == Π       && a == RECEDE)       { a = PROCEED;                  ζ_stay_next(&Z); }
//      ----------------------------------------------------------------------------------------------------------------
        else if (t == Σ       && a == PROCEED)   if (Z.ctx < Z.PI->n)
                                                    { a = PROCEED;                  ζ_down_context(&Z); }
                                               else { a = SUCCEED;                  ζ_up_success(&Z); }
        else if (t == Σ       && a == SUCCEED)      { a = PROCEED;                  ζ_move_next(&Z); }
        else if (t == Σ       && a == FAILURE)      { a = RECEDE;  pop_track(&Z);   }
        else if (t == Σ       && a == RECEDE)       { assert(0); }
//      ----------------------------------------------------------------------------------------------------------------
        else if (t == ARBNO   && a == PROCEED)
                                                 if (Z.ctx == 0)
                                                    { a = SUCCEED; push_track(Z);   ζ_up_success(&Z); }
                                               else { a = PROCEED; push_track(Z);   ζ_down_select(&Z, Z.PI->AP[0]); }
        else if (t == ARBNO   && a == SUCCEED)
                                                    { a = SUCCEED;                  ζ_up_success(&Z); }
        else if (t == ARBNO   && a == FAILURE)
                                                    { a = RECEDE;  pop_track(&Z);   }
        else if (t == ARBNO   && a == RECEDE)
                                                    { a = PROCEED;                  ζ_move_next(&Z); }
//      ----------------------------------------------------------------------------------------------------------------
        else if (t == ARB     && a == PROCEED)   if (Π_ARB(&Z))
                                                    { a = SUCCEED; push_track(Z);   ζ_up_success(&Z); }
                                               else { a = RECEDE;  pop_track(&Z);   }
        else if (t == ARB     && a == RECEDE)       { a = PROCEED;                  ζ_stay_next(&Z); }
//      ----------------------------------------------------------------------------------------------------------------
        else if (t == SUCCESS && a == PROCEED)      { a = SUCCEED; push_track(Z);   ζ_up_success(&Z); }
        else if (t == SUCCESS && a == RECEDE)       { a = PROCEED;                  ζ_stay_next(&Z); }
//      ----------------------------------------------------------------------------------------------------------------
        else if (t == π       && a == PROCEED)      assert(0);
        else if (t == ρ       && a == PROCEED)      assert(0);
        else if (t == FENCE   && a == PROCEED)      assert(0);
//      ----------------------------------------------------------------------------------------------------------------
        else if (t == σ       && a == PROCEED)   if (Π_LITERAL(&Z, Z.PI->s))
                                                    { a = SUCCEED; ζ_up_success(&Z); }
                                               else { a = FAILURE; ζ_up_fail(&Z); }
        else if (t == ANY     && a == PROCEED)   if (Π_ANY(&Z, Z.PI->chars))
                                                    { a = SUCCEED; ζ_up_success(&Z); }
                                               else { a = FAILURE; ζ_up_fail(&Z); }
        else if (t == NOTANY  && a == PROCEED)   if (Π_NOTANY(&Z, Z.PI->chars))
                                                    { a = SUCCEED; ζ_up_success(&Z); }
                                               else { a = FAILURE; ζ_up_fail(&Z); }
        else if (t == SPAN    && a == PROCEED)   if (Π_SPAN(&Z, Z.PI->chars))
                                                    { a = SUCCEED; ζ_up_success(&Z); }
                                               else { a = FAILURE; ζ_up_fail(&Z); }
        else if (t == BREAK   && a == PROCEED)   if (Π_BREAK(&Z, Z.PI->chars))
                                                    { a = SUCCEED; ζ_up_success(&Z); }
                                               else { a = FAILURE; ζ_up_fail(&Z); }
        else if (t == POS     && a == PROCEED)   if (Π_POS(&Z))
                                                    { a = SUCCEED; ζ_up_success(&Z); }
                                               else { a = FAILURE; ζ_up_fail(&Z); }
        else if (t == RPOS    && a == PROCEED)   if (Π_RPOS(&Z))
                                                    { a = SUCCEED; ζ_up_success(&Z); }
                                               else { a = FAILURE; ζ_up_fail(&Z); }
        else if (t == LEN     && a == PROCEED)   if (Π_LEN(&Z))
                                                    { a = SUCCEED; ζ_up_success(&Z); }
                                               else { a = FAILURE; ζ_up_fail(&Z); }
        else if (t == α       && a == PROCEED)   if (Π_alpha(&Z))
                                                    { a = SUCCEED; ζ_up_success(&Z); }
                                               else { a = FAILURE; ζ_up_fail(&Z); }
        else if (t == ω       && a == PROCEED)   if (Π_omega(&Z))
                                                    { a = SUCCEED; ζ_up_success(&Z); }
                                               else { a = FAILURE; ζ_up_fail(&Z); }
        else if (t == ζ       && a == PROCEED)      { a = PROCEED; ζ_over(&Z, &C_3); }
        else if (t == Δ       && a == PROCEED)      { a = PROCEED; Π_DELTA(&Z); ζ_over(&Z, Z.PI->AP[0]); }
        else if (t == δ       && a == PROCEED)      { a = PROCEED; ζ_over(&Z, Z.PI->AP[0]); }
        else if (t == ε       && a == PROCEED)      { a = SUCCEED; ζ_up_success(&Z); }
        else if (t == λ       && a == PROCEED)      { a = SUCCEED; Π_lambda(&Z); ζ_up_success(&Z); }
        else if (t == FAIL    && a == PROCEED)      { a = FAILURE; ζ_up_fail(&Z); }
        else if (t == ABORT   && a == PROCEED)      { a = FAILURE; Z.PI = NULL; }
        else if (t == nPush   && a == PROCEED)      { a = SUCCEED; Π_nPush(&Z); ζ_up_success(&Z); }
        else if (t == nInc    && a == PROCEED)      { a = SUCCEED; Π_nInc(&Z); ζ_up_success(&Z); }
        else if (t == nPop    && a == PROCEED)      { a = SUCCEED; Π_nPop(&Z); ζ_up_success(&Z); }
        else if (t == Shift   && a == PROCEED)      { a = SUCCEED; Π_Shift(&Z); ζ_up_success(&Z); }
        else if (t == Reduce  && a == PROCEED)      { a = SUCCEED; Π_Reduce(&Z); ζ_up_success(&Z); }
        else if (t == Pop     && a == PROCEED)      { a = SUCCEED; Π_Pop(&Z); ζ_up_success(&Z); }
        else { printf("%s\n", t); fflush(stdout); assert(0); }
    }
    fini_tracks();
    heap_free();
}
//----------------------------------------------------------------------------------------------------------------------
// typedef (*PI_function_t)();
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
//  MATCH(&BEAD_0, "READS");
//  MATCH(&BEARDS_0, "ROOSTS");
//  MATCH(&C_0, "x+y*z");
//  MATCH(&ARB_0, "xyz");
    MATCH(&ARBNO_0, "xyz");
//  MATCH(&RE_0, "x|yz");
}
//----------------------------------------------------------------------------------------------------------------------
