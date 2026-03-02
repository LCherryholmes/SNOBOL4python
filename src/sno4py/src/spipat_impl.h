/*
 *                          SPITBOL PATTERNS IN C
 *			  INTERNAL DATA STRUCTURES
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

// $Id: spipat_impl.h,v 1.15 2021-07-31 01:47:29 phil Exp $

typedef struct pe *PE_Ptr;

struct pat {
    size_t Stk;
    PE_Ptr P;
    int Refs;
};

#define PATTERN_CODES \
    PATTERN_CODE(Abort),	\
    PATTERN_CODE(Arb_Y),	\
    PATTERN_CODE(Assign),	\
    PATTERN_CODE(Bal),		\
    PATTERN_CODE(BreakX_X),	\
    PATTERN_CODE(EOP),		\
    PATTERN_CODE(Fail),		\
    PATTERN_CODE(Fence),	\
    PATTERN_CODE(Fence_X),	\
    PATTERN_CODE(Fence_Y),	\
    PATTERN_CODE(R_Enter),	\
    PATTERN_CODE(R_Remove),	\
    PATTERN_CODE(R_Restore),	\
    PATTERN_CODE(Rem),		\
    PATTERN_CODE(Succeed),	\
    PATTERN_CODE(Unanchored),	\
				\
    /* has alt... */		\
    PATTERN_CODE(Alt),		\
    PATTERN_CODE(Arb_X),	\
    PATTERN_CODE(Arbno_S),	\
    PATTERN_CODE(Arbno_X),	\
    /* ...has alt */		\
				\
    PATTERN_CODE(Rpat),		\
				\
    PATTERN_CODE(Pred_Func),	\
				\
    PATTERN_CODE(Assign_Imm),	\
    PATTERN_CODE(Assign_OnM),	\
    PATTERN_CODE(Any_VP),	\
    PATTERN_CODE(Break_VP),	\
    PATTERN_CODE(BreakX_VP),	\
    PATTERN_CODE(NotAny_VP),	\
    PATTERN_CODE(NSpan_VP),	\
    PATTERN_CODE(Span_VP),	\
    PATTERN_CODE(String_VP),	\
				\
    PATTERN_CODE(Call_Imm),	\
    PATTERN_CODE(Call_OnM),	\
				\
    PATTERN_CODE(Null),		\
				\
    PATTERN_CODE(String),	\
    PATTERN_CODE(String_2),	\
    PATTERN_CODE(String_3),	\
    PATTERN_CODE(String_4),	\
    PATTERN_CODE(String_5),	\
    PATTERN_CODE(String_6),	\
				\
    PATTERN_CODE(Setcur),	\
    PATTERN_CODE(Setcur_Func),	\
				\
    PATTERN_CODE(Any_CH),	\
    PATTERN_CODE(Break_CH),	\
    PATTERN_CODE(BreakX_CH),	\
    PATTERN_CODE(Char),		\
    PATTERN_CODE(NotAny_CH),	\
    PATTERN_CODE(NSpan_CH),	\
    PATTERN_CODE(Span_CH),	\
				\
    PATTERN_CODE(Any_CSP),	\
    PATTERN_CODE(Break_CSP),	\
    PATTERN_CODE(BreakX_CSP),	\
    PATTERN_CODE(NotAny_CSP),	\
    PATTERN_CODE(NSpan_CSP),	\
    PATTERN_CODE(Span_CSP),	\
				\
    PATTERN_CODE(Arbno_Y),	\
    PATTERN_CODE(Len_Nat),	\
    PATTERN_CODE(Pos_Nat),	\
    PATTERN_CODE(RPos_Nat),	\
    PATTERN_CODE(RTab_Nat),	\
    PATTERN_CODE(Tab_Nat),	\
				\
    PATTERN_CODE(Pos_NF),	\
    PATTERN_CODE(Len_NF),	\
    PATTERN_CODE(RPos_NF),	\
    PATTERN_CODE(RTab_NF),	\
    PATTERN_CODE(Tab_NF),	\
				\
    PATTERN_CODE(Pos_NP),	\
    PATTERN_CODE(Len_NP),	\
    PATTERN_CODE(RPos_NP),	\
    PATTERN_CODE(RTab_NP),	\
    PATTERN_CODE(Tab_NP),	\
				\
    PATTERN_CODE(Any_VF),	\
    PATTERN_CODE(Break_VF),	\
    PATTERN_CODE(BreakX_VF),	\
    PATTERN_CODE(NotAny_VF),	\
    PATTERN_CODE(NSpan_VF),	\
    PATTERN_CODE(Span_VF),	\
    PATTERN_CODE(String_VF),	\
				\
    PATTERN_CODE(Dynamic_Func)

#define PATTERN_CODE(X) PC_##X
enum Pattern_Code {
    PATTERN_CODES,
    PC_NUM_CODES
};
#undef PATTERN_CODE

// uint16_t limits patterns to 64K nodes.  May not save space, even on
// LP32 systems because of alignment (unless "Pcode" field declared a
// 16-bit bitfield, and even then, MSC might need additional cajoling)!
//
// uint32_t allows 4G pattern nodes, which seems likely
// to be plenty, for MOST machine generated patterns!!

typedef uint32_t IndexT;		/* node index */

struct pe {
    enum Pattern_Code Pcode;

    IndexT Index;
    //  Serial index number of pattern element within pattern

    PE_Ptr Pthen;
    //  Successor element), to be matched after this one

    union {
	/* PC_Arb_Y      |
	   PC_Assign     |
	   PC_Bal        |
	   PC_BreakX_X   |
	   PC_Cancel     |
	   PC_EOP        |
	   PC_Fail       |
	   PC_Fence      |
	   PC_Fence_X    |
	   PC_Fence_Y    |
	   PC_Null       |
	   PC_R_Enter    |
	   PC_R_Remove   |
	   PC_R_Restore  |
	   PC_Rest       |
	   PC_Succeed    |
	   PC_Unanchored => null;
	*/

	/*
	  PC_Alt        |
	  PC_Arb_X      |
	  PC_Arbno_S    |
	  PC_Arbno_X
	*/
	PE_Ptr Alt;

	/* PC_Rpat */
	struct pat **PP;

	/* PC_Pred_Func */
	struct {
	    bool (*func)(void *, void *);
	    void *cookie;
	} BF;

	/* PC_Assign_Imm_VP |
	   PC_Assign_OnM_VP |
	   PC_Any_VP     |
	   PC_Break_VP   |
	   PC_BreakX_VP  |
	   PC_NotAny_VP  |
	   PC_NSpan_VP   |
	   PC_Span_VP    |
	   PC_String_VP
	*/
	VString *VP;

	/*
	  PC_Call_Imm
	  PC_Call_OnM
	*/
	struct {
	    void (*func)(VString, void *, void *);
	    void *cookie;
	} MF;

	/* PC_String */
	VString Str;

	/* PC_String_2 */
	Character Str2[2];

	/* PC_String_3 */
	Character Str3[3];

	/* PC_String_4 */
	Character Str4[4];

	/* PC_String_5 */
	Character Str5[5];

	/* PC_String_6 */
	Character Str6[6];

	/* PC_Setcur */
	size_t *Var;

	/* PC_Setcur_Func */
	struct {
	    void (*func)(size_t, void *, void *);
	    void *cookie;
	} CF;

	/* PC_Any_CH     |
	   PC_Break_CH   |
	   PC_BreakX_CH  |
	   PC_Char       |
	   PC_NotAny_CH  |
	   PC_NSpan_CH   |
	   PC_Span_CH
	*/
	Character Char;

	/*
	  PC_Any_CSP    |
	  PC_Break_CSP  |
	  PC_BreakX_CSP |
	  PC_NotAny_CSP |
	  PC_NSpan_CSP  |
	  PC_Span_CSP
	*/
	struct character_set *CSP;

	/*
	  PC_Arbno_Y    |
	  PC_Len_Nat    |
	  PC_Pos_Nat    |
	  PC_RPos_Nat   |
	  PC_RTab_Nat   |
	  PC_Tab_Nat
	*/
	size_t Nat;

	/*
	  PC_Pos_NF     |
	  PC_Len_NF     |
	  PC_RPos_NF    |
	  PC_RTab_NF    |
	*/
	struct {
	    size_t (*func)(void *, void *);
	    void *cookie;
	} NF;

	/*
	  PC_Pos_NP     |
	  PC_Len_NP     |
	  PC_RPos_NP    |
	  PC_RTab_NP    |
	  PC_Tab_NP
	*/
	const size_t *NP;

	/*
	  PC_Any_VF     |
	  PC_Break_VF   |
	  PC_BreakX_VF  |
	  PC_NotAny_VF  |
	  PC_NSpan_VF   |
	  PC_Span_VF    |
	  PC_String_VF
	*/
	struct {
	    VString (*func)(void *, void *);
	    void *cookie;
	} VF;

	/* PC_Dynamic_Func */
	struct {
	    void (*func)(void *, void *, struct dynamic *);
	    void *cookie;
	} DF;
    } val;
};

extern const struct pe EOP_Element;
#define EOP (PE_Ptr)&EOP_Element

void spipat_build_ref_array(PE_Ptr E, PE_Ptr *RA);
void spipat_printf(const char *fmt, ...);
void spipat_putchar(Character c);
