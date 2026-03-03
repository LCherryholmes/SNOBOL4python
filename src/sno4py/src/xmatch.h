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

// $Id: xmatch.h,v 1.31 2021-07-31 01:47:29 phil Exp $

// this file included twice; once for XMatchD and once for XMatch

static enum spipat_match_ret
XMatchD(struct spipat_match *mp) {
    //  Pointer to current pattern node.
    //  updated as the match proceeds through its constituent elements.
    PE_Ptr Node;

    VString _Subject = mp->subject;

    //  Length of string
    size_t Length = _Subject.len;

    //  If the value is non-negative, then this value is the index showing
    //  the current position of the match in the subject string. The next
    //  character to be matched is at Subject(Cursor + 1). Note that since
    //  our view of the subject string in XMatch always has a lower bound
    //  of one, regardless of original bounds, that this definition exactly
    //  corresponds to the cursor value as referenced by functions like Pos.
    //
    //  If (the value is negative, then this is a saved stack pointer,
    //  typically a base pointer of an inner or outer region. Cursor
    //  temporarily holds such a value when it is popped from the stack
    //  by Fail. In all cases, Cursor is reset to a proper non-negative
    //  cursor value before the match proceeds (e.g. by propagating the
    //  failure and popping a "real" cursor value from the stack.
    int Cursor;

    //  Dummy pattern element used in the unanchored case
    struct pe PE_Unanchored = {PC_Unanchored, 0, mp->pattern->P, {0}};

    //  Keeps track of recursive region level. This is used only for
    //  debugging, it is the number of saved history stack base values.
    unsigned Region_Level = 0;

    //  The pattern matching failure stack for this call to Match.
    //  Heap-allocated so the stack can be large without blowing the C stack.
    size_t _stack_size = (size_t)spipat_stack_size;
    struct Stack_Entry *_Stack = (struct Stack_Entry *)malloc(_stack_size * sizeof(struct Stack_Entry));
    if (!_Stack) {
        spipat_exception("spipat: failed to allocate match stack");
        return SPIPAT_MATCH_EXCEPTION;
    }

    // Hide the fact that stack is indexed -_stack_size .. -1
#define Stack(I) _Stack[_stack_size+(I)]

    //  Current stack pointer. This points to the top element of the stack
    //  that is currently in use. At the outer level this is the special
    //  entry placed on the stack according to the anchor mode.
    int Stack_Ptr;

#define Stack_First (-(int)_stack_size)
    //  This is the initial value of the Stack_Ptr and Stack_Base. The
    //  initial (Stack_First) element of the stack is not used so that
    //  when we pop the last element off, Stack_Ptr is still in range.
#define Stack_Init (Stack_First + 1)

#define Stack_Last -1

    //  This value is the stack base value, i.e. the stack pointer for the
    //  first history stack entry in the current stack region. See separate
    //  section on handling of recursive pattern matches.
    int Stack_Base;

    //  Set true if (assign-on-match or call-on-match operations may be
    //  present in the history stack, which must then be scanned on a
    //  successful match.
    bool Assign_OnM = false;

    struct dynamic_object *dynamic_list = NULL;

    //  Start of processing for XMatchD

    Printf("\n");
    Printf("Initiating pattern match\n");
    Printf("subject = \"%S\"\n", _Subject);
    Printf("length = %d\n", Length);

    if (mp->pattern->P == NULL) {
	Uninitialized_Pattern();
	goto Match_Fail;
    }

    //  In anchored mode, the bottom entry on the stack is an abort entry
    if (mp->flags & SPIPAT_ANCHORED) {
	Stack (Stack_Init).Node   = (PE_Ptr)&CP_Abort;
	Stack (Stack_Init).Cursor = 0;
    }
    else {
	//  In unanchored more, the bottom entry on the stack references
	//  the special pattern element PE_Unanchored, whose Pthen field
	//  points to the initial pattern element. The cursor value in this
	//  entry is the number of anchor moves so far.
	Stack (Stack_Init).Node   = &PE_Unanchored;
	Stack (Stack_Init).Cursor = 0;
    }

    Stack_Ptr    = Stack_Init;
    Stack_Base   = Stack_Ptr;
    Cursor       = 0;
    Node         = mp->pattern->P;
    goto Match;

    /////////////////////////////////////////
    // Main Pattern Matching State Control //
    /////////////////////////////////////////

    //  This is a state machine which uses gotos to change state. The
    //  initial state is Match, to initiate the matching of the first
    //  element, so the goto Match above starts the match. In the
    //  following descriptions, we indicate the global values that
    //  are relevant for the state transition.

    //  Come here if entire match fails

 Match_Fail:
    IPrintf("match fails\n");
    mp->start = 0;
    mp->stop  = 0;
    free_dynamic_objects(dynamic_list);
    free(_Stack);
    return SPIPAT_MATCH_FAILURE;

    //  Come here if entire match succeeds
    //    Cursor        current position in subject string
 Match_Succeed:
    IPrintf("match succeeds\n");
    mp->start = Stack (Stack_Init).Cursor + 1;
    mp->stop  = Cursor;
    IPrintf("matched positions %u .. %u\n", mp->start, mp->stop);
    IPrintf("matched substring = \"%S\"\n", Slice(_Subject, mp->start, mp->stop));

    //  Scan history stack for deferred assignments or writes
    if (Assign_OnM) {
	for (int s = Stack_First; s <= Stack_Ptr; s++) {
	    if (Stack (s).Node == (PE_Ptr)&CP_Assign) {
		int Inner_Base = Stack (s + 1).Cursor;
		int Special_Entry = Inner_Base - 1;
		PE_Ptr Node_OnM = Stack (Special_Entry).Node;
		unsigned Start = Stack (Special_Entry).Cursor + 1;
		unsigned Stop = Stack (s).Cursor;
		VString S = Slice(_Subject, Start, Stop);

		switch (Node_OnM->Pcode) {
		case PC_Assign_OnM:
		    *Node_OnM->val.VP = S;
		    IPrintf("%p deferred assignment of \"%S\"\n", Stack(s).Node, S);
		    break;
		case PC_Call_OnM:
		    Node_OnM->val.MF.func(S, mp->match_cookie,
					  Node_OnM->val.MF.cookie);
		    IPrintf("%p deferred call of \"%S\"\n", Stack(s).Node, S);
		    break;
		case PC_NUM_CODES:
		default:
		    Logic_Error();
		} // switch Node_OnM->Pcode
	    } // CP_Assign
	} // for each stack entry
    } // Assign_OnM

    Printf("\n");
    free_dynamic_objects(dynamic_list);
    free(_Stack);
    return SPIPAT_MATCH_SUCCESS;

    //  Come here if (attempt to match current element fails

    //    Stack_Base    current stack base
    //    Stack_Ptr     current stack pointer

 Fail:
    Cursor = Stack (Stack_Ptr).Cursor;
    Node   = Stack (Stack_Ptr).Node;
    Stack_Ptr--;

    if (Cursor >= 0) {
	IPrintf("failure, cursor reset to %u\n", Cursor);
    }
    goto Match;

    //  Come here if (attempt to match current element succeeds

    //    Cursor        current position in subject string
    //    Node          pointer to node successfully matched
    //    Stack_Base    current stack base
    //    Stack_Ptr     current stack pointer

 Succeed:
    IPrintf("success, cursor = %u\n", Cursor);
    Node = Node->Pthen;

    //  Come here to match the next pattern element

    //    Cursor        current position in subject string
    //    Node          pointer to node to be matched
    //    Stack_Base    current stack base
    //    Stack_Ptr     current stack pointer
 Match:

    //////////////////////////////////////////////////
    // Main Pattern Match Element Matching Routines //
    //////////////////////////////////////////////////

    //  Here is the case statement that processes the current node. The
    //  processing for each element does one of five things:

    //    goto Succeed        to move to the successor
    //    goto Match_Succeed  if (the entire match succeeds
    //    goto Match_Fail     if (the entire match fails
    //    goto Fail           to signal failure of current match

    //  Processing is NOT allowed to fall through

    Match_Trace(Node, _Subject, Cursor);

    switch (Node->Pcode) {
    case PC_Abort:			//  Abort
	IPrintf("%p matching Abort\n", Node);
	goto Match_Fail;

    case PC_Alt:			//  Alternation
	IPrintf("%p setting up alternative %p\n", Node, Node->val.Alt);
	Push (Node->val.Alt);
	Node = Node->Pthen;
	goto Match;

    case PC_Any_CH:			//  Any (one character case)
	IPrintf("%p matching Any '%c'\n", Node, Node->val.Char);
	if (Cursor < Length && Subject(Cursor + 1) == Node->val.Char) {
	    Cursor++;
	    goto Succeed;
	}
	goto Fail;

    case PC_Any_CSP:			//  Any (character set case)
	IPrintf("%p matching Any %Z\n", Node, Node->val.CSP);
	if (Cursor < Length && Is_In (Subject(Cursor + 1), Node->val.CSP)) {
	    Cursor++;
	    goto Succeed;
	}
	else
	    goto Fail;

    case PC_Any_VF:			//  Any (string function case)
    {
	VString S = Node->val.VF.func(mp->match_cookie, Node->val.VF.cookie);

	IPrintf("%p matching Any \"%S\"\n", Node, S);
	if (Cursor < Length && Is_In_Str(Subject(Cursor + 1), S)) {
	    VSTR_RELEASE(S);
	    Cursor++;
	    goto Succeed;
	}
	VSTR_RELEASE(S);
	goto Fail;
    }

    case PC_Any_VP:			//  Any (string pointer case)
    {
	VString S = *Node->val.VP;

	IPrintf("%p matching Any \"%S\"\n", Node, S);
	if (Cursor < Length && Is_In_Str(Subject(Cursor + 1), S)) {
	    Cursor++;
	    goto Succeed;
	}
	goto Fail;
      }

    case PC_Arb_X:			//  Arb (initial match)
	IPrintf("%p matching Arb\n", Node);
	Push (Node->val.Alt);
	Node = Node->Pthen;
	goto Match;

    case PC_Arb_Y:			//  Arb (extension)
	IPrintf("%p extending Arb\n", Node);
	if (Cursor < Length) {
	    Cursor++;
	    Push (Node);
	    goto Succeed;
	}
	goto Fail;
      
    case PC_Arbno_S:		 //  Arbno_S (simple Arbno initialize)
	// This is the node that initiates
	// the match of a simple Arbno structure.
	IPrintf("%p setting up Arbno alternative %p\n", Node, Node->val.Alt);
	Push (Node->val.Alt);
	Node = Node->Pthen;
	goto Match;


    case PC_Arbno_X:		       //  Arbno_X (Arbno initialize).
	// This is the node that initiates
	//  the match of a complex Arbno structure.
	IPrintf("%p setting up Arbno alternative %p\n", Node, Node->val.Alt);
	Push (Node->val.Alt);
	Node = Node->Pthen;
	goto Match;


    case PC_Arbno_Y:			//  Arbno_Y (Arbno rematch). 
    //  This is the node that is executed following successful
    //  matching of one instance of a complex Arbno pattern.
    {
	bool Null_Match = (Cursor == Stack (Stack_Base - 1).Cursor);
	IPrintf("%p extending Arbno\n", Node);
	Pop_Region;

	//  If (arbno extension matched null, then immediately fail
	if (Null_Match) {
	    IPrintf("Arbno extension matched null, so fails\n");
	    goto Fail;
	}

	//  Here we must do a stack check to make sure enough stack
	//  is left. This check will happen once for each instance of
	//  the Arbno pattern that is matched. The Nat field of a
	//  PC_Arbno pattern contains the maximum stack entries needed
	//  for the Arbno with one instance and the successor pattern
	if ((int)(Stack_Ptr + Node->val.Nat) >= Stack_Last) {
	    Pattern_Stack_Overflow();
	    goto Match_Fail;		/* XXX Internal_Error */
	}
	goto Succeed;
    }

    case PC_Assign:
	//  Assign. If (this node is executed, it means the assign-on-match
	//  or call-on-match operation will not happen after all, so we
	//  is propagate the failure, removing the PC_Assign node.
	IPrintf("%p deferred assign/call cancelled\n", Node);
	goto Fail;

    case PC_Assign_Imm:
    {
	//  Assign immediate. This node performs the actual assignment
	VString S = Slice(mp->subject, Stack (Stack_Base - 1).Cursor + 1, Cursor);
	IPrintf("%p executing immediate assignment of \"%S\"\n", Node, S);
	*Node->val.VP = S;
	Pop_Region;
	goto Succeed;
    }

    case PC_Assign_OnM:
	//  Assign on match. This node sets up for the eventual assignment
	IPrintf("%p registering deferred assignment\n", Node);
	Stack (Stack_Base - 1).Node = Node;
	Push ((PE_Ptr)&CP_Assign);
	Pop_Region;
	Assign_OnM = true;
	goto Succeed;

    case PC_Bal:			//  Bal
	IPrintf("%p matching or extending Bal\n", Node);
	if (Cursor >= Length || Subject(Cursor + 1) == ')')
	    goto Fail;
	if (Subject(Cursor + 1) == '(') {
	    unsigned Paren_Count = 1;
	    for (;;) {
		Cursor++;

		if (Cursor >= Length)
		    goto Fail;
		else if (Subject(Cursor + 1) == '(')
		    Paren_Count++;
		else if (Subject(Cursor + 1) == ')') {
		    if (--Paren_Count == 0)
			break;
		}
	    }
	}
	Cursor++;
	Push (Node);
	goto Succeed;

    case PC_Break_CH:			//  Break (one character case)
	IPrintf("%p matching Break '%c'\n", Node, Node->val.Char);

	while (Cursor < Length) {
	    if (Subject(Cursor + 1) == Node->val.Char)
		goto Succeed;
	    Cursor++;
	}
	goto Fail;

    case PC_Break_CSP:			//  Break (character set case)
	IPrintf("%p matching Break %Z\n", Node->val.CSP);

	while (Cursor < Length) {
	    if (Is_In(Subject(Cursor + 1), Node->val.CSP))
		goto Succeed;
	    Cursor++;
	}
	goto Fail;

    case PC_Break_VF:		      //  Break (string function case)
    {
	VString S = Node->val.VF.func(mp->match_cookie, Node->val.VF.cookie);

	IPrintf("%p matching Break \"%S\"\n", Node, S);
	while (Cursor < Length) {
	    if (Is_In_Str (Subject(Cursor + 1), S)) {
		VSTR_RELEASE(S);
		goto Succeed;
	    }
	    Cursor++;
	}
	VSTR_RELEASE(S);
	goto Fail;
    }


    case PC_Break_VP:		       //  Break (string pointer case)
    {
	VString S = *Node->val.VP;

	IPrintf("%p matching Break \"%S\"\n", Node, S);
	while (Cursor < Length) {
	    if (Is_In_Str(Subject(Cursor + 1), S))
		goto Succeed;
	    Cursor++;
	}
	goto Fail;
    }

    case PC_BreakX_CH:		       //  BreakX (one character case)
	IPrintf("%p matching BreakX '%c'\n", Node, Node->val.Char);
	while (Cursor < Length) {
	    if (Subject(Cursor + 1) == Node->val.Char)
		goto Succeed;
	    Cursor++;
	}
	goto Fail;

    case PC_BreakX_CSP:		       //  BreakX (character set case)
	IPrintf("%p matching BreakX \"%s\"\n", Node, Node->val.CSP);
	while (Cursor < Length) {
	    if (Is_In (Subject(Cursor + 1), Node->val.CSP))
		goto Succeed;
	    Cursor++;
	}
	goto Fail;

    case PC_BreakX_VF:		     //  BreakX (string function case)
    {
	VString S = Node->val.VF.func(mp->match_cookie, Node->val.VF.cookie);

	IPrintf("%p matching BreakX \"%S\"\n", Node, S);
	while (Cursor < Length) {
	    if (Is_In_Str(Subject(Cursor + 1), S)) {
		VSTR_RELEASE(S);
		goto Succeed;
	    }
	    Cursor++;
	}
	VSTR_RELEASE(S);
	goto Fail;
    }


    case PC_BreakX_VP:		      //  BreakX (string pointer case)
    {
	VString S = *Node->val.VP;

	IPrintf("%p matching BreakX \"%S\"\n", Node, S);
	while (Cursor < Length) {
	    if (Is_In_Str(Subject(Cursor + 1), S))
		goto Succeed;
	    Cursor++;
	}
	goto Fail;
    }

    //  BreakX_X (BreakX extension). See section on "Compound Pattern
    //  Structures". This node is the alternative that is stacked
    //  to skip past the break character and extend the break.
    case PC_BreakX_X:
	IPrintf("%p extending BreakX\n", Node);
	Cursor++;
	goto Succeed;

    case PC_Char:    //  Character (one character string)
	IPrintf("%p matching '%c'\n", Node, Node->val.Char);
	if (Cursor < Length && Subject(Cursor + 1) == Node->val.Char) {
	    Cursor++;
	    goto Succeed;
	}
	goto Fail;

    case PC_EOP:			//  End of Pattern
	if (Stack_Base == Stack_Init) {
	    IPrintf("end of pattern\n");
	    goto Match_Succeed;
	}
	else {
	    //  End of recursive inner match. See separate section on
	    //  handing of recursive pattern matches for details.

	    // XXX release held pattern object here?
	    IPrintf("terminating recursive match\n");
	    Node = Stack (Stack_Base - 1).Node;
	    Pop_Region;
	    goto Match;
	}

    case PC_Fail:			//  Fail
	IPrintf("%p matching Fail\n", Node);
	goto Fail;

    case PC_Fence:			//  Fence (built in pattern)
	IPrintf("%p matching Fence\n", Node);
	Push ((PE_Ptr)&CP_Abort);
	goto Succeed;

    //  Fence function node X. This is the node that gets control
    //  after a successful match of the fenced pattern.
    case PC_Fence_X:
	IPrintf("%p matching Fence function\n", Node);
	Stack_Ptr++;			/* XXX range check */
	Stack (Stack_Ptr).Cursor = Stack_Base;
	Stack (Stack_Ptr).Node   = (PE_Ptr)&CP_Fence_Y;
	Stack_Base = Stack (Stack_Base).Cursor;
	Region_Level--;
	goto Succeed;

    case PC_Fence_Y:
	//  Fence function node Y. This is the node that gets control on
	//  a failure that occurs after the fenced pattern has matched.

	//  Note: the Cursor at this stage is actually the inner stack
	//  base value. We don't reset this, but we do use it to strip
	//  off all the entries made by the fenced pattern.
	IPrintf("%p pattern matched by Fence caused failure\n", Node);
	Stack_Ptr = Cursor - 2;	/* XXX check stack_ptr */
	goto Fail;


    case PC_Len_Nat:			//  Len (integer case)
	IPrintf("%p matching Len %u\n", Node, Node->val.Nat);
	if (Cursor + Node->val.Nat > Length)
	    goto Fail;
	Cursor += Node->val.Nat;
	goto Succeed;

    case PC_Len_NF:		       //  Len (Integer function case)
    {
	unsigned n = Node->val.NF.func(mp->match_cookie, Node->val.NF.cookie);

	IPrintf("%p matching Len %u\n", Node, n);
	if (Cursor + n > Length)
	    goto Fail;
	Cursor += n;
	goto Succeed;
    }

    case PC_Len_NP:			//  Len (integer pointer case)
	IPrintf("%p matching Len %u\n", Node, *Node->val.NP);
	if (Cursor + *Node->val.NP > Length)
	    goto Fail;
	Cursor += *Node->val.NP;
	goto Succeed;

    case PC_NotAny_CH:		       //  NotAny (one character case)
	IPrintf("%p matching NotAny '%c'\n", Node, Node->val.Char);
	if (Cursor <  Length && Subject(Cursor + 1) != Node->val.Char) {
	    Cursor++;
	    goto Succeed;
	}
	goto Fail;

    case PC_NotAny_CSP:		       //  NotAny (character set case)
	IPrintf("%p matching NotAny %Z\n", Node, Node->val.CSP);
	if (Cursor < Length && !Is_In(Subject(Cursor + 1), Node->val.CSP)) {
	    Cursor++;
	    goto Succeed;
	}
	goto Fail;

    case PC_NotAny_VF:		     //  NotAny (string function case)
    {
	VString S = Node->val.VF.func(mp->match_cookie, Node->val.VF.cookie);

	IPrintf("%p matching NotAny \"%S\"\n", Node, S);
	if (Cursor < Length && !Is_In_Str(Subject(Cursor + 1), S)) {
	    Cursor++;
	    VSTR_RELEASE(S);
	    goto Succeed;
	}
	VSTR_RELEASE(S);
	goto Fail;
    }

    case PC_NotAny_VP:		      //  NotAny (string pointer case)
    {
	VString S = *Node->val.VP;

	IPrintf("%p matching NotAny \"%S\"\n", Node, S);
	if (Cursor < Length && !Is_In_Str(Subject(Cursor + 1), S)) {
	    Cursor++;
	    goto Succeed;
	}
	goto Fail;
    }

    case PC_NSpan_CH:			//  NSpan (one character case)
	IPrintf("%p matching NSpan '%c'\n", Node, Node->val.Char);
	while (Cursor < Length && Subject(Cursor + 1) == Node->val.Char)
	    Cursor++;
	goto Succeed;

    case PC_NSpan_CSP:			//  NSpan (character set case)
	IPrintf("%p matching NSpan %Z\n", Node, Node->val.CSP);
	while (Cursor < Length && Is_In (Subject(Cursor + 1), Node->val.CSP))
	    Cursor++;
	goto Succeed;

    case PC_NSpan_VF:      //  NSpan (string function case)
    {
	VString S = Node->val.VF.func(mp->match_cookie, Node->val.VF.cookie);

	IPrintf("%p matching NSpan \"%S\"\n", Node, S);
	while (Cursor < Length && Is_In_Str(Subject(Cursor + 1), S))
	    Cursor++;
	VSTR_RELEASE(S);
	goto Succeed;
    }

    case PC_NSpan_VP:			//  NSpan (string pointer case)
    {
	VString S = *Node->val.VP;

	IPrintf("%p matching NSpan \"%S\"\n", Node, S);
	while (Cursor < Length && Is_In_Str(Subject(Cursor + 1), S))
	    Cursor++;
	goto Succeed;
    }

    case PC_Null:
	IPrintf("%p matching null\n");
	goto Succeed;

    case PC_Pos_Nat:      //  Pos (integer case)
	IPrintf("%p matching Pos %u\n", Node, Node->val.Nat);
	if (Cursor == Node->val.Nat)
	    goto Succeed;
	goto Fail;

    case PC_Pos_NF:      //  Pos (Integer function case)
    {
	unsigned n = Node->val.NF.func(mp->match_cookie, Node->val.NF.cookie);

	IPrintf("%p matching Pos %u\n", Node, n);
	if (Cursor == n)
	    goto Succeed;
	goto Fail;
    }

    case PC_Pos_NP:      //  Pos (integer pointer case)
	IPrintf("%p matching Pos %u\n", Node, *Node->val.NP);
	if (Cursor == *Node->val.NP)
	    goto Succeed;
	goto Fail;

    case PC_Pred_Func:      //  Predicate function
	IPrintf("%p matching predicate function\n", Node);
	if (Node->val.BF.func(mp->match_cookie, Node->val.BF.cookie))
	    goto Succeed;
	goto Fail;

    case PC_R_Enter:
	//  Region Enter. Initiate new pattern history stack region
	IPrintf("%p starting match of nested pattern\n", Node);
	Stack (Stack_Ptr + 1).Cursor = Cursor;
	Push_Region;
	goto Succeed;

    case PC_R_Remove:
	//  Region Remove node. This is the node stacked by an R_Enter.
	//  It removes the special format stack entry right underneath, and
	//  then restores the outer level stack base and signals failure.

	//  Note: the cursor value at this stage is actually the (negative)
	//  stack base value for the outer level.
	IPrintf("%p failure, match of nested pattern terminated\n", Node);
	Stack_Base = Cursor;
	Region_Level--;
	Stack_Ptr--;
	goto Fail;

    case PC_R_Restore:
	//  Region restore node. This is the node stacked at the end of an
	//  inner level match. Its function is to restore the inner level
	//  region, so that alternatives in this region can be sought.

	//  Note: the Cursor at this stage is actually the negative of the
	//  inner stack base value, which we use to restore the inner region.
	IPrintf("%p failure, search for alternatives in nested pattern\n", Node);
	Region_Level++;
	Stack_Base = Cursor;
	goto Fail;

    case PC_Rem:			//  Rem
	IPrintf("%p matching Rem\n", Node);
	Cursor = Length;
	goto Succeed;

    case PC_Rpat:      //  Initiate recursive match (pattern pointer case)
	Stack (Stack_Ptr + 1).Node = Node->Pthen;
	Push_Region;
	IPrintf("%p initiating recursive match\n", Node);

	if ((int)(Stack_Ptr + (*Node->val.PP)->Stk) >= (int)_stack_size) {
	    Pattern_Stack_Overflow();
	    goto Match_Fail;		/* XXX Internal_Error */
	}

	Node = (*Node->val.PP)->P;
	goto Match;

    case PC_RPos_Nat:      //  RPos (integer case)
	IPrintf("%p matching RPos %u\n", Node, Node->val.Nat);
	if (Cursor == (Length - Node->val.Nat))
	    goto Succeed;
	goto Fail;


    case PC_RPos_NF:      //  RPos (integer function case)
    {
	unsigned n = Node->val.NF.func(mp->match_cookie, Node->val.NF.cookie);

	IPrintf("%p matching RPos %u\n", Node, n);
	if (Length - Cursor == n)
	    goto Succeed;
	goto Fail;
    }


    case PC_RPos_NP:      //  RPos (integer pointer case)
	IPrintf("%p matching RPos %u\n", Node, *Node->val.NP);
	if (Cursor == (Length - *Node->val.NP))
	    goto Succeed;
	goto Fail;


    case PC_RTab_Nat:      //  RTab (integer case)
	IPrintf("%p matching RTab %u\n", Node, Node->val.Nat);
	if (Cursor <= (Length - Node->val.Nat)) {
	    Cursor = Length - Node->val.Nat;
	    goto Succeed;
	}
	goto Fail;

    case PC_RTab_NF:      //  RTab (integer function case)
    {
	unsigned n = Node->val.NF.func(mp->match_cookie, Node->val.NF.cookie);

	IPrintf("%p matching RPos %u\n", Node, n);
	if (Length - Cursor >= n) {
	   Cursor = Length - n;
	   goto Succeed;
	}
	goto Fail;
    }

    case PC_RTab_NP:      //  RTab (integer pointer case)
	IPrintf("%p matching RPos\n", Node, *Node->val.NP);
	if (Cursor <= (Length - *Node->val.NP)) {
	    Cursor = Length - *Node->val.NP;
	    goto Succeed;
	}
	goto Fail;

    case PC_Setcur:    //  Cursor assignment
	IPrintf("%p matching Setcur\n", Node);
	*Node->val.Var = Cursor;
	goto Succeed;

    case PC_Setcur_Func:    //  Cursor assignment
	IPrintf("%p matching Setcur_Func\n", Node);
	(Node->val.CF.func)(Cursor, mp->match_cookie, Node->val.CF.cookie);
	goto Succeed;

    case PC_Span_CH:    //  Span (one character case)
    {
	unsigned P = Cursor;

	IPrintf("%p matching Span '%c'\n", Node, Node->val.Char);
	while (P < Length && Subject(P + 1) == Node->val.Char)
	    P++;

	if (P != Cursor) {
	   Cursor = P;
	   goto Succeed;
	}
	goto Fail;
    }

    case PC_Span_CSP:	//  Span (character set case)
    {
	unsigned P = Cursor;

	IPrintf("%p matching Span %Z\n", Node->val.CSP);
	while (P < Length && Is_In (Subject(P + 1), Node->val.CSP))
	   P++;

	if (P != Cursor) {
	   Cursor = P;
	   goto Succeed;
	}
	goto Fail;
    }

    case PC_Span_VF:      //  Span (string function case)
    {
	VString S = Node->val.VF.func(mp->match_cookie, Node->val.VF.cookie);
	unsigned P;

	IPrintf("%p matching Span \"%S\"\n", Node, S);
	P = Cursor;
	while (P < Length && Is_In_Str(Subject(P + 1), S))
	    P++;

	VSTR_RELEASE(S);
	if (P != Cursor) {
	    Cursor = P;
	    goto Succeed;
	 }
	 goto Fail;
    }

    case PC_Span_VP:      //  Span (string pointer case)
    {
	VString S = *Node->val.VP;
	unsigned P;

	IPrintf("%p matching Span \"%S\"\n", Node, S);
	P = Cursor;
	while (P < Length && Is_In_Str(Subject(P + 1), S))
	    P++;

	if (P != Cursor) {
	    Cursor = P;
	    goto Succeed;
	}
	goto Fail;
    }

    case PC_String_2:      //  String (two character case)
	IPrintf("%p matching \"%c%c\"\n", Node,
		Node->val.Str2[0], Node->val.Str2[1]);
	if ((Length - Cursor) >= 2
	   && Subject(Cursor + 1) == Node->val.Str2[0]
	   && Subject(Cursor + 2) == Node->val.Str2[1]) {
	   Cursor += 2;
	   goto Succeed;
	}
	goto Fail;

    case PC_String_3:	      //  String (three character case)
	IPrintf("%p matching \"%c%c%c\"\n", Node,
		Node->val.Str3[0], Node->val.Str3[1], Node->val.Str3[2]);
	if ((Length - Cursor) >= 3
	   && Subject(Cursor + 1) == Node->val.Str3[0]
	   && Subject(Cursor + 2) == Node->val.Str3[1]
	   && Subject(Cursor + 3) == Node->val.Str3[2]) {
	   Cursor += 3;
	   goto Succeed;
	}
	goto Fail;

    case PC_String_4:	      //  String (four character case)
	IPrintf("%p matching \"%c%c%c%c\"\n", Node,
		Node->val.Str4[0], Node->val.Str4[1], Node->val.Str4[2],
		Node->val.Str4[3]);
	if ((Length - Cursor) >= 4
	   && Subject(Cursor + 1) == Node->val.Str4[0]
	   && Subject(Cursor + 2) == Node->val.Str4[1]
	   && Subject(Cursor + 3) == Node->val.Str4[2]
	   && Subject(Cursor + 4) == Node->val.Str4[3]) {
	   Cursor += 4;
	   goto Succeed;
	}
	goto Fail;

    case PC_String_5:	      //  String (five character case)
	IPrintf("%p matching \"%c%c%c%c%c\"\n", Node,
		Node->val.Str5[0], Node->val.Str5[1], Node->val.Str5[2],
		Node->val.Str5[3], Node->val.Str5[4]);
	if ((Length - Cursor) >= 5
	   && Subject(Cursor + 1) == Node->val.Str5[0]
	   && Subject(Cursor + 2) == Node->val.Str5[1]
	   && Subject(Cursor + 3) == Node->val.Str5[2]
	   && Subject(Cursor + 4) == Node->val.Str5[3]
	   && Subject(Cursor + 5) == Node->val.Str5[4]) {
	   Cursor += 5;
	   goto Succeed;
	}
	goto Fail;

    case PC_String_6:	      //  String (six character case)
	IPrintf("%p matching \"%c%c%c%c%c%c\"\n", Node,
		Node->val.Str6[0], Node->val.Str6[1], Node->val.Str6[2],
		Node->val.Str6[3], Node->val.Str6[4], Node->val.Str6[5]);
	if ((Length - Cursor) >= 6
	   && Subject(Cursor + 1) == Node->val.Str6[0]
	   && Subject(Cursor + 2) == Node->val.Str6[1]
	   && Subject(Cursor + 3) == Node->val.Str6[2]
	   && Subject(Cursor + 4) == Node->val.Str6[3]
	   && Subject(Cursor + 5) == Node->val.Str6[4]
	   && Subject(Cursor + 6) == Node->val.Str6[5]) {
	   Cursor += 6;
	   goto Succeed;
	}
	goto Fail;

    case PC_String:	      //  String (case of more than six characters)
	IPrintf("%p matching \"%S\"\n", Node, Node->val.Str);
	if ((Length - Cursor) >= Node->val.Str.len &&
		VSTR_MATCH(Node->val.Str)) {
	    Cursor += Node->val.Str.len;
	    goto Succeed;
	}
	goto Fail;

    case PC_String_VF:	      //  String (function case)
    {
	VString S = Node->val.VF.func(mp->match_cookie, Node->val.VF.cookie);
	unsigned L = S.len;

	IPrintf("%p matching \"%S\"\n", Node, S);
	if ((Length - Cursor) >= L && VSTR_MATCH(S)) {
	    Cursor += L;
	    VSTR_RELEASE(S);
	    goto Succeed;
	}
	VSTR_RELEASE(S);
	goto Fail;
    }

    case PC_String_VP:      //  String (vstring pointer case)
    {
	VString S = *Node->val.VP;
	unsigned L = S.len;

	IPrintf("%p matching \"%S\"\n", Node, S);
	if ((Length - Cursor) >= L && VSTR_MATCH(S)) {
	    Cursor += L;
	    goto Succeed;
	}
	goto Fail;
    }

    case PC_Succeed:			//  Succeed
	IPrintf("%p matching Succeed\n", Node);
	Push (Node);
	goto Succeed;

    case PC_Tab_Nat:			//  Tab (integer case)
	IPrintf("%p matching Tab %u\n", Node, Node->val.Nat);
	if (Cursor <= Node->val.Nat) {
	    Cursor = Node->val.Nat;
	    goto Succeed;
	}
	goto Fail;

    case PC_Tab_NF:			//  Tab (integer function case)
    {
	unsigned n = Node->val.NF.func(mp->match_cookie, Node->val.NF.cookie);

	IPrintf("%p matching Tab %u\n", Node, n);
	if (Cursor <= n) {
	    Cursor = n;
	    goto Succeed;
	}
	goto Fail;
    }

    case PC_Tab_NP:			//  Tab (integer pointer case)
	IPrintf("%p matching Tab %u\n", *Node->val.NP);
	if (Cursor <= *Node->val.NP) {
	    Cursor = *Node->val.NP;
	    goto Succeed;
	}
	goto Fail;

    case PC_Unanchored:			//  Unanchored movement
	IPrintf("attempting to move anchor point\n"); // no node addr
	if (Cursor > Length)
	    goto Match_Fail;   //  All done if we tried every position

	//  Otherwise extend the anchor point, and restack ourself
	Cursor++;
	Push (Node);
	goto Succeed;

    case PC_Call_Imm:
    {
	//  Call immediate. This node performs the call
	VString S = Slice(mp->subject, Stack (Stack_Base - 1).Cursor + 1, Cursor);
	IPrintf("%p executing immediate write of \"%S\"\n", Node, S);
	Node->val.MF.func(S, mp->match_cookie, Node->val.MF.cookie);
	Pop_Region;
	goto Succeed;
    }

    case PC_Call_OnM:
	//  Write on match. This node sets up for the eventual write
	IPrintf("%p registering deferred call\n", Node);
	Stack (Stack_Base - 1).Node = Node;
	Push ((PE_Ptr)&CP_Assign);
	Pop_Region;
	Assign_OnM = true;
	goto Succeed;

    case PC_Dynamic_Func:
        {
	    struct dynamic d;

	    IPrintf("%p calling dynamic function\n", Node);
	    Node->val.DF.func(mp->match_cookie, Node->val.DF.cookie, &d);
	    switch (d.type) {
	    case DY_BOOL:
		if (d.val.pred)
		    goto Succeed;
		goto Fail;
	    case DY_VSTR:
		IPrintf("%p matching \"%S\"\n", Node, d.val.str);
		if ((Length - Cursor) >= d.val.str.len && VSTR_MATCH(d.val.str)) {
		    Cursor += d.val.str.len;
		    VSTR_RELEASE(d.val.str);
		    goto Succeed;
		}
		VSTR_RELEASE(d.val.str);
		goto Fail;

	    case DY_PAT:
		Stack (Stack_Ptr + 1).Node = Node->Pthen;
		Push_Region;
		IPrintf("%p initiating recursive match\n", Node);
		if ((int)(Stack_Ptr + d.val.pat.p->Stk) >= (int)_stack_size) {
		    Pattern_Stack_Overflow();
		    goto Match_Fail;	/* XXX Internal_Error */
		}

		// CROCK: keep list of objects to release when match done
		if (!save_dynamic_object(&dynamic_list,
					 d.val.pat.release,
					 d.val.pat.cookie)) {
		    spipat_exception("save_dynamic_object failed");
		    goto Match_Fail;	/* XXX Internal_Error */
		}
		Node = d.val.pat.p->P;
		goto Match;

	    case DY_UNK:
		goto Fail;
	    default:
		Logic_Error();
		goto Match_Fail;
	    }
	case PC_NUM_CODES:
	    break;			/* fall thru to Logic_Error */
	}
    } // switch (Node->Pcode)

    //  We are NOT allowed to fall though this case statement, since every
    //  match routine must end by executing a goto to the appropriate point
    //  in the finite state machine model.
    Logic_Error();
    goto Match_Fail;			/* XXX Internal_Error? */
}