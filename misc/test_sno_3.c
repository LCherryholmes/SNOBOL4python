#ifdef __GNUC__
#define __kernel
#define __global
#include <malloc.h>
#include <string.h>
#include <stdbool.h>
extern int printf(const char *, ...);
extern void assert(int a);
#endif
/*----------------------------------------------------------------------------*/
typedef struct { const char * σ; int δ; } str_t;
typedef struct { unsigned int pos; __global char * buffer; } output_t;
/*----------------------------------------------------------------------------*/
#if 0
void write_nl(output_t * out) {}
int  write_int(output_t * out, int v) {}
void write_sz(output_t * out, const char * s) {}
void write_flush(output_t * out) {}
#else
#if 1
void    write_nl(output_t * out)                 { printf("%s", "\n"); }
int     write_int(output_t * out, int v)         { printf("%d", v); return v; }
void    write_sz(output_t * out, const char * s) { printf("%s", s); }
str_t   write_str(output_t * out, str_t str) {
            printf("%.*s", str.δ, str.σ);
            return str;
        }
void    write_flush(output_t * out) {}
#else
    void write_nl(output_t * out) {
        out->buffer[out->pos++] = '\n';
        out->buffer[out->pos] = 0;
    }

    int write_int(output_t * out, int v) {
        int n = v;
        if (v < 0) { out->buffer[out->pos++] = '-'; n = -v; }
        if (n == 0) out->buffer[out->pos++] = '0';
        else {
            int i = 0;
            char temp[16] = "";
            while (n > 0) { temp[i++] = '0' + (n % 10); n /= 10; }
            while (i > 0) out->buffer[out->pos++] = temp[--i];
        }
        out->buffer[out->pos++] = '\n';
        out->buffer[out->pos] = '\0';
        return v;
    }

    void write_sz(output_t * out, const char * s) {
        for (int i = 0; s[i]; i++)
            out->buffer[out->pos++] = s[i];
        out->buffer[out->pos++] = '\n';
        out->buffer[out->pos] = 0;
    }

    void write_flush(output_t * out) {
#   ifdef __GNUC__
        printf("%s", out->buffer);
#   endif
    }
#endif
#endif
/*----------------------------------------------------------------------------*/
static int Δ = 0;
static int Ω = 0;
static const char * Σ = (const char *) 0;
static const int α = 0;
static const int β = 1;
static const str_t empty = (str_t) {(const char *) 0, 0};
static inline bool is_empty(str_t x) { return x.σ == (const char *) 0; }
static inline int len(const char * s) { int δ = 0; for (; *s; δ++) s++; return δ; }
static inline str_t str(const char * σ, int δ) { return (str_t) {σ, δ}; }
static inline str_t cat(str_t x, str_t y) { return (str_t) {x.σ, x.δ + y.δ}; }
static output_t * out = (output_t *) 0;
/*----------------------------------------------------------------------------*/
static inline void * enter(void ** ζζ, size_t size) {
    void * ζ = *ζζ;
    if (size)
        if (ζ) memset(ζ, 0, size);
        else ζ = *ζζ = calloc(1, size);
    return ζ;
}
/*----------------------------------------------------------------------------*/
typedef struct _V V_t;
typedef struct _I I_t;
typedef struct _E E_t;
typedef struct _X X_t;
typedef struct _C C_t;
typedef struct _match49 match49_t;
/*----------------------------------------------------------------------------*/
typedef struct _V {
} V_t;
/*----------------------------------------------------------------------------*/
typedef struct _I {
    int SPAN7_δ;
} I_t;
/*----------------------------------------------------------------------------*/
typedef struct _E {
    int alt10_i;
    V_t * V11_ζ;
    I_t * I12_ζ;
    X_t * X15_ζ;
} E_t;
/*----------------------------------------------------------------------------*/
typedef struct _X {
    int alt19_i;
    E_t * E21_ζ;
    X_t * X23_ζ;
    E_t * E25_ζ;
    X_t * X27_ζ;
    E_t * E29_ζ;
    X_t * X31_ζ;
    E_t * E33_ζ;
    X_t * X35_ζ;
    X_t * X38_ζ;
    X_t * X41_ζ;
    E_t * E42_ζ;
} X_t;
/*----------------------------------------------------------------------------*/
typedef struct _C {
    X_t * X47_ζ;
} C_t;
/*----------------------------------------------------------------------------*/
typedef struct _match49 {
    C_t * C51_ζ;
} match49_t;
/*----------------------------------------------------------------------------*/
str_t V(V_t **, int);
str_t I(I_t **, int);
str_t E(E_t **, int);
str_t X(X_t **, int);
str_t C(C_t **, int);
str_t match49(match49_t **, int);
/*============================================================================*/
str_t V(V_t ** ζζ, int entry) {
    V_t * ζ = *ζζ;
    if (entry == α){ ζ = enter((void **) ζζ, sizeof(V_t));   goto V_α; }
    if (entry == β){                                         goto V_β; }
    /*------------------------------------------------------------------------*/
    str_t         ANY4;
    ANY4_α:       if (Σ[Δ] == 'a')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'b')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'c')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'd')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'e')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'f')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'g')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'h')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'i')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'j')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'k')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'l')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'm')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'n')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'o')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'p')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'q')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'r')                          goto ANY4_αγ;
                  if (Σ[Δ] == 's')                          goto ANY4_αγ;
                  if (Σ[Δ] == 't')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'u')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'v')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'w')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'x')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'y')                          goto ANY4_αγ;
                  if (Σ[Δ] == 'z')                          goto ANY4_αγ;
                                                            goto ANY4_ω;
    ANY4_αγ:      ANY4 = str(Σ+Δ,1); Δ+=1;                  goto ANY4_γ;
    ANY4_β:       Δ-=1;                                     goto ANY4_ω;
    /*------------------------------------------------------------------------*/
    str_t         OUTPUT3;
    OUTPUT3_α:                                              goto ANY4_α;
    OUTPUT3_β:                                              goto ANY4_β;
    ANY4_γ:       OUTPUT3 = write_str(out, ANY4);           
                  write_nl(out);                            goto OUTPUT3_γ;
    ANY4_ω:                                                 goto OUTPUT3_ω;
    /*------------------------------------------------------------------------*/
    V_α:                                                    goto OUTPUT3_α;
    V_β:                                                    goto OUTPUT3_β;
    OUTPUT3_γ:    return OUTPUT3;
    OUTPUT3_ω:    return empty;
}
/*============================================================================*/
str_t I(I_t ** ζζ, int entry) {
    I_t * ζ = *ζζ;
    if (entry == α){ ζ = enter((void **) ζζ, sizeof(I_t));   goto I_α; }
    if (entry == β){                                         goto I_β; }
    /*------------------------------------------------------------------------*/
    str_t         SPAN7;
    SPAN7_α:      for (ζ->SPAN7_δ = 0; Σ[Δ+ζ->SPAN7_δ]; ζ->SPAN7_δ++) {
                      if (Σ[Δ+ζ->SPAN7_δ] == '0') continue;
                      if (Σ[Δ+ζ->SPAN7_δ] == '1') continue;
                      if (Σ[Δ+ζ->SPAN7_δ] == '2') continue;
                      if (Σ[Δ+ζ->SPAN7_δ] == '3') continue;
                      if (Σ[Δ+ζ->SPAN7_δ] == '4') continue;
                      if (Σ[Δ+ζ->SPAN7_δ] == '5') continue;
                      if (Σ[Δ+ζ->SPAN7_δ] == '6') continue;
                      if (Σ[Δ+ζ->SPAN7_δ] == '7') continue;
                      if (Σ[Δ+ζ->SPAN7_δ] == '8') continue;
                      if (Σ[Δ+ζ->SPAN7_δ] == '9') continue;
                      break;                                
                  }                                         
                  if (ζ->SPAN7_δ <= 0)                      goto SPAN7_ω;
                  SPAN7 = str(Σ+Δ,ζ->SPAN7_δ); Δ+=ζ->SPAN7_δ;goto SPAN7_γ;
    SPAN7_β:      Δ-=ζ->SPAN7_δ;                            goto SPAN7_ω;
    /*------------------------------------------------------------------------*/
    str_t         OUTPUT6;
    OUTPUT6_α:                                              goto SPAN7_α;
    OUTPUT6_β:                                              goto SPAN7_β;
    SPAN7_γ:      OUTPUT6 = write_str(out, SPAN7);          
                  write_nl(out);                            goto OUTPUT6_γ;
    SPAN7_ω:                                                goto OUTPUT6_ω;
    /*------------------------------------------------------------------------*/
    I_α:                                                    goto OUTPUT6_α;
    I_β:                                                    goto OUTPUT6_β;
    OUTPUT6_γ:    return OUTPUT6;
    OUTPUT6_ω:    return empty;
}
/*============================================================================*/
str_t E(E_t ** ζζ, int entry) {
    E_t * ζ = *ζζ;
    if (entry == α){ ζ = enter((void **) ζζ, sizeof(E_t));   goto E_α; }
    if (entry == β){                                         goto E_β; }
    /*------------------------------------------------------------------------*/
    str_t         V11;
    V11_α:        V11 = V(&ζ->V11_ζ, α);                    goto V11_λ;
    V11_β:        V11 = V(&ζ->V11_ζ, β);                    goto V11_λ;
    V11_λ:        if (is_empty(V11))                        goto V11_ω;
                  else                                      goto V11_γ;
    /*------------------------------------------------------------------------*/
    str_t         I12;
    I12_α:        I12 = I(&ζ->I12_ζ, α);                    goto I12_λ;
    I12_β:        I12 = I(&ζ->I12_ζ, β);                    goto I12_λ;
    I12_λ:        if (is_empty(I12))                        goto I12_ω;
                  else                                      goto I12_γ;
    /*------------------------------------------------------------------------*/
    str_t         s14;
    s14_α:        if (Σ[Δ+0] != '(')                        goto s14_ω;
                  s14 = str(Σ+Δ,1); Δ+=1;                   goto s14_γ;
    s14_β:        Δ-=1;                                     goto s14_ω;
    /*------------------------------------------------------------------------*/
    str_t         X15;
    X15_α:        X15 = X(&ζ->X15_ζ, α);                    goto X15_λ;
    X15_β:        X15 = X(&ζ->X15_ζ, β);                    goto X15_λ;
    X15_λ:        if (is_empty(X15))                        goto X15_ω;
                  else                                      goto X15_γ;
    /*------------------------------------------------------------------------*/
    str_t         s16;
    s16_α:        if (Σ[Δ+0] != ')')                        goto s16_ω;
                  s16 = str(Σ+Δ,1); Δ+=1;                   goto s16_γ;
    s16_β:        Δ-=1;                                     goto s16_ω;
    /*------------------------------------------------------------------------*/
    str_t         seq13;
    seq13_α:      seq13 = str(Σ+Δ,0);                       goto s14_α;
    seq13_β:                                                goto s16_β;
    s14_γ:        seq13 = cat(seq13, s14);                  goto X15_α;
    s14_ω:                                                  goto seq13_ω;
    X15_γ:        seq13 = cat(seq13, X15);                  goto s16_α;
    X15_ω:                                                  goto s14_β;
    s16_γ:        seq13 = cat(seq13, s16);                  goto seq13_γ;
    s16_ω:                                                  goto X15_β;
    /*------------------------------------------------------------------------*/
    str_t         alt10;
    alt10_α:      ζ->alt10_i = 1;                           goto V11_α;
    alt10_β:      if (ζ->alt10_i == 1)                      goto V11_β;
                  if (ζ->alt10_i == 2)                      goto I12_β;
                  if (ζ->alt10_i == 3)                      goto seq13_β;
                                                            goto alt10_ω;
    V11_γ:        alt10 = V11;                              goto alt10_γ;
    V11_ω:        ζ->alt10_i++;                             goto I12_α;
    I12_γ:        alt10 = I12;                              goto alt10_γ;
    I12_ω:        ζ->alt10_i++;                             goto seq13_α;
    seq13_γ:      alt10 = seq13;                            goto alt10_γ;
    seq13_ω:                                                goto alt10_ω;
    /*------------------------------------------------------------------------*/
    str_t         OUTPUT9;
    OUTPUT9_α:                                              goto alt10_α;
    OUTPUT9_β:                                              goto alt10_β;
    alt10_γ:      OUTPUT9 = write_str(out, alt10);          
                  write_nl(out);                            goto OUTPUT9_γ;
    alt10_ω:                                                goto OUTPUT9_ω;
    /*------------------------------------------------------------------------*/
    E_α:                                                    goto OUTPUT9_α;
    E_β:                                                    goto OUTPUT9_β;
    OUTPUT9_γ:    return OUTPUT9;
    OUTPUT9_ω:    return empty;
}
/*============================================================================*/
str_t X(X_t ** ζζ, int entry) {
    X_t * ζ = *ζζ;
    if (entry == α){ ζ = enter((void **) ζζ, sizeof(X_t));   goto X_α; }
    if (entry == β){                                         goto X_β; }
    /*------------------------------------------------------------------------*/
    str_t         E21;
    E21_α:        E21 = E(&ζ->E21_ζ, α);                    goto E21_λ;
    E21_β:        E21 = E(&ζ->E21_ζ, β);                    goto E21_λ;
    E21_λ:        if (is_empty(E21))                        goto E21_ω;
                  else                                      goto E21_γ;
    /*------------------------------------------------------------------------*/
    str_t         s22;
    s22_α:        if (Σ[Δ+0] != '+')                        goto s22_ω;
                  s22 = str(Σ+Δ,1); Δ+=1;                   goto s22_γ;
    s22_β:        Δ-=1;                                     goto s22_ω;
    /*------------------------------------------------------------------------*/
    str_t         X23;
    X23_α:        X23 = X(&ζ->X23_ζ, α);                    goto X23_λ;
    X23_β:        X23 = X(&ζ->X23_ζ, β);                    goto X23_λ;
    X23_λ:        if (is_empty(X23))                        goto X23_ω;
                  else                                      goto X23_γ;
    /*------------------------------------------------------------------------*/
    str_t         seq20;
    seq20_α:      seq20 = str(Σ+Δ,0);                       goto E21_α;
    seq20_β:                                                goto X23_β;
    E21_γ:        seq20 = cat(seq20, E21);                  goto s22_α;
    E21_ω:                                                  goto seq20_ω;
    s22_γ:        seq20 = cat(seq20, s22);                  goto X23_α;
    s22_ω:                                                  goto E21_β;
    X23_γ:        seq20 = cat(seq20, X23);                  goto seq20_γ;
    X23_ω:                                                  goto s22_β;
    /*------------------------------------------------------------------------*/
    str_t         E25;
    E25_α:        E25 = E(&ζ->E25_ζ, α);                    goto E25_λ;
    E25_β:        E25 = E(&ζ->E25_ζ, β);                    goto E25_λ;
    E25_λ:        if (is_empty(E25))                        goto E25_ω;
                  else                                      goto E25_γ;
    /*------------------------------------------------------------------------*/
    str_t         s26;
    s26_α:        if (Σ[Δ+0] != '-')                        goto s26_ω;
                  s26 = str(Σ+Δ,1); Δ+=1;                   goto s26_γ;
    s26_β:        Δ-=1;                                     goto s26_ω;
    /*------------------------------------------------------------------------*/
    str_t         X27;
    X27_α:        X27 = X(&ζ->X27_ζ, α);                    goto X27_λ;
    X27_β:        X27 = X(&ζ->X27_ζ, β);                    goto X27_λ;
    X27_λ:        if (is_empty(X27))                        goto X27_ω;
                  else                                      goto X27_γ;
    /*------------------------------------------------------------------------*/
    str_t         seq24;
    seq24_α:      seq24 = str(Σ+Δ,0);                       goto E25_α;
    seq24_β:                                                goto X27_β;
    E25_γ:        seq24 = cat(seq24, E25);                  goto s26_α;
    E25_ω:                                                  goto seq24_ω;
    s26_γ:        seq24 = cat(seq24, s26);                  goto X27_α;
    s26_ω:                                                  goto E25_β;
    X27_γ:        seq24 = cat(seq24, X27);                  goto seq24_γ;
    X27_ω:                                                  goto s26_β;
    /*------------------------------------------------------------------------*/
    str_t         E29;
    E29_α:        E29 = E(&ζ->E29_ζ, α);                    goto E29_λ;
    E29_β:        E29 = E(&ζ->E29_ζ, β);                    goto E29_λ;
    E29_λ:        if (is_empty(E29))                        goto E29_ω;
                  else                                      goto E29_γ;
    /*------------------------------------------------------------------------*/
    str_t         s30;
    s30_α:        if (Σ[Δ+0] != '*')                        goto s30_ω;
                  s30 = str(Σ+Δ,1); Δ+=1;                   goto s30_γ;
    s30_β:        Δ-=1;                                     goto s30_ω;
    /*------------------------------------------------------------------------*/
    str_t         X31;
    X31_α:        X31 = X(&ζ->X31_ζ, α);                    goto X31_λ;
    X31_β:        X31 = X(&ζ->X31_ζ, β);                    goto X31_λ;
    X31_λ:        if (is_empty(X31))                        goto X31_ω;
                  else                                      goto X31_γ;
    /*------------------------------------------------------------------------*/
    str_t         seq28;
    seq28_α:      seq28 = str(Σ+Δ,0);                       goto E29_α;
    seq28_β:                                                goto X31_β;
    E29_γ:        seq28 = cat(seq28, E29);                  goto s30_α;
    E29_ω:                                                  goto seq28_ω;
    s30_γ:        seq28 = cat(seq28, s30);                  goto X31_α;
    s30_ω:                                                  goto E29_β;
    X31_γ:        seq28 = cat(seq28, X31);                  goto seq28_γ;
    X31_ω:                                                  goto s30_β;
    /*------------------------------------------------------------------------*/
    str_t         E33;
    E33_α:        E33 = E(&ζ->E33_ζ, α);                    goto E33_λ;
    E33_β:        E33 = E(&ζ->E33_ζ, β);                    goto E33_λ;
    E33_λ:        if (is_empty(E33))                        goto E33_ω;
                  else                                      goto E33_γ;
    /*------------------------------------------------------------------------*/
    str_t         s34;
    s34_α:        if (Σ[Δ+0] != '/')                        goto s34_ω;
                  s34 = str(Σ+Δ,1); Δ+=1;                   goto s34_γ;
    s34_β:        Δ-=1;                                     goto s34_ω;
    /*------------------------------------------------------------------------*/
    str_t         X35;
    X35_α:        X35 = X(&ζ->X35_ζ, α);                    goto X35_λ;
    X35_β:        X35 = X(&ζ->X35_ζ, β);                    goto X35_λ;
    X35_λ:        if (is_empty(X35))                        goto X35_ω;
                  else                                      goto X35_γ;
    /*------------------------------------------------------------------------*/
    str_t         seq32;
    seq32_α:      seq32 = str(Σ+Δ,0);                       goto E33_α;
    seq32_β:                                                goto X35_β;
    E33_γ:        seq32 = cat(seq32, E33);                  goto s34_α;
    E33_ω:                                                  goto seq32_ω;
    s34_γ:        seq32 = cat(seq32, s34);                  goto X35_α;
    s34_ω:                                                  goto E33_β;
    X35_γ:        seq32 = cat(seq32, X35);                  goto seq32_γ;
    X35_ω:                                                  goto s34_β;
    /*------------------------------------------------------------------------*/
    str_t         s37;
    s37_α:        if (Σ[Δ+0] != '+')                        goto s37_ω;
                  s37 = str(Σ+Δ,1); Δ+=1;                   goto s37_γ;
    s37_β:        Δ-=1;                                     goto s37_ω;
    /*------------------------------------------------------------------------*/
    str_t         X38;
    X38_α:        X38 = X(&ζ->X38_ζ, α);                    goto X38_λ;
    X38_β:        X38 = X(&ζ->X38_ζ, β);                    goto X38_λ;
    X38_λ:        if (is_empty(X38))                        goto X38_ω;
                  else                                      goto X38_γ;
    /*------------------------------------------------------------------------*/
    str_t         seq36;
    seq36_α:      seq36 = str(Σ+Δ,0);                       goto s37_α;
    seq36_β:                                                goto X38_β;
    s37_γ:        seq36 = cat(seq36, s37);                  goto X38_α;
    s37_ω:                                                  goto seq36_ω;
    X38_γ:        seq36 = cat(seq36, X38);                  goto seq36_γ;
    X38_ω:                                                  goto s37_β;
    /*------------------------------------------------------------------------*/
    str_t         s40;
    s40_α:        if (Σ[Δ+0] != '-')                        goto s40_ω;
                  s40 = str(Σ+Δ,1); Δ+=1;                   goto s40_γ;
    s40_β:        Δ-=1;                                     goto s40_ω;
    /*------------------------------------------------------------------------*/
    str_t         X41;
    X41_α:        X41 = X(&ζ->X41_ζ, α);                    goto X41_λ;
    X41_β:        X41 = X(&ζ->X41_ζ, β);                    goto X41_λ;
    X41_λ:        if (is_empty(X41))                        goto X41_ω;
                  else                                      goto X41_γ;
    /*------------------------------------------------------------------------*/
    str_t         seq39;
    seq39_α:      seq39 = str(Σ+Δ,0);                       goto s40_α;
    seq39_β:                                                goto X41_β;
    s40_γ:        seq39 = cat(seq39, s40);                  goto X41_α;
    s40_ω:                                                  goto seq39_ω;
    X41_γ:        seq39 = cat(seq39, X41);                  goto seq39_γ;
    X41_ω:                                                  goto s40_β;
    /*------------------------------------------------------------------------*/
    str_t         E42;
    E42_α:        E42 = E(&ζ->E42_ζ, α);                    goto E42_λ;
    E42_β:        E42 = E(&ζ->E42_ζ, β);                    goto E42_λ;
    E42_λ:        if (is_empty(E42))                        goto E42_ω;
                  else                                      goto E42_γ;
    /*------------------------------------------------------------------------*/
    str_t         alt19;
    alt19_α:      ζ->alt19_i = 1;                           goto seq20_α;
    alt19_β:      if (ζ->alt19_i == 1)                      goto seq20_β;
                  if (ζ->alt19_i == 2)                      goto seq24_β;
                  if (ζ->alt19_i == 3)                      goto seq28_β;
                  if (ζ->alt19_i == 4)                      goto seq32_β;
                  if (ζ->alt19_i == 5)                      goto seq36_β;
                  if (ζ->alt19_i == 6)                      goto seq39_β;
                  if (ζ->alt19_i == 7)                      goto E42_β;
                                                            goto alt19_ω;
    seq20_γ:      alt19 = seq20;                            goto alt19_γ;
    seq20_ω:      ζ->alt19_i++;                             goto seq24_α;
    seq24_γ:      alt19 = seq24;                            goto alt19_γ;
    seq24_ω:      ζ->alt19_i++;                             goto seq28_α;
    seq28_γ:      alt19 = seq28;                            goto alt19_γ;
    seq28_ω:      ζ->alt19_i++;                             goto seq32_α;
    seq32_γ:      alt19 = seq32;                            goto alt19_γ;
    seq32_ω:      ζ->alt19_i++;                             goto seq36_α;
    seq36_γ:      alt19 = seq36;                            goto alt19_γ;
    seq36_ω:      ζ->alt19_i++;                             goto seq39_α;
    seq39_γ:      alt19 = seq39;                            goto alt19_γ;
    seq39_ω:      ζ->alt19_i++;                             goto E42_α;
    E42_γ:        alt19 = E42;                              goto alt19_γ;
    E42_ω:                                                  goto alt19_ω;
    /*------------------------------------------------------------------------*/
    str_t         OUTPUT18;
    OUTPUT18_α:                                             goto alt19_α;
    OUTPUT18_β:                                             goto alt19_β;
    alt19_γ:      OUTPUT18 = write_str(out, alt19);         
                  write_nl(out);                            goto OUTPUT18_γ;
    alt19_ω:                                                goto OUTPUT18_ω;
    /*------------------------------------------------------------------------*/
    X_α:                                                    goto OUTPUT18_α;
    X_β:                                                    goto OUTPUT18_β;
    OUTPUT18_γ:   return OUTPUT18;
    OUTPUT18_ω:   return empty;
}
/*============================================================================*/
str_t C(C_t ** ζζ, int entry) {
    C_t * ζ = *ζζ;
    if (entry == α){ ζ = enter((void **) ζζ, sizeof(C_t));   goto C_α; }
    if (entry == β){                                         goto C_β; }
    /*------------------------------------------------------------------------*/
    str_t         POS46;
    POS46_α:      if (Δ != 0)                               goto POS46_ω;
                  POS46 = str(Σ+Δ,0);                       goto POS46_γ;
    POS46_β:                                                goto POS46_ω;
    /*------------------------------------------------------------------------*/
    str_t         X47;
    X47_α:        X47 = X(&ζ->X47_ζ, α);                    goto X47_λ;
    X47_β:        X47 = X(&ζ->X47_ζ, β);                    goto X47_λ;
    X47_λ:        if (is_empty(X47))                        goto X47_ω;
                  else                                      goto X47_γ;
    /*------------------------------------------------------------------------*/
    str_t         RPOS48;
    RPOS48_α:     if (Δ != Ω-0)                             goto RPOS48_ω;
                  RPOS48 = str(Σ+Δ,0);                      goto RPOS48_γ;
    RPOS48_β:                                               goto RPOS48_ω;
    /*------------------------------------------------------------------------*/
    str_t         seq45;
    seq45_α:      seq45 = str(Σ+Δ,0);                       goto POS46_α;
    seq45_β:                                                goto RPOS48_β;
    POS46_γ:      seq45 = cat(seq45, POS46);                goto X47_α;
    POS46_ω:                                                goto seq45_ω;
    X47_γ:        seq45 = cat(seq45, X47);                  goto RPOS48_α;
    X47_ω:                                                  goto POS46_β;
    RPOS48_γ:     seq45 = cat(seq45, RPOS48);               goto seq45_γ;
    RPOS48_ω:                                               goto X47_β;
    /*------------------------------------------------------------------------*/
    str_t         OUTPUT44;
    OUTPUT44_α:                                             goto seq45_α;
    OUTPUT44_β:                                             goto seq45_β;
    seq45_γ:      OUTPUT44 = write_str(out, seq45);         
                  write_nl(out);                            goto OUTPUT44_γ;
    seq45_ω:                                                goto OUTPUT44_ω;
    /*------------------------------------------------------------------------*/
    C_α:                                                    goto OUTPUT44_α;
    C_β:                                                    goto OUTPUT44_β;
    OUTPUT44_γ:   return OUTPUT44;
    OUTPUT44_ω:   return empty;
}
/*============================================================================*/
str_t match49(match49_t ** ζζ, int entry) {
    match49_t * ζ = *ζζ;
    if (entry == α){ ζ = enter((void **) ζζ, sizeof(match49_t));goto match49_α; }
    if (entry == β){                                         goto match49_β; }
    /*------------------------------------------------------------------------*/
    str_t         subj50;
    subj50_α:     Δ = 0; Σ = "x+y*z";                       
                  Ω = len(Σ); subj50 = str(Σ,Ω);            goto subj50_γ;
    subj50_β:                                               goto subj50_ω;
    /*------------------------------------------------------------------------*/
    str_t         C51;
    C51_α:        C51 = C(&ζ->C51_ζ, α);                    goto C51_λ;
    C51_β:        C51 = C(&ζ->C51_ζ, β);                    goto C51_λ;
    C51_λ:        if (is_empty(C51))                        goto C51_ω;
                  else                                      goto C51_γ;
    /*------------------------------------------------------------------------*/
    str_t         match49;
    match49_α:                                              goto subj50_α;
    match49_β:                                              goto C51_β;
    subj50_γ:                                               goto C51_α;
    subj50_ω:     return empty;
    C51_γ:        return C51;
    C51_ω:        return empty;
}
/*============================================================================*/
__kernel void snobol(
    __global const char * in,
    __global       char * buffer,
             const int    num_chars) {
    /*------------------------------------------------------------------------*/
    const char cszFailure[9] = "Failure.";
    const char cszSuccess[10] = "Success: ";
    output_t output = {0, buffer};
    output_t * out = &output;
    for (int i = 0; i < num_chars; i++)
        buffer[i] = 0;
    /*------------------------------------------------------------------------*/
    str_t         main1;
    match49_t     match49_ζ;
    match49_t *   match49_ζζ;
                  match49_ζζ = &match49_ζ;
                  main1 = match49(&match49_ζζ, α);          goto match49_λ;
    match49_β:    main1 = match49(&match49_ζζ, β);          goto match49_λ;
    match49_λ:    if (is_empty(main1))                      goto match49_ω;
                  else                                      goto match49_γ;
/*----------------------------------------------------------------------------*/
    match49_γ:    write_sz(out, cszSuccess);
                  write_str(out, main1);
                  write_nl(out);                            goto match49_β;
    match49_ω:    write_sz(out, cszFailure);
                  write_nl(out);                            return;
}

#ifdef __GNUC__
static char szOutput[1024] = {0};
int main() {
    snobol((const char *) 0, szOutput, sizeof(szOutput));
    return 0;
}
#endif
    /*------------------------------------------------------------------------*/
