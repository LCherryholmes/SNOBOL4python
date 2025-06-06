#ifdef __GNUC__
#define __kernel
#define __global
#include <malloc.h>
#include <string.h>
#include <stdbool.h>
extern int printf(const char *, ...);
extern void assert(int a);
#endif
/*------------------------------------------------------------------------------------------------*/
typedef struct { const char * σ; int δ; } str_t;
typedef struct { unsigned int pos; __global char * buffer; } output_t;
/*------------------------------------------------------------------------------------------------*/
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
/*------------------------------------------------------------------------------------------------*/
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
static inline void Shift(const char * t, str_t v) { /**/ }
static output_t * out = (output_t *) 0;
/*------------------------------------------------------------------------------------------------*/
#define ENTER(ref, size) enter((void **) (ref), (size))
static inline void * enter(void ** ζζ, size_t size) {
    void * ζ = *ζζ;
    if (size)
        if (ζ) memset(ζ, 0, size);
        else ζ = *ζζ = calloc(1, size);
    return ζ;
}
/*------------------------------------------------------------------------------------------------*/
typedef struct _re_Quantifier re_Quantifier_t;
/*------------------------------------------------------------------------------------------------*/
typedef struct _re_Quantifier {
    int alt3_i;
} re_Quantifier_t;
/*------------------------------------------------------------------------------------------------*/
str_t re_Quantifier(re_Quantifier_t **, int);
/*================================================================================================*/
str_t re_Quantifier(re_Quantifier_t ** ζζ, int entry) {
    re_Quantifier_t * ζ = *ζζ;
    if (entry == α)     { ζ = ENTER(ζζ, sizeof(re_Quantifier_t));     goto re_Quantifier_α; }
    if (entry == β)     {                                             goto re_Quantifier_β; }
    /*--------------------------------------------------------------------------------------------*/
    str_t               s5;
    s5_α:               if (Σ[Δ+0] != '*')                            goto s5_ω;
                        s5 = str(Σ+Δ,1); Δ+=1;                        goto s5_γ;
    s5_β:               Δ-=1;                                         goto s5_ω;
    /*--------------------------------------------------------------------------------------------*/
    const char *        csz6;
    csz6_α:             csz6 = "*";                                   goto csz6_γ;
    /*--------------------------------------------------------------------------------------------*/
    str_t               condition4;
    condition4_α:                                                     goto s5_α;
    condition4_β:                                                     goto s5_β;
    s5_γ:                                                             goto csz6_α;
    s5_ω:                                                             goto condition4_ω;
    csz6_γ:             Shift(csz6, condition4);                      goto condition4_γ;
    csz6_ω:                                                           goto condition4_ω;
    /*--------------------------------------------------------------------------------------------*/
    str_t               s8;
    s8_α:               if (Σ[Δ+0] != '+')                            goto s8_ω;
                        s8 = str(Σ+Δ,1); Δ+=1;                        goto s8_γ;
    s8_β:               Δ-=1;                                         goto s8_ω;
    /*--------------------------------------------------------------------------------------------*/
    const char *        csz9;
    csz9_α:             csz9 = "+";                                   goto csz9_γ;
    /*--------------------------------------------------------------------------------------------*/
    str_t               condition7;
    condition7_α:                                                     goto s8_α;
    condition7_β:                                                     goto s8_β;
    s8_γ:                                                             goto csz9_α;
    s8_ω:                                                             goto condition7_ω;
    csz9_γ:             Shift(csz9, condition7);                      goto condition7_γ;
    csz9_ω:                                                           goto condition7_ω;
    /*--------------------------------------------------------------------------------------------*/
    str_t               s11;
    s11_α:              if (Σ[Δ+0] != '?')                            goto s11_ω;
                        s11 = str(Σ+Δ,1); Δ+=1;                       goto s11_γ;
    s11_β:              Δ-=1;                                         goto s11_ω;
    /*--------------------------------------------------------------------------------------------*/
    const char *        csz12;
    csz12_α:            csz12 = "?";                                  goto csz12_γ;
    /*--------------------------------------------------------------------------------------------*/
    str_t               condition10;
    condition10_α:                                                    goto s11_α;
    condition10_β:                                                    goto s11_β;
    s11_γ:                                                            goto csz12_α;
    s11_ω:                                                            goto condition10_ω;
    csz12_γ:            Shift(csz12, condition10);                    goto condition10_γ;
    csz12_ω:                                                          goto condition10_ω;
    /*--------------------------------------------------------------------------------------------*/
    str_t               alt3;
    alt3_α:             ζ->alt3_i = 1;                                goto condition4_α;
    alt3_β:             if (ζ->alt3_i == 1)                           goto condition4_β;
                        if (ζ->alt3_i == 2)                           goto condition7_β;
                        if (ζ->alt3_i == 3)                           goto condition10_β;
                                                                      goto alt3_ω;
    condition4_γ:       alt3 = condition4;                            goto alt3_γ;
    condition4_ω:       ζ->alt3_i++;                                  goto condition7_α;
    condition7_γ:       alt3 = condition7;                            goto alt3_γ;
    condition7_ω:       ζ->alt3_i++;                                  goto condition10_α;
    condition10_γ:      alt3 = condition10;                           goto alt3_γ;
    condition10_ω:                                                    goto alt3_ω;
    /*--------------------------------------------------------------------------------------------*/
    re_Quantifier_α:                                                  goto alt3_α;
    re_Quantifier_β:                                                  goto alt3_β;
    alt3_γ:             return alt3;
    alt3_ω:             return empty;
}
/*================================================================================================*/
__kernel void snobol(
    __global const char * in,
    __global       char * buffer,
             const int    num_chars) {
    /*--------------------------------------------------------------------------------------------*/
    const char cszFailure[9] = "Failure.";
    const char cszSuccess[10] = "Success: ";
    output_t output = {0, buffer};
    output_t * out = &output;
    for (int i = 0; i < num_chars; i++)
        buffer[i] = 0;
    /*--------------------------------------------------------------------------------------------*/
    str_t               main1;
    re_Quantifier_t     re_Quantifier_ζ;
    re_Quantifier_t *   re_Quantifier_ζζ;
                        re_Quantifier_ζζ = &re_Quantifier_ζ;
                        main1 = re_Quantifier(&re_Quantifier_ζζ, α);  goto re_Quantifier_λ;
    re_Quantifier_β:    main1 = re_Quantifier(&re_Quantifier_ζζ, β);  goto re_Quantifier_λ;
    re_Quantifier_λ:    if (is_empty(main1))                          goto re_Quantifier_ω;
                        else                                          goto re_Quantifier_γ;
/*------------------------------------------------------------------------------------------------*/
    re_Quantifier_γ:    write_sz(out, cszSuccess);
                        write_str(out, main1);
                        write_nl(out);                                goto re_Quantifier_β;
    re_Quantifier_ω:    write_sz(out, cszFailure);
                        write_nl(out);                                return;
}

#ifdef __GNUC__
static char szOutput[1024] = {0};
int main() {
    snobol((const char *) 0, szOutput, sizeof(szOutput));
    return 0;
}
#endif
    /*--------------------------------------------------------------------------------------------*/
