#include <malloc.h>
//----------------------------------------------------------------------------------------------------------------------
static const char ε[] = "ε";
static const char σ[] = "σ";
static const char Σ[] = "Σ";
static const char Π[] = "Π";
static const char ρ[] = "ρ";
static const char ARBNO[] = "ARBNO";
static const char FENCE[] = "FENCE";
static const char π[] = "π";
static const char Δ[] = "Δ";
static const char δ[] = "δ";
static const char ANY[] = "ANY";
static const char NOTANY[] = "NOTANY";
static const char SPAN[] = "SPAN";
static const char BREAK[] = "BREAK";
static const char POS[] = "POS";
static const char RPOS[] = "RPOS";
static const char λ[] = "λ";
static const char ζ[] = "ζ";
//----------------------------------------------------------------------------------------------------------------------
typedef struct PATTERN PATTERN;
typedef struct PATTERN {
    const char * type;
    const char * s;
    union {
        PATTERN * AP[32];
        const long n;
        const char * N;
        const char * command;
        const char * chars;
    };
} PATTERN;
//----------------------------------------------------------------------------------------------------------------------
static PATTERN P1 = {POS, .n=0};
static PATTERN P2 = {λ, .command="S = []"};
static PATTERN P8 = {ANY, .chars="abcdefghijklmnopqrstuvwxyz"};
static PATTERN P7 = {Δ, .s="N", &P8};
static PATTERN P9 = {λ, .command="S.append(int(globals()[N]))"};
static PATTERN P6 = {Σ, NULL, {&P7, &P9}};
static PATTERN P12 = {SPAN, .chars="0123456789"};
static PATTERN P11 = {Δ, .s="N", &P12};
static PATTERN P13 = {λ, .command="S.append(int(N))"};
static PATTERN P10 = {Σ, NULL, {&P11, &P13}};
static PATTERN P15 = {σ, .s="("};
static PATTERN P16 = {ζ, .N="X"};
static PATTERN P17 = {σ, .s=")"};
static PATTERN P14 = {Σ, NULL, {&P15, &P16, &P17}};
static PATTERN P5 = {Π, NULL, {&P6, &P10, &P14}};
static PATTERN P18 = {σ, .s="+"};
static PATTERN P19 = {ζ, .N="X"};
static PATTERN P20 = {λ, .command="S.append(S.pop() + S.pop())"};
static PATTERN P4 = {Σ, NULL, {&P5, &P18, &P19, &P20}};
static PATTERN P25 = {ANY, .chars="abcdefghijklmnopqrstuvwxyz"};
static PATTERN P24 = {Δ, .s="N", &P25};
static PATTERN P26 = {λ, .command="S.append(int(globals()[N]))"};
static PATTERN P23 = {Σ, NULL, {&P24, &P26}};
static PATTERN P29 = {SPAN, .chars="0123456789"};
static PATTERN P28 = {Δ, .s="N", &P29};
static PATTERN P30 = {λ, .command="S.append(int(N))"};
static PATTERN P27 = {Σ, NULL, {&P28, &P30}};
static PATTERN P32 = {σ, .s="("};
static PATTERN P33 = {ζ, .N="X"};
static PATTERN P34 = {σ, .s=")"};
static PATTERN P31 = {Σ, NULL, {&P32, &P33, &P34}};
static PATTERN P22 = {Π, NULL, {&P23, &P27, &P31}};
static PATTERN P35 = {σ, .s="-"};
static PATTERN P36 = {ζ, .N="X"};
static PATTERN P37 = {λ, .command="S.append(S.pop() - S.pop())"};
static PATTERN P21 = {Σ, NULL, {&P22, &P35, &P36, &P37}};
static PATTERN P42 = {ANY, .chars="abcdefghijklmnopqrstuvwxyz"};
static PATTERN P41 = {Δ, .s="N", &P42};
static PATTERN P43 = {λ, .command="S.append(int(globals()[N]))"};
static PATTERN P40 = {Σ, NULL, {&P41, &P43}};
static PATTERN P46 = {SPAN, .chars="0123456789"};
static PATTERN P45 = {Δ, .s="N", &P46};
static PATTERN P47 = {λ, .command="S.append(int(N))"};
static PATTERN P44 = {Σ, NULL, {&P45, &P47}};
static PATTERN P49 = {σ, .s="("};
static PATTERN P50 = {ζ, .N="X"};
static PATTERN P51 = {σ, .s=")"};
static PATTERN P48 = {Σ, NULL, {&P49, &P50, &P51}};
static PATTERN P39 = {Π, NULL, {&P40, &P44, &P48}};
static PATTERN P52 = {σ, .s="*"};
static PATTERN P53 = {ζ, .N="X"};
static PATTERN P54 = {λ, .command="S.append(S.pop() * S.pop())"};
static PATTERN P38 = {Σ, NULL, {&P39, &P52, &P53, &P54}};
static PATTERN P59 = {ANY, .chars="abcdefghijklmnopqrstuvwxyz"};
static PATTERN P58 = {Δ, .s="N", &P59};
static PATTERN P60 = {λ, .command="S.append(int(globals()[N]))"};
static PATTERN P57 = {Σ, NULL, {&P58, &P60}};
static PATTERN P63 = {SPAN, .chars="0123456789"};
static PATTERN P62 = {Δ, .s="N", &P63};
static PATTERN P64 = {λ, .command="S.append(int(N))"};
static PATTERN P61 = {Σ, NULL, {&P62, &P64}};
static PATTERN P66 = {σ, .s="("};
static PATTERN P67 = {ζ, .N="X"};
static PATTERN P68 = {σ, .s=")"};
static PATTERN P65 = {Σ, NULL, {&P66, &P67, &P68}};
static PATTERN P56 = {Π, NULL, {&P57, &P61, &P65}};
static PATTERN P69 = {σ, .s="/"};
static PATTERN P70 = {ζ, .N="X"};
static PATTERN P71 = {λ, .command="S.append(S.pop() // S.pop())"};
static PATTERN P55 = {Σ, NULL, {&P56, &P69, &P70, &P71}};
static PATTERN P73 = {σ, .s="+"};
static PATTERN P74 = {ζ, .N="X"};
static PATTERN P72 = {Σ, NULL, {&P73, &P74}};
static PATTERN P76 = {σ, .s="-"};
static PATTERN P77 = {ζ, .N="X"};
static PATTERN P78 = {λ, .command="S.append(-S.pop())"};
static PATTERN P75 = {Σ, NULL, {&P76, &P77, &P78}};
static PATTERN P82 = {ANY, .chars="abcdefghijklmnopqrstuvwxyz"};
static PATTERN P81 = {Δ, .s="N", &P82};
static PATTERN P83 = {λ, .command="S.append(int(globals()[N]))"};
static PATTERN P80 = {Σ, NULL, {&P81, &P83}};
static PATTERN P86 = {SPAN, .chars="0123456789"};
static PATTERN P85 = {Δ, .s="N", &P86};
static PATTERN P87 = {λ, .command="S.append(int(N))"};
static PATTERN P84 = {Σ, NULL, {&P85, &P87}};
static PATTERN P89 = {σ, .s="("};
static PATTERN P90 = {ζ, .N="X"};
static PATTERN P91 = {σ, .s=")"};
static PATTERN P88 = {Σ, NULL, {&P89, &P90, &P91}};
static PATTERN P79 = {Π, NULL, {&P80, &P84, &P88}};
static PATTERN P3 = {Π, NULL, {&P4, &P21, &P38, &P55, &P72, &P75, &P79}};
static PATTERN P92 = {λ, .command="print(S.pop())"};
static PATTERN P93 = {RPOS, .n=0};
static PATTERN P0 = {Σ, NULL, {&P1, &P2, &P3, &P92, &P93}};
//----------------------------------------------------------------------------------------------------------------------
typedef enum {
    START,
    SUCCESS,
    RESUME,
    FAILURE
} action_t;
//----------------------------------------------------------------------------------------------------------------------
typedef struct {
    action_t action;
    PATTERN * pattern;
    int pos;
    int ctx;
} state_t;
//----------------------------------------------------------------------------------------------------------------------
static int iStates = 0;
static state_t * aStates = NULL;
//----------------------------------------------------------------------------------------------------------------------
static void init_states() {
    iStates = 0;
    aStates = NULL;
}
static void push_state(action_t action, PATTERN * pattern, int pos) {
    state_t state = {action, pattern, pos, 0};
    aStates = realloc(aStates, ++iStates * sizeof(state_t));
    aStates[iStates - 1] = state;
}
static state_t * top_state() {
    if (iStates > 0)
        return &aStates[iStates - 1];
    else return NULL;
}
static state_t pop_state() {
    state_t state = {START, NULL, 0, 0};
    if (iStates > 0) {
        state = aStates[iStates - 1];
        aStates = realloc(aStates, --iStates * sizeof(state_t));
    }
    return state;
}
//----------------------------------------------------------------------------------------------------------------------
void MATCH(PATTERN * pattern, const char * subject) {
    init_states();
    push_state(START, pattern, 0);
    while (iStates > 0) {
        state_t * pState = top_state();
        action_t action = pState->action;
        const char * type = pState->pattern->type;
        if (type == ε)          {   switch (action) {
                                    case START:     { pState->action = RESUME; }
                                    case RESUME:    { pState->action = FAILURE; }
                                }}
        if (type == σ)          {   switch (action) {
                                    case START:
                                    case RESUME:
                                }}
        if (type == Σ)          {   switch (action) {
                                    case START:     {   pState->action = RESUME;
                                                        push_state(START, pattern->AP[pState->ctx], pState->pos);
                                                    }
                                    case RESUME:
                                }}
        if (type == Π)          {   switch (action) {
                                    case START:     {   pState->action = RESUME;
                                                        push_state(START, pattern->AP[pState->ctx], pState->pos);
                                                    }
                                    case RESUME:    {   pState->ctx++;
                                                        if (pState->ctx < pattern->n) {
                                                            push_state(START, pattern->AP[pState->ctx], pState->pos);
                                                        } else pop_state();
                                                    }
                                }
        }
        if (type == ρ) {
        }
        if (type == ARBNO) {
        }
        if (type == FENCE) {
        }
        if (type == π) {
        }
        if (type == Δ) {
        }
        if (type == δ) {
        }
        if (type == ANY) {
        }
        if (type == NOTANY) {
        }
        if (type == SPAN) {
        }
        if (type == BREAK) {
        }
        if (type == POS) {
        }
        if (type == RPOS) {
        }
        if (type == λ) {
        }
        if (type == ζ) {
        }
    }
}
//----------------------------------------------------------------------------------------------------------------------
int main() {
    MATCH(&P0, "x+y*z");
}
//----------------------------------------------------------------------------------------------------------------------
