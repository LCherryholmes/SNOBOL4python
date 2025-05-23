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
static const char LEN[]     = "LEN";
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
        const char *    t;         /* Shift, Reduce, Pop */
    };
    union {
        const PATTERN * AP[30];    /* Δ */
        const char *    N;         /* ζ */
        const char *    command;   /* λ */
        const char *    chars;     /* ANY, NOTANY, SPAN, BREAK */
        const char *    v;         /* Shift, Reduce  */
    };
} PATTERN;
//----------------------------------------------------------------------------------------------------------------------
#define MAX_DEPTH 2
void preview(const PATTERN * PI, int depth) {
    if (depth >= MAX_DEPTH) return;
    const char * type = PI->type;
    if      (type == ε)         { printf("ε()"); }
    else if (type == σ)         { printf("\"%s\"", PI->s); }
    else if (type == λ)         { printf("λ(\"%s\")", PI->command); }
    else if (type == ζ)         { printf("ζ(\"%s\")", PI->N); }
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
}
//======================================================================================================================
#include "BEAD_PATTERN.h"
#include "BEARDS_PATTERN.h"
#include "C_PATTERN.h"
#include "RE_PATTERN.h"
//======================================================================================================================
#define HEAP_SIZE_INIT 1024
#define HEAP_SIZE_BUMP 512
#define HEAP_HEAD_STRING 1
#define HEAP_HEAD_STATE 2
#define HEAP_HEAD_COMAND 3
typedef struct _heap {
    int pos;
    int size;
    unsigned char * a;
} heap_t;
//----------------------------------------------------------------------------------------------------------------------
static heap_t empty_heap = {0, 0, NULL };
static void heap_init(heap_t * heap) { heap->pos = 0; heap->size = 0; heap->a = NULL; }
static void heap_free(heap_t * heap) { heap->pos = 0; heap->size = 0; free(heap->a); heap->a = NULL; }
static void * heap_alloc(heap_t * heap, int size) {
    size = (size + 7) >> 3 << 3;
    if (heap->pos + size >= heap->size) {
        if (heap->a == NULL) {
            heap->a = (unsigned char *) malloc(HEAP_SIZE_INIT);
            memset(heap->a, 0, HEAP_SIZE_INIT);
            heap->size = HEAP_SIZE_INIT;
        } else {
            heap->a = (unsigned char *) realloc(heap->a, heap->size + HEAP_SIZE_BUMP);
            memset(heap->a + heap->size, 0, HEAP_SIZE_BUMP);
            heap->size += HEAP_SIZE_BUMP;
        }
    }
    void * mem = &heap->a[heap->pos];
    heap->pos += size;
    return mem;
}
//======================================================================================================================
typedef struct _command command_t;
typedef struct _command { const char * string; command_t * command; } command_t;
//----------------------------------------------------------------------------------------------------------------------
static command_t * alloc_command(heap_t * heap) { return (command_t *) heap_alloc(heap, sizeof(command_t)); }
static command_t * pop_command(command_t * command) { if (command) return command->command; else return NULL; }
static command_t * push_command(command_t * command, const char * string, heap_t * heap) {
    command_t * COMMAND = alloc_command(heap);
    COMMAND->string = string;
    COMMAND->command = command;
    return COMMAND;
}
//----------------------------------------------------------------------------------------------------------------------
static const char * alloc_string(heap_t * heap, const char * string) {
    char * mem = (char *) heap_alloc(heap, strlen(string) + 1);
    strcpy(mem, string);
    return mem;
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
    state_t *       psi; // state stack
    command_t *     lambda; // command stack
} state_t;
//----------------------------------------------------------------------------------------------------------------------
static state_t empty_state = {NULL, 0, 0, NULL, 0, NULL, 0, NULL, NULL };
static state_t * alloc_state(heap_t * heap) { return (state_t *) heap_alloc(heap, sizeof(state_t)); }
static state_t * pop_state(state_t * psi) { if (psi) return psi->psi; else return NULL; }
static state_t * push_state(state_t * psi, state_t * s, heap_t * heap) {
    state_t * PSI = alloc_state(heap);
    *PSI = *s;
    PSI->psi = psi;
    return PSI;
}
//----------------------------------------------------------------------------------------------------------------------
static int iTracks = 0;
static state_t *aTracks = NULL;
static void init_tracks() { iTracks = 0; aTracks = NULL; }
static void fini_tracks() { iTracks = 0; if (aTracks) free(aTracks); aTracks = NULL; }
static void push_track(state_t s) { aTracks = realloc(aTracks, ++iTracks * sizeof(state_t)); aTracks[iTracks - 1] = s; }
static void pop_track(state_t * s) {
    if (iTracks > 0) {
        state_t state = aTracks[iTracks - 1];
        aTracks = realloc(aTracks, --iTracks * sizeof(state_t));
        if (s) *s = state;
    } else if (s) *s = empty_state;
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
static int min(int x1, int x2) { if (x1 < x2) return x1; else return x2; }
static int max(int x1, int x2) { if (x1 > x2) return x1; else return x2; }
//----------------------------------------------------------------------------------------------------------------------
#define WINDOW 12
static void animate(int action, state_t s, int iteration) {
//  --------------------------------------------------------------------------------------------------------------------
    char head[WINDOW+3]; memset(head, 0, sizeof(head));
    char tail[WINDOW+3]; memset(tail, 0, sizeof(tail));
    int α_delta = min(s.DELTA, WINDOW);
    int ω_delta = min(s.OMEGA - s.DELTA, WINDOW);
    const char * sigma = NULL;
    int i;
    i = 0;
    tail[i++] = '"';
    for (sigma = s.SIGMA - α_delta; sigma < s.SIGMA;)
        tail[i++] = *(sigma++);
    tail[i++] = '"';
    tail[i++] = 0;
    i = 0;
    head[i++] = '"';
    for (sigma = s.SIGMA + ω_delta; sigma > s.SIGMA;)
        head[i++] = *(--sigma);
    head[i++] = '"';
    head[i++] = 0;
//  --------------------------------------------------------------------------------------------------------------------
    char status[20]; sprintf(status, "%s/%d", s.PI->type, s.ctx + 1);
    printf("%3d %2d %-*s %*s %3d %*s %-8s ",
        iteration,
        iTracks,
        12, status,
        WINDOW, tail,
        s.DELTA,
        WINDOW, head,
        actions[action]
    );
    preview(s.PI, 0);
    printf("\n");
    fflush(stdout);
}
//----------------------------------------------------------------------------------------------------------------------
static bool Π_ARB(state_t * s) {
    if (s->DELTA + s->ctx <= s->OMEGA) {
        s->sigma + s->ctx;
        s->delta + s->ctx;
        return true;
    } else return false;
}
//----------------------------------------------------------------------------------------------------------------------
static bool Π_LITERAL(state_t * s, const char * string) {
    for ( s->sigma = s->SIGMA, s->delta = s->DELTA
        ; *string
        ; s->sigma++, s->delta++, string++) {
        if (*s->sigma == 0) return false;
        if (*s->sigma != *string) return false;
    }
    return true;
}
//----------------------------------------------------------------------------------------------------------------------
static bool Π_ANY(state_t * s, const char * chars) {
    s->sigma = s->SIGMA;
    s->delta = s->DELTA;
    if (*s->sigma != 0) {
        const char * c;
        for (c = chars; *c; c++)
            if (*s->sigma == *c)
                break;
        if (*c != 0) {
            s->sigma++;
            s->delta++;
            return true;
        } else return false;
    } else return false;
}
//----------------------------------------------------------------------------------------------------------------------
static bool Π_NOTANY(state_t * s, const char * chars) {
    s->sigma = s->SIGMA;
    s->delta = s->DELTA;
    if (*s->sigma != 0) {
        const char * c;
        for (c = chars; *c; c++)
            if (*s->sigma == *c)
                break;
        if (*c == 0) {
            s->sigma++;
            s->delta++;
            return true;
        } else return false;
    } else return false;
}
//----------------------------------------------------------------------------------------------------------------------
static bool Π_SPAN(state_t * s, const char * chars) {
    for ( s->sigma = s->SIGMA
        , s->delta = s->DELTA
        ; *s->sigma
        ; s->sigma++
        , s->delta++) {
        const char * c;
        for (c = chars; *c; c++)
            if (*s->sigma == *c)
                break;
        if (!*c) break;
    }
    return s->delta > s->DELTA;
}
//----------------------------------------------------------------------------------------------------------------------
static bool Π_BREAK(state_t * s, const char * chars) {
    for ( s->sigma = s->SIGMA
        , s->delta = s->DELTA
        ; *s->sigma
        ; s->sigma++
        , s->delta++) {
        const char * c;
        for (c = chars; *c; c++)
            if (*s->sigma == *c)
                break;
        if (*c) break;
    }
    return *s->sigma != 0;
}
//======================================================================================================================
static void ζ_down(state_t * s, heap_t * heap) {
    s->psi = push_state(s->psi, s, heap);
    s->sigma = s->SIGMA;
    s->delta = s->DELTA;
    s->PI = s->PI->AP[s->ctx];
    s->ctx = 0;
}
//----------------------------------------------------------------------------------------------------------------------
static void ζ_over(state_t * s, const PATTERN * PI) { s->sigma = s->SIGMA; s->delta = s->DELTA; s->ctx = 0; s->PI = PI; }
static void ζ_stay_next(state_t * s)                { s->sigma = s->SIGMA; s->delta = s->DELTA; s->ctx++; }
static void ζ_move_next(state_t * s)                { s->SIGMA = s->sigma; s->DELTA = s->delta; s->ctx++; }
//----------------------------------------------------------------------------------------------------------------------
static void ζ_up_success(state_t * s) {
    if (s->psi) {
        s->PI = s->psi->PI;
        s->ctx = s->psi->ctx;
        s->psi = pop_state(s->psi);
    } else s->PI = NULL;
}
//----------------------------------------------------------------------------------------------------------------------
static void ζ_up_fail(state_t * s) {
    s->sigma = s->SIGMA;
    s->delta = s->DELTA;
    if (s->psi) {
        s->PI = s->psi->PI;
        s->ctx = s->psi->ctx;
        s->psi = pop_state(s->psi);
    } else s->PI = NULL;
}
//----------------------------------------------------------------------------------------------------------------------
static inline bool Π_move(state_t * s, int delta) {
    if (delta >= 0 && s->DELTA + delta <= s->OMEGA) {
          s->sigma += delta;
          s->delta += delta;
          return true;
    } else false;
}
static inline bool Π_POS(state_t * s)   { return s->PI->n == s->DELTA; }
static inline bool Π_RPOS(state_t * s)  { return s->PI->n == s->OMEGA - s->DELTA; }
static inline bool Π_alpha(state_t * s) { return s->DELTA == 0 || (s->DELTA > 0 && s->SIGMA[-1] == '\n'); }
static inline bool Π_omega(state_t * s) { return s->DELTA == s->OMEGA || (s->DELTA < s->OMEGA && s->SIGMA[0] == '\n'); }
static inline bool Π_LEN(state_t * s)   { return Π_move(s, s->PI->n); }
static inline bool Π_TAB(state_t * s)   { return Π_move(s, s->PI->n - s->DELTA); }
static inline bool Π_REM(state_t * s)   { return Π_move(s, s->OMEGA - s->DELTA); }
static inline bool Π_RTAB(state_t * s)  { return Π_move(s, s->OMEGA - s->DELTA - s->PI->n); }
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
static inline bool Π_nPush(state_t * s, heap_t * heap)  { s->lambda = push_command(s->lambda, "N = N_push(N)", heap); return true; }
static inline bool Π_nInc(state_t * s, heap_t * heap)   { s->lambda = push_command(s->lambda, "N_inc(N)",      heap); return true; }
static inline bool Π_nPop(state_t * s, heap_t * heap)   { s->lambda = push_command(s->lambda, "N = N_pop(N)", heap);  return true; }
//----------------------------------------------------------------------------------------------------------------------
static inline bool Π_Shift(state_t * s, heap_t * heap)  {
    char cmd_text[128];
    if (s->PI->t == NULL)       sprintf(cmd_text, "shift();");
    else if (s->PI->v == NULL)  sprintf(cmd_text, "shift(\"%s\");", s->PI->t);
    else                        sprintf(cmd_text, "shift(\"%s\", \"%s\");", s->PI->t, s->PI->v);
    s->lambda = push_command(s->lambda, alloc_string(heap, cmd_text), heap);
    return true;
}
//----------------------------------------------------------------------------------------------------------------------
static inline bool Π_Reduce(state_t * s, heap_t * heap) {
    char top_text[32];
    if      (s->PI->n == -2)    sprintf(top_text, "istack[itop + 1]");
    else if (s->PI->n == -1)    sprintf(top_text, "istack[itop]");
    else                        sprintf(top_text, "%s", s->PI->n);
    char cmd_text[128];
    if      (s->PI->t == NULL)  sprintf(cmd_text, "reduce();");
    else if (s->PI->v == NULL)  sprintf(cmd_text, "reduce(\"%s\");", s->PI->t);
    else                        sprintf(cmd_text, "reduce(\"%s\", \"%s\");", s->PI->t, top_text);
    s->lambda = push_command(s->lambda, alloc_string(heap, cmd_text), heap);
    return true;
}
//----------------------------------------------------------------------------------------------------------------------
static inline bool Π_Pop(state_t * s, heap_t * heap) {
    char cmd_text[128];
    if (s->PI->v == NULL)
        sprintf(cmd_text, "pop();");
    else sprintf(cmd_text, "pop(\"%s\");", s->PI->v);
    s->lambda = push_command(s->lambda, alloc_string(heap, cmd_text), heap);
    return true;
}
//----------------------------------------------------------------------------------------------------------------------
static inline bool Π_theta(state_t * s, heap_t * heap) {
    char cmd_text[128];
    if (strcmp(s->PI->N, "OUTPUT") == 0)
        sprintf(cmd_text, "printf(\" %d\");", s->DELTA);
    else sprintf(cmd_text, "%s = %d;", s->PI->N, s->DELTA);
    s->lambda = push_command(s->lambda, alloc_string(heap, cmd_text), heap);
    return true;
}
//----------------------------------------------------------------------------------------------------------------------
static inline bool Π_DELTA(state_t * s, heap_t * heap) {
    char cmd_text[128];
    if (strcmp(s->PI->N, "OUTPUT") == 0)
        sprintf(cmd_text, "printf(\"%%s\", subject[%d:%d]);", s->DELTA, s->delta);
    else sprintf(cmd_text, "%s = subject[%d:%d];", s->PI->N, s->DELTA, s->delta);
    s->lambda = push_command(s->lambda, alloc_string(heap, cmd_text), heap);
    return true;
}
//----------------------------------------------------------------------------------------------------------------------
static inline bool Π_lambda(state_t * s, heap_t * heap) {
    s->lambda = push_command(s->lambda, alloc_string(heap, s->PI->command), heap);
    return true;
}
//----------------------------------------------------------------------------------------------------------------------
static void MATCH(const PATTERN * pattern, const char * subject) {
    init_tracks();
    int iteration = 0;
    int a = PROCEED;
    num_t num; num = empty_num;
    heap_t heap; heap = empty_heap;
    state_t S = {subject, 0, strlen(subject), NULL, 0, pattern, 0, NULL};
    while (S.PI) {
        iteration++; if (iteration > 5000) break;
        animate(a, S, iteration);
        const char * t = S.PI->t;
        if      (t == Π         && a == PROCEED)   if   (S.ctx < S.PI->n)
                                                        { a = PROCEED; push_track(S); ζ_down(&S, &heap); break; }
                                                   else { a = RECEDE;  pop_track(&S); break; }
        else if (t == Π         && a == SUCCEED)        { a = SUCCEED; ζ_up_success(&S); break; }
        else if (t == Π         && a == FAILURE)        { a = PROCEED; pop_track(NULL); ζ_stay_next(&S); break; }
        else if (t == Π         && a == RECEDE)         { a = PROCEED; ζ_stay_next(&S); break; }
        else if (t == Σ         && a == PROCEED)        if  (S.ctx < S.PI->n)
                                                        { a = PROCEED; ζ_down(&S, &heap); break; }
                                                   else { a = SUCCEED; ζ_up_success(&S); break; }
        else if (t == Σ         && a == SUCCEED)        { a = PROCEED; ζ_move_next(&S); break; }
        else if (t == Σ         && a == FAILURE)        { a = RECEDE;  pop_track(&S); break; }
        else if (t == Σ         && a == RECEDE)         { assert(0); }
        else if (t == ARB       && a == PROCEED)   if   (Π_ARB(&S))
                                                        { a = SUCCEED; push_track(S); ζ_up_success(&S);; break; }
                                                   else { a = RECEDE;  pop_track(&S); break; }
        else if (t == ARB       && a == RECEDE)         { a = PROCEED; ζ_stay_next(&S); break; }
        else if (t == ARBNO     && a == PROCEED)    if  (S.ctx == 0)
                                                        { a = PROCEED; push_track(S); ζ_up_success(&S); break; }
                                                   else { a = PROCEED; push_track(S); ζ_over(&S, S.PI->AP[0]); break; }
        else if (t == ARBNO     && a == SUCCEED)        { a = SUCCEED; ζ_up_success(&S); break; }
        else if (t == ARBNO     && a == FAILURE)        { a = PROCEED; pop_track(NULL); ζ_stay_next(&S); break; }
        else if (t == ARBNO     && a == RECEDE)         { a = PROCEED; ζ_stay_next(&S); break; }
        else if (t == SUCCESS   && a == PROCEED)        { a = SUCCEED; push_track(S); ζ_up_success(&S); break; }
        else if (t == SUCCESS   && a == RECEDE)         { a = SUCCEED; ζ_up_success(&S); break; }
        else if (t == σ         && a == PROCEED)   if   (Π_LITERAL(&S, S.PI->s))
                                                        { a = SUCCEED; ζ_up_success(&S); }
                                                   else { a = FAILURE; ζ_up_fail(&S); }
        else if (t == ANY       && a == PROCEED)   if   (Π_ANY(&S, S.PI->chars))
                                                        { a = SUCCEED; ζ_up_success(&S); }
                                                   else { a = FAILURE; ζ_up_fail(&S); }
        else if (t == NOTANY    && a == PROCEED)   if   (Π_NOTANY(&S, S.PI->chars))
                                                        { a = SUCCEED; ζ_up_success(&S); }
                                                   else { a = FAILURE; ζ_up_fail(&S); }
        else if (t == SPAN      && a == PROCEED)   if   (Π_SPAN(&S, S.PI->chars))
                                                        { a = SUCCEED; ζ_up_success(&S); }
                                                   else { a = FAILURE; ζ_up_fail(&S); }
        else if (t == BREAK     && a == PROCEED)   if   (Π_BREAK(&S, S.PI->chars))
                                                        { a = SUCCEED; ζ_up_success(&S); }
                                                   else { a = FAILURE; ζ_up_fail(&S); }
        else if (t == FENCE     && a == PROCEED)   assert(0); /*not implemented*/
        else if (t == POS       && a == PROCEED)   if   (Π_POS(&S))
                                                        { a = SUCCEED; ζ_up_success(&S); }
                                                   else { a = FAILURE; ζ_up_fail(&S); }
        else if (t == RPOS      && a == PROCEED)   if   (Π_RPOS(&S))
                                                        { a = SUCCEED; ζ_up_success(&S); }
                                                   else { a = FAILURE; ζ_up_fail(&S); }
        else if (t == LEN       && a == PROCEED)   if   (Π_LEN(&S))
                                                        { a = SUCCEED; ζ_up_success(&S); }
                                                   else { a = FAILURE; ζ_up_fail(&S); }
        else if (t == π         && a == PROCEED)   assert(0); /*not implemented*/
        else if (t == ρ         && a == PROCEED)   assert(0); /*not implemented*/
        else if (t == α         && a == PROCEED)   if   (Π_alpha(&S))
                                                        { a = SUCCEED; ζ_up_success(&S); }
                                                   else { a = FAILURE; ζ_up_fail(&S); }
        else if (t == ω         && a == PROCEED)   if   (Π_omega(&S))
                                                        { a = SUCCEED; ζ_up_success(&S); }
                                                   else { a = FAILURE; ζ_up_fail(&S); }
        else if (t == ζ         && a == PROCEED)        { a = PROCEED; ζ_over(&S, &C_3); }
        else if (t == Δ         && a == PROCEED)        { a = PROCEED; Π_DELTA(&S, &heap); ζ_over(&S, S.PI->AP[0]); }
        else if (t == δ         && a == PROCEED)        { a = PROCEED; ζ_over(&S, S.PI->AP[0]); }
        else if (t == ε         && a == PROCEED)        { a = SUCCEED; ζ_up_success(&S); }
        else if (t == λ         && a == PROCEED)        { a = SUCCEED; Π_lambda(&S, &heap); ζ_up_success(&S); }
        else if (t == FAIL      && a == PROCEED)        { a = FAILURE; ζ_up_fail(&S); }
        else if (t == ABORT     && a == PROCEED)        { a = FAILURE; S.PI = NULL; }
        else if (t == nPush     && a == PROCEED)        { a = SUCCEED; Π_nPush(&S, &heap); ζ_up_success(&S); }
        else if (t == nInc      && a == PROCEED)        { a = SUCCEED; Π_nInc(&S, &heap); ζ_up_success(&S); }
        else if (t == nPop      && a == PROCEED)        { a = SUCCEED; Π_nPop(&S, &heap); ζ_up_success(&S); }
        else if (t == Shift     && a == PROCEED)        { a = SUCCEED; Π_Shift(&S, &heap); ζ_up_success(&S); }
        else if (t == Reduce    && a == PROCEED)        { a = SUCCEED; Π_Reduce(&S, &heap); ζ_up_success(&S); }
        else if (t == Pop       && a == PROCEED)        { a = SUCCEED; Π_Pop(&S, &heap); ζ_up_success(&S); }
        else { printf("%s\n", t); fflush(stdout); assert(0); }
    }
    fini_tracks();
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
    MATCH(&ARB_0, "xyz");
    MATCH(&ARBNO_0, "xyz");
//  MATCH(&C_0, "x+y*z");
//  MATCH(&RE_0, "(x|y)z");
}
//----------------------------------------------------------------------------------------------------------------------
