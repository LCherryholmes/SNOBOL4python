#ifdef __GNUC__
#define __kernel
#define __global
extern int printf(char *, ...);
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
    typedef struct _state {
        str_t POS0;
        str_t BIRD;
        str_t RPOS0;
        str_t seq;
        str_t write;
    } state_t;
    state_t state;
    state_t * ζ = &state;
    /*------------------------------------------------------------------------*/
    int Δ = 0;
    int Ω = len(Σ);
    goto main1_α;
    /*------------------------------------------------------------------------*/
    POS0_α:     if (Δ != 0)                         goto POS0_ω;
                ζ->POS0 = str(Σ+Δ, 0);              goto POS0_γ;
    POS0_β:                                         goto POS0_ω;
    /*------------------------------------------------------------------------*/
    BIRD_α:     if (Σ[Δ+0] != 'B')                  goto BIRD_ω;
                if (Σ[Δ+1] != 'I')                  goto BIRD_ω;
                if (Σ[Δ+2] != 'R')                  goto BIRD_ω;
                if (Σ[Δ+3] != 'D')                  goto BIRD_ω;
                ζ->BIRD = str(Σ+Δ, 4);
                Δ += 4;                             goto BIRD_γ;
    BIRD_β:     Δ -= 4;                             goto BIRD_ω;
    /*------------------------------------------------------------------------*/
    RPOS0_α:    if (Δ != Ω)                         goto RPOS0_ω;
                ζ->RPOS0 = str(Σ+Δ, 0);             goto RPOS0_γ;
    RPOS0_β:                                        goto RPOS0_ω;
    /*------------------------------------------------------------------------*/
    seq_α:      ζ->seq = str(Σ+Δ, 0);               goto POS0_α;
    seq_β:                                          goto RPOS0_β;
    POS0_γ:     ζ->seq = cat(ζ->seq, ζ->POS0);      goto BIRD_α;
    POS0_ω:                                         goto seq_ω;
    BIRD_γ:     ζ->seq = cat(ζ->seq, ζ->BIRD);      goto RPOS0_α;
    BIRD_ω:                                         goto POS0_β;
    RPOS0_γ:    ζ->seq = cat(ζ->seq, ζ->RPOS0);     goto seq_γ;
    RPOS0_ω:                                        goto BIRD_β;
    /*------------------------------------------------------------------------*/
    write_α:                                        goto seq_α;
    write_β:                                        goto seq_β;
    seq_γ:      ζ->write = write_str(out, ζ->seq);  goto write_γ;
    seq_ω:                                          goto write_ω;
    /*------------------------------------------------------------------------*/
    main1_α:                                        goto write_α;
    main1_β:                                        return;
    write_γ:    write_sz(out, cszSuccess);          return; /*goto write_β;*/
    write_ω:    write_sz(out, cszFailure);          return;
}

#ifdef __GNUC__
static char szOutput[1024] = {0};
static const char cszInput[] = "BIRD";
int main() {
    snobol(cszInput, szOutput, sizeof(szOutput));
    return 0;
}
#endif
