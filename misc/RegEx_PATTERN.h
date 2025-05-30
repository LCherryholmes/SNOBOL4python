static PATTERN RE_Quantifier_2 = {σ, .s="*"};
static PATTERN RE_Quantifier_3 = {Shift, .t="*", .v="None"};
static PATTERN RE_Quantifier_1 = {Σ, 2, {&RE_Quantifier_2, &RE_Quantifier_3}};
static PATTERN RE_Quantifier_5 = {σ, .s="+"};
static PATTERN RE_Quantifier_6 = {Shift, .t="+", .v="None"};
static PATTERN RE_Quantifier_4 = {Σ, 2, {&RE_Quantifier_5, &RE_Quantifier_6}};
static PATTERN RE_Quantifier_8 = {σ, .s="?"};
static PATTERN RE_Quantifier_9 = {Shift, .t="?", .v="None"};
static PATTERN RE_Quantifier_7 = {Σ, 2, {&RE_Quantifier_8, &RE_Quantifier_9}};
static PATTERN RE_Quantifier_0 = {Π, 3, {&RE_Quantifier_1, &RE_Quantifier_4, &RE_Quantifier_7}};

static PATTERN RE_Item_2  = {σ, .s="."};
static PATTERN RE_Item_3  = {Shift, .t=".", .v="None"};
static PATTERN RE_Item_1  = {Σ, 2, {&RE_Item_2, &RE_Item_3}};
static PATTERN RE_Item_5  = {σ, .s="\\"};
static PATTERN RE_Item_7  = {ANY, .chars=".\\(|*+?)"};
static PATTERN RE_Item_6  = {Δ, .s="tx", &RE_Item_7};
static PATTERN RE_Item_8  = {Shift, .t="\u03c3", .v="tx"};
static PATTERN RE_Item_4  = {Σ, 3, {&RE_Item_5, &RE_Item_6, &RE_Item_8}};
static PATTERN RE_Item_11 = {ANY, .chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"};
static PATTERN RE_Item_10 = {Δ, .s="tx", &RE_Item_11};
static PATTERN RE_Item_12 = {Shift, .t="\u03c3", .v="tx"};
static PATTERN RE_Item_9  = {Σ, 2, {&RE_Item_10, &RE_Item_12}};
static PATTERN RE_Item_14 = {σ, .s="("};
static PATTERN RE_Item_15 = {ζ, .N="RE_Expression"};
static PATTERN RE_Item_16 = {σ, .s=")"};
static PATTERN RE_Item_13 = {Σ, 3, {&RE_Item_14, &RE_Item_15, &RE_Item_16}};
static PATTERN RE_Item_0  = {Π, 4, {&RE_Item_1, &RE_Item_4, &RE_Item_9, &RE_Item_13}};

static PATTERN RE_Factor_1 = {ζ, .N="RE_Item"};
static PATTERN RE_Factor_4 = {ζ, .N="RE_Quantifier"};
static PATTERN RE_Factor_5 = {Reduce, .n=2, .t="\u03c2"};
static PATTERN RE_Factor_3 = {Σ, 2, {&RE_Factor_4, &RE_Factor_5}};
static PATTERN RE_Factor_6 = {ε};
static PATTERN RE_Factor_2 = {Π, 2, {&RE_Factor_3, &RE_Factor_6}};
static PATTERN RE_Factor_0 = {Σ, 2, {&RE_Factor_1, &RE_Factor_2}};

static PATTERN RE_Term_1 = {nPush};
static PATTERN RE_Term_4 = {ζ, .N="RE_Factor"};
static PATTERN RE_Term_5 = {nInc};
static PATTERN RE_Term_3 = {Σ, 2, {&RE_Term_4, &RE_Term_5}};
static PATTERN RE_Term_2 = {ARBNO, 1, &RE_Term_3};
static PATTERN RE_Term_6 = {Reduce, .n=-1, .t="\u03a3"};
static PATTERN RE_Term_7 = {nPop};
static PATTERN RE_Term_0 = {Σ, 4, {&RE_Term_1, &RE_Term_2, &RE_Term_6, &RE_Term_7}};

static PATTERN RE_Expression_1  = {nPush};
static PATTERN RE_Expression_2  = {ζ, .N="RE_Term"};
static PATTERN RE_Expression_3  = {nInc};
static PATTERN RE_Expression_6  = {σ, .s="|"};
static PATTERN RE_Expression_7  = {ζ, .N="RE_Term"};
static PATTERN RE_Expression_8  = {nInc};
static PATTERN RE_Expression_5  = {Σ, 3, {&RE_Expression_6, &RE_Expression_7, &RE_Expression_8}};
static PATTERN RE_Expression_4  = {ARBNO, 1, &RE_Expression_5};
static PATTERN RE_Expression_9  = {Reduce, .n=-1, .t="\u03a0"};
static PATTERN RE_Expression_10 = {nPop};
static PATTERN RE_Expression_0  = {Σ, 6, {&RE_Expression_1, &RE_Expression_2, &RE_Expression_3, &RE_Expression_4, &RE_Expression_9, &RE_Expression_10}};

static PATTERN RE_RegEx_1 = {POS, .n=0};
static PATTERN RE_RegEx_2 = {ζ, .N="RE_Expression"};
static PATTERN RE_RegEx_3 = {Pop, .v="RE_tree"};
static PATTERN RE_RegEx_4 = {RPOS, .n=0};
static PATTERN RE_RegEx_0 = {Σ, 4, {&RE_RegEx_1, &RE_RegEx_2, &RE_RegEx_3, &RE_RegEx_4}};
