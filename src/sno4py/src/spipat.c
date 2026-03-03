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

// $Id: spipat.c,v 1.23 2021-07-31 01:47:29 phil Exp $

//  Note: the data structures and general approach used in this implementation
//  are derived from the original MINIMAL sources for SPITBOL. The code is not
//  a direct translation, but the approach is followed closely. In particular,
//  we use the one stack approach developed in the SPITBOL implementation.

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>			/* spipat_malloc/free */
#include <stdarg.h>
#include <stdbool.h>
#include <string.h>			/* memcpy */
#if CHARSIZE > 8
#include <uchar.h>
#endif

#include "spipat.h"
#include "spipat_impl.h"

// Size used for internal pattern matching stack. Increase this size if
// complex patterns cause Pattern_Stack_Overflow to occur
int spipat_stack_size = 10000;  /* match stack entries; tunable via set_match_stack_size() */

#if defined(__cplusplus)
#define DYNAMIC(TYPE, VAR, SIZE) TYPE *VAR = new TYPE[SIZE]
#elif defined(_MSC_VER)
//  MSVC does not support C99 VLAs; use _alloca for stack allocation.
#include <malloc.h>
#define DYNAMIC(TYPE, VAR, SIZE) TYPE *VAR = (TYPE *)_alloca(sizeof(TYPE)*(SIZE))
#elif defined(__GNUC__) || __STDC_VERSION__ >= 199901L
#define DYNAMIC(TYPE, VAR, SIZE) TYPE VAR[SIZE]
#else
#define DYNAMIC(TYPE, VAR, SIZE) TYPE *VAR = alloca(sizeof(TYPE)*(SIZE))
#endif

#ifdef _MSC_VER
//  MSVC cannot use function pointer types directly in va_arg().
//  Define typedefs so the va_arg calls compile cleanly.
typedef bool     (*BF_func_t)(void *, void *);
typedef void     (*MF_func_t)(VString, void *, void *);
typedef void     (*CF_func_t)(size_t, void *, void *);
typedef size_t   (*NF_func_t)(void *, void *);
typedef VString  (*VF_func_t)(void *, void *);
typedef void     (*DF_func_t)(void *, void *, struct dynamic *);
#endif

////////////////////////
// Internal Debugging //
////////////////////////

//  define to activate some built-in debugging traceback
//#define INTERNAL_DEBUG

#ifdef INTERNAL_DEBUG
#define DPrintf(...) spipat_printf(__VA_ARGS__)
#else
#define DPrintf(...)
#endif

#define N (PE_Ptr)NULL
   //  Shorthand used to initialize Copy fields to null

static struct pat *new_Pattern(size_t, PE_Ptr);
static PE_Ptr Concat(PE_Ptr L, PE_Ptr R, size_t Incr);
static PE_Ptr S_To_PE(VString Str);
static PE_Ptr C_To_PE(Character C);
static PE_Ptr Copy(PE_Ptr P);
static PE_Ptr Bracket(PE_Ptr E, PE_Ptr P, PE_Ptr A);
static PE_Ptr Alternate(PE_Ptr L, PE_Ptr R);
static PE_Ptr Arbno_Simple(PE_Ptr P);
static void Set_Successor(PE_Ptr Pat, PE_Ptr Succ);
static struct pat *BreakX_Make(PE_Ptr B);
static void Uninitialized_Pattern(void);
static VString copy_String(VString);
static PE_Ptr copy_PE(PE_Ptr);

//////////////////////////////////////////////////
// Description of Algorithm and Data Structures //
//////////////////////////////////////////////////

//  A pattern structure is represented as a linked graph of nodes
//  with the following structure:

//      +------------------------------------+
//      I                Pcode               I
//      +------------------------------------+
//      I                Index               I
//      +------------------------------------+
//      I                Pthen               I
//      +------------------------------------+
//      I             parameter(s)           I
//      +------------------------------------+

//     Pcode is a code value indicating the type of the patterm node. This
//     code is used both as the discriminant value for the record, and as
//     the case index in the main match routine that branches to the proper
//     match code for the given element.

//     Index is a serial index number. The use of these serial index
//     numbers is described in a separate section.

//     Pthen is a pointer to the successor node, i.e the node to be matched
//     if the attempt to match the node succeeds. If this is the last node
//     of the pattern to be matched, then Pthen points to a dummy node
//     of kind PC_EOP (end of pattern), which initiales pattern exit.

//     The parameter or parameters are present for certain node types,
//     and the type varies with the pattern code.

static PE_Ptr new_PE(enum Pattern_Code, IndexT, PE_Ptr, ...);

//	Range of pattern codes that has an Alt field. This is used in the
//	recursive traversals, since these links must be followed.
#define PC_HAS_ALT(CODE) ((CODE) >= PC_Alt &&  (CODE) <= PC_Arbno_X)

//	This is the end of pattern element, and is thus the representation of
//	a null pattern. It has a zero index element since it is never placed
//	inside a pattern. Furthermore it does not need a successor, since it
//	marks the end of the pattern, so that no more successors are needed.
const struct pe EOP_Element = { PC_EOP, 0, N, {0} };

//	This is the end of pattern pointer, that is used in the Pthen pointer
//	of other nodes to signal end of pattern.

//	The following array is used to determine if a pattern used as an
//	argument for Arbno is eligible for treatment using the simple Arbno
//	structure (i.e. it is a pattern that is guaranteed to match at least
//	one character on success, and not to make any entries on the stack.

static const unsigned char OK_For_Simple_Arbno[] = {
    [PC_Any_CSP] = 1,
    [PC_Any_CH] = 1,
    [PC_Any_VF] = 1,
    [PC_Any_VP] = 1,
    [PC_Char] = 1,
    [PC_Len_Nat] = 1,
    [PC_NotAny_CSP] = 1,
    [PC_NotAny_CH] = 1,
    [PC_NotAny_VF] = 1,
    [PC_NotAny_VP] = 1,
    [PC_Span_CSP] = 1,
    [PC_Span_CH] = 1,
    [PC_Span_VF] = 1,
    [PC_Span_VP] = 1,
    [PC_String] = 1,
    [PC_String_2] = 1,
    [PC_String_3] = 1,
    [PC_String_4] = 1,
    [PC_String_5] = 1,
    [PC_String_6] = 1,
};

///////////////////////////////
// The Pattern History Stack //
///////////////////////////////

//	The pattern history stack is used for controlling backtracking when
//	a match fails. The idea is to stack entries that give a cursor value
//	to be restored, and a node to be reestablished as the current node to
//	attempt an appropriate rematch operation. The processing for a pattern
//	element that has rematch alternatives pushes an appropriate entry or
//	entry on to the stack, and the proceeds. If a match fails at any point,
//	the top element of the stack is popped off, resetting the cursor and
//	the match continues by accessing the node stored with this entry.

struct Stack_Entry {
    int Cursor;
      //  Saved cursor value that is restored when this entry is popped
      //  from the stack if a match attempt fails. Occasionally, this
      //  field is used to store a history stack pointer instead of a
      //  cursor. Such cases are noted in the documentation and the value
      //  stored is negative since stack pointer values are always negative.
    struct pe *Node;
      //  This pattern element reference is reestablished as the current
      //  Node to be matched (which will attempt an appropriate rematch).
};

//  The type used for a history stack. The actual instance of the stack
//  is declared as a local variable in the Match routine, to properly
//  handle recursive calls to Match. All stack pointer values are negative
//  to distinguish them from normal cursor values.

//  Note: the pattern matching stack is used only to handle backtracking.
//  If no backtracking occurs, its entries are never accessed, and never
//  popped off, and in particular it is normal for a successful match
//  to terminate with entries on the stack that are simply discarded.

//  Note: in subsequent diagrams of the stack, we always place element
//  zero (the deepest element) at the top of the page, then build the
//  stack down on the page with the most recent (top of stack) element
//  being the bottom-most entry on the page.

//  Stack checking is handled by labeling every pattern with the maximum
//  number of stack entries that are required, so a single check at the
//  start of matching the pattern suffices. There are two exceptions.

//  First, the count does not include entries for recursive pattern
//  references. Such recursions must therefore perform a specific
//  stack check with respect to the number of stack entries required
//  by the recursive pattern that is accessed and the amount of stack
//  that remains unused.

//  Second, the count includes only one iteration of an Arbno pattern,
//  so a specific check must be made on subsequent iterations that there
//  is still enough stack space left. The Arbno node has a field that
//  records the number of stack entries required by its argument for
//  this purpose.

///////////////////////////////////////////////////
// Use of Serial Index Field in Pattern Elements //
///////////////////////////////////////////////////

//  The serial index numbers for the pattern elements are assigned as
//  a pattern is consructed from its constituent elements. Note that there
//  is never any sharing of pattern elements between patterns (copies are
//  always made), so the serial index numbers are unique to a particular
//  pattern as referenced from the P field of a value of type Pattern.

//  The index numbers meet three separate invariants, which are used for
//  various purposes as described in this section.

//  First, the numbers uniquely identify the pattern elements within a
//  pattern. If Num is the number of elements in a given pattern, then
//  the serial index numbers for the elements of this pattern will range
//  from 1 .. Num, so that each element has a separate value.

//  The purpose of this assignment is to provide a convenient auxiliary
//  data structure mechanism during operations which must traverse a
//  pattern (e.g. copy and finalization processing). Once constructed
//  patterns are strictly read only. This is necessary to allow sharing
//  of patterns between tasks. This means that we cannot go marking the
//  pattern (e.g. with a visited bit). Instead we cosntuct a separate
//  vector that contains the necessary information indexed by the Index
//  values in the pattern elements. For this purpose the only requirement
//  is that they be uniquely assigned.

//  Second, the pattern element referenced directly, i.e. the leading
//  pattern element, is always the maximum numbered element and therefore
//  indicates the total number of elements in the pattern. More precisely,
//  the element referenced by the P field of a pattern value, or the
//  element returned by any of the internal pattern construction routines
//  in the body (that return a value of type PE_Ptr) always is this
//  maximum element,

//  The purpose of this requirement is to allow an immediate determination
//  of the number of pattern elements within a pattern. This is used to
//  properly size the vectors used to contain auxiliary information for
//  traversal as described above.

//  Third, as compound pattern structures are constructed, the way in which
//  constituent parts of the pattern are constructed is stylized. This is
//  an automatic consequence of the way that these compounjd structures
//  are constructed, and basically what we are doing is simply documenting
//  and specifying the natural result of the pattern construction. The
//  section describing compound pattern structures gives details of the
//  numbering of each compound pattern structure.

//  The purpose of specifying the stylized numbering structures for the
//  compound patterns is to help simplify the processing in the Image
//  function, since it eases the task of retrieving the original recursive
//  structure of the pattern from the flat graph structure of elements.
//  This use in the Image function is the only point at which the code
//  makes use of the stylized structures.

void spipat_build_ref_array(PE_Ptr E, PE_Ptr *RA);

//  Given a pattern element which is the leading element of a pattern
//  structure, and a Ref_Array with bounds 1 .. E.Index, fills in the
//  Ref_Array so that its N'th entry references the element of the
//  referenced pattern whose Index value is N.

///////////////////////////////
// Recursive Pattern Matches //
///////////////////////////////

//  The pattern primitive (+P) where P is a Pattern_Ptr or Pattern_Func
//  causes a recursive pattern match. This cannot be handled by an actual
//  recursive call to the outer level Match routine, since this would not
//  allow for possible backtracking into the region matched by the inner
//  pattern. Indeed this is the classical clash between recursion and
//  backtracking, and a simple recursive stack structure does not suffice.

//  This section describes how this recursion and the possible associated
//  backtracking is handled. We still use a single stack, but we establish
//  the concept of nested regions on this stack, each of which has a stack
//  base value pointing to the deepest stack entry of the region. The base
//  value for the outer level is zero.

//  When a recursive match is established, two special stack entries are
//  made. The first entry is used to save the original node that starts
//  the recursive match. This is saved so that the successor field of
//  this node is accessible at the end of the match, but it is never
//  popped and executed.

//  The second entry corresponds to a standard new region action. A
//  PC_R_Remove node is stacked, whose cursor field is used to store
//  the outer stack base, and the stack base is reset to point to
//  this PC_R_Remove node. Then the recursive pattern is matched and
//  it can make history stack entries in the normal matter, so now
//  the stack looks like:

//     (stack entries made by outer level)

//     (Special entry, node is (+P) successor
//      cursor entry is not used)

//     (PC_R_Remove entry, "cursor" value is (negative)     <-- Stack base
//      saved base value for the enclosing region)

//     (stack entries made by inner level)

//  If a subsequent failure occurs and pops the PC_R_Remove node, it
//  removes itself and the special entry immediately underneath it,
//  restores the stack base value for the enclosing region, and then
//  again signals failure to look for alternatives that were stacked
//  before the recursion was initiated.

//  Now we need to consider what happens if the inner pattern succeeds, as
//  signalled by accessing the special PC_EOP pattern primitive. First we
//  recognize the nested case by looking at the Base value. If this Base
//  value is Stack_First, then the entire match has succeeded, but if the
//  base value is greater than Stack_First, then we have successfully
//  matched an inner pattern, and processing continues at the outer level.

//  There are two cases. The simple case is when the inner pattern has made
//  no stack entries, as recognized by the fact that the current stack
//  pointer is equal to the current base value. In this case it is fine to
//  remove all trace of the recursion by restoring the outer base value and
//  using the special entry to find the appropriate successor node.

//  The more complex case arises when the inner match does make stack
//  entries. In this case, the PC_EOP processing stacks a special entry
//  whose cursor value saves the saved inner base value (the one that
//  references the corresponding PC_R_Remove value), and whose node
//  pointer references a PC_R_Restore node, so the stack looks like:

//     (stack entries made by outer level)

//     (Special entry, node is (+P) successor,
//      cursor entry is not used)

//     (PC_R_Remove entry, "cursor" value is (negative)
//      saved base value for the enclosing region)

//     (stack entries made by inner level)

//     (PC_Region_Replace entry, "cursor" value is (negative)
//      stack pointer value referencing the PC_R_Remove entry).

//  If the entire match succeeds, then these stack entries are, as usual,
//  ignored and abandoned. If on the other hand a subsequent failure
//  causes the PC_Region_Replace entry to be popped, it restores the
//  inner base value from its saved "cursor" value and then fails again.
//  Note that it is OK that the cursor is temporarily clobbered by this
//  pop, since the second failure will reestablish a proper cursor value.

/////////////////////////////////
// Compound Pattern Structures //
/////////////////////////////////

//  This section discusses the compound structures used to represent
//  constructed patterns. It shows the graph structures of pattern
//  elements that are constructed, and in the case of patterns that
//  provide backtracking possibilities, describes how the history
//  stack is used to control the backtracking. Finally, it notes the
//  way in which the Index numbers are assigned to the structure.

//  In all diagrams, solid lines (built witth minus signs or vertical
//  bars, represent successor pointers (Pthen fields) with > or V used
//  to indicate the direction of the pointer. The initial node of the
//  structure is in the upper left of the diagram. A dotted line is an
//  alternative pointer from the element above it to the element below
//  it. See individual sections for details on how alternatives are used.

///////////////////
// Concatenation //
///////////////////

//  In the pattern structures listed in this section, a line that looks
//  lile ----> with nothing to the right indicates an end of pattern
//  (EOP) pointer that represents the end of the match.

//  When a pattern concatenation (L & R) occurs, the resulting structure
//  is obtained by finding all such EOP pointers in L, and replacing
//  them to point to R. This is the most important flattening that
//  occurs in constructing a pattern, and it means that the pattern
//  matching circuitry does not have to keep track of the structure
//  of a pattern with respect to concatenation, since the appropriate
//  succesor is always at hand.

//  Concatenation itself generates no additional possibilities for
//  backtracking, but the constituent patterns of the concatenated
//  structure will make stack entries as usual. The maximum amount
//  of stack required by the structure is thus simply the sum of the
//  maximums required by L and R.

//  The index numbering of a concatenation structure works by leaving
//  the numbering of the right hand pattern, R, unchanged and adjusting
//  the numbers in the left hand pattern, L up by the count of elements
//  in R. This ensures that the maximum numbered element is the leading
//  element as required (given that it was the leading element in L).

/////////////////
// Alternation //
/////////////////

//  A pattern (L or R) constructs the structure:

//    +---+     +---+
// A  |   +---->| L |---->
//    +---+     +---+
//      .
//      .
//    +---+
//    | R |---->
//    +---+

//  The A element here is a PC_Alt node, and the dotted line represents
//  the contents of the Alt field. When the PC_Alt element is matched,
//  it stacks a pointer to the leading element of R on the history stack
//  so that on subsequent failure, a match of R is attempted.

//  The A node is the higest numbered element in the pattern. The
//  original index numbers of R are unchanged, but the index numbers
//  of the L pattern are adjusted up by the count of elements in R.

//  Note that the difference between the index of the L leading element
//  the index of the R leading element (after building the alt structure)
//  indicates the number of nodes in L, and this is true even after the
//  structure is incorporated into some larger structure. For example,
//  if the A node has index 16, and L has index 15 and R has index
//  5, then we know that L has 10 (15-5) elements in it.

//  Suppose that we now concatenate this structure to another pattern
//  with 9 elements in it. We will now have the A node with an index
//  of 25, L with an index of 24 and R with an index of 14. We still
//  know that L has 10 (24-14) elements in it, numbered 15-24, and
//  consequently the successor of the alternation structure has an
//  index with a value less than 15. This is used in Image to figure
//  out the original recursive structure of a pattern.

//  To clarify the interaction of the alternation and concatenation
//  structures, here is a more complex example of the structure built
//  for the pattern:

//      (V or W or X) (Y or Z)

//  where A,B,C,D,E are all single element patterns:

//    +---+     +---+       +---+     +---+
//    I A I---->I V I---+-->I A I---->I Y I---->
//    +---+     +---+   I   +---+     +---+
//      .               I     .
//      .               I     .
//    +---+     +---+   I   +---+
//    I A I---->I W I-->I   I Z I---->
//    +---+     +---+   I   +---+
//      .               I
//      .               I
//    +---+             I
//    I X I------------>+
//    +---+

//  The numbering of the nodes would be as follows:

//    +---+     +---+       +---+     +---+
//    I 8 I---->I 7 I---+-->I 3 I---->I 2 I---->
//    +---+     +---+   I   +---+     +---+
//      .               I     .
//      .               I     .
//    +---+     +---+   I   +---+
//    I 6 I---->I 5 I-->I   I 1 I---->
//    +---+     +---+   I   +---+
//      .               I
//      .               I
//    +---+             I
//    I 4 I------------>+
//    +---+

//  Note: The above structure actually corresponds to

//    (A or (B or C)) (D or E)

//  rather than

//    ((A or B) or C) (D or E)

//  which is the more natural interpretation, but in fact alternation
//  is associative, and the construction of an alternative changes the
//  left grouped pattern to the right grouped pattern in any case, so
//  that the Image function produces a more natural looking output.

/////////
// Arb //
/////////

//  An Arb pattern builds the structure

//    +---+
//    | X |---->
//    +---+
//      .
//      .
//    +---+
//    | Y |---->
//    +---+

//  The X node is a PC_Arb_X node, which matches null, and stacks a
//  pointer to Y node, which is the PC_Arb_Y node that matches one
//  extra character and restacks itself.

//  The PC_Arb_X node is numbered 2, and the PC_Arb_Y node is 1

/////////////////////////
// Arbno (simple case) //
/////////////////////////

//  The simple form of Arbno can be used where the pattern always
//  matches at least one character if it succeeds, and it is known
//  not to make any history stack entries. In this case, Arbno (P)
//  can construct the following structure:

//      +-------------+
//      |             ^
//      V             |
//    +---+           |
//    | S |---->      |
//    +---+           |
//      .             |
//      .             |
//    +---+           |
//    | P |---------->+
//    +---+

//  The S (PC_Arbno_S) node matches null stacking a pointer to the
//  pattern P. If a subsequent failure causes P to be matched and
//  this match succeeds, then node A gets restacked to try another
//  instance if needed by a subsequent failure.

//  The node numbering of the constituent pattern P is not affected.
//  The S node has a node number of P.Index + 1.

//////////////////////////
// Arbno (complex case) //
//////////////////////////

//  A call to Arbno (P), where P can match null (or at least is not
//  known to require a non-null string) and/or P requires pattern stack
//  entries, constructs the following structure:

//      +--------------------------+
//      |                          ^
//      V                          |
//    +---+                        |
//    | X |---->                   |
//    +---+                        |
//      .                          |
//      .                          |
//    +---+     +---+     +---+    |
//    | E |---->| P |---->| Y |--->+
//    +---+     +---+     +---+

//  The node X (PC_Arbno_X) matches null, stacking a pointer to the
//  E-P-X structure used to match one Arbno instance.

//  Here E is the PC_R_Enter node which matches null and creates two
//  stack entries. The first is a special entry whose node field is
//  not used at all, and whose cursor field has the initial cursor.

//  The second entry corresponds to a standard new region action. A
//  PC_R_Remove node is stacked, whose cursor field is used to store
//  the outer stack base, and the stack base is reset to point to
//  this PC_R_Remove node. Then the pattern P is matched, and it can
//  make history stack entries in the normal manner, so now the stack
//  looks like:

//     (stack entries made before assign pattern)

//     (Special entry, node field not used,
//      used only to save initial cursor)

//     (PC_R_Remove entry, "cursor" value is (negative)  <-- Stack Base
//      saved base value for the enclosing region)

//     (stack entries made by matching P)

//  If the match of P fails, then the PC_R_Remove entry is popped and
//  it removes both itself and the special entry underneath it,
//  restores the outer stack base, and signals failure.

//  If the match of P succeeds, then node Y, the PC_Arbno_Y node, pops
//  the inner region. There are two possibilities. If matching P left
//  no stack entries, then all traces of the inner region can be removed.
//  If there are stack entries, then we push an PC_Region_Replace stack
//  entry whose "cursor" value is the inner stack base value, and then
//  restore the outer stack base value, so the stack looks like:

//     (stack entries made before assign pattern)

//     (Special entry, node field not used,
//      used only to save initial cursor)

//     (PC_R_Remove entry, "cursor" value is (negative)
//      saved base value for the enclosing region)

//     (stack entries made by matching P)

//     (PC_Region_Replace entry, "cursor" value is (negative)
//      stack pointer value referencing the PC_R_Remove entry).

//  Now that we have matched another instance of the Arbno pattern,
//  we need to move to the successor. There are two cases. If the
//  Arbno pattern matched null, then there is no point in seeking
//  alternatives, since we would just match a whole bunch of nulls.
//  In this case we look through the alternative node, and move
//  directly to its successor (i.e. the successor of the Arbno
//  pattern). If on the other hand a non-null string was matched,
//  we simply follow the successor to the alternative node, which
//  sets up for another possible match of the Arbno pattern.

//  As noted in the section on stack checking, the stack count (and
//  hence the stack check) for a pattern includes only one iteration
//  of the Arbno pattern. To make sure that multiple iterations do not
//  overflow the stack, the Arbno node saves the stack count required
//  by a single iteration, and the Concat function increments this to
//  include stack entries required by any successor. The PC_Arbno_Y
//  node uses this count to ensure that sufficient stack remains
//  before proceeding after matching each new instance.

//  The node numbering of the constituent pattern P is not affected.
//  Where N is the number of nodes in P, the Y node is numbered N + 1,
//  the E node is N + 2, and the X node is N + 3.

//////////////////////
// Assign Immediate //
//////////////////////

//  Immediate assignment (P * V) constructs the following structure

//    +---+     +---+     +---+
//    | E |---->| P |---->| A |---->
//    +---+     +---+     +---+

//  Here E is the PC_R_Enter node which matches null and creates two
//  stack entries. The first is a special entry whose node field is
//  not used at all, and whose cursor field has the initial cursor.

//  The second entry corresponds to a standard new region action. A
//  PC_R_Remove node is stacked, whose cursor field is used to store
//  the outer stack base, and the stack base is reset to point to
//  this PC_R_Remove node. Then the pattern P is matched, and it can
//  make history stack entries in the normal manner, so now the stack
//  looks like:

//     (stack entries made before assign pattern)

//     (Special entry, node field not used,
//      used only to save initial cursor)

//     (PC_R_Remove entry, "cursor" value is (negative)  <-- Stack Base
//      saved base value for the enclosing region)

//     (stack entries made by matching P)

//  If the match of P fails, then the PC_R_Remove entry is popped
//  and it removes both itself and the special entry underneath it,
//  restores the outer stack base, and signals failure.

//  If the match of P succeeds, then node A, which is the actual
//  PC_Assign_Imm node, executes the assignment (using the stack
//  base to locate the entry with the saved starting cursor value),
//  and the pops the inner region. There are two possibilities, if
//  matching P left no stack entries, then all traces of the inner
//  region can be removed. If there are stack entries, then we push
//  an PC_Region_Replace stack entry whose "cursor" value is the
//  inner stack base value, and then restore the outer stack base
//  value, so the stack looks like:

//     (stack entries made before assign pattern)

//     (Special entry, node field not used,
//      used only to save initial cursor)

//     (PC_R_Remove entry, "cursor" value is (negative)
//      saved base value for the enclosing region)

//     (stack entries made by matching P)

//     (PC_Region_Replace entry, "cursor" value is the (negative)
//      stack pointer value referencing the PC_R_Remove entry).

//  If a subsequent failure occurs, the PC_Region_Replace node restores
//  the inner stack base value and signals failure to explore rematches
//  of the pattern P.

//  The node numbering of the constituent pattern P is not affected.
//  Where N is the number of nodes in P, the A node is numbered N + 1,
//  and the E node is N + 2.

/////////////////////
// Assign On Match //
/////////////////////

//  The assign on match (**) pattern is quite similar to the assign
//  immediate pattern, except that the actual assignment has to be
//  delayed. The following structure is constructed:

//    +---+     +---+     +---+
//    | E |---->| P |---->| A |---->
//    +---+     +---+     +---+

//  The operation of this pattern is identical to that described above
//  for deferred assignment, up to the point where P has been matched.

//  The A node, which is the PC_Assign_OnM node first pushes a
//  PC_Assign node onto the history stack. This node saves the ending
//  cursor and acts as a flag for the final assignment, as further
//  described below.

//  It then stores a pointer to itself in the special entry node field.
//  This was otherwise unused, and is now used to retrive the address
//  of the variable to be assigned at the end of the pattern.

//  After that the inner region is terminated in the usual manner,
//  by stacking a PC_R_Restore entry as described for the assign
//  immediate case. Note that the optimization of completely
//  removing the inner region does not happen in this case, since
//  we have at least one stack entry (the PC_Assign one we just made).
//  The stack now looks like:

//     (stack entries made before assign pattern)

//     (Special entry, node points to copy of
//      the PC_Assign_OnM node, and the
//      cursor field saves the initial cursor).

//     (PC_R_Remove entry, "cursor" value is (negative)
//      saved base value for the enclosing region)

//     (stack entries made by matching P)

//     (PC_Assign entry, saves final cursor)

//     (PC_Region_Replace entry, "cursor" value is (negative)
//      stack pointer value referencing the PC_R_Remove entry).

//  If a subsequent failure causes the PC_Assign node to execute it
//  simply removes itself and propagates the failure.

//  If the match succeeds, then the history stack is scanned for
//  PC_Assign nodes, and the assignments are executed (examination
//  of the above diagram will show that all the necessary data is
//  at hand for the assignment).

//  To optimize the common case where no assign-on-match operations
//  are present, a global flag Assign_OnM is maintained which is
//  initialize to false, and gets set true as part of the execution
//  of the PC_Assign_OnM node. The scan of the history stack for
//  PC_Assign entries is done only if this flag is set.

//  The node numbering of the constituent pattern P is not affected.
//  Where N is the number of nodes in P, the A node is numbered N + 1,
//  and the E node is N + 2.

/////////
// Bal //
/////////

//  Bal builds a single node:

//    +---+
//    | B |---->
//    +---+

//  The node B is the PC_Bal node which matches a parentheses balanced
//  string, starting at the current cursor position. It then updates
//  the cursor past this matched string, and stacks a pointer to itself
//  with this updated cursor value on the history stack, to extend the
//  matched string on a subequent failure.

//  Since this is a single node it is numbered 1 (the reason we include
//  it in the compound patterns section is that it backtracks).

////////////
// BreakX //
////////////

//  BreakX builds the structure

//    +---+     +---+
//    | B |---->| A |---->
//    +---+     +---+
//      ^         .
//      |         .
//      |       +---+
//      +<------| X |
//              +---+

//  Here the B node is the BreakX_xx node that performs a normal Break
//  function. The A node is an alternative (PC_Alt) node that matches
//  null, but stacks a pointer to node X (the PC_BreakX_X node) which
//  extends the match one character (to eat up the previously detected
//  break character), and then rematches the break.

//  The B node is numbered 3, the alternative node is 1, and the X
//  node is 2.

///////////
// Fence //
///////////

//  Fence builds a single node:

//    +---+
//    | F |---->
//    +---+

//  The element F, PC_Fence,  matches null, and stacks a pointer to a
//  PC_Abort element which will abort the match on a subsequent failure.

//  Since this is a single element it is numbered 1 (the reason we
//  include it in the compound patterns section is that it backtracks).

////////////////////
// Fence Function //
////////////////////

//  A call to the Fence function builds the structure:

//    +---+     +---+     +---+
//    | E |---->| P |---->| X |---->
//    +---+     +---+     +---+

//  Here E is the PC_R_Enter node which matches null and creates two
//  stack entries. The first is a special entry which is not used at
//  all in the fence case (it is present merely for uniformity with
//  other cases of region enter operations).

//  The second entry corresponds to a standard new region action. A
//  PC_R_Remove node is stacked, whose cursor field is used to store
//  the outer stack base, and the stack base is reset to point to
//  this PC_R_Remove node. Then the pattern P is matched, and it can
//  make history stack entries in the normal manner, so now the stack
//  looks like:

//     (stack entries made before fence pattern)

//     (Special entry, not used at all)

//     (PC_R_Remove entry, "cursor" value is (negative)  <-- Stack Base
//      saved base value for the enclosing region)

//     (stack entries made by matching P)

//  If the match of P fails, then the PC_R_Remove entry is popped
//  and it removes both itself and the special entry underneath it,
//  restores the outer stack base, and signals failure.

//  If the match of P succeeds, then node X, the PC_Fence_X node, gets
//  control. One might be tempted to think that at this point, the
//  history stack entries made by matching P can just be removed since
//  they certainly are not going to be used for rematching (that is
//  whole point of Fence after all!) However, this is wrong, because
//  it would result in the loss of possible assign-on-match entries
//  for deferred pattern assignments.

//  Instead what we do is to make a special entry whose node references
//  PC_Fence_Y, and whose cursor saves the inner stack base value, i.e.
//  the pointer to the PC_R_Remove entry. Then the outer stack base
//  pointer is restored, so the stack looks like:

//     (stack entries made before assign pattern)

//     (Special entry, not used at all)

//     (PC_R_Remove entry, "cursor" value is (negative)
//      saved base value for the enclosing region)

//     (stack entries made by matching P)

//     (PC_Fence_Y entry, "cursor" value is (negative) stack
//      pointer value referencing the PC_R_Remove entry).

//  If a subsequent failure occurs, then the PC_Fence_Y entry removes
//  the entire inner region, including all entries made by matching P,
//  and alternatives prior to the Fence pattern are sought.

//  The node numbering of the constituent pattern P is not affected.
//  Where N is the number of nodes in P, the X node is numbered N + 1,
//  and the E node is N + 2.

/////////////
// Succeed //
/////////////

//  Succeed builds a single node:

//    +---+
//    | S |---->
//    +---+

//  The node S is the PC_Succeed node which matches null, and stacks
//  a pointer to itself on the history stack, so that a subsequent
//  failure repeats the same match.

//  Since this is a single node it is numbered 1 (the reason we include
//  it in the compound patterns section is that it backtracks).

////////////////////
// Call Immediate //
////////////////////

//  The structure built for a write immediate operation:

//    +---+     +---+     +---+
//    | E |---->| P |---->| C |---->
//    +---+     +---+     +---+

//  Here E is the PC_R_Enter node and C is the PC_Call_Imm node. The
//  handling is identical to that described above for Assign Immediate,
//  except that at the point where a successful match occurs, the matched
//  substring is written to the referenced file.

//  The node numbering of the constituent pattern P is not affected.
//  Where N is the number of nodes in P, the W node is numbered N + 1,
//  and the E node is N + 2.

///////////////////
// Call On Match //
///////////////////

//  The structure built for call write on match operation:

//    +---+     +---+     +---+
//    | E |---->| P |---->| C |---->
//    +---+     +---+     +---+

//  Here E is the PC_R_Enter node and C is the PC_Call_OnM node. The
//  handling is identical to that described above for Assign On Match,
//  except that at the point where a successful match has completed,
//  the matched substring is written to the referenced file.

//  The node numbering of the constituent pattern P is not affected.
//  Where N is the number of nodes in P, the W node is numbered N + 1,
//  and the E node is N + 2.

///////////////////////
// Constant Patterns //
///////////////////////

//  The following pattern elements are referenced only from the pattern
//  history stack. In each case the processing for the pattern element
//  results in pattern match abort, or futher failure, so there is no
//  need for a successor and no need for a node number

// would love for these to be "const" but end up with pointer mismatches
static const struct pe CP_Assign    = {PC_Assign,    0, N, {0}};
static const struct pe CP_Abort     = {PC_Abort,     0, N, {0}};
static const struct pe CP_Fence_Y   = {PC_Fence_Y,   0, N, {0}};
static const struct pe CP_R_Remove  = {PC_R_Remove,  0, N, {0}};
static const struct pe CP_R_Restore = {PC_R_Restore, 0, N, {0}};

///////////////////////
// Local Subprograms //
///////////////////////

//  This is the common pattern match routine. It is passed a string and
//  a pattern, and it indicates success or failure, and on success the
//  section of the string matched. It does not perform any assignments
//  to the subject string, so pattern replacement is for the caller.
//
//  Subject The subject string. The lower bound is always one. In the
//          Match procedures, it is fine to use strings whose lower bound
//          is not one, but we perform a one time conversion before the
//          call to XMatch, so that XMatch does not have to be bothered
//          with strange lower bounds.
//
//  Pat_P   Points to initial pattern element of pattern to be matched
//
//  Pat_S   Maximum required stack entries for pattern to be matched
//
//  Start   If match is successful, starting index of matched section.
//          This value is always non-zero. A value of zero is used to
//          indicate a failed match.
//
//  Stop    If match is successful, ending index of matched section.
//          This can be zero if we match the null string at the start,
//          in which case Start is set to zero, and Stop to one. If the
//          Match fails, then the contents of Stop is undefined.

////////////////////////////////////////////////////////////////

typedef uint32_t charset_bits_t;
#define CHARSET_T_NUMBITS 32

#if CHARSIZE == 8
#define CHARSET_SIZE 256
#else
#define CHARSET_NUM_PLANES 17		/* 0x00xxxx thru 0x10xxxx */
// OR
//#define CHARSET_SIZE (0x10FFFF+1)
#endif

typedef struct character_set {
    uint32_t refcount;
#ifdef CHARSET_NUM_PLANES
    charset_bits_t *planes[CHARSET_NUM_PLANES];
#define PLANE_SHIFT 16
#define PLANE_SIZE (1<<(PLANE_SHIFT))
#define PLANE_MASK (PLANE_SIZE-1)
#else
    charset_bits_t bits[CHARSET_SIZE/CHARSET_T_NUMBITS];
#endif
} Character_Set;

#ifdef CHARSET_NUM_PLANES
static bool
Is_In(Character c, Character_Set *csp) {
    int plane;
    charset_bits_t *pp;			/* plane pointer */
    if (c < 0)
	return false;
    plane = c >> PLANE_SHIFT;
    if (plane >= CHARSET_NUM_PLANES)
	return false;
    c &= PLANE_MASK;
    pp = csp->planes[plane];
    if (!pp)
	return false;
    return pp[c/CHARSET_T_NUMBITS] & (1 << (c % CHARSET_T_NUMBITS));
}

static void
Set_Add(Character c, Character_Set *csp) {
    int plane;
    charset_bits_t *pp;			/* plane pointer */
    if (c < 0)
	return;
    plane = c >> PLANE_SHIFT;
    if (plane >= CHARSET_NUM_PLANES)
	return;
    c &= PLANE_MASK;
    pp = csp->planes[plane];
    if (!pp) {
	pp = csp->planes[plane] = spipat_malloc(PLANE_SIZE);
	if (!pp)
	    spipat_exception("Set_Add malloc failed");
	memset(pp, 0, PLANE_SIZE);
    }
    pp[c/CHARSET_T_NUMBITS] |= (1 << (c % CHARSET_T_NUMBITS));
}

#else // CHARSET_NUM_PLANES not defined

#define Is_In(CHAR,CSP) ((CSP)->bits[(CHAR)/CHARSET_T_NUMBITS] & (1<<((CHAR)%CHARSET_T_NUMBITS)))
#define Set_Add(CHAR,CSP) ((CSP)->bits[(CHAR)/CHARSET_T_NUMBITS] |= (1<<((CHAR)%CHARSET_T_NUMBITS)))

#endif // CHARSET_NUM_PLANES not defined

static bool
Is_In_Str(int c, VString S) {
    while (S.len-- > 0)
	if (*S.ptr++ == c)
	    return true;
    return false;
}

static Character_Set *
To_Set(VString S) {
    Character_Set *csp;

    csp = spipat_malloc(sizeof(Character_Set));
    if (!csp)
	spipat_exception("To_Set malloc failed");
    memset(csp, 0, sizeof(Character_Set));
    while (S.len-- > 0) {
	Character c = *S.ptr++;
	Set_Add(c, csp);
    }
    // set refcount to one??
    return csp;
}

static void
Free_Set(Character_Set *csp) {
    if (csp->refcount > 0) {
	csp->refcount--;
	return;
    }
#ifdef CHARSET_NUM_PLANES
    for (int plane = 0; plane < CHARSET_NUM_PLANES; plane++)
	if (csp->planes[plane])
	    free(csp->planes[plane]);
#endif
    free(csp);
}

static void
Copy_Set(Character_Set *csp) {
    if (csp)				/* paranoia */
	csp->refcount++;
}

/////////////////
// new_Pattern //
/////////////////

static struct pat *
new_Pattern(size_t Stk, PE_Ptr P) {
    struct pat *Pat = spipat_malloc(sizeof(struct pat));

    if (!Pat)
	spipat_exception("new_Pattern spipat_malloc failed");
    Pat->Stk = Stk;
    Pat->P = P;
    Pat->Refs = 1;
    return Pat;
}

/////////////////
// copy_String //
/////////////////

static VString
copy_String(VString Str) {
    VString ret;
    void *ptr;
    ptr = spipat_malloc(sizeof(Character)*Str.len);
    if (!ptr)
	spipat_exception("copy_String spipat_malloc failed");
    memcpy(ptr, Str.ptr, sizeof(Character)*Str.len);
    ret.ptr = ptr;
    ret.len = Str.len;
    ret.release = NULL;			/* no underlying object */
    ret.cookie = NULL;
    return ret;
}

/////////////
// Copy_PE //
/////////////

static PE_Ptr
copy_PE(PE_Ptr Ptr) {
    PE_Ptr ret = spipat_malloc(sizeof(struct pe));

    if (!ret)
	spipat_exception("copy_PE spipat_malloc failed");
    *ret = *Ptr;

    /* deal with stuff in "val" here (hide impl details from Copy */
    switch (Ptr->Pcode) {
    case PC_Pred_Func:
	spipat_copy_cookie(Ptr->val.BF.cookie);
	break;
    case PC_Call_Imm:
    case PC_Call_OnM:
	spipat_copy_cookie(Ptr->val.MF.cookie);
	break;
    case PC_Pos_NF:
    case PC_Len_NF:
    case PC_RPos_NF:
    case PC_RTab_NF:
	spipat_copy_cookie(Ptr->val.NF.cookie);
	break;
    case PC_Any_VF:
    case PC_Break_VF:
    case PC_BreakX_VF:
    case PC_NotAny_VF:
    case PC_NSpan_VF:
    case PC_Span_VF:
    case PC_String_VF:
	spipat_copy_cookie(Ptr->val.VF.cookie);
	break;
    case PC_Dynamic_Func:
	spipat_copy_cookie(Ptr->val.DF.cookie);
	break;
    case PC_Any_CSP:
    case PC_Break_CSP:
    case PC_BreakX_CSP:
    case PC_NotAny_CSP:
    case PC_NSpan_CSP:
    case PC_Span_CSP:
	Copy_Set(Ptr->val.CSP);
	break;
    default:
	break;
    }
    return ret;
}

void
spipat_putchar(Character c) {
#if CHARSIZE == 8
    putchar(c);
#else
    char buf[MB_CUR_MAX];
    size_t len = c32rtomb(buf, c, NULL);
    for (int i = 0; i < len; i++)
	putchar(buf[i]);
#endif
}

// spipat_printf
void
spipat_printf(const char *fmt, ...) {
    va_list ap;
    char c;

    va_start(ap, fmt);

    while ((c = *fmt++)) {
	if (c == '%') {
	    // handle '#' for alternate formatting style (framge with quotes as appropriate)?
	    switch ((c = *fmt++)) {
	    case '%':
		putchar(c);
		break;
	    case 'c':
		putchar(va_arg(ap, int)); /* char promoted to int */
		break;
	    case 'd':
		printf("%d", va_arg(ap, int));
		break;
	    case 'p':
		printf("%p", va_arg(ap, void *));
		break;
	    case 's':			/* print a C string */
		printf("%s", va_arg(ap, char *)); /* char promoted to int */
		break;
	    case 'S':			/* print a VString (passed by value) */
	    {
		VString S = va_arg(ap, VString);
		while (S.len-- > 0)
		    spipat_putchar(*S.ptr++);
		break;
	    }
	    case 'z':
		printf("%zu", va_arg(ap, size_t));
		break;
	    case 'Z':
	    {
		Character_Set *Set = va_arg(ap, Character_Set *);
		(void) Set;
		printf("<CS>");
		break;
	    }
	    default:
		printf("bad spipat_printf formatting character '%c'\n", c);
		return;			/* XXX complain? */
	    }
	}
	else
	    putchar(c);
    }
    va_end(ap);
}

////////////////////////////////////////////////////////////////

//////////
// "and //
//////////

struct pat *
spipat_and_str_pat(VString L, struct pat *R) {
    return new_Pattern(R->Stk, Concat(S_To_PE (L), Copy(R->P), R->Stk));
}

struct pat *
spipat_and_pat_str(struct pat *L, VString R) {
    return new_Pattern(L->Stk, Concat(Copy(L->P), S_To_PE (R), 0));
}

struct pat *
spipat_and_chr_pat(Character L, struct pat *R) {
    return new_Pattern(R->Stk, Concat(C_To_PE (L), Copy(R->P), R->Stk));
}

struct pat *
spipat_and_pat_chr(struct pat *L, Character R) {
    return new_Pattern(L->Stk, Concat(Copy(L->P), C_To_PE (R), 0));
}

struct pat *
spipat_and(struct pat *L, struct pat *R) {
    return new_Pattern(L->Stk + R->Stk,
		       Concat(Copy(L->P), Copy(R->P), R->Stk));
}

/////////
// "*" //
/////////

//  Assign immediate

//    +---+     +---+     +---+
//    | E |---->| P |---->| A |---->
//    +---+     +---+     +---+

//  The node numbering of the constituent pattern P is not affected.
//  Where N is the number of nodes in P, the A node is numbered N + 1,
//  and the E node is N + 2.

struct pat *
spipat_assign_immed(struct pat *P, VString *Var) {
    PE_Ptr Pat = Copy(P->P);
    PE_Ptr E   = new_PE(PC_R_Enter,	  0, EOP);
    PE_Ptr A   = new_PE(PC_Assign_Imm,    0, EOP, Var);
    return new_Pattern(P->Stk + 3, Bracket(E, Pat, A));
}

//  Call immediate

//    +---+     +---+     +---+
//    | E |---->| P |---->| C |---->
//    +---+     +---+     +---+

//  The node numbering of the constituent pattern P is not affected.
//  Where N is the number of nodes in P, the W node is numbered N + 1,
//  and the E node is N + 2.

struct pat *
spipat_call_immed(struct pat *P, void (*func)(VString, void *, void *), void *cookie) {
    PE_Ptr Pat = Copy(P->P);
    PE_Ptr E   = new_PE(PC_R_Enter,   0, EOP);
    PE_Ptr C   = new_PE(PC_Call_Imm, 0, EOP, func, cookie);
    return new_Pattern(3, Bracket(E, Pat, C));
}

//////////
// "**" //
//////////

//  Assign on match

//    +---+     +---+     +---+
//    | E |---->| P |---->| A |---->
//    +---+     +---+     +---+

//  The node numbering of the constituent pattern P is not affected.
//  Where N is the number of nodes in P, the A node is numbered N + 1,
//  and the E node is N + 2.

struct pat *
spipat_assign_onmatch(struct pat *P, VString *Var) {
    PE_Ptr Pat = Copy(P->P);
    PE_Ptr E   = new_PE(PC_R_Enter,    0, EOP);
    PE_Ptr A   = new_PE(PC_Assign_OnM, 0, EOP, Var);
    return new_Pattern(P->Stk + 3, Bracket(E, Pat, A));
}

//  Call on match

//    +---+     +---+     +---+
//    | E |---->| P |---->| C |---->
//    +---+     +---+     +---+

//  The node numbering of the constituent pattern P is not affected.
//  Where N is the number of nodes in P, the W node is numbered N + 1,
//  and the E node is N + 2.

struct pat *
spipat_call_onmatch(struct pat *P, void (*func)(VString, void *, void *), void *cookie) {
    PE_Ptr Pat = Copy(P->P);
    PE_Ptr E   = new_PE(PC_R_Enter,  0, EOP);
    PE_Ptr C   = new_PE(PC_Call_OnM, 0, EOP, func, cookie);

    return new_Pattern(P->Stk + 3, Bracket(E, Pat, C));
}

struct pat *
spipat_string(VString Str) {
    return new_Pattern(0, S_To_PE(Str));
}

struct pat *
spipat_char(Character c) {
    return new_Pattern(0, C_To_PE(c));
}

/////////
// "+" //
/////////

struct pat *
spipat_string_ptr(VString *Str) {
    return new_Pattern(0, new_PE(PC_String_VP, 1, EOP, Str));
}

struct pat *
spipat_string_fnc(VString (*Func)(void *, void *), void *Cookie) {
    return new_Pattern(0, new_PE(PC_String_VF, 1, EOP, Func, Cookie));
}

struct pat *
spipat_pattern_ptr(struct pat **P) {
    return new_Pattern(3, new_PE(PC_Rpat, 1, EOP, P));
}

struct pat *
spipat_predicate(bool (*Func)(void *, void *), void *Cookie) {
    return new_Pattern(3, new_PE(PC_Pred_Func, 1, EOP, Func, Cookie));
}

struct pat *
spipat_dynamic_fnc(void (*Func)(void *, void *, struct dynamic *), void *Cookie) {
    /* XXX dunno about new_Pattern args */
    return new_Pattern(3, new_PE(PC_Dynamic_Func, 1, EOP, Func, Cookie));
}

//////////
// "or" //
//////////

struct pat *
spipat_or_str_pat(VString L, struct pat *R) {
    return new_Pattern(R->Stk + 1, Alternate(S_To_PE (L), Copy(R->P)));
}

struct pat *
spipat_or_pat_str(struct pat *L, VString R) {
    return new_Pattern(L->Stk + 1, Alternate(Copy(L->P), S_To_PE (R)));
}

struct pat *
spipat_or_str_str(VString L, VString R) {
    return new_Pattern(1, Alternate(S_To_PE (L), S_To_PE (R)));
}

struct pat *
spipat_or_pat_pat(struct pat *L, struct pat *R) {
#define UNSIGNED_MAX(A,B) (((A) > (B)) ? (A) : (B))
    return new_Pattern(UNSIGNED_MAX(L->Stk, R->Stk) + 1,
		       Alternate(Copy(L->P), Copy(R->P)));
}

struct pat *
spipat_or_chr_pat(Character L, struct pat *R) {
    return new_Pattern(1, Alternate(C_To_PE (L), Copy(R->P)));
}

struct pat *
spipat_or_pat_chr(struct pat *L, Character R) {
    return new_Pattern(1, Alternate(Copy(L->P), C_To_PE (R)));
}

struct pat *
spipat_or_chr_chr(Character L, Character R) {
    return new_Pattern(1, Alternate(C_To_PE (L), C_To_PE (R)));
}

struct pat *
spipat_or_str_chr(VString L, Character R) {
    return new_Pattern(1, Alternate(S_To_PE (L), C_To_PE (R)));
}

struct pat *
spipat_or_chr_str(Character L, VString R) {
    return new_Pattern(1, Alternate(C_To_PE (L), S_To_PE (R)));
}

///////////
// Abort //
///////////

struct pat *
spipat_abort(void) {
    return new_Pattern(0, new_PE(PC_Abort, 1, EOP));
}

#if 0
////////////
// Adjust //
////////////

//  No two patterns share the same pattern elements, so the adjust
//  procedure for a Pattern assignment must do a deep copy of the
//  pattern element structure.

static void
Adjust(struct pat *Object) {
    Object->P = Copy(Object->P);
}
#endif

///////////////
// Alternate //
///////////////

static PE_Ptr
Alternate(PE_Ptr L, PE_Ptr R) {
    //  If the left pattern is null, then we just add the alternation
    //  node with an index one greater than the right hand pattern.
    if (L == EOP)
	return new_PE(PC_Alt, R->Index + 1, EOP, R);
    else {
	//  If the left pattern is non-null, then build a reference vector
	//  for its elements, and adjust their index values to acccomodate
	//  the right hand elements. Then add the alternation node.
	int n = L->Index;
	DYNAMIC(PE_Ptr, Refs, n);

	spipat_build_ref_array(L, Refs);

	for (int j = 0; j < n; j++)
	    Refs[j]->Index += R->Index;
	return new_PE(PC_Alt, L->Index + 1, L, R);
    }
}

/////////
// Any //
/////////

struct pat *
spipat_any_str(VString Str) {
    return new_Pattern(0, new_PE(PC_Any_CSP, 1, EOP, To_Set (Str)));
}

struct pat *
spipat_any_chr(Character Chr) {
    return new_Pattern(0, new_PE(PC_Any_CH, 1, EOP, Chr));
}

#ifdef CHARSET_PUBLIC
struct pat *
spipat_any_csp(Character_Set *CSP) {
    return new_Pattern(0, new_PE(PC_Any_CSP, 1, EOP, CSP));
}
#endif

struct pat *
spipat_any_ptr(VString *Str) {
    return new_Pattern(0, new_PE(PC_Any_VP, 1, EOP, Str));
}

struct pat *
spipat_any_fnc(VString (*Func)(void *, void *), void *Cookie) {
    return new_Pattern(0, new_PE(PC_Any_VF, 1, EOP, Func, Cookie));
}

/////////
// Arb //
/////////

//    +---+
//    | X |---->
//    +---+
//      .
//      .
//    +---+
//    | Y |---->
//    +---+

//  The PC_Arb_X element is numbered 2, and the PC_Arb_Y element is 1

struct pat *
spipat_arb(void) {
    PE_Ptr y = new_PE(PC_Arb_Y, 1, EOP);
    PE_Ptr x = new_PE(PC_Arb_X, 2, EOP, y);
    return new_Pattern(1, x);
}

///////////
// Arbno //
///////////

struct pat *
spipat_arbno_str(VString P) {
    if (P.len == 0)
	return new_Pattern(0, EOP);
    else
	return new_Pattern(0, Arbno_Simple(S_To_PE (P)));
}

struct pat *
spipat_arbno_chr(Character P) {
   return new_Pattern(0, Arbno_Simple(C_To_PE (P)));
}

struct pat *
spipat_arbno(struct pat *P) {
    PE_Ptr Pat = Copy(P->P);

    if (P->Stk == 0 && OK_For_Simple_Arbno[Pat->Pcode])
	return new_Pattern(0, Arbno_Simple(Pat));

    //  This is the complex case, either the pattern makes stack entries
    //  or it is possible for the pattern to match the null string (more
    //  accurately, we don't know that this is not the case).

    //      +--------------------------+
    //      |                          ^
    //      V                          |
    //    +---+                        |
    //    | X |---->                   |
    //    +---+                        |
    //      .                          |
    //      .                          |
    //    +---+     +---+     +---+    |
    //    | E |---->| P |---->| Y |--->+
    //    +---+     +---+     +---+

    //  The node numbering of the constituent pattern P is not affected.
    //  Where N is the number of nodes in P, the Y node is numbered N + 1,
    //  the E node is N + 2, and the X node is N + 3.
    else {
	PE_Ptr E = new_PE(PC_R_Enter, 0, EOP);
	PE_Ptr X = new_PE(PC_Arbno_X, 0, EOP, E);
	PE_Ptr Y = new_PE(PC_Arbno_Y, 0, X,   P->Stk + 3);
	PE_Ptr EPY = Bracket(E, Pat, Y);

	X->val.Alt = EPY;
	X->Index = EPY->Index + 1;
	return new_Pattern(P->Stk + 3, X);
    }
}

//////////////////
// Arbno_Simple //
//////////////////

//      +-------------+
//      |             ^
//      V             |
//    +---+           |
//    | S |---->      |
//    +---+           |
//      .             |
//      .             |
//    +---+           |
//    | P |---------->+
//    +---+

//  The node numbering of the constituent pattern P is not affected.
//  The S node has a node number of P->Index + 1.

//  Note that we know that P cannot be EOP, because a null pattern
//  does not meet the requirements for simple Arbno.

static PE_Ptr
Arbno_Simple(PE_Ptr P) {
    PE_Ptr S = new_PE(PC_Arbno_S, P->Index + 1, EOP, P);
    Set_Successor (P, S);
    return S;
}

/////////
// Bal //
/////////

struct pat *
spipat_bal(void) {
    return new_Pattern(1, new_PE(PC_Bal, 1, EOP));
}

/////////////
// Bracket //
/////////////

static PE_Ptr
Bracket(PE_Ptr E, PE_Ptr P, PE_Ptr A) {
    if (P == EOP) {
	E->Pthen = A;
	E->Index = 2;
	A->Index = 1;
    }
    else {
	E->Pthen = P;
	Set_Successor (P, A);
	E->Index = P->Index + 2;
	A->Index = P->Index + 1;
    }
    return E;
}

///////////
// Break //
///////////

struct pat *
spipat_break_str(VString Str) {
    return new_Pattern(0, new_PE(PC_Break_CSP, 1, EOP, To_Set (Str)));
}

struct pat *
spipat_break_chr(Character Str) {
    return new_Pattern(0, new_PE(PC_Break_CH, 1, EOP, Str));
}

#ifdef CHARSET_PUBLIC
struct pat *
spipat_break_csp(CSP csp) {
    return new_Pattern(0, new_PE(PC_Break_CSP, 1, EOP, csp));
}
#endif

struct pat *
spipat_break_ptr(VString *Str) {
    return new_Pattern(0, new_PE(PC_Break_VP, 1, EOP, Str));
}

struct pat *
spipat_break_fnc(VString (*Func)(void *, void *), void *Cookie) {
    return new_Pattern(0, new_PE(PC_Break_VF, 1, EOP, Func, Cookie));
}

////////////
// BreakX //
////////////

struct pat *
spipat_breakx_str(VString Str) {
    return BreakX_Make(new_PE(PC_BreakX_CSP, 3, N, To_Set (Str)));
}

struct pat *
spipat_breakx_chr(Character Chr) {
   return BreakX_Make(new_PE(PC_BreakX_CH, 3, N, Chr));
}

#ifdef CHARSET_PUBLIC
struct pat *
spipat_breakx_csp(CSP csp) {
    return BreakX_Make(new_PE(PC_BreakX_CSP, 3, N, csp));
}
#endif

struct pat *
spipat_breakx_ptr(VString *Str) {
    return BreakX_Make(new_PE(PC_BreakX_VP, 3, N, Str));
}

struct pat *
spipat_breakx_fnc(VString (*Func)(void *, void *), void *Cookie) {
    return BreakX_Make(new_PE(PC_BreakX_VF, 3, N, Func, Cookie));
}

/////////////////
// BreakX_Make //
/////////////////

//    +---+     +---+
//    | B |---->| A |---->
//    +---+     +---+
//      ^         .
//      |         .
//      |       +---+
//      +<------| X |
//              +---+

//  The B node is numbered 3, the alternative node is 1, and the X
//  node is 2.

static struct pat *
BreakX_Make(PE_Ptr B) {
    PE_Ptr X = new_PE(PC_BreakX_X, 2, B);
    PE_Ptr A = new_PE(PC_Alt,      1, EOP, X);

    B->Pthen = A;
    return new_Pattern(2, B);
}

/////////////////////
// spipat_build_ref_array //
/////////////////////

//  Record given pattern element if not already recorded in RA,
//  and also record any referenced pattern elements recursively.

static void
Record_PE(PE_Ptr E, PE_Ptr *RA) {
    DPrintf("  Record_PE called with PE_Ptr = %p", E);

    if (E == EOP || RA[E->Index-1] != NULL) {
	DPrintf(", nothing to do\n");
	return;
    }
    else {
	DPrintf(", recording %z\n", E->Index-1);
	RA[E->Index-1] = E;
	Record_PE(E->Pthen, RA);

	if (PC_HAS_ALT(E->Pcode))
	    Record_PE(E->val.Alt, RA);
    }
}

void
spipat_build_ref_array(PE_Ptr E, PE_Ptr *RA) {
    DPrintf("Entering spipat_build_ref_array\n");
    for (int i = 0; i < E->Index; i++)
	RA[i] = NULL;
    Record_PE (E, RA);
    DPrintf("\n");
}

/////////////
// C_To_PE //
/////////////

static PE_Ptr
C_To_PE (Character C) {
    return new_PE(PC_Char, 1, EOP, C);
}

////////////
// Concat //
////////////

//  Concat needs to traverse the left operand performing the following
//  set of fixups:

//    a) Any successor pointers (Pthen fields) that are set to EOP are
//       reset to point to the second operand.

//    b) Any PC_Arbno_Y node has its stack count field incremented
//       by the parameter Incr provided for this purpose.

//    d) Num fields of all pattern elements in the left operand are
//       adjusted to include the elements of the right operand.

//  Note: we do not use Set_Successor in the processing for Concat, since
//  there is no point in doing two traversals, we may as well do everything
//  at the same time.

static PE_Ptr
Concat(PE_Ptr L, PE_Ptr R, size_t Incr) {
    if (L == EOP)
	return R;

    if (R == EOP)
	return L;

    //  We build a reference array for L whose N'th element points to
    //  the pattern element of L whose original Index value is N.
    int n = L->Index;
    DYNAMIC(PE_Ptr, Refs, n);

    spipat_build_ref_array(L, Refs);

    for (int j = 0; j < n; j++) {
	PE_Ptr P = Refs[j];

	P->Index += R->Index;

	if (P->Pcode == PC_Arbno_Y)
	    P->val.Nat += Incr;

	if (P->Pthen == EOP)
	    P->Pthen = R;

	if (PC_HAS_ALT(P->Pcode) && P->val.Alt == EOP)
	   P->val.Alt = R;
    } // for
    return L;
}

//////////
// Copy //
//////////

static PE_Ptr
Copy(PE_Ptr P) {
    if (P == NULL) {
	Uninitialized_Pattern();
	return NULL;
    }
    else {
	PE_Ptr E;
	DYNAMIC(PE_Ptr, Refs, P->Index);
	//  References to elements in P, indexed by Index field

#ifdef _MSC_VER
	PE_Ptr *Copies = (PE_Ptr *)_alloca(sizeof(PE_Ptr) * P->Index);
#else
	PE_Ptr Copies[P->Index];
#endif
	//  Holds copies of elements of P, indexed by Index field

	spipat_build_ref_array(P, Refs);

	//  Now copy all nodes
	for (int j = 0; j < P->Index; j++)
	    Copies[j] = copy_PE(Refs[j]);

	//  Adjust all internal references

	for (int j = 0; j < P->Index; j++) {
	    E = Copies[j];

	    //  Adjust successor pointer to point to copy

	    if (E->Pthen != EOP)
		E->Pthen = Copies[E->Pthen->Index-1];

	    //  Adjust Alt pointer if there is one to point to copy

	    if (PC_HAS_ALT(E->Pcode) && E->val.Alt != EOP)
		E->val.Alt = Copies[E->val.Alt->Index-1];

	    //  Copy referenced string

	    if (E->Pcode == PC_String)
		E->val.Str = copy_String(E->val.Str);
	} // for j
	return Copies[P->Index-1];
    } // else
} // Copy

//////////
// Fail //
//////////

struct pat *
spipat_fail(void) {
    return new_Pattern(0, new_PE(PC_Fail, 1, EOP));
}

///////////
// Fence //
///////////

//  Simple case

struct pat *
spipat_fence_simple(void) {
    return new_Pattern(1, new_PE(PC_Fence, 1, EOP));
}

//  Function case

//    +---+     +---+     +---+
//    | E |---->| P |---->| X |---->
//    +---+     +---+     +---+

//  The node numbering of the constituent pattern P is not affected.
//  Where N is the number of nodes in P, the X node is numbered N + 1,
//  and the E node is N + 2.

struct pat *
spipat_fence_function(struct pat *P) {
    PE_Ptr Pat     = Copy(P->P);
    PE_Ptr E       = new_PE(PC_R_Enter, 0, EOP);
    PE_Ptr X       = new_PE(PC_Fence_X, 0, EOP);
    return new_Pattern(P->Stk + 1, Bracket(E, Pat, X));
}

//////////////
// Finalize //
//////////////

void
spipat_hold(struct pat *Object) {
    Object->Refs++;
}

void
spipat_free(struct pat *Object) {
    //  Nothing to do if already freed
    if (Object->P == NULL)
	return;

    // Still referenced?
    if (Object->Refs > 0) {
	if (--Object->Refs > 0)
	    return;
    }

    //  Otherwise we must free all elements
    int n = Object->P->Index;
    DYNAMIC(PE_Ptr, Refs, n);

    //  References to elements in pattern to be finalized
    spipat_build_ref_array(Object->P, Refs);

    for (int j = 0; j < n; j++) {
	switch (Refs[j]->Pcode) {
	case PC_String:
	    free((char *)Refs[j]->val.Str.ptr);
	    break;
	case PC_Pred_Func:
	    spipat_free_cookie(Refs[j]->val.BF.cookie);
	    break;
	case PC_Call_Imm:
	case PC_Call_OnM:
	    spipat_free_cookie(Refs[j]->val.MF.cookie);
	    break;
	case PC_Pos_NF:
	case PC_Len_NF:
	case PC_RPos_NF:
	case PC_RTab_NF:
	    spipat_free_cookie(Refs[j]->val.NF.cookie);
	    break;
	case PC_Any_VF:
	case PC_Break_VF:
	case PC_BreakX_VF:
	case PC_NotAny_VF:
	case PC_NSpan_VF:
	case PC_Span_VF:
	case PC_String_VF:
	    spipat_free_cookie(Refs[j]->val.VF.cookie);
	    break;
	case PC_Dynamic_Func:
	    spipat_free_cookie(Refs[j]->val.DF.cookie);
	    break;
	case PC_Any_CSP:
	case PC_Break_CSP:
	case PC_BreakX_CSP:
	case PC_NotAny_CSP:
	case PC_NSpan_CSP:
	case PC_Span_CSP:
	    Free_Set(Refs[j]->val.CSP);
	    break;
	default:
	    break;
	}
	free(Refs[j]);
    }
    Object->P = NULL;

    free(Object);
}

/////////
// Len //
/////////

struct pat *
spipat_len(size_t Count) {
    //  Note, the following is not just an optimization, it is needed
    //  to ensure that Arbno (Len (0)) does not generate an infinite
    //  matching loop (since PC_Len_Nat is OK_For_Simple_Arbno).

    if (Count == 0)
	return new_Pattern(0, new_PE(PC_Null, 1, EOP));
    else
	return new_Pattern(0, new_PE(PC_Len_Nat, 1, EOP, Count));
}

struct pat *
spipat_len_fnc(size_t (*Count)(void *, void *), void *Cookie) {
    return new_Pattern(0, new_PE(PC_Len_NF, 1, EOP, Count, Cookie));
}

struct pat *
spipat_len_ptr(const size_t *Count) {
    return new_Pattern(0, new_PE(PC_Len_NP, 1, EOP, Count));
}

/////////////////
// Logic_Error //
/////////////////

static void __dead
Logic_Error(void) {
    spipat_exception("Internal logic error in spitbol patterns");
}


////////////
// new_PE //
////////////

static PE_Ptr
new_PE(enum Pattern_Code Code, IndexT Index, PE_Ptr Then, ...) {
    PE_Ptr Node = spipat_malloc(sizeof(struct pe));
    va_list ap;

    if (!Node)
	spipat_exception("new_PE spipat_malloc failed");
    Node->Pcode = Code;
    Node->Index = Index;
    Node->Pthen = Then;
    va_start(ap, Then);
    switch (Code) {
    case PC_Arb_Y:
    case PC_Assign:
    case PC_Bal:
    case PC_BreakX_X:
    case PC_Abort:
    case PC_EOP:
    case PC_Fail:
    case PC_Fence:
    case PC_Fence_X:
    case PC_Fence_Y:
    case PC_Null:
    case PC_R_Enter:
    case PC_R_Remove:
    case PC_R_Restore:
    case PC_Rem:
    case PC_Succeed:
    case PC_Unanchored:
	break;

    case PC_Alt:
    case PC_Arb_X:
    case PC_Arbno_S:
    case PC_Arbno_X:
	Node->val.Alt = va_arg(ap, PE_Ptr);
	break;

    case PC_Rpat:
	Node->val.PP = va_arg(ap, struct pat **);
	break;

    case PC_Pred_Func:
#ifdef _MSC_VER
	Node->val.BF.func = va_arg(ap, BF_func_t);
#else
	Node->val.BF.func = va_arg(ap, bool (*)(void *, void *));
#endif
	Node->val.BF.cookie = va_arg(ap, void *);
	break;

    case PC_Assign_Imm:
    case PC_Assign_OnM:
    case PC_Any_VP:
    case PC_Break_VP:
    case PC_BreakX_VP:
    case PC_NotAny_VP:
    case PC_NSpan_VP:
    case PC_Span_VP:
    case PC_String_VP:
	Node->val.VP = va_arg(ap, VString *);
	break;

    case PC_Call_Imm:
    case PC_Call_OnM:
#ifdef _MSC_VER
	Node->val.MF.func = va_arg(ap, MF_func_t);
#else
	Node->val.MF.func = va_arg(ap, void (*)(VString, void *, void *));
#endif
	Node->val.MF.cookie = va_arg(ap, void *);
	break;

    case PC_String:
	Node->val.Str = va_arg(ap, VString);
	break;

#define COPY_STRING(N) memcpy(Node->val.N, va_arg(ap, Character *), sizeof(Node->val.N))

    case PC_String_2:
	COPY_STRING(Str2);
	break;

    case PC_String_3:
	COPY_STRING(Str3);
	break;

    case PC_String_4:
	COPY_STRING(Str4);
	break;

    case PC_String_5:
	COPY_STRING(Str5);
	break;

    case PC_String_6:
	COPY_STRING(Str6);
	break;
#undef COPY_STRING

    case PC_Setcur:
	Node->val.Var = va_arg(ap, size_t *);
	break;

    case PC_Setcur_Func:
#ifdef _MSC_VER
	Node->val.CF.func = va_arg(ap, CF_func_t);
#else
	Node->val.CF.func = va_arg(ap, void (*)(size_t, void *, void *));
#endif
	Node->val.CF.cookie = va_arg(ap, void *);
	break;

    case PC_Any_CH:
    case PC_Break_CH:
    case PC_BreakX_CH:
    case PC_Char:
    case PC_NotAny_CH:
    case PC_NSpan_CH:
    case PC_Span_CH:
	Node->val.Char = va_arg(ap, int); /* char promoted to int */
	break;

    case PC_Any_CSP:
    case PC_Break_CSP:
    case PC_BreakX_CSP:
    case PC_NotAny_CSP:
    case PC_NSpan_CSP:
    case PC_Span_CSP:
	Node->val.CSP = va_arg(ap, Character_Set *);
	break;

    case PC_Arbno_Y:
    case PC_Len_Nat:
    case PC_Pos_Nat:
    case PC_RPos_Nat:
    case PC_RTab_Nat:
    case PC_Tab_Nat:
	Node->val.Nat = va_arg(ap, size_t);
	break;

    case PC_Pos_NF:
    case PC_Len_NF:
    case PC_RPos_NF:
    case PC_RTab_NF:
#ifdef _MSC_VER
	Node->val.NF.func = va_arg(ap, NF_func_t);
#else
	Node->val.NF.func = va_arg(ap, size_t (*)(void *, void *));
#endif
	Node->val.NF.cookie = va_arg(ap, void *);
	break;

    case PC_Pos_NP:
    case PC_Len_NP:
    case PC_RPos_NP:
    case PC_RTab_NP:
    case PC_Tab_NP:
	Node->val.NP = va_arg(ap, const size_t *);
	break;

    case PC_Any_VF:
    case PC_Break_VF:
    case PC_BreakX_VF:
    case PC_NotAny_VF:
    case PC_NSpan_VF:
    case PC_Span_VF:
    case PC_String_VF:
#ifdef _MSC_VER
	Node->val.VF.func = va_arg(ap, VF_func_t);
#else
	Node->val.VF.func = va_arg(ap, VString (*)(void *, void *));
#endif
	Node->val.VF.cookie = va_arg(ap, void *);
	break;

    case PC_Dynamic_Func:
#ifdef _MSC_VER
	Node->val.DF.func = va_arg(ap, DF_func_t);
#else
	Node->val.DF.func = va_arg(ap,
				   void (*)(void *, void *, struct dynamic *));
#endif
	Node->val.DF.cookie = va_arg(ap, void *);
	break;

    default:
	Logic_Error();
    }
    va_end(ap);
    return Node;
}

////////////
// NotAny //
////////////

struct pat *
spipat_notany_str(VString Str) {
    return new_Pattern(0, new_PE(PC_NotAny_CSP, 1, EOP, To_Set (Str)));
}

struct pat *
spipat_notany_chr(Character c) {
    return new_Pattern(0, new_PE(PC_NotAny_CH, 1, EOP, c));
}

#ifdef CHARSET_PUBLIC
struct pat *
spipat_notany_csp(CSP csp) {
    return new_Pattern(0, new_PE(PC_NotAny_CSP, 1, EOP, csp));
}
#endif

struct pat *
spipat_notany_ptr(VString *Str) {
    return new_Pattern(0, new_PE(PC_NotAny_VP, 1, EOP, Str));
}

struct pat *
spipat_notany_fnc(VString (*Func)(void *, void *), void *Cookie) {
    return new_Pattern(0, new_PE(PC_NotAny_VF, 1, EOP, Func, Cookie));
}

///////////
// NSpan //
///////////

struct pat *
spipat_nspan_str(VString Str) {
    return new_Pattern(0, new_PE(PC_NSpan_CSP, 1, EOP, To_Set (Str)));
}

struct pat *
spipat_nspan_chr(Character Chr) {
    return new_Pattern(0, new_PE(PC_NSpan_CH, 1, EOP, Chr));
}

#ifdef CHARSET_PUBLIC
struct pat *
spipat_nspan_csp(CSP csp) {
    return new_Pattern(0, new_PE(PC_NSpan_CSP, 1, EOP, csp));
}
#endif

struct pat *
spipat_nspan_ptr(VString *Str) {
    return new_Pattern(0, new_PE(PC_NSpan_VP, 1, EOP, Str));
}

struct pat *
spipat_nspan_fnc(VString (*Func)(void *, void *), void *Cookie) {
    return new_Pattern(0, new_PE(PC_NSpan_VF, 1, EOP, Func, Cookie));
}

/////////
// Pos //
/////////

struct pat *
spipat_pos(size_t Count) {
    return new_Pattern(0, new_PE(PC_Pos_Nat, 1, EOP, Count));
}

struct pat *
spipat_pos_fnc(size_t (*Func)(void *, void *), void *Cookie) {
    return new_Pattern(0, new_PE(PC_Pos_NF, 1, EOP, Func, Cookie));
}

struct pat *
spipat_pos_ptr(const size_t *Ptr) {
    return new_Pattern(0, new_PE(PC_Pos_NP, 1, EOP, Ptr));
}

#if 0
/////////////
// Replace //
/////////////

procedure Replace
  (Result  : in out Match_Result;
   Replace : VString)
   S : String_Access;
   L : Natural;
{
   Get_String (Replace, S, L);

   if (Result.Var != null) {
      Replace_Slice (Result.Var, Result.Start, Result.Stop, S (1 .. L));
      Result.Var = null;
   }
}
#endif

//////////
// Rest //
//////////

struct pat *
spipat_rem(void) {
    return new_Pattern(0, new_PE(PC_Rem, 1, EOP));
}

//////////
// Rpos //
//////////

struct pat *
spipat_rpos(size_t Count) {
    return new_Pattern(0, new_PE(PC_RPos_Nat, 1, EOP, Count));
}

struct pat *
spipat_rpos_fnc(size_t (*Func)(void *, void *), void *Cookie) {
    return new_Pattern(0, new_PE(PC_RPos_NF, 1, EOP, Func, Cookie));
}

struct pat *
spipat_rpos_ptr(const size_t *Ptr) {
    return new_Pattern(0, new_PE(PC_RPos_NP, 1, EOP, Ptr));
}

//////////
// Rtab //
//////////

struct pat *
spipat_rtab(size_t Count) {
    return new_Pattern(0, new_PE(PC_RTab_Nat, 1, EOP, Count));
}

struct pat *
spipat_rtab_fnc(size_t (*Func)(void *, void *), void *Cookie) {
    return new_Pattern(0, new_PE(PC_RTab_NF, 1, EOP, Func, Cookie));
}

struct pat *
spipat_rtab_ptr(const size_t *Ptr) {
    return new_Pattern(0, new_PE(PC_RTab_NP, 1, EOP, Ptr));
}

/////////////
// S_To_PE //
/////////////

static PE_Ptr
S_To_PE(VString Str) {
    switch (Str.len) {
    case 0:
	return new_PE(PC_Null,     1, EOP);

    case 1:
	return new_PE(PC_Char,     1, EOP, Str.ptr[0]);

    case 2:
	return new_PE(PC_String_2, 1, EOP, Str.ptr);

    case 3:
	return new_PE(PC_String_3, 1, EOP, Str.ptr);

    case 4:
	return new_PE(PC_String_4, 1, EOP, Str.ptr);

    case 5:
	return new_PE(PC_String_5, 1, EOP, Str.ptr);

    case 6:
	return new_PE(PC_String_6, 1, EOP, Str.ptr);

    default:
	return new_PE(PC_String, 1, EOP, copy_String(Str));
   }
}

///////////////////
// Set_Successor //
///////////////////

//  Note: this procedure is not used by the normal concatenation circuit,
//  since other fixups are required on the left operand in this case, and
//  they might as well be done all together.

static void
Set_Successor(PE_Ptr Pat, PE_Ptr Succ) {
    if (Pat == NULL)
	Uninitialized_Pattern();
    else if (Pat == EOP)
	Logic_Error();
    else {
	DYNAMIC(PE_Ptr, Refs, Pat->Index);
	//  We build a reference array for L whose N'th element points to
	//  the pattern element of L whose original Index value is N.

	spipat_build_ref_array(Pat, Refs);

	for (int j = 0; j < Pat->Index; j++) {
	    PE_Ptr P = Refs[j];
	    if (P->Pthen == EOP)
		P->Pthen = Succ;

	    if (PC_HAS_ALT(P->Pcode) && P->val.Alt == EOP)
		P->val.Alt = Succ;
	}
    }
}

////////////
// Setcur //
////////////

struct pat *
spipat_setcur(size_t *Var) {
    return new_Pattern(0, new_PE(PC_Setcur, 1, EOP, Var));
}

struct pat *
spipat_setcur_fnc(void (*func)(size_t, void *, void *), void *cookie) {
    return new_Pattern(0, new_PE(PC_Setcur_Func, 1, EOP, func, cookie));
}

//////////
// Span //
//////////

struct pat *
spipat_span_str(VString Str) {
    return new_Pattern(0, new_PE(PC_Span_CSP, 1, EOP, To_Set (Str)));
}

struct pat *
spipat_span_chr(Character Chr) {
    return new_Pattern(0, new_PE(PC_Span_CH, 1, EOP, Chr));
}

#ifdef CHARSET_PUBLIC
struct pat *
spipat_span_csp(CSP csp) {
    return new_Pattern(0, new_PE(PC_Span_CSP, 1, EOP, csp));
}
#endif

struct pat *
spipat_span_ptr(VString *Ptr) {
    return new_Pattern(0, new_PE(PC_Span_VP, 1, EOP, Ptr));
}

struct pat *
spipat_span_fnc(VString (*Func)(void *, void *), void *Cookie) {
    return new_Pattern(0, new_PE(PC_Span_VF, 1, EOP, Func, Cookie));
}

/////////////
// Succeed //
/////////////

struct pat *
spipat_succeed(void) {
    return new_Pattern(1, new_PE(PC_Succeed, 1, EOP));
}

/////////
// Tab //
/////////

struct pat *
spipat_tab(size_t Count) {
    return new_Pattern(0, new_PE(PC_Tab_Nat, 1, EOP, Count));
}

struct pat *
spipat_tab_fnc(size_t (*Func)(void *, void *), void *Cookie) {
    return new_Pattern(0, new_PE(PC_Tab_NF, 1, EOP, Func, Cookie));
}

struct pat *
spipat_tab_ptr(const size_t *Ptr) {
    return new_Pattern(0, new_PE(PC_Tab_NP, 1, EOP, Ptr));
}

///////////////////////////
// Uninitialized_Pattern //
///////////////////////////

static void __dead
Uninitialized_Pattern(void) {
    spipat_exception("Uninitialized_Pattern");
}

/////////////
// XMatchD //
/////////////

struct dynamic_object {
    struct dynamic_object *next;
    void (*release)(void *obj);
    void *obj;
};

static int
save_dynamic_object(struct dynamic_object **list,
		    void (*release)(void *obj), void *obj) {
    struct dynamic_object *dop;
    dop = (struct dynamic_object *)
	spipat_malloc(sizeof(struct dynamic_object));
    if (!dop)
	return 0;

    dop->release = release;
    dop->obj = obj;
    dop->next = *list;
    *list = dop;
    return 1;
}

static void
free_dynamic_objects(struct dynamic_object *dop) {
    while (dop) {
	struct dynamic_object *next = dop->next;
	//printf("releasing %p\n", dop->obj);
	(dop->release)(dop->obj);
	free(dop);
	dop = next;
    }
}

    ////////////////
    // Pop_Region //
    ////////////////

#define Pop_Region \
{ \
  Region_Level--; \
  if (Stack_Ptr == Stack_Base) { \
     Stack_Ptr -= 2; \
     /* XXX check Stack_Ptr? */ \
     Stack_Base = Stack (Stack_Ptr + 2).Cursor; \
  } else { \
     Stack_Ptr++; \
     /* XXX check Stack_Ptr? */ \
     Stack (Stack_Ptr).Cursor = Stack_Base; \
     Stack (Stack_Ptr).Node   = (PE_Ptr)&CP_R_Restore; \
     Stack_Base = Stack (Stack_Base).Cursor; \
  } \
}

#define Push(NODE) \
{ \
  Stack_Ptr++; \
  /* XXX check Stack_Ptr? */ \
  Stack (Stack_Ptr).Cursor = Cursor; \
  Stack (Stack_Ptr).Node   = NODE; \
}

#define Push_Region \
{ \
  Region_Level++; \
  Stack_Ptr += 2; \
  /* XXX check Stack_Ptr? */ \
  Stack (Stack_Ptr).Cursor = Stack_Base; \
  Stack (Stack_Ptr).Node   = (PE_Ptr)&CP_R_Remove; \
  Stack_Base = Stack_Ptr; \
}

#define Pattern_Stack_Overflow() spipat_exception("Pattern Stack Overflow")

// hide the fact that subject indexing is one-based, C arrays are zero based
#define Subject(X) _Subject.ptr[(X)-1]

#define VSTR_MATCH(S) \
	(memcmp(&Subject(Cursor+1), S.ptr, S.len*sizeof(Character)) == 0)

// C99 Compound literal... could be a function
#define Slice(STR,START,STOP) \
    (VString) { (STR).ptr + (START) - 1, (STOP)-(START)+1, NULL, NULL }

#define VSTR_RELEASE(VS) if (VS.release) (VS.release)(VS.cookie); else (void)0

#undef spipat_exception
#define spipat_exception(STR) \
    do { mp->exception = STR; return SPIPAT_MATCH_EXCEPTION; } while (0)

// non-debug version of Match engine
#define XMatchD XMatch
#define IPrintf(...)
#define Printf(...)
#define Match_Trace(PE, SUBJ, CURS)
#include "xmatch.h"

// debug version of Match engine
#undef XMatchD
#undef IPrintf
#undef Printf

#define IPrintf(...) do { Indent(Region_Level); spipat_printf(__VA_ARGS__); } while(0)
#define Printf(...) spipat_printf(__VA_ARGS__)

static void
Indent(int i) {
    while (i-- >= 1)
	spipat_printf("| ");
}

#undef Match_Trace
#undef spipat_exception

#if CHARSIZE == 32
#define spipat_exception spipat32_exception // UGH!
#endif

// only output if SPIPAT_TRACE flag is set??
static void
Match_Trace(PE_Ptr n, VString subj, int cursor) {
    if (cursor < 0)
	return;

    putchar('\n');			/* blank line */
    (void) n;				/* display node addr, type, data?? */
    spipat_printf("%S\n", subj);
    // display caret under cursor location
    // (won't work for backspace or zero-width glyphs!)
    // alternative (for wide patterns) could be inserting /\ or <*> within
    // (might still suck for "combining characters"!!!)
    for (int i = 0; i < cursor; i++) {
	if (subj.ptr[i] == '\t')
	    putchar('\t');
	else
	    putchar(' ');
    }
    putchar('^');
    putchar('\n');
}


#include "xmatch.h"

enum spipat_match_ret
spipat_match2(struct spipat_match *mp) {
    if (mp->flags & SPIPAT_DEBUG)
	return XMatchD(mp);
    else
	return XMatch(mp);
}
