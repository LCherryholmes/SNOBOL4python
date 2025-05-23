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
        const char *    v;         /* Shift, Reduce, Pop  */
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
#include "C_PATTERN.h"
#include "BEAD_PATTERN.h"
#include "BEARDS_PATTERN.h"
//======================================================================================================================
typedef struct _state state_t;
typedef struct _state {
    const char *    SIGMA;
    int             DELTA;
    const char *    sigma;
    int             delta;
    const PATTERN * PI;
    int             ctx;
    state_t *       psi;
} state_t;
//======================================================================================================================
#define HEAP_SIZE_INIT 64
#define HEAP_SIZE_BUMP 64
typedef struct _heap {
    int pos;
    int size;
    state_t * a;
} heap_t;
//----------------------------------------------------------------------------------------------------------------------
static heap_t empty_heap = {0, 0, NULL };
static state_t empty_state = {NULL,  0, NULL,  0, NULL,  0, NULL };
static state_t * alloc_state(heap_t * heap) {
    if (heap->pos >= heap->size) {
        if (heap->a == NULL) {
            heap->a = (state_t *) malloc(HEAP_SIZE_INIT * sizeof(state_t));
            memset(heap->a, -1, HEAP_SIZE_INIT * sizeof(state_t));
            heap->size = HEAP_SIZE_INIT;
        } else {
            heap->a = (state_t *) realloc(heap->a, (heap->size + HEAP_SIZE_BUMP) * sizeof(state_t));
            memset(heap->a + heap->size, -1, HEAP_SIZE_BUMP * sizeof(state_t));
            heap->size += HEAP_SIZE_BUMP;
        }
    }
    heap->a[heap->pos] = empty_state;
    return &heap->a[heap->pos++];
}
static void * free_states(heap_t * heap) { heap->pos = 0; heap->size = 0; free(heap->a); heap->a = NULL; }
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
#define FAIL 2
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
static void animate(int action, state_t s, int iteration, int LENGTH) {
//  --------------------------------------------------------------------------------------------------------------------
    char head[WINDOW+3]; memset(head, 0, sizeof(head));
    char tail[WINDOW+3]; memset(tail, 0, sizeof(tail));
    int α_delta = min(s.DELTA, WINDOW);
    int ω_delta = min(LENGTH - s.DELTA, WINDOW);
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
    if (s->delta > s->DELTA)
        return true;
    return false;
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
    if (*s->sigma == 0)
        return false;
    else return true;
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
static void MATCH(const PATTERN * pattern, const char * subject) {
    init_tracks();
    int iteration = 0;
    int action = PROCEED;
    heap_t heap; heap = empty_heap;
    const int LENGTH = strlen(subject);
    state_t state = {subject, 0, NULL, 0, pattern, 0, NULL};
    while (state.PI) {
        iteration++; // if (iteration > 1000) break;
        animate(action, state, iteration, LENGTH);
        const char * type = state.PI->type;
        if (type == Π)
            switch (action) {
                case PROCEED:  if   (state.ctx < state.PI->n)
                                    { action = PROCEED; push_track(state); ζ_down(&state, &heap); break; }
                               else { action = RECEDE;  pop_track(&state); break; }
                case SUCCEED:       { action = SUCCEED; ζ_up_success(&state); break; }
                case FAIL:          { action = PROCEED; pop_track(NULL); ζ_stay_next(&state); break; }
                case RECEDE:        { action = PROCEED; ζ_stay_next(&state); break; }
            }
        else if (type == Σ)
            switch (action) {
                case PROCEED:  if   (state.ctx < state.PI->n)
                                    { action = PROCEED; ζ_down(&state, &heap); break; }
                               else { action = SUCCEED; ζ_up_success(&state); break; }
                case SUCCEED:       { action = PROCEED; ζ_move_next(&state); break; }
                case FAIL:          { action = RECEDE;  pop_track(&state); break; }
                case RECEDE:        { assert(0); }
            }
        else if (type == ε
             && action == PROCEED)  { action = SUCCEED; ζ_up_success(&state); }
        else if (type == λ
             && action == PROCEED)  { action = SUCCEED; ζ_up_success(&state); }
        else if (type == ζ
             && action == PROCEED)  { action = PROCEED; ζ_over(&state, &C_3); }
        else if (type == Δ
             && action == PROCEED)  { action = PROCEED; ζ_over(&state, state.PI->AP[0]); }
        else if (type == δ
             && action == PROCEED)  { action = PROCEED; ζ_over(&state, state.PI->AP[0]); }
        else if (type == σ
             && action == PROCEED)  if   (Π_LITERAL(&state, state.PI->s))
                                         { action = SUCCEED; ζ_up_success(&state); }
                                    else { action = FAIL;    ζ_up_fail(&state); }
        else if (type == ANY
             && action == PROCEED)  if   (Π_ANY(&state, state.PI->chars))
                                         { action = SUCCEED; ζ_up_success(&state); }
                                    else { action = FAIL;    ζ_up_fail(&state); }
        else if (type == NOTANY
             && action == PROCEED)  if   (Π_NOTANY(&state, state.PI->chars))
                                         { action = SUCCEED; ζ_up_success(&state); }
                                    else { action = FAIL;    ζ_up_fail(&state); }
        else if (type == SPAN
             && action == PROCEED)  if   (Π_SPAN(&state, state.PI->chars))
                                         { action = SUCCEED; ζ_up_success(&state); }
                                    else { action = FAIL;    ζ_up_fail(&state); }
        else if (type == BREAK
             && action == PROCEED ) if   (Π_BREAK(&state, state.PI->chars))
                                         { action = SUCCEED; ζ_up_success(&state); }
                                    else { action = FAIL;    ζ_up_fail(&state); }
        else if (type == POS
             && action == PROCEED)  if   (state.DELTA == state.PI->n)
                                         { action = SUCCEED; ζ_up_success(&state); }
                                    else { action = FAIL;    ζ_up_fail(&state); }
        else if (type == RPOS
             && action == PROCEED)  if   (LENGTH - state.DELTA == state.PI->n)
                                         { action = SUCCEED; ζ_up_success(&state); }
                                    else { action = FAIL;    ζ_up_fail(&state); }
        else if (type == ρ)         assert(0); /*not implemented*/
        else if (type == ARBNO)     assert(0); /*not implemented*/
        else if (type == FENCE)     assert(0); /*not implemented*/
        else if (type == π)         assert(0); /*not implemented*/
    }
    fini_tracks();
}
//----------------------------------------------------------------------------------------------------------------------
int main() {
    MATCH(&BEAD_0, "READS");
    MATCH(&BEARDS_0, "ROOSTS");
    MATCH(&C_0, "x+y*z");
}
//----------------------------------------------------------------------------------------------------------------------
