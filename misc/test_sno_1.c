#ifdef __GNUC__
#define __kernel
#define __global
#include <assert.h>
extern int printf(char *, ...);
//extern void assert(int a);
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
extern int printf(char *, ...);
void    write_nl(output_t * out) { printf("%s", "\n"); }
int     write_int(output_t * out, int v) { printf("%d\n", v); return v; }
void    write_sz(output_t * out, const char * s) { printf("%s\n", s); }
str_t   write_str(output_t * out, str_t str) {
            printf("%.*s\n", str.δ, str.σ);
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
__kernel void snobol(
    __global const char * Σ,
    __global       char * buffer,
             const int    num_chars) {
    /*------------------------------------------------------------------------*/
    const char cszFailure[9] = "Failure.";
    const char cszSuccess[9] = "Success!";
    const str_t empty = {0, 0};
    output_t output = {0, buffer};
    output_t * out = &output;
    for (int i = 0; i < num_chars; i++)
        buffer[i] = 0;
    /*------------------------------------------------------------------------*/
    inline int len(const char * s) { int δ = 0; for (; *s; δ++) s++; return δ; }
    inline str_t str(const char * σ, int δ) { return (str_t) {σ, δ}; }
    inline str_t cat(str_t x, str_t y) { return (str_t) {x.σ, x.δ + y.δ}; }
    /*------------------------------------------------------------------------*/
    int Δ = 0;
    int Ω = len(Σ);
    goto main1_α;
    /*------------------------------------------------------------------------*/
    /*          POS(0) ARBNO('Bird' | 'Blue' | LEN(1)) $ OUTPUT RPOS(0)       */
    /*------------------------------------------------------------------------*/
    str_t       POS0;
    POS0_α:     if (Δ != 0)                         goto POS0_ω;
                POS0 = str(Σ+Δ, 0);                 goto POS0_γ;
    POS0_β:                                         goto POS0_ω;
    /*------------------------------------------------------------------------*/
    str_t       BIRD;
    BIRD_α:     if (Σ[Δ+0] != 'B')                  goto BIRD_ω;
                if (Σ[Δ+1] != 'i')                  goto BIRD_ω;
                if (Σ[Δ+2] != 'r')                  goto BIRD_ω;
                if (Σ[Δ+3] != 'd')                  goto BIRD_ω;
                BIRD = str(Σ+Δ, 4);
                Δ += 4;                             goto BIRD_γ;
    BIRD_β:     Δ -= 4;                             goto BIRD_ω;
    /*------------------------------------------------------------------------*/
    str_t       BLUE;
    BLUE_α:     if (Σ[Δ+0] != 'B')                  goto BLUE_ω;
                if (Σ[Δ+1] != 'l')                  goto BLUE_ω;
                if (Σ[Δ+2] != 'u')                  goto BLUE_ω;
                if (Σ[Δ+3] != 'e')                  goto BLUE_ω;
                BLUE = str(Σ+Δ, 4);
                Δ += 4;                             goto BLUE_γ;
    BLUE_β:     Δ -= 4;                             goto BLUE_ω;
    /*------------------------------------------------------------------------*/
    str_t       LEN1;
    LEN1_α:     if (Δ+1 > Ω)                        goto LEN1_ω;
                LEN1 = str(Σ+Δ,1); Δ+=1;            goto LEN1_γ;
    LEN1_β:     Δ-=1;                               goto LEN1_ω;
    /*------------------------------------------------------------------------*/
    typedef struct _1 { str_t ARBNO; str_t alt; int alt_i; } _1_t;
    _1_t _1[64];
    _1_t * ζ = &_1[0];
    /*------------------------------------------------------------------------*/
    alt_α:      ζ->alt_i = 1;                       goto BIRD_α;
    alt_β:      if (ζ->alt_i == 1)                  goto BIRD_β;
                if (ζ->alt_i == 2)                  goto BLUE_β;
                if (ζ->alt_i == 3)                  goto LEN1_β;
                                                    goto alt_ω;
    BIRD_γ:     ζ->alt = BIRD;                      goto alt_γ;
    BIRD_ω:     ζ->alt_i++;                         goto BLUE_α;
    BLUE_γ:     ζ->alt = BLUE;                      goto alt_γ;
    BLUE_ω:     ζ->alt_i++;                         goto LEN1_α;
    LEN1_γ:     ζ->alt = LEN1;                      goto alt_γ;
    LEN1_ω:                                         goto alt_ω;
    /*------------------------------------------------------------------------*/
    str_t       ARBNO;
    int         ARBNO_i;
    ARBNO_α:    ζ = &_1[ARBNO_i=0];
                ζ->ARBNO = str(Σ+Δ, 0);             goto alt_α;
    ARBNO_β:    ζ = &_1[++ARBNO_i];
                ζ->ARBNO = ARBNO;                   goto alt_α;
    alt_γ:      ARBNO = cat(ζ->ARBNO, ζ->alt);      goto ARBNO_γ;
    alt_ω:      if (ARBNO_i <= 0)                   goto ARBNO_ω;
                ARBNO_i--; ζ = &_1[ARBNO_i];        goto alt_β;
    /*------------------------------------------------------------------------*/
    str_t       assign;
    assign_α:                                       goto ARBNO_α;
    assign_β:                                       goto ARBNO_β;
    ARBNO_γ:    assign = write_str(out, ARBNO);
                write_nl(out);                      goto assign_γ;
    ARBNO_ω:                                        goto assign_ω;
    /*------------------------------------------------------------------------*/
    str_t       RPOS0;
    RPOS0_α:    if (Δ != Ω)                         goto RPOS0_ω;
                RPOS0 = str(Σ+Δ, 0);                goto RPOS0_γ;
    RPOS0_β:                                        goto RPOS0_ω;
    /*------------------------------------------------------------------------*/
    str_t       seq;
    seq_α:      seq = str(Σ+Δ, 0);                  goto POS0_α;
    seq_β:                                          goto RPOS0_β;
    POS0_γ:     seq = cat(seq, POS0);               goto assign_α;
    POS0_ω:                                         goto seq_ω;
    assign_γ:   seq = cat(seq, BIRD);               goto RPOS0_α;
    assign_ω:                                       goto POS0_β;
    RPOS0_γ:    seq = cat(seq, RPOS0);              goto seq_γ;
    RPOS0_ω:                                        goto assign_β;
    /*------------------------------------------------------------------------*/
    str_t       write;
    write_α:                                        goto seq_α;
    write_β:                                        goto seq_β;
    seq_γ:      write = write_str(out, seq);        goto write_γ;
    seq_ω:                                          goto write_ω;
    /*------------------------------------------------------------------------*/
    main1_α:                                        goto write_α;
    main1_β:                                        return;
    write_γ:    write_sz(out, cszSuccess);          return; /*goto write_β;*/
    write_ω:    write_sz(out, cszFailure);          return;
}

#ifdef __GNUC__
static char szOutput[1024] = {0};
static const char cszInput[] = "BlueGoldBirdFish";
int main() {
    snobol(cszInput, szOutput, sizeof(szOutput));
    return 0;
}
#endif
