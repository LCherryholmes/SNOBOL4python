extern int printf(char *, ...);
void main() {
    goto main1;    
    //============================================================================
    // ICON Programming Language: (1st pass, attribute grammar generated)
    //
    //                  every write(5 > ((1 to 2) * (3 to 4)));
    //----------------- --------------------------- ------------------------------
int x5_V;
    x5_start:           x5_V = 5;                   goto x5_succeed;
    x5_resume:                                      goto x5_fail;
    //----------------- --------------------------- -----------------------------
int x1_V;
    x1_start:           x1_V = 1;                   goto x1_succeed;
    x1_resume:                                      goto x1_fail;
    //----------------- --------------------------- ------------------------------
int x2_V;
    x2_start:           x2_V = 2;                   goto x2_succeed;
    x2_resume:                                      goto x2_fail;
    //----------------- --------------------------- ------------------------------
int to1_I;
int to1_V;
    to1_start:                                      goto x1_start;
    x1_fail:                                        goto to1_fail;
    x2_fail:                                        goto x1_resume;
    to1_code:           if (to1_I > x2_V)           goto x2_resume;
                        else to1_V = to1_I;         goto to1_succeed;
    to1_resume:         to1_I = to1_I + 1;          goto to1_code;
    x1_succeed:                                     goto x2_start;
    x2_succeed:         to1_I = x1_V;               goto to1_code;
    //----------------- --------------------------- ------------------------------
int x3_V;
    x3_start:           x3_V = 3;                   goto x3_succeed;
    x3_resume:                                      goto x3_fail;
    //----------------- --------------------------- ------------------------------
int x4_V;
    x4_start:           x4_V = 4;                   goto x4_succeed;
    x4_resume:                                      goto x4_fail;
    //----------------- --------------------------- ------------------------------
int to2_I;
int to2_V;
    to2_start:                                      goto x3_start;
    x3_fail:                                        goto to2_fail;
    x4_fail:                                        goto x3_resume;
    to2_code:           if (to2_I > x4_V)           goto x4_resume;
                        else to2_V = to2_I;         goto to2_succeed;
    to2_resume:         to2_I = to2_I + 1;          goto to2_code;
    x3_succeed:                                     goto x4_start;
    x4_succeed:         to2_I = x3_V;               goto to2_code;
    //----------------- --------------------------- ------------------------------
int mult_V;
    mult_start:                                     goto to1_start;
    to1_fail:                                       goto mult_fail;
    to2_fail:                                       goto to1_resume;
    mult_resume:                                    goto to2_resume;
    to1_succeed:                                    goto to2_start;
    to2_succeed:        mult_V = to1_V * to2_V;     goto mult_succeed;
    //----------------- --------------------------- ------------------------------
int greater_V;
    greater_start:                                  goto x5_start;
    x5_fail:                                        goto greater_fail;
    mult_fail:                                      goto x5_resume;
    greater_resume:                                 goto mult_resume;
    x5_succeed:                                     goto mult_start;
    mult_succeed:       if (x5_V <= mult_V)         goto mult_resume;
                        else greater_V = mult_V;    goto greater_succeed;
    //----------------- --------------------------- ------------------------------
int write1_V;
    write1_start:                                   goto greater_start;
    write1_resume:                                  goto greater_resume;
    greater_fail:                                   goto write1_fail;
    greater_succeed:    write1_V = greater_V;
                        printf("%d\n", write1_V);   goto write1_succeed;
    //============================================================================
    // ICON Programming Language: 2nd pass, optimization
    //
    //                  every write(5 > ((1 to 2) * (3 to 4)));
    //----------------- --------------------------- ------------------------------
int to3_I;
    write2_start:       to3_I = 1;                  goto to3_code;
    to3_resume:         to3_I = to3_I + 1;
    to3_code:           if (to3_I > 2)              goto write2_fail;
int to4_I;
                        to4_I = 3;                  goto to4_code;
    write2_resume:      to4_I = to4_I + 1;
    to4_code:           if (to4_I > 4)              goto to3_resume;
                        mult_V = to3_I * to4_I;
                        if (5 <= mult_V)            goto write2_resume;
                        greater_V = mult_V;
                        printf("%d\n", greater_V);  goto write2_succeed;
    //============================================================================
    main1:              printf("\n");               goto write1_start;
    write1_fail:        printf("Failure.\n");       goto main2;
    write1_succeed:     printf("Success!\n");       goto write1_resume;
    main2:              printf("\n");               goto write2_start;
    write2_fail:        printf("Failure.\n");       return;
    write2_succeed:     printf("Success!\n");       goto write2_resume;
    //----------------- --------------------------- ------------------------------
}
