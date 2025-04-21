#------------------------------------------------------------------------------
cdef void report(s=""): pass # print(s) #
#-----------------------------------------------------------------------------------
# ICON Programming Language: (1st pass, attribute grammar generated)
#
#                       every write(5 > ((1 to 2) * (3 to 4)));
#-----------------------------------------------------------------------------------
cdef int x1_V
cdef int x2_V
cdef int x3_V
cdef int x4_V
cdef int x5_V
cdef int to1_I
cdef int to1_V
cdef int to2_I
cdef int to2_V
cdef int mult_V
cdef int greater_V
cdef int write_V
#-----------------------------------------------------------------------------------
cdef void * x5_start():         global x5_V;           x5_V = 5;            return <void *> x5_succeed
cdef void * x5_resume():                                                    return <void *> x5_fail
#-----------------------------------------------------------------------------------
cdef void * x1_start():         global x1_V;           x1_V = 1;            return <void *> x1_succeed
cdef void * x1_resume():                                                    return <void *> x1_fail
#-----------------------------------------------------------------------------------
cdef void * x2_start():         global x2_V;           x2_V = 2;            return <void *> x2_succeed
cdef void * x2_resume():                                                    return <void *> x2_fail
#-----------------------------------------------------------------------------------
cdef void * to1_start():                                                    return <void *> x1_start
cdef void * x1_fail():                                                      return <void *> to1_fail
cdef void * x2_fail():                                                      return <void *> x1_resume
cdef void * to1_code():
                                global to1_I, x2_V, to1_V
                                if to1_I > x2_V:                            return <void *> x2_resume
                                else: to1_V = to1_I;                        return <void *> to1_succeed
cdef void * to1_resume():       global to1_I;           to1_I = to1_I + 1;  return <void *> to1_code
cdef void * x1_succeed():                                                   return <void *> x2_start
cdef void * x2_succeed():       global to1_I, x1_V;     to1_I = x1_V;       return <void *> to1_code
#-----------------------------------------------------------------------------------
cdef void * x3_start():         global x3_V;            x3_V = 3;           return <void *> x3_succeed
cdef void * x3_resume():                                                    return <void *> x3_fail
#-----------------------------------------------------------------------------------
cdef void * x4_start():         global x4_V;            x4_V = 4;           return <void *> x4_succeed
cdef void * x4_resume():                                                    return <void *> x4_fail
#-----------------------------------------------------------------------------------
cdef void * to2_start():                                                    return <void *> x3_start
cdef void * x3_fail():                                                      return <void *> to2_fail
cdef void * x4_fail():                                                      return <void *> x3_resume
cdef void * to2_code():
                                global to2_I, x4_V, to2_V
                                if to2_I > x4_V:                            return <void *> x4_resume
                                else: to2_V = to2_I;                        return <void *> to2_succeed
cdef void * to2_resume():       global to2_I;           to2_I = to2_I + 1;  return <void *> to2_code
cdef void * x3_succeed():                                                   return <void *> x4_start
cdef void * x4_succeed():       global to2_I, x3_V;     to2_I = x3_V;       return <void *> to2_code
#-----------------------------------------------------------------------------------
cdef void * mult_start():                                                   return <void *> to1_start
cdef void * to1_fail():                                                     return <void *> mult_fail
cdef void * to2_fail():                                                     return <void *> to1_resume
cdef void * mult_resume():                                                  return <void *> to2_resume
cdef void * to1_succeed():                                                  return <void *> to2_start
cdef void * to2_succeed():
                                global mult_V, to1_V, to2_V
                                mult_V = to1_V * to2_V;                     return <void *> mult_succeed
#-----------------------------------------------------------------------------------
cdef void * greater_start():                                                return <void *> x5_start
cdef void * x5_fail():                                                      return <void *> greater_fail
cdef void * mult_fail():                                                    return <void *> x5_resume
cdef void * greater_resume():                                               return <void *> mult_resume
cdef void * x5_succeed():                                                   return <void *> mult_start
cdef void * mult_succeed():
                              global x5_V, mult_V, greater_V
                              if x5_V <= mult_V:                            return <void *> mult_resume
                              else: greater_V = mult_V;                     return <void *> greater_succeed
#-----------------------------------------------------------------------------------
cdef void * write1_start():                                                 return <void *> greater_start
cdef void * write1_resume():                                                return <void *> greater_resume
cdef void * greater_fail():                                                 return <void *> write1_fail
cdef void * greater_succeed():
                              global write_V, greater_V
                              write_V = greater_V
                              report(write_V);                              return <void *> write1_succeed
#-----------------------------------------------------------------------------------
# ICON Programming Language: (2nd pass, optimization)
#
#                       every write(5 > ((1 to 2) * (3 to 4)));
#-----------------------------------------------------------------------------------
cdef void * write2_start():   global to3_I;           to3_I = 1;            return <void *> to3_code
cdef void * to3_resume():     global to3_I;           to3_I = to3_I + 1;    return <void *> to3_code
cdef void * to3_code():
                              global to3_I, to4_I
                              if to3_I > 2:                                 return <void *> write2_fail
                              else: to4_I = 3;                              return <void *> to4_code
cdef void * write2_resume():  global to4_I;           to4_I = to4_I + 1;    return <void *> to4_code
cdef void * to4_code():
                              global to4_I, mult_V, to3_I, greater_V
                              if to4_I > 4:                                 return <void *> to3_resume
                              else:
                                  mult_V = to3_I * to4_I
                                  if 5 <= mult_V:                           return <void *> write2_resume
                                  else:
                                      greater_V = mult_V
                                      report(greater_V);                    return <void *> write2_succeed
#-----------------------------------------------------------------------------------
cdef void * icon1():                                                        return <void *> write1_start
cdef void * write1_fail():    report("Failure.");                           return <void *> END
cdef void * write1_succeed(): report("Success!");                           return <void *> write1_resume
cdef void * icon2():                                                        return <void *> write2_start
cdef void * write2_fail():    report("Failure.");                           return <void *> END
cdef void * write2_succeed(): report("Success!");                           return <void *> write2_resume
#-----------------------------------------------------------------------------------
cdef void * END(): pass
#-----------------------------------------------------------------------------------
ctypedef void * (*pfunc)()
cdef void RUN(void * goto):
    while goto := <void *>(<pfunc>goto)():
        if goto == <void *>END:
            return
#-----------------------------------------------------------------------------------
def main_fast():
 import timeit
 if True:
     time1 = timeit.timeit(lambda: RUN(<void *> icon1), number = 1_000_000, globals = globals());
     print(time1)
     time2 = timeit.timeit(lambda: RUN(<void *> icon2), number = 1_000_000, globals = globals());
     print(time2)
 else:
     report()
     RUN(<void *> icon1)
     report()
     RUN(<void *> icon2)
#-----------------------------------------------------------------------------------
if __name__ == '__main__':
    main_fast()
#-----------------------------------------------------------------------------------