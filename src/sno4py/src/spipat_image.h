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

/* $Id: spipat_image.h,v 1.10 2021-07-31 01:47:29 phil Exp $ */

struct state {
    char *ptr;
    size_t len;
    size_t size;

    bool Kill_Concat;
    struct pe **Refs;

    /* formatting: */
    const char *quote;
    const char *cquote;
    const char *concat;
    const char **strings;

    void (*appendc)(struct state *, Character c);
    void (*append)(struct state *, const char *);
    void (*vstr)(struct state *, struct pe *);
    void (*fnoargs)(struct state *, struct pe *);
    void (*cs)(struct state *, struct pe *);
    void (*fcs)(struct state *, struct pe *);
    void (*vf)(struct state *, struct pe *);
    void (*fvf)(struct state *, struct pe *);
    void (*vp)(struct state *, struct pe *);
    void (*fvp)(struct state *, struct pe *);
    void (*assign)(struct state *, struct pe *);
    void (*ch)(struct state *, struct pe *);
    void (*fch)(struct state *, struct pe *);
    void (*nat)(struct state *, struct pe *);
    void (*fnat)(struct state *, struct pe *);
    void (*np)(struct state *, struct pe *);
    void (*fnp)(struct state *, struct pe *);
    void (*nf)(struct state *, struct pe *);
    void (*fnf)(struct state *, struct pe *);
    void (*pp)(struct state *, struct pe *);
    void (*fpp)(struct state *, struct pe *);
    void (*bf)(struct state *, struct pe *);
    void (*fbf)(struct state *, struct pe *);
    void (*cf)(struct state *, struct pe *);
    void (*fcf)(struct state *, struct pe *);
    void (*df)(struct state *, struct pe *);
    void (*fdf)(struct state *, struct pe *);
};

extern const char *image_strs[];

void spipat_image_seq(struct state *sp,
		      struct pe *E, struct pe *Succ, bool Paren);
void spipat_image_init_state(struct state *sp);
size_t spipat_image_custom(struct state *sp, struct pat *P);
