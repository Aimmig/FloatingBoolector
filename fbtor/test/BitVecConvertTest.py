from fbtor.BitVecConvert import FPType, RMode, BitVecConvStatic, WIDTH, MAN, EXP
import pytest

"""
Test cases for the string to bitstring implementation:
"""

#TO-DO: Cover more cases ...

def test_Zero():
     for t in FPType:
         for r in RMode:
            for sign in ["+","-"]:
                res = BitVecConvStatic.convertToBinary(sign+"0",t,r)
                signbit = "0"
                if sign == "-":
                   signbit ="1"
                print(res)
                assert res == (signbit + (t.value[WIDTH]-1)*"0")

def test_Inf():
     for t in FPType:
         for r in RMode:
            for sign in ["+","-"]:
                res = BitVecConvStatic.convertToBinary(sign+"inf",t,r)
                signbit = "0"
                if sign == "-":
                   signbit ="1"
                print(res)
                assert res == (signbit + t.value[EXP]*"1"+ t.value[MAN]*"0")
