#!/usr/bin/python3

from fbtor.FBoolectorTypes import FPType, RMode, WIDTH
from fbtor.FBoolector import FBoolector
from pyboolector import BTOR_OPT_MODEL_GEN

if __name__ == "__main__":
    fptype = FPType.double
    rmode = RMode.to_zero
    
    # Try to solve a simple quadratic equation which is 0 at the following points
    val1="5e12"
    val2="32e-5"
    
    # setup FBoolector, variables etc
    fbtor = FBoolector(fptype,rmode)
    fbtor.Set_opt(BTOR_OPT_MODEL_GEN, 1)
    s = fbtor.BitVecSort(fbtor.fptype.value[WIDTH])
    x = fbtor.fVar(s)
    x1 = fbtor.fConst(val1)
    x2 = fbtor.fConst(val2)
    
    # First (simpler) approach is to use 0=(x-1)(x-x2)
    f = fbtor.fMul(fbtor.fSub(x,x1),fbtor.fSub(x,x2))
    formula1 = fbtor.fEq(fbtor.fConst("0"),f)
    fbtor.Assert(formula1)
    
    #manually exclude x1 or x2, if both are excluded formula becomes UNSAT
    #fbtor.Assert(fbtor.Not(fbtor.fEq(x,x1)))
    #fbtor.Assert(fbtor.Not(fbtor.fEq(x,x2)))
    
    result = fbtor.Sat()
    
    if (result == fbtor.SAT):
        print("1. approach is SAT, found")
        print(x.assignment)
        print("Expected values are:")
        print(x1.assignment)
        print(x2.assignment)
        #fbtor.Print_model(format="smt2")
    elif(result == fbtor.UNSAT):
        print("1. approach: UNSAT")
    
    ##########################################
    
    #overwrite boolector and setup stuff again
    fbtor = FBoolector(fptype,rmode)
    fbtor.Set_opt(BTOR_OPT_MODEL_GEN, 1)
    s = fbtor.BitVecSort(fbtor.fptype.value[WIDTH])
    x = fbtor.fVar(s)
    x1 = fbtor.fConst(val1)
    x2 = fbtor.fConst(val2)
    eps = fbtor.fConst("1e-25")
    
    #Now solve the same formula but in the form 0=(x^2 -(x1+x2)*x)+ x1*x2
    f = fbtor.fAdd(fbtor.fSub(fbtor.fMul(x,x),
                              fbtor.fMul(fbtor.fAdd(x1,x2),x)
                         ),
                   fbtor.fMul(x1,x2)
                  )
    formula2 = fbtor.fEq(fbtor.fConst("0"),f)
    fbtor.Assert(formula2)
    
    #manually exclude x1 or x2, if both are excluded formula becomes UNSAT
    fbtor.Assert(fbtor.Not(fbtor.fEq(x,x1)))
    fbtor.Assert(fbtor.Not(fbtor.fEq(x,x2)))
    
    #manually restrict search area
    #fbtor.Assert(fbtor.fGt(x,fbtor.fAdd(fbtor.fConst("1e-5"),x2)))
    #fbtor.Assert(fbtor.fLt(x,x1))
    #fbtor.Assert(fbtor.And(fbtor.fGt(x,fbtor.fAdd(x1,eps)),fbtor.fLt(x,fbtor.fSub(x2,eps))))
    
    # This examples shows, that our implementation is able to solve (simple) quadratic equation.
    # The fact the IEE floating point numbers are not mathematically is also visible here, because
    # there are some solutions that are only a small epsilon away from the expected solution.
    result = fbtor.Sat()
    
    if (result == fbtor.SAT):
        print("2. approach is SAT, found:")
        print(x.assignment)
        print("Expected values are:")
        print(x1.assignment)
        print(x2.assignment)
        #fbtor.Print_model(format="smt2")
    elif(result == fbtor.UNSAT):
        print("2. approach: UNSAT")
