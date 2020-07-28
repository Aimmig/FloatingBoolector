from fbtor.BitVecConvert import BitVecConvStatic
from fbtor.FBoolectorTypes import FPType, RMode, WIDTH, MAN, EXP
from .test_converter import *
import pytest

"""
Test cases for the string to bitstring implementation:
"""

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

@pytest.mark.parametrize('inp,expected,fptype,rmode',subnormal)
def test_subnormal(inp,expected, fptype,rmode):
    assert BitVecConvStatic.convertToBinary(inp,fptype,rmode) == expected

@pytest.mark.parametrize('inp,expected,fptype,rmode', small)
def test_small(inp,expected, fptype,rmode):
    assert BitVecConvStatic.convertToBinary(inp,fptype,rmode) == expected

@pytest.mark.parametrize('inp,expected,fptype,rmode', large)
def test_large(inp,expected, fptype,rmode):
    assert BitVecConvStatic.convertToBinary(inp,fptype,rmode) == expected

@pytest.mark.parametrize('inp,expected,fptype,rmode', normal)
def test_normal(inp,expected, fptype,rmode):
    assert BitVecConvStatic.convertToBinary(inp,fptype,rmode) == expected
