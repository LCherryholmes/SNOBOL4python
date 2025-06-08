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
static inline bool not_null(str_t x) { return x.σ != (const char *) 0; }
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
typedef struct _match2 match2_t;
/*------------------------------------------------------------------------------------------------*/
/*------------------------------------------------------------------------------------------------*/
/*------------------------------------------------------------------------------------------------*/
typedef struct _match2 {
    a_t * a6_ζ;
} match2_t;
/*------------------------------------------------------------------------------------------------*/
str_t match2(match2_t **, int);
/*================================================================================================*/
str_t match2(match2_t ** ζζ, int entry) {
    match2_t * ζ = *ζζ;
    if (entry == α)     { ζ = ENTER(ζζ, sizeof(match2_t));            goto match2_α; }
    if (entry == β)     {                                             goto match2_β; }
    /*--------------------------------------------------------------------------------------------*/
    str_t               subj3;
    subj3_α:            Δ = 0; Σ = "SUBJECT";
                        Ω = len(Σ); subj3 = str(Σ,Ω);                 goto subj3_γ;
    subj3_β:                                                          goto subj3_ω;
    /*--------------------------------------------------------------------------------------------*/
    str_t               s5;
    s5_α:               if (Σ[Δ+0] != 'J')                            goto s5_ω;
                        s5 = str(Σ+Δ,1); Δ+=1;                        goto s5_γ;
    s5_β:               Δ-=1;                                         goto s5_ω;
    /*--------------------------------------------------------------------------------------------*/
    str_t               a6;
    a6_α:               a6 = a(&ζ->a6_ζ, α);                          goto a6_λ;
    a6_β:               a6 = a(&ζ->a6_ζ, β);                          goto a6_λ;
    a6_λ:               if (not_null(a6))                             goto a6_γ;
                        else                                          goto a6_ω;
    /*--------------------------------------------------------------------------------------------*/
    str_t               condition4;
    condition4_α:                                                     goto a6_α;
    condition4_β:                                                     goto a6_β;
    a6_γ:               condition4 = a6;
                        printf("%d %d\n", a6.σ-Σ, a6.δ);              goto condition4_γ;
    a6_ω:                                                             goto condition4_ω;
    /*--------------------------------------------------------------------------------------------*/
    str_t               match2;
    match2_α:                                                         goto subj3_α;
    match2_β:                                                         goto condition4_β;
    subj3_γ:                                                          goto condition4_α;
    subj3_ω:            return empty;
    condition4_γ:       return condition4;
    condition4_ω:       return empty;
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
    match2_t            match2_ζ;
    match2_t *          match2_ζζ;
                        match2_ζζ = &match2_ζ;
                        main1 = match2(&match2_ζζ, α);                goto match2_λ;
    match2_β:           main1 = match2(&match2_ζζ, β);                goto match2_λ;
    match2_λ:           if (not_null(main1))                          goto match2_γ;
                        else                                          goto match2_ω;
/*------------------------------------------------------------------------------------------------*/
    match2_γ:           write_sz(out, cszSuccess);
                        write_str(out, main1);
                        write_nl(out);                                goto match2_β;
    match2_ω:           write_sz(out, cszFailure);
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
