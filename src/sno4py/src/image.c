/*
 *                          SPITBOL PATTERNS IN C
 *			   Pattern Image Function
 *
 *          Copyright (C) 2007-2021, Philip L. Budne			
 *          Copyright (C) 1998-2005, AdaCore
 *
 * This file is part of SPIPAT
 *
 * SPIPAT is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 * 
 * SPIPAT is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GCC; see the file COPYING.  If not, write to the Free
 * Software Foundation, 51 Franklin Street, Fifth Floor, Boston, MA
 * 02110-1301, USA.
 *
 * As a special exception, if you link this file with other files to
 * produce an executable, this file does not by itself cause the
 * resulting executable to be covered by the GNU General Public
 * License. This exception does not however invalidate any other
 * reasons why the executable file might be covered by the GNU Public
 * License.
 *
 * SPIPAT was developed from the GNAT.SPITBOL.PATTERNS package.
 * GNAT was originally developed  by the GNAT team at  New York University.
 * Extensive contributions were provided by Ada Core Technologies Inc.
 */

// $Id: image.c,v 1.15 2021-07-31 01:47:29 phil Exp $

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>

#include "spipat.h"
#include "spipat_impl.h"
#include "spipat_image.h"

//  E refers to a pattern structure. This procedure appends to Result
//  a representation of the single simple or compound pattern structure
//  at the start of E and updates E to point to its successor.

static void
AppendC(struct state *sp, Character c) {
    if (sp->len < sp->size && sp->ptr)
	*sp->ptr++ = c;
    sp->len++;
}

static void
Append(struct state *sp, const char *s2) {
    char c;
    while ((c = *s2++))
	AppendC(sp, c);
}

#define Append(SP, S) ((SP)->append)(SP, S)
#define AppendC(SP, C) ((SP)->appendc)(SP, C)

static void
AppendCS(struct state *sp, PE_Ptr e) {
    Append(sp, "<CS>");			/* XXX FIXME */
    (void) e;
}

static void
AppendMF(struct state *sp, PE_Ptr e) {
    char buf[64];
    snprintf(buf, sizeof(buf), "%p(%p)", e->val.MF.func, e->val.MF.cookie);
    Append(sp, buf);
}

static void
AppendN(struct state *sp, PE_Ptr e) {
    char buf[32];
    snprintf(buf, sizeof(buf), "%zu", e->val.Nat);
    Append(sp, buf);
}

static void
AppendNF(struct state *sp, PE_Ptr e) {
    char buf[64];
    snprintf(buf, sizeof(buf), "%p(%p)", e->val.NF.func, e->val.NF.cookie);
    Append(sp, buf);
}

static void
AppendNP(struct state *sp, PE_Ptr e) {
    char buf[32];
    snprintf(buf, sizeof(buf), "%p", e->val.NP);
    Append(sp, buf);
}

static void
AppendPP(struct state *sp, PE_Ptr e) {
    char buf[32];
    snprintf(buf, sizeof(buf), "%p", e->val.PP);
    Append(sp, buf);
}

static void
AppendVF(struct state *sp, PE_Ptr e) {
    char buf[64];
    snprintf(buf, sizeof(buf), "%p(%p)", e->val.VF.func, e->val.VF.cookie);
    Append(sp, buf);
}

static void
AppendVP(struct state *sp, PE_Ptr e) {
    char buf[32];
    snprintf(buf, sizeof(buf), "%p", e->val.VP);
    Append(sp, buf);
}

static void
AppendStrChr(struct state *sp, int c) {
    if (c == '"')
	AppendC(sp, '\\');
    AppendC(sp, c);
}

static void
AppendVStr(struct state *sp, PE_Ptr e) {
    const Character *cp = e->val.Str.ptr;
    int len = e->val.Str.len;
    while (len-- > 0)
	AppendStrChr(sp, *cp++);
}

static void
AppendBF(struct state *sp, PE_Ptr e) {
    char buf[64];
    snprintf(buf, sizeof(buf), "%p(%p)", e->val.BF.func, e->val.BF.cookie);
    Append(sp, buf);
}

static void
AppendDF(struct state *sp, PE_Ptr e) {
    char buf[64];
    snprintf(buf, sizeof(buf), "%p(%p)", e->val.DF.func, e->val.DF.cookie);
    Append(sp, buf);
}

static void
AppendCF(struct state *sp, PE_Ptr e) {
    char buf[64];
    snprintf(buf, sizeof(buf), "%p(%p)", e->val.CF.func, e->val.CF.cookie);
    Append(sp, buf);
}

static void
AppendFNoargs(struct state *sp, PE_Ptr e) {
    Append(sp, sp->strings[e->Pcode]);
    AppendC(sp, '(');
    AppendC(sp, ')');
}

static void
AppendFCS(struct state *sp, PE_Ptr e) {
    Append(sp, sp->strings[e->Pcode]);
    AppendC(sp, '(');
    (sp->cs)(sp, e);
    AppendC(sp, ')');
}

static void
AppendFVF(struct state *sp, PE_Ptr e) {
    Append(sp, sp->strings[e->Pcode]);
    AppendC(sp, '(');
    (sp->vf)(sp, e);
    AppendC(sp, ')');
}

static void
AppendFVP(struct state *sp, PE_Ptr e) {
    Append(sp, sp->strings[e->Pcode]);
    AppendC(sp, '(');
    (sp->vp)(sp, e);
    AppendC(sp, ')');
}


static void
AppendAssign(struct state *sp, PE_Ptr e) {
    int l = strlen(sp->concat);
    if (l > 0 && sp->len > l && sp->len < sp->size && sp->ptr) {
	sp->ptr -= l;		/* delete concat */
	sp->len -= l;
    }
    AppendC(sp, ' ');
    Append(sp, sp->strings[e->Pcode]);
    (sp->vp)(sp, sp->Refs[e->Index]);
}

static void
AppendFCH(struct state *sp, PE_Ptr e) {
    Append(sp, sp->strings[e->Pcode]);
    AppendC(sp, '(');
    (sp->ch)(sp, e);
    AppendC(sp, ')');
}

static void
AppendCH(struct state *sp, PE_Ptr e) {
    Append(sp, sp->cquote);
    AppendC(sp, e->val.Char);
    Append(sp, sp->cquote);
}

static void
AppendFNat(struct state *sp, PE_Ptr e) {
    Append(sp, sp->strings[e->Pcode]);
    AppendC(sp, '(');
    (sp->nat)(sp, e);
    AppendC(sp, ')');
}


static void
AppendFNF(struct state *sp, PE_Ptr e) {
    Append(sp, sp->strings[e->Pcode]);
    AppendC(sp, '(');
    (sp->nf)(sp, e);
    AppendC(sp, ')');
}

static void
AppendFNP(struct state *sp, PE_Ptr e) {
    Append(sp, sp->strings[e->Pcode]);
    AppendC(sp, '(');
    (sp->np)(sp, e);
    AppendC(sp, ')');
}

static void
AppendFPP(struct state *sp, PE_Ptr e) {
    Append(sp, sp->strings[e->Pcode]);
    AppendC(sp, '(');
    (sp->pp)(sp, e);
    AppendC(sp, ')');
}

static void
AppendFBF(struct state *sp, PE_Ptr e) {
    Append(sp, sp->strings[e->Pcode]);
    AppendC(sp, '(');
    (sp->bf)(sp, e);
    AppendC(sp, ')');
}

static void
AppendFDF(struct state *sp, PE_Ptr e) {
    Append(sp, sp->strings[e->Pcode]);
    AppendC(sp, '(');
    (sp->df)(sp, e);
    AppendC(sp, ')');
}

static void
AppendFCF(struct state *sp, PE_Ptr e) {
    Append(sp, sp->strings[e->Pcode]);
    AppendC(sp, '(');
    (sp->cf)(sp, e);
    AppendC(sp, ')');
}

static PE_Ptr
Image_One(struct state *sp, PE_Ptr E) {
    //  Successor set as result in E unless reset
    PE_Ptr ER = E->Pthen;

    switch (E->Pcode) {
    case PC_Alt:
    {
	//  Number of elements in left pattern of alternation
	IndexT Elmts_In_L = E->Pthen->Index - E->val.Alt->Index;

	//  Number of lowest index in elements of left pattern
	IndexT Lowest_In_L = E->Index - Elmts_In_L;

	//  The successor of the alternation node must have a lower
	//  index than any node that is in the left pattern or a
	//  higher index than the alternation node itself.
	while (ER != EOP && ER->Index >= Lowest_In_L && ER->Index < E->Index)
	    ER = ER->Pthen;

	AppendC(sp, '(');
	PE_Ptr E1 = E;
	do {
	    spipat_image_seq(sp, E1->Pthen, ER, false);
	    Append(sp, sp->strings[PC_Alt]);
	    E1 = E1->val.Alt;
	} while (E1->Pcode == PC_Alt);

	spipat_image_seq(sp, E1, ER, false);
	AppendC(sp, ')');
	break;
    }

    case PC_Abort:
    case PC_Arb_X:
    case PC_Bal:
    case PC_Fail:
    case PC_Fence:
    case PC_Rem:
    case PC_Succeed:
	(sp->fnoargs)(sp, E);
	break;

    case PC_Any_CSP:
    case PC_Break_CSP:
    case PC_BreakX_CSP:
    case PC_NotAny_CSP:
    case PC_NSpan_CSP:
    case PC_Span_CSP:
	(sp->fcs)(sp, E);
	break;

    case PC_Any_VF:
    case PC_Break_VF:
    case PC_BreakX_VF:
    case PC_NotAny_VF:
    case PC_NSpan_VF:
    case PC_Span_VF:
    case PC_String_VF:
	(sp->fvf)(sp, E);
	break;

    case PC_Any_VP:
    case PC_Break_VP:
    case PC_BreakX_VP:
    case PC_NotAny_VP:
    case PC_NSpan_VP:
    case PC_Span_VP:
    case PC_String_VP:
	(sp->fvp)(sp, E);
	break;

    case PC_Arbno_S:
	Append(sp, sp->strings[E->Pcode]);
	AppendC(sp, '(');
	spipat_image_seq(sp, E->val.Alt, E, false);
	AppendC(sp, ')');
	break;

    case PC_Arbno_X:
	Append(sp, sp->strings[E->Pcode]);
	AppendC(sp, '(');
	spipat_image_seq(sp, E->val.Alt->Pthen, sp->Refs[E->Index - 3], false);
	AppendC(sp, ')');
	break;

    case PC_Assign_Imm:
    case PC_Assign_OnM:
	(sp->assign)(sp, E);
	break;

    case PC_Any_CH:
    case PC_Break_CH:
    case PC_BreakX_CH:
    case PC_NotAny_CH:
    case PC_NSpan_CH:
    case PC_Span_CH:
	(sp->fch)(sp, E);
	break;

    case PC_Char:
	(sp->ch)(sp, E);
	break;

    case PC_Fence_X:
	// Fixes thanks to Robin Haberkorn
	Append(sp, sp->strings[E->Pcode]);
	AppendC(sp, '(');
	spipat_image_seq (sp, sp->Refs[E->Index]->Pthen, E, false); // PC_R_Enter at Refs[E->Index]
	AppendC(sp, ')');
	break;

    case PC_Len_Nat:
    case PC_Pos_Nat:
    case PC_RPos_Nat:
    case PC_RTab_Nat:
    case PC_Tab_Nat:
	(sp->fnat)(sp, E);
	break;

    case PC_Len_NF:
    case PC_Pos_NF:
    case PC_RPos_NF:
    case PC_RTab_NF:
    case PC_Tab_NF:
	(sp->fnf)(sp, E);
	break;

    case PC_Len_NP:
    case PC_Pos_NP:
    case PC_RPos_NP:
    case PC_RTab_NP:
    case PC_Setcur:
    case PC_Tab_NP:
	(sp->fnp)(sp, E);
	break;

    case PC_Null:
	// Fixes thanks to Robin Haberkorn
	Append(sp, sp->quote);
	Append(sp, sp->quote);
	break;

    case PC_R_Enter:
	sp->Kill_Concat = true;
	// Fixed thanks to Robin Haberkorn
	ER = sp->Refs[E->Index - 2]; // allows correct processing of PC_Fence_X & PC_Call_*
	break;

    case PC_Rpat:
	(sp->fpp)(sp, E);
	break;

    case PC_Pred_Func:
	(sp->fbf)(sp, E);
	break;

    case PC_Dynamic_Func:
	(sp->fdf)(sp, E);
	break;
	
    case PC_Setcur_Func:
	(sp->fcf)(sp, E);
	break;

    case PC_String:
	Append(sp, sp->quote);
	(sp->vstr)(sp, E);
	Append(sp, sp->quote);
	break;

    case PC_String_2:
	Append(sp, sp->quote);
	AppendStrChr(sp, E->val.Str2[0]);
	AppendStrChr(sp, E->val.Str2[1]);
	Append(sp, sp->quote);
	break;

    case PC_String_3:
	Append(sp, sp->quote);
	AppendStrChr(sp, E->val.Str3[0]);
	AppendStrChr(sp, E->val.Str3[1]);
	AppendStrChr(sp, E->val.Str3[2]);
	Append(sp, sp->quote);
	break;

    case PC_String_4:
	Append(sp, sp->quote);
	AppendStrChr(sp, E->val.Str4[0]);
	AppendStrChr(sp, E->val.Str4[1]);
	AppendStrChr(sp, E->val.Str4[2]);
	AppendStrChr(sp, E->val.Str4[3]);
	Append(sp, sp->quote);
	break;

    case PC_String_5:
	Append(sp, sp->quote);
	AppendStrChr(sp, E->val.Str5[0]);
	AppendStrChr(sp, E->val.Str5[1]);
	AppendStrChr(sp, E->val.Str5[2]);
	AppendStrChr(sp, E->val.Str5[3]);
	AppendStrChr(sp, E->val.Str5[4]);
	Append(sp, sp->quote);
	break;

    case PC_String_6:
	Append(sp, sp->quote);
	AppendStrChr(sp, E->val.Str6[0]);
	AppendStrChr(sp, E->val.Str6[1]);
	AppendStrChr(sp, E->val.Str6[2]);
	AppendStrChr(sp, E->val.Str6[3]);
	AppendStrChr(sp, E->val.Str6[4]);
	AppendStrChr(sp, E->val.Str6[5]);
	Append(sp, sp->quote);
	break;

    case PC_Call_Imm:
    case PC_Call_OnM:
	// Fixed thanks to Robin Haberkorn
	AppendC(sp, '(');
	spipat_image_seq(sp, E, sp->Refs[E->Index]->Pthen, true);
	Append(sp, sp->strings[E->Pcode]);
	AppendMF(sp, E);
	AppendC(sp, ')');
	break;

    case PC_Arb_Y:
    case PC_Arbno_Y:
    case PC_Assign:
    case PC_BreakX_X:
    case PC_EOP:
    case PC_Fence_Y:
    case PC_R_Remove:
    case PC_R_Restore:
    case PC_Unanchored:
    case PC_NUM_CODES:
	//  Other pattern codes should not appear as leading elements
	Append(sp, "???");
	break;
    }

    return ER;
} // Image_One

///////////////
// spipat_image_seq //
///////////////

//  E refers to a pattern structure whose successor is given by Succ.
//  This procedure appends a representation of this pattern.
//  The Paren parameter indicates whether parentheses are required if
//  the output is more than one element.

void
spipat_image_seq(struct state *sp, PE_Ptr E, PE_Ptr Succ, bool Paren) {
    //  The image of EOP is "" (the null string)
    if (E == EOP) {
	Append(sp, "\"\"");
    }
    else {
	PE_Ptr E1 = E;
	bool Mult = false;

	// else generate appropriate concatenation sequence
	if (E1 != Succ && E1 != EOP) {
	    Mult = true;
	    if (Paren)
		AppendC(sp, '(');
	}
	for (;;) {
	    E1 = Image_One(sp, E1);
	    if (E1 == Succ || E1 == EOP)
		break;
	    if (sp->Kill_Concat)
		sp->Kill_Concat = false;
	    else {
		Append(sp, sp->concat);
	    }
	}
	if (Mult && Paren)
	    AppendC(sp, ')');
    }
} // spipat_image_seq

void
spipat_image_init_state(struct state *sp) {
#undef Append
#undef AppendC

    sp->quote = "\"";
    sp->cquote = "'";
    sp->concat = " + ";
    sp->strings = image_strs;

    sp->append = Append;
    sp->appendc = AppendC;

    sp->vstr = AppendVStr;
    sp->fnoargs = AppendFNoargs;
    sp->cs = AppendCS;
    sp->fcs = AppendFCS;
    sp->vf = AppendVF;
    sp->fvf = AppendFVF;
    sp->vp = AppendVP;
    sp->fvp = AppendFVP;
    sp->assign = AppendAssign;
    sp->fch = AppendFCH;
    sp->ch = AppendCH;
    sp->nat = AppendN;
    sp->fnat = AppendFNat;
    sp->np = AppendNP;
    sp->fnp = AppendFNP;
    sp->nf = AppendNF;
    sp->fnf = AppendFNF;
    sp->pp = AppendPP;
    sp->fpp = AppendFPP;
    sp->bf = AppendBF;
    sp->fbf = AppendFBF;
    sp->cf = AppendCF;
    sp->fcf = AppendFCF;
    sp->df = AppendDF;
    sp->fdf = AppendFDF;
}

size_t
spipat_image_custom(struct state *sp, struct pat *P) {
    //  We build a reference array whose N'th element points to the
    //  pattern element whose Index value is N.
#ifdef _MSC_VER
    //  MSVC does not support C99 variable-length arrays — use malloc/free.
    PE_Ptr *Refs = (PE_Ptr *)malloc(P->P->Index * sizeof(PE_Ptr));
    if (!Refs) return 0;
#else
    PE_Ptr Refs[P->P->Index];
#endif
    spipat_build_ref_array(P->P, Refs);

    sp->size--;			/* reserve space for NUL */
    sp->len = 0;
    sp->Kill_Concat = false; //  Set true to delete next & to be output
    sp->Refs = Refs;
    spipat_image_seq(sp, P->P, EOP, false);

    /* make into a c-string */
    if (sp->ptr)
	*sp->ptr = '\0';

#ifdef _MSC_VER
    free(Refs);
#endif
    return sp->len;
}

size_t
spipat_image(struct pat *P, char *buf, size_t size) {
    struct state state;

    spipat_image_init_state(&state);
    state.ptr = buf;
    state.size = size;
    return spipat_image_custom(&state, P);
}
