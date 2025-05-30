#ifdef __GNUC__
#define __kernel
#define __global
extern int printf(char *, ...);
extern void assert(int a);
#endif

typedef struct { const char * σ; int δ; } m_t;
typedef struct { unsigned int pos; __global char * buffer; } output_t;

#if 0
void write_nl(output_t * out) {}
int  write_int(output_t * out, int v) {}
void write_str(output_t * out, const char * s) {}
void write_flush(output_t * out) {}
#else
#if 1
extern int printf(char *, ...);
void write_nl(output_t * out) { printf("%s", "\n"); }
int  write_int(output_t * out, int v) { printf("%d\n", v); return v; }
void write_str(output_t * out, const char * s) { printf("%s\n", s); }
m_t  write_slice(output_t * out, m_t slice) { printf("%.*s\n", slice.σ, slice.δ); return slice; }
void write_flush(output_t * out) {}
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

    void write_str(output_t * out, const char * s) {
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

__kernel void icon(
    __global const char * in,
    __global       char * buffer,
             const int    num_chars)
{
    const char cszFailure[9] = "Failure.";
    const char cszSuccess[9] = "Success!";
    const m_t  empty = {0, 0};
    const m_t  fail = {0, -1};
    output_t output = {0, buffer};
    output_t * out = &output;
    for (int i = 0; i < num_chars; i++)
        buffer[i] = 0;
/*----------------------------------------------------------------------------*/
    inline int str_len(const char * s) { int len = 0; for (; *s; len++) s++; return len; }
/*----------------------------------------------------------------------------*/
    const char * Σ = in;
    int Ω = str_len(Σ);
    int Δ = 0;
    goto main1_α;
/*----------------------------------------------------------------------------*/
    m_t         POS0 = empty;
    POS0_α:     if (Δ != 0)                     goto POS0_ω;
                POS0 = (m_t) {Σ, 0};            goto POS0_Ω;
    POS0_β:     POS0 = (m_t) {0,-1};            goto POS0_ω;
/*----------------------------------------------------------------------------*/
    m_t         bird = empty;
    bird_α:     bird = (m_t) {Σ, 0};
                if (bird.σ[0] != 'B')           goto bird_ω;
                if (bird.σ[1] != 'I')           goto bird_ω;
                if (bird.σ[2] != 'R')           goto bird_ω;
                if (bird.σ[3] != 'D')           goto bird_ω;
                bird = (m_t) {Σ, 4};            goto bird_Ω;
    bird_β:     bird = (m_t) {0,-1};            goto bird_ω;
/*----------------------------------------------------------------------------*/
    m_t         RPOS0 = empty;
    RPOS0_α:    if (Δ != Ω)                     goto RPOS0_ω;
                RPOS0 = (m_t) {Σ, 0};           goto RPOS0_Ω;
    RPOS0_β:    RPOS0 = (m_t) {0,-1};           goto RPOS0_ω;
/*----------------------------------------------------------------------------*/
    m_t         seq7 = empty;
    seq7_α:                                     goto bird_α;
    seq7_β:                                     goto RPOS0_β;
    bird_ω:                                     goto seq7_ω;
    bird_Ω:                                     goto RPOS0_α;
    RPOS0_ω:                                    goto bird_β;
    RPOS0_Ω:    seq7.σ = bird.σ;
                seq7.δ = bird.δ + RPOS0.δ;      goto seq7_Ω;
/*----------------------------------------------------------------------------*/
    m_t         seq4 = empty;
    seq4_α:                                     goto POS0_α;
    seq4_β:                                     goto seq7_β;
    POS0_ω:                                     goto seq4_ω;
    POS0_Ω:                                     goto seq7_α;
    seq7_ω:                                     goto POS0_β;
    seq7_Ω:     seq4.σ = POS0.σ;
                seq4.δ = POS0.δ + seq7.δ;       goto seq4_Ω;
/*----------------------------------------------------------------------------*/
    m_t         write = empty;
    write_α:                                    goto seq4_α;
    write_β:                                    goto seq4_β;
    seq4_ω:                                     goto write_ω;
    seq4_Ω:     write = write_slice(out, seq4); goto write_Ω;
/*----------------------------------------------------------------------------*/
    main1_α:                                    goto write_α;
    main1_β:                                    return;
    write_ω:   write_str(out, cszFailure);      return;
    write_Ω:   write_str(out, cszSuccess);      goto write_β;
}

#ifdef __GNUC__
static char buffer[1024] = {0};
int main() {
    icon(0, buffer, sizeof(buffer));
    return 0;
}
#endif
