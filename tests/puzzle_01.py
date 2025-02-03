# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# 1
# In a certain bank the positions of cashier, manager, and teller are held by
# Brown, Jones, and Smith, though not necessarily respectively.  The teller, who
# was an only child, earns the least.  Smith, who married Brown's sister, earns
# more than the manager. What position does each man fill?
from pyDatalog import pyDatalog as pro
# pro.create_terms('factorial, N')
# factorial[N] = N * factorial[N - 1]
# factorial[1] = 1
# print(factorial[3] == N)
pro.create_terms("brown,jones,smith")
pro.create_terms("X,Y,Cashier,Manager,Teller")
pro.create_terms("puzzle,person,differ,display")
pro.create_terms("_,true,false")
+person(brown)
+person(jones)
+person(smith)
+false()
true() <= ~false()
differ(X, X) <= false
differ(_, _) <= true()
differ(X, X, _) <= false()
differ(X, _, X) <= false()
differ(_, X, X) <= false()
differ(_, _, _) <= true()
print(
   person(Cashier) 
 & person(Manager)
 & person(Teller) 
 & differ(Cashier, Manager, Teller)
 & differ(smith, Manager) 
 & differ(Teller, brown) 
 & differ(smith, Teller))

"""
   display(Cashier, Manager, Teller)
   )
#  Smith is the cashier.
#  Brown is the manager.
#  Jones is the teller.

#-------------------------------------------------------------------------------
display(Cashier, Manager, Teller) :-
   write('Cashier='), write(Cashier),
   write(' Manager='), write(Manager),
   write(' Teller='), write(Teller),
   write('\n').
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
"""