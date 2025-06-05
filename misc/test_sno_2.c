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
/*============================================================================*/
typedef struct _delim {
} delim_t;
/*----------------------------------------------------------------------------*/
str_t delim(delim_t * ζ, int entry) {
    if (entry == α) goto delim_α;
    if (entry == β) goto delim_β;
    /*------------------------------------------------------------------------*/
    str_t         SPAN3;
    int           SPAN3_δ;
    SPAN3_α:      for (SPAN3_δ = 0; Σ[Δ+SPAN3_δ]; SPAN3_δ++) {
                      if (Σ[Δ+SPAN3_δ] == ' ') continue;    
                      break;                                
                  }                                         
                  if (SPAN3_δ <= 0)                         goto SPAN3_ω;
                  SPAN3 = str(Σ+Δ,SPAN3_δ); Δ+=SPAN3_δ;     goto SPAN3_γ;
    SPAN3_β:      Δ-=SPAN3_δ;                               goto SPAN3_ω;
    /*------------------------------------------------------------------------*/
    delim_α:                                                goto SPAN3_α;
    delim_β:                                                goto SPAN3_β;
    SPAN3_γ:      return SPAN3;
    SPAN3_ω:      return empty;
}
    /*------------------------------------------------------------------------*/
/*============================================================================*/
typedef struct _word {
} word_t;
/*----------------------------------------------------------------------------*/
str_t word(word_t * ζ, int entry) {
    if (entry == α) goto word_α;
    if (entry == β) goto word_β;
    /*------------------------------------------------------------------------*/
    str_t         NOTANY7;
    NOTANY7_α:    if (Σ[Δ] == '(')                          goto NOTANY7_αω;
                  if (Σ[Δ] == ' ')                          goto NOTANY7_αω;
                  if (Σ[Δ] == ')')                          goto NOTANY7_αω;
                  NOTANY7 = str(Σ+Δ,1); Δ+=1;               goto NOTANY7_γ;
    NOTANY7_αω:                                             goto NOTANY7_ω;
    NOTANY7_β:    Δ-=1;                                     goto NOTANY7_ω;
    /*------------------------------------------------------------------------*/
    str_t         BREAK8;
    int           BREAK8_δ;
    BREAK8_α:     for (BREAK8_δ = 0; Σ[Δ+BREAK8_δ]; BREAK8_δ++) {
                      if (Σ[Δ+BREAK8_δ] == '(') break;      
                      if (Σ[Δ+BREAK8_δ] == ' ') break;      
                      if (Σ[Δ+BREAK8_δ] == ')') break;      
                  }                                         
                  if (Δ+BREAK8_δ >= Ω)                      goto BREAK8_ω;
                  BREAK8 = str(Σ+Δ,BREAK8_δ); Δ+=BREAK8_δ;  goto BREAK8_γ;
    BREAK8_β:     Δ-=BREAK8_δ;                              goto BREAK8_ω;
    /*------------------------------------------------------------------------*/
    str_t         seq6;
    seq6_α:       seq6 = str(Σ+Δ,0);                        goto NOTANY7_α;
    seq6_β:                                                 goto BREAK8_β;
    NOTANY7_γ:    seq6 = cat(seq6, NOTANY7);                goto BREAK8_α;
    NOTANY7_ω:                                              goto seq6_ω;
    BREAK8_γ:     seq6 = cat(seq6, BREAK8);                 goto seq6_γ;
    BREAK8_ω:                                               goto NOTANY7_β;
    /*------------------------------------------------------------------------*/
    str_t         OUTPUT5;
    OUTPUT5_α:                                              goto seq6_α;
    OUTPUT5_β:                                              goto seq6_β;
    seq6_γ:       OUTPUT5 = write_str(out, seq6);           
                  write_nl(out);                            goto OUTPUT5_γ;
    seq6_ω:                                                 goto OUTPUT5_ω;
    /*------------------------------------------------------------------------*/
    word_α:                                                 goto OUTPUT5_α;
    word_β:                                                 goto OUTPUT5_β;
    OUTPUT5_γ:    return OUTPUT5;
    OUTPUT5_ω:    return empty;
}
    /*------------------------------------------------------------------------*/
/*============================================================================*/
typedef struct _13 {
    int           alt14_i;
    str_t         ARBNO;
} _13_t;
/*----------------------------------------------------------------------------*/
typedef struct _group {
    int           _13_i;
    _13_t         _13_a[64];
} group_t;
/*----------------------------------------------------------------------------*/
str_t group(group_t * ζ, int entry) {
    if (entry == α) goto group_α;
    if (entry == β) goto group_β;
    /*------------------------------------------------------------------------*/
    str_t         s11;
    s11_α:        if (Σ[Δ+0] != '(')                        goto s11_ω;
                  s11 = str(Σ+Δ,1); Δ+=1;                   goto s11_γ;
    s11_β:        Δ-=1;                                     goto s11_ω;
    /*------------------------------------------------------------------------*/
    str_t         word12;
    word_t        word12_ζ;
    word12_α:     word12 = word(&word12_ζ, α);              goto word12_λ;
    word12_β:     word12 = word(&word12_ζ, β);              goto word12_λ;
    word12_λ:     if (is_empty(word12))                     goto word12_ω;
                  else                                      goto word12_γ;
    /*------------------------------------------------------------------------*/
    _13_t *       ψ13;
    str_t         delim16;
    delim_t       delim16_ζ;
    delim16_α:    delim16 = delim(&delim16_ζ, α);           goto delim16_λ;
    delim16_β:    delim16 = delim(&delim16_ζ, β);           goto delim16_λ;
    delim16_λ:    if (is_empty(delim16))                    goto delim16_ω;
                  else                                      goto delim16_γ;
    /*------------------------------------------------------------------------*/
    str_t         group17;
    group_t       group17_ζ;
    group17_α:    group17 = group(&group17_ζ, α);           goto group17_λ;
    group17_β:    group17 = group(&group17_ζ, β);           goto group17_λ;
    group17_λ:    if (is_empty(group17))                    goto group17_ω;
                  else                                      goto group17_γ;
    /*------------------------------------------------------------------------*/
    str_t         seq15;
    seq15_α:      seq15 = str(Σ+Δ,0);                       goto delim16_α;
    seq15_β:                                                goto group17_β;
    delim16_γ:    seq15 = cat(seq15, delim16);              goto group17_α;
    delim16_ω:                                              goto seq15_ω;
    group17_γ:    seq15 = cat(seq15, group17);              goto seq15_γ;
    group17_ω:                                              goto delim16_β;
    /*------------------------------------------------------------------------*/
    str_t         word18;
    word_t        word18_ζ;
    word18_α:     word18 = word(&word18_ζ, α);              goto word18_λ;
    word18_β:     word18 = word(&word18_ζ, β);              goto word18_λ;
    word18_λ:     if (is_empty(word18))                     goto word18_ω;
                  else                                      goto word18_γ;
    /*------------------------------------------------------------------------*/
    str_t         alt14;
    alt14_α:      ψ13->alt14_i = 1;                         goto seq15_α;
    alt14_β:      if (ψ13->alt14_i == 1)                    goto seq15_β;
                  if (ψ13->alt14_i == 2)                    goto word18_β;
                                                            goto alt14_ω;
    seq15_γ:      alt14 = seq15;                            goto alt14_γ;
    seq15_ω:      ψ13->alt14_i++;                           goto word18_α;
    word18_γ:     alt14 = word18;                           goto alt14_γ;
    word18_ω:                                               goto alt14_ω;
    /*------------------------------------------------------------------------*/
    str_t         ARBNO13;
    ARBNO13_α:    ψ13 = &ζ->_13_a[ζ->_13_i=0];
                  ψ13->ARBNO = str(Σ+Δ, 0);                 goto alt14_γ;
    ARBNO13_β:    ψ13 = &ζ->_13_a[++ζ->_13_i];
                  ψ13->ARBNO = ARBNO13;                     goto alt14_α;
    alt14_γ:      ARBNO13 = cat(ψ13->ARBNO, alt14);         goto ARBNO13_γ;
    alt14_ω:      if (--ζ->_13_i < 0)                       goto ARBNO13_ω;
                  ψ13 = &ζ->_13_a[ζ->_13_i];                goto alt14_β;
    /*------------------------------------------------------------------------*/
    str_t         s19;
    s19_α:        if (Σ[Δ+0] != ')')                        goto s19_ω;
                  s19 = str(Σ+Δ,1); Δ+=1;                   goto s19_γ;
    s19_β:        Δ-=1;                                     goto s19_ω;
    /*------------------------------------------------------------------------*/
    str_t         seq10;
    seq10_α:      seq10 = str(Σ+Δ,0);                       goto s11_α;
    seq10_β:                                                goto s19_β;
    s11_γ:        seq10 = cat(seq10, s11);                  goto word12_α;
    s11_ω:                                                  goto seq10_ω;
    word12_γ:     seq10 = cat(seq10, word12);               goto ARBNO13_α;
    word12_ω:                                               goto s11_β;
    ARBNO13_γ:    seq10 = cat(seq10, ARBNO13);              goto s19_α;
    ARBNO13_ω:                                              goto word12_β;
    s19_γ:        seq10 = cat(seq10, s19);                  goto seq10_γ;
    s19_ω:                                                  goto ARBNO13_β;
    /*------------------------------------------------------------------------*/
    group_α:                                                goto seq10_α;
    group_β:                                                goto seq10_β;
    seq10_γ:      return seq10;
    seq10_ω:      return empty;
}
    /*------------------------------------------------------------------------*/
/*============================================================================*/
typedef struct _23 {
    int           _25_i;
    str_t         _25_s;
    str_t         ARBNO;
} _23_t;
/*----------------------------------------------------------------------------*/
typedef struct _treebank {
    int           _23_i;
    _23_t         _23_a[64];
} treebank_t;
/*----------------------------------------------------------------------------*/
str_t treebank(treebank_t * ζ, int entry) {
    if (entry == α) goto treebank_α;
    if (entry == β) goto treebank_β;
    /*------------------------------------------------------------------------*/
    str_t         POS22;
    POS22_α:      if (Δ != 0)                               goto POS22_ω;
                  POS22 = str(Σ+Δ,0);                       goto POS22_γ;
    POS22_β:                                                goto POS22_ω;
    /*------------------------------------------------------------------------*/
    _23_t *       ψ23;
    str_t         group26;
    group_t       group26_ζ;
    group26_α:    group26 = group(&group26_ζ, α);           goto group26_λ;
    group26_β:    group26 = group(&group26_ζ, β);           goto group26_λ;
    group26_λ:    if (is_empty(group26))                    goto group26_ω;
                  else                                      goto group26_γ;
    /*------------------------------------------------------------------------*/
    str_t         ARBNO25;
    ARBNO25_α:    ψ23->_25_i = 0;
                  ψ23->_25_s = str(Σ+Δ, 0);                 goto group26_γ;
    ARBNO25_β:    ψ23->_25_i++;
                  ψ23->_25_s = ARBNO25;                     goto group26_α;
    group26_γ:    ARBNO25 = cat(ψ23->_25_s, group26);       goto ARBNO25_γ;
    group26_ω:    if (--ψ23->_25_i < 0)                     goto ARBNO25_ω;
                  else                                      goto group26_β;
    /*------------------------------------------------------------------------*/
    str_t         delim27;
    delim_t       delim27_ζ;
    delim27_α:    delim27 = delim(&delim27_ζ, α);           goto delim27_λ;
    delim27_β:    delim27 = delim(&delim27_ζ, β);           goto delim27_λ;
    delim27_λ:    if (is_empty(delim27))                    goto delim27_ω;
                  else                                      goto delim27_γ;
    /*------------------------------------------------------------------------*/
    str_t         seq24;
    seq24_α:      seq24 = str(Σ+Δ,0);                       goto ARBNO25_α;
    seq24_β:                                                goto delim27_β;
    ARBNO25_γ:    seq24 = cat(seq24, ARBNO25);              goto delim27_α;
    ARBNO25_ω:                                              goto seq24_ω;
    delim27_γ:    seq24 = cat(seq24, delim27);              goto seq24_γ;
    delim27_ω:                                              goto ARBNO25_β;
    /*------------------------------------------------------------------------*/
    str_t         ARBNO23;
    ARBNO23_α:    ψ23 = &ζ->_23_a[ζ->_23_i=0];
                  ψ23->ARBNO = str(Σ+Δ, 0);                 goto seq24_γ;
    ARBNO23_β:    ψ23 = &ζ->_23_a[++ζ->_23_i];
                  ψ23->ARBNO = ARBNO23;                     goto seq24_α;
    seq24_γ:      ARBNO23 = cat(ψ23->ARBNO, seq24);         goto ARBNO23_γ;
    seq24_ω:      if (--ζ->_23_i < 0)                       goto ARBNO23_ω;
                  ψ23 = &ζ->_23_a[ζ->_23_i];                goto seq24_β;
    /*------------------------------------------------------------------------*/
    str_t         RPOS28;
    RPOS28_α:     if (Δ != Ω-0)                             goto RPOS28_ω;
                  RPOS28 = str(Σ+Δ,0);                      goto RPOS28_γ;
    RPOS28_β:                                               goto RPOS28_ω;
    /*------------------------------------------------------------------------*/
    str_t         seq21;
    seq21_α:      seq21 = str(Σ+Δ,0);                       goto POS22_α;
    seq21_β:                                                goto RPOS28_β;
    POS22_γ:      seq21 = cat(seq21, POS22);                goto ARBNO23_α;
    POS22_ω:                                                goto seq21_ω;
    ARBNO23_γ:    seq21 = cat(seq21, ARBNO23);              goto RPOS28_α;
    ARBNO23_ω:                                              goto POS22_β;
    RPOS28_γ:     seq21 = cat(seq21, RPOS28);               goto seq21_γ;
    RPOS28_ω:                                               goto ARBNO23_β;
    /*------------------------------------------------------------------------*/
    treebank_α:                                             goto seq21_α;
    treebank_β:                                             goto seq21_β;
    seq21_γ:      return seq21;
    seq21_ω:      return empty;
}
    /*------------------------------------------------------------------------*/
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
    str_t         subj30;
    subj30_α:     Δ = 0; Σ = "(S (NP (FW i)) (VP (VBP am)) (.  .)) ";
                  Ω = len(Σ); subj30 = str(Σ,Ω);            goto subj30_γ;
    subj30_β:                                               goto subj30_ω;
    /*------------------------------------------------------------------------*/
    str_t         treebank31;
    treebank_t    treebank31_ζ;
    treebank31_α: treebank31 = treebank(&treebank31_ζ, α);  goto treebank31_λ;
    treebank31_β: treebank31 = treebank(&treebank31_ζ, β);  goto treebank31_λ;
    treebank31_λ: if (is_empty(treebank31))                 goto treebank31_ω;
                  else                                      goto treebank31_γ;
    /*------------------------------------------------------------------------*/
    str_t         match29;
    match29_α:                                              goto subj30_α;
    match29_β:                                              goto match29_ω;
    subj30_γ:                                               goto treebank31_α;
    subj30_ω:                                               goto match29_ω;
    treebank31_γ: match29 = treebank31;                     goto match29_γ;
    treebank31_ω:                                           goto match29_ω;
    /*------------------------------------------------------------------------*/
                                                            goto main1_α;
    main1_α:                                                goto match29_α;
    main1_β:                                                return;
    match29_γ:    write_sz(out, cszSuccess);                
                  write_str(out, match29);                  
                  write_nl(out);                            goto match29_β;
    match29_ω:    write_sz(out, cszFailure);                
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
