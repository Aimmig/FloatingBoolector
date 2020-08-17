#!/usr/bin/python3

from fbtor.FBoolectorTypes import FPType, RMode, WIDTH
from fbtor.FBoolector import FBoolector
from pyboolector import BTOR_OPT_MODEL_GEN

if __name__ == "__main__":
    fptype = FPType.single
    rmode = RMode.to_zero
    
    # setup FBoolector, variables etc
    fbtor = FBoolector(fptype,rmode)
    fbtor.Set_opt(BTOR_OPT_MODEL_GEN, 1)
    
    sqr = fbtor.fConst("2")
    sqrt = fbtor.fConst("1.41421356237")
    #sqr = fbtor.fConst("100")
    #sqrt = fbtor.fConst("10")
    
    x = fbtor.fVar(fbtor.FloatSort())
    
    #"""
    fbtor.Assert(fbtor.Eq(
        fbtor.fMul(x, x),
        sqr))
    
    fbtor.Assert(fbtor.fGte(x, fbtor.fConst("0")))
    
    """
    
    d = fbtor.Add(
            fbtor.Udiv(
                fbtor.fExponent(sqr),
                fbtor.Const(2, fbtor.fptype.value[0])),
            fbtor.Const(2**(fbtor.fptype.value[0] - 2), fbtor.fptype.value[0]))
    
    fbtor.Assert(fbtor.And(fbtor.And(
        fbtor.Eq(fbtor.fSign(x), fbtor.fSign(sqr)),
        fbtor.Eq(fbtor.fMantisse(x), fbtor.fMantisse(sqr))),
        fbtor.Eq(fbtor.fExponent(x), d)))
    
    for i in range(5):
        x = fbtor.fDiv(
            fbtor.fAdd(
                x,
                fbtor.fDiv(sqr, x)),
            fbtor.fConst("2"))
    #"""
    
    result = fbtor.Sat()
    
    if result == fbtor.SAT:
        print(sqrt.assignment)
        print(x.assignment)
    else:
        print("Unsat")
    