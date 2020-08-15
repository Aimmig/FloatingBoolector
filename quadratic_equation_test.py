#!/usr/bin/python3

#TO-DO: cleanup ....

from fbtor.FBoolectorTypes import FPType, RMode, WIDTH
from fbtor.FBoolector import FBoolector
from pyboolector import BTOR_OPT_MODEL_GEN

if __name__ == "__main__":
    fptype = FPType.double
    rmode = RMode.to_zero
    
    # Try to solve a simple quadratic equation which is 0 at the following points
    val1="2"
    val2="256"
    
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
    fbtor.Assert(fbtor.Not(fbtor.fEq(x,x1)))
    fbtor.Assert(fbtor.Not(fbtor.fEq(x,x2)))
    
    result = fbtor.Sat()
    
    if (result == fbtor.SAT):
        print("1. approach: SAT")
        print(x1.assignment)
        print(x2.assignment)
        print("found:")
        print(x.assignment)
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
    #fbtor.Assert(fbtor.Not(fbtor.fEq(x,x1)))
    fbtor.Assert(fbtor.Not(fbtor.fEq(x,x2)))
    
    #manually restrict search area
    #fbtor.Assert(fbtor.fGt(x,fbtor.fAdd(fbtor.fConst("1e-5"),x2)))
    #fbtor.Assert(fbtor.fLt(x,x1))
    #fbtor.Assert(fbtor.And(fbtor.fGt(x,fbtor.fAdd(x1,eps)),fbtor.fLt(x,fbtor.fSub(x2,eps))))
    
    # TO-DO: NEU FORMULIEREN NACH FIX --------------------------------------------
   
    # THIS IS WRONG after the fix
    # NOTE: Formula2 is even UNSAT when not restricting the possible output values.
    # Our implementation is therefore not able to find the expected zero values
    # This means Formula1 is not satisfiablity equvivalent to Formula2 even
    # if they are mathematically equivalent
    #
    # Depending on the chosen values at the top, it might be possible for Formula2 to
    # be SAT, e.g when x1=0 such that the equation reduces to x^2-x2*x=0.
    # But in such cases both Formula1 & Formula2 might expose more SAT-assignments than
    # one would expect e.g. it finds a value (very small x') where x'!=x2 with x'*x' -x2*x' = 0
    # This shows that even Formula1 can't (generally) be used to "just" calculate all solutions
    # (Also Formula1 isn't quite usefull for solving the equation at the first place)
    
    result = fbtor.Sat()
    
    if (result == fbtor.SAT):
        print("2. approach: SAT")
        print(x1.assignment)
        print(x2.assignment)
        print("found:")
        print(x.assignment)
        #fbtor.Print_model(format="smt2")
    elif(result == fbtor.UNSAT):
        print("2. approach: UNSAT")
