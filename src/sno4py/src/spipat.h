/*
 *                          SPITBOL PATTERNS IN C
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

// $Id: spipat.h,v 1.19 2021-07-31 01:47:29 phil Exp $

#ifndef __dead
#ifdef __GNUC__
#define __dead __attribute__((__noreturn__))
#else
#define __dead
#endif
#endif

#ifndef CHARSIZE
#define CHARSIZE 8
#endif

#if CHARSIZE == 8
// Python2 uses "char"; Character_Set code wants unsigned
typedef unsigned char Character;
#elif CHARSIZE == 32
typedef int32_t Character;

// UGH: make sure match between compilation and library!!
#define spipat_abort spipat32_abort
#define spipat_and spipat32_and
#define spipat_and_chr_pat spipat32_and_chr_pat
#define spipat_and_pat_chr spipat32_and_pat_chr
#define spipat_and_pat_str spipat32_and_pat_str
#define spipat_and_str_pat spipat32_and_str_pat
#define spipat_any_chr spipat32_any_chr
#define spipat_any_fnc spipat32_any_fnc
#define spipat_any_ptr spipat32_any_ptr
#define spipat_any_csp spipat32_any_csp
#define spipat_any_str spipat32_any_str
#define spipat_arb spipat32_arb
#define spipat_arbno spipat32_arbno
#define spipat_arbno_chr spipat32_arbno_chr
#define spipat_arbno_str spipat32_arbno_str
#define spipat_assign_immed spipat32_assign_immed
#define spipat_assign_onmatch spipat32_assign_onmatch
#define spipat_bal spipat32_bal
#define spipat_break_chr spipat32_break_chr
#define spipat_break_fnc spipat32_break_fnc
#define spipat_break_ptr spipat32_break_ptr
#define spipat_break_csp spipat32_break_csp
#define spipat_break_str spipat32_break_str
#define spipat_breakx_chr spipat32_breakx_chr
#define spipat_breakx_fnc spipat32_breakx_fnc
#define spipat_breakx_ptr spipat32_breakx_ptr
#define spipat_breakx_csp spipat32_breakx_csp
#define spipat_breakx_str spipat32_breakx_str
#define spipat_build_ref_array spipat32_build_ref_array
#define spipat_copy_cookie spipat32_copy_cookie
#define spipat_call_immed spipat32_call_immed
#define spipat_call_onmatch spipat32_call_onmatch
#define spipat_char spipat32_char
#define spipat_dump spipat32_dump
#define spipat_dynamic_fnc spipat32_dynamic_fnc
#define spipat_exception spipat32_exception
#define spipat_fail spipat32_fail
#define spipat_fence_function spipat32_fence_function
#define spipat_fence_simple spipat32_fence_simple
#define spipat_free spipat32_free
#define spipat_free_cookie spipat32_free_cookie
#define spipat_hold spipat32_hold
#define spipat_image spipat32_image
#define spipat_image_custom spipat32_image_custom
#define spipat_image_init_state spipat32_image_init_state
#define spipat_image_seq spipat32_image_seq
#define spipat_len spipat32_len
#define spipat_len_fnc spipat32_len_fnc
#define spipat_len_ptr spipat32_len_ptr
#define spipat_malloc spipat32_malloc
#define spipat_match2 spipat32_match2
#define spipat_notany_chr spipat32_notany_chr
#define spipat_notany_fnc spipat32_notany_fnc
#define spipat_notany_ptr spipat32_notany_ptr
#define spipat_notany_csp spipat32_notany_csp
#define spipat_notany_str spipat32_notany_str
#define spipat_nspan_chr spipat32_nspan_chr
#define spipat_nspan_fnc spipat32_nspan_fnc
#define spipat_nspan_ptr spipat32_nspan_ptr
#define spipat_nspan_csp spipat32_nspan_csp
#define spipat_nspan_str spipat32_nspan_str
#define spipat_or_chr_chr spipat32_or_chr_chr
#define spipat_or_chr_pat spipat32_or_chr_pat
#define spipat_or_chr_str spipat32_or_chr_str
#define spipat_or_pat_chr spipat32_or_pat_chr
#define spipat_or_pat_pat spipat32_or_pat_pat
#define spipat_or_pat_str spipat32_or_pat_str
#define spipat_or_str_chr spipat32_or_str_chr
#define spipat_or_str_pat spipat32_or_str_pat
#define spipat_or_str_str spipat32_or_str_str
#define spipat_parse spipat32_parse
#define spipat_pattern_ptr spipat32_pattern_ptr
#define spipat_pos spipat32_pos
#define spipat_pos_fnc spipat32_pos_fnc
#define spipat_pos_ptr spipat32_pos_ptr
#define spipat_predicate spipat32_predicate
#define spipat_printf spipat32_printf
#define spipat_putchar spipat32_putchar
#define spipat_rem spipat32_rem
#define spipat_rpos spipat32_rpos
#define spipat_rpos_fnc spipat32_rpos_fnc
#define spipat_rpos_ptr spipat32_rpos_ptr
#define spipat_rtab spipat32_rtab
#define spipat_rtab_fnc spipat32_rtab_fnc
#define spipat_rtab_ptr spipat32_rtab_ptr
#define spipat_setcur spipat32_setcur
#define spipat_setcur_fnc spipat32_setcur_fnc
#define spipat_span_chr spipat32_span_chr
#define spipat_span_fnc spipat32_span_fnc
#define spipat_span_ptr spipat32_span_ptr
#define spipat_span_csp spipat32_span_csp
#define spipat_span_str spipat32_span_str
#define spipat_string spipat32_string
#define spipat_string_fnc spipat32_string_fnc
#define spipat_string_ptr spipat32_string_ptr
#define spipat_succeed spipat32_succeed
#define spipat_tab spipat32_tab
#define spipat_tab_fnc spipat32_tab_fnc
#define spipat_tab_ptr spipat32_tab_ptr
#define spipat_version spipat32_version
#else
#error CHARSIZE not 8 or 32
#endif

#ifdef CHARSET_PUBLIC
typedef struct character_set *CSP;
#endif

typedef struct {
    const Character *ptr;
    size_t len;
    void (*release)(void *);
    void *cookie;
} VString;

// Pointer, Len, Release, Cookie to VString using C99 compound literal
#define PLRC2VSTRING(P,L,R,C) (VString) { (Character *)(P), (L), R, C }

// Pointer, Len to VString
#define PL2VSTRING(P,L)  PLRC2VSTRING(P,L,0,0)

// C-string to VString
#define C2VSTRING(S) PL2VSTRING((S), strlen(S))

////////////////////////////////////////////////////////////////

// "And"

struct pat *spipat_and_str_pat(VString L, struct pat *R);
struct pat *spipat_and_pat_str(struct pat *L, VString R);
struct pat *spipat_and_chr_pat(Character L, struct pat *R);
struct pat *spipat_and_pat_chr(struct pat *L, Character R);
struct pat *spipat_and(struct pat *L, struct pat *R);
#define spipat_and_pat_pat spipat_and

//  Assign immediate
struct pat *spipat_assign_immed(struct pat *P, VString *Var);
struct pat *spipat_call_immed(struct pat *P, void (*func)(VString, void *, void *), void *cookie);

//  Assign on match
struct pat *spipat_assign_onmatch(struct pat *P, VString *Var);
struct pat *spipat_call_onmatch(struct pat *P, void (*func)(VString, void *, void *), void *cookie);

struct pat *spipat_char(Character);
struct pat *spipat_string(VString Str);
struct pat *spipat_string_ptr(VString *Str);
struct pat *spipat_string_fnc(VString (*Func)(void *, void *), void *);

struct pat *spipat_pattern_ptr(struct pat **P);
struct pat *spipat_predicate(bool (*Func)(void *, void *), void *);

// "or"

struct pat *spipat_or_str_pat(VString L, struct pat *R);
struct pat *spipat_or_pat_str(struct pat *L, VString R);
struct pat *spipat_or_str_str(VString L, VString R);
struct pat *spipat_or_pat_pat(struct pat *L, struct pat *R);
struct pat *spipat_or_chr_pat(Character L, struct pat *R);
struct pat *spipat_or_pat_chr(struct pat *L, Character R);
struct pat *spipat_or_chr_chr(Character L, Character R);
struct pat *spipat_or_str_chr(VString L, Character R);
struct pat *spipat_or_chr_str(Character L, VString R);
#define spipat_or spipat_or_pat_pat

// Any

struct pat *spipat_any_str(VString Str);
struct pat *spipat_any_chr(Character Chr);
struct pat *spipat_any_ptr(VString *Str);
struct pat *spipat_any_fnc(VString (*Func)(void *, void *), void *);
#ifdef CHARSET_PUBLIC
struct pat *spipat_any_csp(CSP csp);
#endif

// Arb

struct pat *spipat_arb(void);

// Arbno

struct pat *spipat_arbno_str(VString P);
struct pat *spipat_arbno_chr(Character P);
struct pat *spipat_arbno(struct pat *P);

// Bal

struct pat *spipat_bal(void);

// Break

struct pat *spipat_break_str(VString Str);
struct pat *spipat_break_chr(Character Str);
struct pat *spipat_break_ptr(VString *Str);
struct pat *spipat_break_fnc(VString (*Func)(void *, void *), void*);
#ifdef CHARSET_PUBLIC
struct pat *spipat_break_csp(CSP csp);
#endif

// BreakX

struct pat *spipat_breakx_str(VString Str);
struct pat *spipat_breakx_chr(Character Str);
struct pat *spipat_breakx_ptr(VString *Str);
struct pat *spipat_breakx_fnc(VString (*Func)(void *, void *), void*);
#ifdef CHARSET_PUBLIC
struct pat *spipat_breakx_csp(CSP csp);
#endif

// Abort (Cancel)

struct pat *spipat_abort(void);

// Fail

struct pat *spipat_fail(void);

// Fence

struct pat *spipat_fence_simple(void);
struct pat *spipat_fence_function(struct pat *P);

// Finalize

void spipat_free(struct pat *Object);
void spipat_hold(struct pat *Object);

// Len

struct pat *spipat_len(size_t Count);
struct pat *spipat_len_fnc(size_t (*Count)(void *, void *), void *);
struct pat *spipat_len_ptr(const size_t *Count);

// NotAny

struct pat *spipat_notany_str(VString Str);
struct pat *spipat_notany_chr(Character c);
struct pat *spipat_notany_ptr(VString *Str);
struct pat *spipat_notany_fnc(VString (*func)(void *, void *), void *);
#ifdef CHARSET_PUBLIC
struct pat *spipat_notany_csp(CSP csp);
#endif

// NSpan

struct pat *spipat_nspan_str(VString Str);
struct pat *spipat_nspan_chr(Character Chr);
struct pat *spipat_nspan_ptr(VString *Str);
struct pat *spipat_nspan_fnc(VString (*Func)(void *, void *), void *);
#ifdef CHARSET_PUBLIC
struct pat *spipat_nspan_csp(CSP csp);
#endif

// Pos

struct pat *spipat_pos(size_t Count);
struct pat *spipat_pos_fnc(size_t (*Func)(void *, void *), void *);
struct pat *spipat_pos_ptr(const size_t *Ptr);

// Rem (Rest)

struct pat *spipat_rem(void);

// Rpos

struct pat *spipat_rpos(size_t Count);
struct pat *spipat_rpos_fnc(size_t (*Func)(void *, void *), void *);
struct pat *spipat_rpos_ptr(const size_t *Ptr);

// Rtab

struct pat *spipat_rtab(size_t Count);
struct pat *spipat_rtab_fnc(size_t (*Func)(void *, void *), void *);
struct pat *spipat_rtab_ptr(const size_t *Ptr);

// Setcur

struct pat *spipat_setcur(size_t *Var);
struct pat *spipat_setcur_fnc(void (*func)(size_t, void *, void *), void *);

// Span

struct pat *spipat_span_str(VString Str);
struct pat *spipat_span_chr(Character Chr);
struct pat *spipat_span_ptr(VString *Ptr);
struct pat *spipat_span_fnc(VString (*Func)(void *, void *), void *);
#ifdef CHARSET_PUBLIC
struct pat *spipat_span_csp(CSP csp);
#endif

// Succeed

struct pat *spipat_succeed(void);

// Tab

struct pat *spipat_tab(size_t Count);
struct pat *spipat_tab_fnc(size_t (*Func)(void *, void *), void *);
struct pat *spipat_tab_ptr(const size_t *Ptr);

// *** EXPERIMENTAL ***

struct dynamic {
    enum { DY_VSTR, DY_BOOL, DY_PAT, DY_UNK } type;
    union {
	VString str;			/* type == DT_VSTR */
	bool pred;			/* type == BY_BOOL */
	struct {			/* type == DY_PAT */
	    struct pat *p;
	    void (*release)(void *cookie);
	    void *cookie;
	} pat;
    } val;
};

struct pat *spipat_dynamic_fnc(void (*Func)(void *, void *, struct dynamic *), void *cookie);

////////////////////////////////////////////////////////////////

#define SPIPAT_DEBUG 1
#define SPIPAT_ANCHORED 2

struct spipat_match {
    int flags;				/* SPIPAT_XXX */
    VString subject;
    struct pat *pattern;
    void *match_cookie;
    size_t start, stop;			/* output */
    const char *exception;
};

enum spipat_match_ret {
    SPIPAT_MATCH_EXCEPTION,
    SPIPAT_MATCH_FAILURE,
    SPIPAT_MATCH_SUCCESS
};

enum spipat_match_ret spipat_match2(struct spipat_match *);
/* compatibility */
#define spipat_match(MP) (spipat_match2(MP) == SPIPAT_MATCH_SUCCESS)

void spipat_dump(struct pat *);
size_t spipat_image(struct pat *, char *buf, size_t buflen);

/* experimental! */
struct pat *spipat_parse(const char *string, ...);

/* optionally user supplied; should take enum? */
void __dead spipat_exception(const char *);

/* optionally user supplied (eg for use w/ GC) */
void *spipat_malloc(size_t);

/* optionally user supplied; called to release cookie from ..._fnc patterns */
void spipat_free_cookie(void *);

/* optionally user supplied; called when _fnc pattern cookie copied */
void spipat_copy_cookie(void *);

/* returns version as string */
const char *spipat_version(void);
