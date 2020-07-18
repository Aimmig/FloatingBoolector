#!/usr/bin/python

from BitVecConvert import BitVecConvStatic as bvconst
from BitVecConvert import FPType, RMode

if __name__ == "__main__":
     test_val = ["-0","+0","1e-315","1e-323","256.000000000000000000000000000000000030518","-3e-39","1e-40","1.175E-38","1.176e-38","1e-38","3.4e38 ","1.7976931348623157E308","3.45e38","1.797693134e308","-1.797693135e308","+.000","-0.000000001", "-.0",".000000001","1.000000000000001", ".1000","1e200","12345671561654e8","-876987411112e-7","45e-2","9231e-4","-23e3","1e-1","12325e-2"]
     #test_val = ["100", "1e- 2","-0.0101e-0",".0101","10100e-6"]
     for num in test_val:
        print(bvconst.convertToScientificNotation(num))
        fptype = FPType.single
        for r in RMode:
            print(r.name)
            bv = bvconst.convertToBinary(num,fptype,r)
            print(bv)
        print("----")
