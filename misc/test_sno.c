#ifdef __GNUC__
#define __kernel
#define __global
extern int printf(char *, ...);
extern void assert(int a);
#endif

typedef struct {
             unsigned int    pos;
    __global unsigned char * buffer;
} output_t;

#if 0
void write_nl(output_t * out) {}
int  write_int(output_t * out, int v) {}
void write_str(output_t * out, const unsigned char * s) {}
void write_flush(output_t * out) {}
#else
#if 1
extern int printf(char *, ...);
void write_nl(output_t * out) { printf("%s", "\n"); }
int  write_int(output_t * out, int v) { printf("%d\n", v); return v; }
void write_str(output_t * out, const unsigned char * s) { printf("%s\n", s); }
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

    void write_str(output_t * out, const unsigned char * s) {
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
    __global const unsigned char * in,
    __global       unsigned char * buffer,
             const unsigned int num_chars)
{
    const unsigned char cszFailure[9] = "Failure.";
    const unsigned char cszSuccess[9] = "Success!";
    output_t output = { 0, buffer };
    output_t * out = &output;
    buffer[0] = 0;
    for (int i = 0; i < num_chars; i++)
        buffer[i] = 0;
                        goto main1_start;
int POS6_value;
    POS6_start:         POS6_value = POS;
                        goto POS6_succeed;
    POS6_resume:        goto POS6_fail;
int uminus5_value;
    uminus5_start:      goto POS6_start;
    uminus5_resume:     goto POS6_resume;
    POS6_fail:          goto uminus5_fail;
    POS6_succeed:       uminus5_value = -POS6_value;
                        goto uminus5_succeed;
int bird9_value;
    bird9_start:        bird9_value = bird;
                        goto bird9_succeed;
    bird9_resume:       goto bird9_fail;
int uminus8_value;
    uminus8_start:      goto bird9_start;
    uminus8_resume:     goto bird9_resume;
    bird9_fail:         goto uminus8_fail;
    bird9_succeed:      uminus8_value = -bird9_value;
                        goto uminus8_succeed;
int RPOS11_value;
    RPOS11_start:       RPOS11_value = RPOS;
                        goto RPOS11_succeed;
    RPOS11_resume:      goto RPOS11_fail;
int uminus10_value;
    uminus10_start:     goto RPOS11_start;
    uminus10_resume:    goto RPOS11_resume;
    RPOS11_fail:        goto uminus10_fail;
    RPOS11_succeed:     uminus10_value = -RPOS11_value;
                        goto uminus10_succeed;
int plus7_value;
    plus7_start:        goto uminus8_start;
    plus7_resume:       goto uminus10_resume;
    uminus8_fail:       goto plus7_fail;
    uminus8_succeed:    goto uminus10_start;
    uminus10_fail:      goto uminus8_resume;
    uminus10_succeed:   plus7_value = uminus8_value + uminus10_value;
                        goto plus7_succeed;
int plus4_value;
    plus4_start:        goto uminus5_start;
    plus4_resume:       goto plus7_resume;
    uminus5_fail:       goto plus4_fail;
    uminus5_succeed:    goto plus7_start;
    plus7_fail:         goto uminus5_resume;
    plus7_succeed:      plus4_value = uminus5_value + plus7_value;
                        goto plus4_succeed;
int write3_value;
    write3_start:       goto plus4_start;
    write3_resume:      goto plus4_resume;
    plus4_fail:         goto write3_fail;
    plus4_succeed:      write3_value = write_int(out, plus4_value);
                        goto write3_succeed;
    main1_start:        goto write3_start;
    main1_resume:       return; /* function re-entry? */
    write3_fail:        write_str(out, cszFailure);
                        return;
    write3_succeed:     write_str(out, cszSuccess);
                        goto write3_resume;
}

#ifdef __GNUC__
static unsigned char buffer[1024] = {0};
int main() {
    icon(0, buffer, sizeof(buffer));
    return 0;
}
#endif
