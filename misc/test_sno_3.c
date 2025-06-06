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
/*----------------------------------------------------------------------------*/
typedef struct _V {
} V_t;
/*----------------------------------------------------------------------------*/
typedef struct _I {
    int SPAN5_δ;
} I_t;
/*----------------------------------------------------------------------------*/
typedef struct _E {
    int alt7_i;
    V_t * V8_ζ;
    I_t * I9_ζ;
    X_t * X12_ζ;
} E_t;
/*----------------------------------------------------------------------------*/
typedef struct _X {
    int alt15_i;
    E_t * E17_ζ;
    X_t * X19_ζ;
    E_t * E21_ζ;
    X_t * X23_ζ;
    E_t * E25_ζ;
    X_t * X27_ζ;
    E_t * E29_ζ;
    X_t * X31_ζ;
    X_t * X34_ζ;
    X_t * X37_ζ;
    E_t * E38_ζ;
} X_t;
/*----------------------------------------------------------------------------*/
typedef struct _C {
    X_t * X42_ζ;
} C_t;
/*----------------------------------------------------------------------------*/
str_t V(V_t **, int);
str_t I(I_t **, int);
str_t E(E_t **, int);
str_t X(X_t **, int);
str_t C(C_t **, int);
/*============================================================================*/
str_t V(V_t ** ζζ, int entry) {
    V_t * ζ = *ζζ;
    if (entry == α){ ζ = enter((void **) ζζ, sizeof(V_t));   goto V_α; }
    if (entry == β){                                         goto V_β; }
    /*------------------------------------------------------------------------*/
    str_t         ANY3;
    ANY3_α:       if (Σ[Δ] == 'a')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'b')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'c')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'd')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'e')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'f')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'g')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'h')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'i')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'j')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'k')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'l')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'm')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'n')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'o')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'p')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'q')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'r')                          goto ANY3_αγ;
                  if (Σ[Δ] == 's')                          goto ANY3_αγ;
                  if (Σ[Δ] == 't')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'u')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'v')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'w')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'x')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'y')                          goto ANY3_αγ;
                  if (Σ[Δ] == 'z')                          goto ANY3_αγ;
                                                            goto ANY3_ω;
    ANY3_αγ:      ANY3 = str(Σ+Δ,1); Δ+=1;                  goto ANY3_γ;
    ANY3_β:       Δ-=1;                                     goto ANY3_ω;
    /*------------------------------------------------------------------------*/
    V_α:                                                    goto ANY3_α;
    V_β:                                                    goto ANY3_β;
    ANY3_γ:       return ANY3;
    ANY3_ω:       return empty;
}
/*============================================================================*/
str_t I(I_t ** ζζ, int entry) {
    I_t * ζ = *ζζ;
    if (entry == α){ ζ = enter((void **) ζζ, sizeof(I_t));   goto I_α; }
    if (entry == β){                                         goto I_β; }
    /*------------------------------------------------------------------------*/
    str_t         SPAN5;
    SPAN5_α:      for (ζ->SPAN5_δ = 0; Σ[Δ+ζ->SPAN5_δ]; ζ->SPAN5_δ++) {
                      if (Σ[Δ+ζ->SPAN5_δ] == '0') continue;
                      if (Σ[Δ+ζ->SPAN5_δ] == '1') continue;
                      if (Σ[Δ+ζ->SPAN5_δ] == '2') continue;
                      if (Σ[Δ+ζ->SPAN5_δ] == '3') continue;
                      if (Σ[Δ+ζ->SPAN5_δ] == '4') continue;
                      if (Σ[Δ+ζ->SPAN5_δ] == '5') continue;
                      if (Σ[Δ+ζ->SPAN5_δ] == '6') continue;
                      if (Σ[Δ+ζ->SPAN5_δ] == '7') continue;
                      if (Σ[Δ+ζ->SPAN5_δ] == '8') continue;
                      if (Σ[Δ+ζ->SPAN5_δ] == '9') continue;
                      break;                                
                  }                                         
                  if (ζ->SPAN5_δ <= 0)                      goto SPAN5_ω;
                  SPAN5 = str(Σ+Δ,ζ->SPAN5_δ); Δ+=ζ->SPAN5_δ;goto SPAN5_γ;
    SPAN5_β:      Δ-=ζ->SPAN5_δ;                            goto SPAN5_ω;
    /*------------------------------------------------------------------------*/
    I_α:                                                    goto SPAN5_α;
    I_β:                                                    goto SPAN5_β;
    SPAN5_γ:      return SPAN5;
    SPAN5_ω:      return empty;
}
/*============================================================================*/
str_t E(E_t ** ζζ, int entry) {
    E_t * ζ = *ζζ;
    if (entry == α){ ζ = enter((void **) ζζ, sizeof(E_t));   goto E_α; }
    if (entry == β){                                         goto E_β; }
    /*------------------------------------------------------------------------*/
    str_t         V8;
    V8_α:         V8 = V(&ζ->V8_ζ, α);                      goto V8_λ;
    V8_β:         V8 = V(&ζ->V8_ζ, β);                      goto V8_λ;
    V8_λ:         if (is_empty(V8))                         goto V8_ω;
                  else                                      goto V8_γ;
    /*------------------------------------------------------------------------*/
    str_t         I9;
    I9_α:         I9 = I(&ζ->I9_ζ, α);                      goto I9_λ;
    I9_β:         I9 = I(&ζ->I9_ζ, β);                      goto I9_λ;
    I9_λ:         if (is_empty(I9))                         goto I9_ω;
                  else                                      goto I9_γ;
    /*------------------------------------------------------------------------*/
    str_t         s11;
    s11_α:        if (Σ[Δ+0] != '(')                        goto s11_ω;
                  s11 = str(Σ+Δ,1); Δ+=1;                   goto s11_γ;
    s11_β:        Δ-=1;                                     goto s11_ω;
    /*------------------------------------------------------------------------*/
    str_t         X12;
    X12_α:        X12 = X(&ζ->X12_ζ, α);                    goto X12_λ;
    X12_β:        X12 = X(&ζ->X12_ζ, β);                    goto X12_λ;
    X12_λ:        if (is_empty(X12))                        goto X12_ω;
                  else                                      goto X12_γ;
    /*------------------------------------------------------------------------*/
    str_t         s13;
    s13_α:        if (Σ[Δ+0] != ')')                        goto s13_ω;
                  s13 = str(Σ+Δ,1); Δ+=1;                   goto s13_γ;
    s13_β:        Δ-=1;                                     goto s13_ω;
    /*------------------------------------------------------------------------*/
    str_t         seq10;
    seq10_α:      seq10 = str(Σ+Δ,0);                       goto s11_α;
    seq10_β:                                                goto s13_β;
    s11_γ:        seq10 = cat(seq10, s11);                  goto X12_α;
    s11_ω:                                                  goto seq10_ω;
    X12_γ:        seq10 = cat(seq10, X12);                  goto s13_α;
    X12_ω:                                                  goto s11_β;
    s13_γ:        seq10 = cat(seq10, s13);                  goto seq10_γ;
    s13_ω:                                                  goto X12_β;
    /*------------------------------------------------------------------------*/
    str_t         alt7;
    alt7_α:       ζ->alt7_i = 1;                            goto V8_α;
    alt7_β:       if (ζ->alt7_i == 1)                       goto V8_β;
                  if (ζ->alt7_i == 2)                       goto I9_β;
                  if (ζ->alt7_i == 3)                       goto seq10_β;
                                                            goto alt7_ω;
    V8_γ:         alt7 = V8;                                goto alt7_γ;
    V8_ω:         ζ->alt7_i++;                              goto I9_α;
    I9_γ:         alt7 = I9;                                goto alt7_γ;
    I9_ω:         ζ->alt7_i++;                              goto seq10_α;
    seq10_γ:      alt7 = seq10;                             goto alt7_γ;
    seq10_ω:                                                goto alt7_ω;
    /*------------------------------------------------------------------------*/
    E_α:                                                    goto alt7_α;
    E_β:                                                    goto alt7_β;
    alt7_γ:       return alt7;
    alt7_ω:       return empty;
}
/*============================================================================*/
str_t X(X_t ** ζζ, int entry) {
    X_t * ζ = *ζζ;
    if (entry == α){ ζ = enter((void **) ζζ, sizeof(X_t));   goto X_α; }
    if (entry == β){                                         goto X_β; }
    /*------------------------------------------------------------------------*/
    str_t         E17;
    E17_α:        E17 = E(&ζ->E17_ζ, α);                    goto E17_λ;
    E17_β:        E17 = E(&ζ->E17_ζ, β);                    goto E17_λ;
    E17_λ:        if (is_empty(E17))                        goto E17_ω;
                  else                                      goto E17_γ;
    /*------------------------------------------------------------------------*/
    str_t         s18;
    s18_α:        if (Σ[Δ+0] != '+')                        goto s18_ω;
                  s18 = str(Σ+Δ,1); Δ+=1;                   goto s18_γ;
    s18_β:        Δ-=1;                                     goto s18_ω;
    /*------------------------------------------------------------------------*/
    str_t         X19;
    X19_α:        X19 = X(&ζ->X19_ζ, α);                    goto X19_λ;
    X19_β:        X19 = X(&ζ->X19_ζ, β);                    goto X19_λ;
    X19_λ:        if (is_empty(X19))                        goto X19_ω;
                  else                                      goto X19_γ;
    /*------------------------------------------------------------------------*/
    str_t         seq16;
    seq16_α:      seq16 = str(Σ+Δ,0);                       goto E17_α;
    seq16_β:                                                goto X19_β;
    E17_γ:        seq16 = cat(seq16, E17);                  goto s18_α;
    E17_ω:                                                  goto seq16_ω;
    s18_γ:        seq16 = cat(seq16, s18);                  goto X19_α;
    s18_ω:                                                  goto E17_β;
    X19_γ:        seq16 = cat(seq16, X19);                  goto seq16_γ;
    X19_ω:                                                  goto s18_β;
    /*------------------------------------------------------------------------*/
    str_t         E21;
    E21_α:        E21 = E(&ζ->E21_ζ, α);                    goto E21_λ;
    E21_β:        E21 = E(&ζ->E21_ζ, β);                    goto E21_λ;
    E21_λ:        if (is_empty(E21))                        goto E21_ω;
                  else                                      goto E21_γ;
    /*------------------------------------------------------------------------*/
    str_t         s22;
    s22_α:        if (Σ[Δ+0] != '-')                        goto s22_ω;
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
    s26_α:        if (Σ[Δ+0] != '*')                        goto s26_ω;
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
    s30_α:        if (Σ[Δ+0] != '/')                        goto s30_ω;
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
    str_t         s33;
    s33_α:        if (Σ[Δ+0] != '+')                        goto s33_ω;
                  s33 = str(Σ+Δ,1); Δ+=1;                   goto s33_γ;
    s33_β:        Δ-=1;                                     goto s33_ω;
    /*------------------------------------------------------------------------*/
    str_t         X34;
    X34_α:        X34 = X(&ζ->X34_ζ, α);                    goto X34_λ;
    X34_β:        X34 = X(&ζ->X34_ζ, β);                    goto X34_λ;
    X34_λ:        if (is_empty(X34))                        goto X34_ω;
                  else                                      goto X34_γ;
    /*------------------------------------------------------------------------*/
    str_t         seq32;
    seq32_α:      seq32 = str(Σ+Δ,0);                       goto s33_α;
    seq32_β:                                                goto X34_β;
    s33_γ:        seq32 = cat(seq32, s33);                  goto X34_α;
    s33_ω:                                                  goto seq32_ω;
    X34_γ:        seq32 = cat(seq32, X34);                  goto seq32_γ;
    X34_ω:                                                  goto s33_β;
    /*------------------------------------------------------------------------*/
    str_t         s36;
    s36_α:        if (Σ[Δ+0] != '-')                        goto s36_ω;
                  s36 = str(Σ+Δ,1); Δ+=1;                   goto s36_γ;
    s36_β:        Δ-=1;                                     goto s36_ω;
    /*------------------------------------------------------------------------*/
    str_t         X37;
    X37_α:        X37 = X(&ζ->X37_ζ, α);                    goto X37_λ;
    X37_β:        X37 = X(&ζ->X37_ζ, β);                    goto X37_λ;
    X37_λ:        if (is_empty(X37))                        goto X37_ω;
                  else                                      goto X37_γ;
    /*------------------------------------------------------------------------*/
    str_t         seq35;
    seq35_α:      seq35 = str(Σ+Δ,0);                       goto s36_α;
    seq35_β:                                                goto X37_β;
    s36_γ:        seq35 = cat(seq35, s36);                  goto X37_α;
    s36_ω:                                                  goto seq35_ω;
    X37_γ:        seq35 = cat(seq35, X37);                  goto seq35_γ;
    X37_ω:                                                  goto s36_β;
    /*------------------------------------------------------------------------*/
    str_t         E38;
    E38_α:        E38 = E(&ζ->E38_ζ, α);                    goto E38_λ;
    E38_β:        E38 = E(&ζ->E38_ζ, β);                    goto E38_λ;
    E38_λ:        if (is_empty(E38))                        goto E38_ω;
                  else                                      goto E38_γ;
    /*------------------------------------------------------------------------*/
    str_t         alt15;
    alt15_α:      ζ->alt15_i = 1;                           goto seq16_α;
    alt15_β:      if (ζ->alt15_i == 1)                      goto seq16_β;
                  if (ζ->alt15_i == 2)                      goto seq20_β;
                  if (ζ->alt15_i == 3)                      goto seq24_β;
                  if (ζ->alt15_i == 4)                      goto seq28_β;
                  if (ζ->alt15_i == 5)                      goto seq32_β;
                  if (ζ->alt15_i == 6)                      goto seq35_β;
                  if (ζ->alt15_i == 7)                      goto E38_β;
                                                            goto alt15_ω;
    seq16_γ:      alt15 = seq16;                            goto alt15_γ;
    seq16_ω:      ζ->alt15_i++;                             goto seq20_α;
    seq20_γ:      alt15 = seq20;                            goto alt15_γ;
    seq20_ω:      ζ->alt15_i++;                             goto seq24_α;
    seq24_γ:      alt15 = seq24;                            goto alt15_γ;
    seq24_ω:      ζ->alt15_i++;                             goto seq28_α;
    seq28_γ:      alt15 = seq28;                            goto alt15_γ;
    seq28_ω:      ζ->alt15_i++;                             goto seq32_α;
    seq32_γ:      alt15 = seq32;                            goto alt15_γ;
    seq32_ω:      ζ->alt15_i++;                             goto seq35_α;
    seq35_γ:      alt15 = seq35;                            goto alt15_γ;
    seq35_ω:      ζ->alt15_i++;                             goto E38_α;
    E38_γ:        alt15 = E38;                              goto alt15_γ;
    E38_ω:                                                  goto alt15_ω;
    /*------------------------------------------------------------------------*/
    X_α:                                                    goto alt15_α;
    X_β:                                                    goto alt15_β;
    alt15_γ:      return alt15;
    alt15_ω:      return empty;
}
/*============================================================================*/
str_t C(C_t ** ζζ, int entry) {
    C_t * ζ = *ζζ;
    if (entry == α){ ζ = enter((void **) ζζ, sizeof(C_t));   goto C_α; }
    if (entry == β){                                         goto C_β; }
    /*------------------------------------------------------------------------*/
    str_t         POS41;
    POS41_α:      if (Δ != 0)                               goto POS41_ω;
                  POS41 = str(Σ+Δ,0);                       goto POS41_γ;
    POS41_β:                                                goto POS41_ω;
    /*------------------------------------------------------------------------*/
    str_t         X42;
    X42_α:        X42 = X(&ζ->X42_ζ, α);                    goto X42_λ;
    X42_β:        X42 = X(&ζ->X42_ζ, β);                    goto X42_λ;
    X42_λ:        if (is_empty(X42))                        goto X42_ω;
                  else                                      goto X42_γ;
    /*------------------------------------------------------------------------*/
    str_t         RPOS43;
    RPOS43_α:     if (Δ != Ω-0)                             goto RPOS43_ω;
                  RPOS43 = str(Σ+Δ,0);                      goto RPOS43_γ;
    RPOS43_β:                                               goto RPOS43_ω;
    /*------------------------------------------------------------------------*/
    str_t         seq40;
    seq40_α:      seq40 = str(Σ+Δ,0);                       goto POS41_α;
    seq40_β:                                                goto RPOS43_β;
    POS41_γ:      seq40 = cat(seq40, POS41);                goto X42_α;
    POS41_ω:                                                goto seq40_ω;
    X42_γ:        seq40 = cat(seq40, X42);                  goto RPOS43_α;
    X42_ω:                                                  goto POS41_β;
    RPOS43_γ:     seq40 = cat(seq40, RPOS43);               goto seq40_γ;
    RPOS43_ω:                                               goto X42_β;
    /*------------------------------------------------------------------------*/
    C_α:                                                    goto seq40_α;
    C_β:                                                    goto seq40_β;
    seq40_γ:      return seq40;
    seq40_ω:      return empty;
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
                                                            goto main1_α;
    str_t         subj45;
    subj45_α:     Δ = 0; Σ = "x+y*z";                       
                  Ω = len(Σ); subj45 = str(Σ,Ω);            goto subj45_γ;
    subj45_β:                                               goto subj45_ω;
    /*------------------------------------------------------------------------*/
    str_t         C46;
    C46_α:        C46 = C(&ζ->C46_ζ, α);                    goto C46_λ;
    C46_β:        C46 = C(&ζ->C46_ζ, β);                    goto C46_λ;
    C46_λ:        if (is_empty(C46))                        goto C46_ω;
                  else                                      goto C46_γ;
    /*------------------------------------------------------------------------*/
    str_t         match44;
    match44_α:                                              goto subj45_α;
    match44_β:                                              goto match44_ω;
    subj45_γ:                                               goto C46_α;
    subj45_ω:                                               goto match44_ω;
    C46_γ:        match44 = C46;                            goto match44_γ;
    C46_ω:                                                  goto match44_ω;
    main1_α:                                                goto match44_α;
    main1_β:                                                return;
    match44_γ:    write_sz(out, cszSuccess);                
                  write_str(out, match44);                  
                  write_nl(out);                            goto match44_β;
    match44_ω:    write_sz(out, cszFailure);                
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
