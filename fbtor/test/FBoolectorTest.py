from fbtor.BitVecConvert import BitVecConvStatic
from fbtor.FBoolectorTypes import WIDTH
import pytest
from fbtor.FBoolector import FBoolector
from pyboolector import Boolector, BTOR_OPT_MODEL_GEN
from .test_set import *
from .test_converter import set_fSign,set_fMantisse,set_fExponent

""" Test cases for the FBoolector implementation:
    For testing bool-functions (comparison operators) it is sufficent to assert Boolector.UNSAT/Boolector.SAT to such an comparison expression
    For testing arithmetic functions either the constant or (better) the actual bit-assignment can be asserted
"""

# ----------------------------------------------------------------------------------
# Setup & preparations functions
# ----------------------------------------------------------------------------------

# Setup boolector & sort object
def _setup_(fptype, rmode):
     fbtor = FBoolector(fptype, rmode)
     fbtor.Set_opt(BTOR_OPT_MODEL_GEN,1)
     sort = fbtor.BitVecSort(fbtor.fptype.value[WIDTH])
     return fbtor, sort

# create 2 variables from FBoolector & sort and assert them to the given constant values
def prepare(fbtor, sort, const):
     variables = []
     for i in range(len(const)):
        #x = fbtor.Var(sort,str(i))
        #fbtor.Assert(fbtor.Eq(x,fbtor.fConst(const[i])))
        variables.append(fbtor.fConst(const[i]))
     return variables

# ----------------------------------------------------------------------------------
# Template functions for different assertion tests
# ----------------------------------------------------------------------------------

# check if comparison formula is Boolector.UNSAT/Boolector.SAT and assert expected value
def AssertCompare(fbtor, expected):
     result = fbtor.Sat()
     if result == Boolector.SAT:
         print("Boolector.SAT")
         fbtor.Print_model(format="smt2")
     else:
         print("Boolector.UNSAT")
     assert result == expected

# checks expected bit-string value with the assignment of the result node
def AssertArithmetic(fbtor, result, expected):
     # arithmetic formula should aways be Boolector.SAT
     print(fbtor.Sat())
     fbtor.Print_model(format="smt2")
     # expected value is normal string
     if not len(expected) == (fbtor.fptype.value[WIDTH]):
        expected = BitVecConvStatic.convertToBinary(expected, fbtor.fptype, fbtor.rmode)
     # expected value is bit string:
     assert result.assignment == expected

# ----------------------------------------------------------------------------------
# Template functions for comparison & arithmetic functions
# ----------------------------------------------------------------------------------

# template function for different comparison operators
def compareTemplate(fbtor, sort, const, expected, function):
     print("--------------")
     [x,y] = prepare(fbtor, sort, const)
     fbtor.Assert(function(x,y))
     AssertCompare(fbtor, expected)

def arithmeticTemplate(fbtor, sort, const, expected, function):
     print("--------------")
     # binary arithmetic operator to be tested
     if len(const) == 2:
        [x,y] = prepare(fbtor, sort, const)
        result = function(x,y)
     # unary arithmetic operator to be tested
     if len(const) == 1:
        [x] = prepare(fbtor, sort, const)
        result = function(x)
     AssertArithmetic(fbtor, result, expected)

# ----------------------------------------------------------------------------------
# Here the real test begin now: compare-operators
# ----------------------------------------------------------------------------------

@pytest.mark.parametrize('x_const,y_const,expected,fptype,rmode', set_fEq)
def test_fEq(x_const, y_const, expected,fptype,rmode):
     fbtor, sort = _setup_(fptype,rmode)
     compareTemplate(fbtor, sort, [x_const, y_const], expected, fbtor.fEq)

@pytest.mark.parametrize('x_const,y_const,expected,fptype,rmode',set_fGtE)
def test_fGtE(x_const, y_const, expected,fptype,rmode):
     fbtor, sort = _setup_(fptype,rmode)
     compareTemplate(fbtor, sort, [x_const, y_const], expected, fbtor.fGte)

@pytest.mark.parametrize('x_const,y_const,expected,fptype,rmode', set_fLtE)
def test_fLtE(x_const, y_const, expected,fptype,rmode):
     fbtor, sort = _setup_(fptype,rmode)
     compareTemplate(fbtor, sort, [x_const, y_const], expected, fbtor.fLte)

@pytest.mark.parametrize('x_const,y_const,expected,fptype,rmode', set_fGt)
def test_fGt(x_const, y_const, expected,fptype,rmode):
     fbtor, sort = _setup_(fptype,rmode)
     compareTemplate(fbtor, sort, [x_const, y_const], expected, fbtor.fGt)

@pytest.mark.parametrize('x_const,y_const,expected,fptype,rmode', set_fLt)
def test_fLt(x_const, y_const, expected,fptype,rmode):
     fbtor, sort = _setup_(fptype,rmode)
     compareTemplate(fbtor, sort, [x_const, y_const], expected, fbtor.fLt)

# ----------------------------------------------------------------------------------
# Test fSign, fExponent, fMantisse method
# ----------------------------------------------------------------------------------

@pytest.mark.parametrize('x_const,expected,fptype,rmode', set_fSign)
def test_Sign(x_const, expected, fptype, rmode):
     fbtor, sort = _setup_(fptype, rmode)
     #x = fbtor.Var(sort,"x")
     #fbtor.Assert(fbtor.Eq(x,fbtor.fConst(x_const)))
     x = fbtor.fConst(x_const)
     fbtor.Sat()
     assert fbtor.fSign(x).assignment == expected

@pytest.mark.parametrize('x_const,expected,fptype,rmode', set_fExponent)
def test_fExponent(x_const, expected, fptype, rmode):
     fbtor, sort = _setup_(fptype, rmode)
     #x = fbtor.Var(sort,"x")
     #fbtor.Assert(fbtor.Eq(x,fbtor.fConst(x_const)))
     x = fbtor.fConst(x_const)
     fbtor.Sat()
     assert fbtor.fExponent(x).assignment == expected

@pytest.mark.parametrize('x_const,expected,fptype,rmode', set_fMantisse)
def test_fMantisse(x_const, expected, fptype, rmode):
     fbtor, sort = _setup_(fptype, rmode)
     #x = fbtor.Var(sort,"x")
     #fbtor.Assert(fbtor.Eq(x,fbtor.fConst(x_const)))
     x = fbtor.fConst(x_const)
     fbtor.Sat()
     assert fbtor.fMantisse(x).assignment == expected

# ----------------------------------------------------------------------------------
# Test fNeg method
# ----------------------------------------------------------------------------------

@pytest.mark.parametrize('const,expected',
     [
      ("-0","+0"),("+1","-1"), ("5e17","-5e17"), ("-inf","+inf")
     ])
def test_fNeg(const, expected):
     fbtor, sort = _setup_(FPType.single, RMode.to_zero)
     arithmeticTemplate(fbtor, sort, [const], expected, fbtor.fNeg)


# TO-DO: Test arithmetic functions

# ----------------------------------------------------------------------------------
# Here the real test begin now: arithmetic operators
# ----------------------------------------------------------------------------------


@pytest.mark.parametrize('x_const,y_const,expected,fptype,rmode', set_fAdd)
def test_fAdd(x_const, y_const, expected, fptype, rmode):
    fbtor, sort = _setup_(fptype, rmode)
    arithmeticTemplate(fbtor, sort, [x_const, y_const], expected, fbtor.fAdd)
    
@pytest.mark.parametrize('x_const,y_const,expected,fptype,rmode', set_fSub)
def test_fSub(x_const, y_const, expected, fptype, rmode):
    fbtor, sort = _setup_(fptype, rmode)
    arithmeticTemplate(fbtor, sort, [x_const, y_const], expected, fbtor.fSub)

@pytest.mark.parametrize('x_const,y_const,expected,fptype,rmode', set_fMul)
def test_fMul(x_const, y_const, expected, fptype, rmode):
    fbtor, sort = _setup_(fptype, rmode)
    arithmeticTemplate(fbtor, sort, [x_const, y_const], expected, fbtor.fMul)

@pytest.mark.parametrize('x_const,y_const,expected,fptype,rmode', set_fDiv)
def test_fDiv(x_const, y_const, expected, fptype, rmode):
    fbtor, sort = _setup_(fptype, rmode)
    arithmeticTemplate(fbtor, sort, [x_const, y_const], expected, fbtor.fDiv)

# ----------------------------------------------------------------------------------
# Here the real test begin now: convert operators
# ----------------------------------------------------------------------------------

@pytest.mark.parametrize('x_const,width,expected,fptype,rmode', set_fConvert)
def test_fConvert(x_const, width, expected, fptype, rmode):
    fbtor, sort = _setup_(fptype, rmode)
    arithmeticTemplate(fbtor, sort, [x_const], expected, fbtor.fConvert)