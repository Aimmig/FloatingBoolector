from fbtor.FBoolectorTypes import FPType, RMode, EXP, MAN, WIDTH
from fbtor.BitVecConvert import BitVecConvStatic
from pyboolector import _BoolectorBitVecSort, Boolector

import math

"""The FBoolector class extends Boolector such that floating point formulas
   can be generated and solved using the Boolector bitvector logic.

   This is done by overring the following functionality:

   -The choosen rounding mode and concrete floating point type can be set
    once in the constructor and are fixed for all operations.
   -Rounding modes are implemented according to IEE 754.
   -The 'floating point nodes' are actually just bitvector nodes of the
    appropriate length.
   -Basic arithmetic operatores for addition, multiplication etc, which
    simulate these IEE 754 operations on bitvector nodes, are implemented
   -The usual comparision operators are implemented.
   -TO-DO: shortly mention fConvert & Convert
   -Some helper functions for checking special cases like infinity,NaN
    etc, which are used internally but might be usefull for proving
    formulas.

   Note:
   -Because our nodes are just normal bitvector nodes, all functions
    natively offered by boolector can be applied.
   -Boolector natively offers operator overloading, so the provided
    floating point operations all use prefix notation, to clearly
    distinguish them from the native boolector ones.
"""
class FBoolector(Boolector):
    
    """
    Creates an FBoolector object that extends Boolector object

    @param fptype: the floating point type to use
    @type fptype: FPType
    @param rmode: the rounding mode to use
    @type rmode: RMode
    @rtype: FBoolector
    @returns a new boolector object, that additionally holds fptype
    """
    def __init__(self, fptype, rmode):
        super().__init__()
        self.fptype = fptype
        self.rmode = rmode

    """
    Create a BitVecSort of the corresponding length for the floating point type.
    This 'sort' is used as a 'FloatSort'

    @rtype: BitVecSort
    @returns: the BitVecSort of appropriate length
    """
    def FloatSort(self):
        return super().BitVecSort(self.fptype.value[WIDTH])

    """
    Create a boolector variable

    @param sort: the boolector sort to use
    @type sort: BitVecSort
    @param symbol: optional symbol for the variable
    @type symbol: str
    @rtype: BoolectorBVNode
    @returns: a new boolector variable of the sort/symbol
    """
    def fVar(self, sort, symbol = None):
        return super().Var(sort, symbol)

    """
    Create a bitvector node from string. The rounding mode & floating point type from the FBoolector object are used

    @param num: number to convert
    @type num: str
    @param debug: debug flag for conversion
    @type debug: bool
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the IEE representation of the given number
    """
    def fConst(self, num: str, debug: bool=False):
        return super().Const(BitVecConvStatic.convertToBinary(num, self.fptype, self.rmode, debug), self.fptype.value[WIDTH])
    
    """
    Gets the sign of a node

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode (length 1) that indicates the sign of the node
    """
    def fSign(self, node):
        return super().Slice(node,self.fptype.value[WIDTH]-1,self.fptype.value[WIDTH]-1)

    """
    Gets the mantisse of a node

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the mantissa
    """
    def fMantisse(self, node):
        return super().Slice(node, self.fptype.value[MAN]-1, 0)

    """
    Gets the mantisse including the implicit leading bit

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: new BoolectorBVNode with implicit leading bit & mantisse
    """
    def fMantisseIm(self, node):
        return super().Cond(
            self.fSubnormal(node),
            super().Concat(self.Const(0, 1), self.fMantisse(node)),
            super().Concat(self.Const(1, 1), self.fMantisse(node)))

    """
    Gets the exponent of a node

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the exponent
    """
    def fExponent(self, node):
        return super().Slice(node, self.fptype.value[EXP]+self.fptype.value[MAN]-1, self.fptype.value[MAN])
    
    """
    Checks if node represents NaN

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: new BoolectorBVNode (length 1) that indicates wether node is NaN or not
    """
    def fNaN(self, node):
        return super().And(
            super().Eq(self.fExponent(node), super().Const(2**self.fptype.value[EXP]-1, self.fptype.value[EXP])),
            super().Not(super().Eq(self.fMantisse(node), super().Const(0, self.fptype.value[MAN]))))

    """
    Checks if node represents infinity

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: new BoolectorBVNode (length 1) that indicates wether node is infinity or not
    """
    def fInf(self,node):
        return super().And(
            super().Eq(self.fExponent(node), super().Const(2**self.fptype.value[EXP]-1, self.fptype.value[EXP])),
            super().Eq(self.fMantisse(node), super().Const(0, self.fptype.value[MAN])))

    """
    Checks if node represents positiv infinity

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: new BoolectorBVNode (length 1) that indicates wether node is +infinity or not
    """
    def fPInf(self, node):
        return super().And(
            super().Not(self.fSign(node)),
            self.fInf(node))

    """
    Checks if node represents negative infinity

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: new BoolectorBVNode (length 1) that indicates wether node is -infinity or not
    """
    def fNInf(self, node):
        return super().And(
            self.fSign(node),
            self.fInf(node))

    """
    Checks if node represents the number 0

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: new BoolectorBVNode (length 1) that indicates wether node is 0
    """
    def fNull(self, node):
        return super().And(
            super().Eq(self.fExponent(node), super().Const(0, self.fptype.value[EXP])),
            super().Eq(self.fMantisse(node), super().Const(0, self.fptype.value[MAN])))

    """
    Checks if node is a subnormal number

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: new BoolectorBVNode (length 1) that indicates wether node is subnormal
    """
    def fSubnormal(self,node):
        return super().And(
            super().Eq(self.fExponent(node), super().Const(0, self.fptype.value[EXP])),
            super().Not(super().Eq(self.fMantisse(node), super().Const(0, self.fptype.value[MAN]))))

    """
    Converts a floating point number to a BitVectorNode

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the same number as the input node
              interpreted as integer
    """
    def Convert(self, width, node): #TODO special cases, rounding
        var = super().Var(super().BitVecSort(width))
        
        #real exponent without offset
        shift = super().Sub(
            super().Concat(super().Const(0), self.fExponent(node)),
            super().Const(2**(self.fptype.value[EXP] - 1) - 1, self.fptype.value[EXP] + 1))
        
        #Detection for minumum value
        mind = super().And(super().And(
            self.fSign(node),
            super().Eq(shift, super().Const(width - 1, self.fptype.value[EXP] + 1))),
            super().Eq(self.fMantisse(node), super().Const(0, self.fptype.value[MAN])))
        
        #Overflow detection
        over = super().And(
            super().Sgt(shift, super().Const(width - 2, self.fptype.value[EXP] + 1)),
            super().Not(mind))
        #Underflow / Subnormal detection
        under = super().Slt(shift, super().Const(0, self.fptype.value[EXP] + 1))
        
        bits = max(width, self.fptype.value[MAN] + 1)
        ebits = self.nextPower2(bits)
        
        #Positive Result without special cases
        man = super().Slice(super().Cond(
                super().Ugte(super().Slice(shift, math.log(ebits, 2) - 1, 0),
                    super().Const(self.fptype.value[MAN], math.log(ebits, 2))),
                super().Sll(
                    super().Concat(super().Const(0, ebits - self.fptype.value[MAN] - 1), self.fMantisseIm(node)),
                    super().Sub(
                        super().Slice(shift, math.log(ebits, 2) - 1, 0),
                        super().Const(self.fptype.value[MAN], math.log(ebits, 2)))),
                super().Srl(
                    super().Concat(super().Const(0, ebits - self.fptype.value[MAN] - 1), self.fMantisseIm(node)),
                    super().Sub(
                        super().Const(self.fptype.value[MAN], math.log(ebits, 2)),
                        super().Slice(shift, math.log(ebits, 2) - 1, 0)))),
            width - 1, 0)
        
        #Result
        super().Assert(super().Eq(var, super().Cond(
            super().Or(super().Or(over, under), super().Or(self.fNaN(node), self.fInf(node))),
            super().Const(0, width),
            super().Cond(
                self.fSign(node),
                super().Cond(
                    mind,
                    super().Const(2**(width - 1), width),
                    super().Neg(man)),
                man))))
        
        return var
        
    """
    Converts a BitVectorNode to a floating point number

    @param node: the node representing a integer number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the same number as the input node
              interpreted as floating point number
    """
    def fConvert(self, node):
        width = node.width
        var = self.fVar(self.FloatSort())
        
        #Sign
        super().Assert(super().Cond(
            super().Sgte(node, super().Const(0, width)),
            super().Not(self.fSign(var)),
            self.fSign(var)))
        
        #Positive input BitVector
        pos = super().Cond(
            super().Sgte(node, super().Const(0, width)),
            node,
            super().Neg(node))
        
        mbits = max(width, self.fptype.value[MAN] + 4)
        embits = self.nextPower2(mbits)
        
        posnull = super().Eq(super().Const(0, width), pos)
        
        #Position of the first 1 in pos
        log = super().Var(super().BitVecSort(math.log(embits, 2)))
        super().Assert(super().Cond(
            posnull,
            super().Eq(super().Const(0, math.log(embits, 2)), log),
            super().Eq(super().Const(1, embits), super().Srl(super().Concat(super().Const(0, embits - width), pos), log))))
        
        #Shifted Pos, highest bit equals 1
        shman = super().Slice(
            super().Sll(
                super().Concat(super().Const(0, embits - width), pos),
                super().Sub(
                    super().Const(mbits - 1, math.log(embits, 2)),
                    log)),
            mbits - 1, 0)
        
        ebits = max(math.log(embits, 2), self.fptype.value[EXP] + 1)
        eV = super().Var(super().BitVecSort(self.fptype.value[EXP]))
        
        #Extended Exponend
        eeV = super().Concat(super().Var((super().BitVecSort(ebits - self.fptype.value[EXP]))), eV)
        
        #Extended log
        elog = super().Concat(super().Const(0, ebits - math.log(embits, 2)), log)
        
        #Calculation of the extended Exponend
        super().Assert(super().Eq(eeV, super().Add(super().Const(2**(self.fptype.value[EXP] - 1) - 1, ebits), elog)))
        
        #Overflow detection
        over = super().Ugte(eeV, super().Const(2**(self.fptype.value[EXP]) - 1, ebits))
        
        #Exponent
        super().Assert(super().Eq(self.fExponent(var), super().Cond(
            over,
            super().Const(-1, self.fptype.value[EXP]),
            eV)))
        
        #Mantisse
        super().Assert(super().Eq(self.fMantisse(var), super().Cond(
            over,
            super().Const(0, self.fptype.value[MAN]),
            super().Slice(shman, mbits - 2, mbits - self.fptype.value[MAN] - 1))))
        
        guard = super().Cond(
            over,
            super().Const(False),
            super().Slice(shman, mbits - self.fptype.value[MAN] - 2, mbits - self.fptype.value[MAN] - 2))
        roundb = super().Cond(
            over,
            super().Const(False),
            super().Slice(shman, mbits - self.fptype.value[MAN] - 3, mbits - self.fptype.value[MAN] - 3))
        sticky = super().Cond(
            over,
            super().Const(False),
            super().Not(super().Eq(
                super().Const(0, mbits - self.fptype.value[MAN] - 3),
                super().Slice(shman, mbits - self.fptype.value[MAN] - 4, 0))))
        
        null = self.fVar(self.FloatSort())
        super().Assert(self.fNull(null))
        
        return super().Cond(posnull, null, self.fRound(var, guard, roundb, sticky))

    """
    Compute node that has that represents negative floating point number

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the same number as the input node
              but with inverted sign-bit
    """
    def fNeg(self, node):
        var = self.fVar(self.FloatSort())
        super().Assert(super().And(super().And(
            super().Eq(self.fMantisse(node), self.fMantisse(var)),
            super().Eq(self.fExponent(node), self.fExponent(var))),
            super().Eq(self.fSign(node), super().Not(self.fSign(var)))))
        return var

    """
    Gets the absolute value of a node

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the same number as the input node
              but with sign-bit always set to 0
    """
    def fAbs(self, node):
        var = self.fVar(self.FloatSort())
        super().Assert(super().And(super().And(
            super().Not(self.fSign(var)),
            super().Eq(self.fMantisse(node), self.fMantisse(var))),
            super().Eq(self.fExponent(node), self.fExponent(var))))
        return var

    """
    Computes next larger power of 2

    @param number: input
    @type number: int
    @rtype: int
    @returns: the next larger power of 2 for the given number
    """
    def nextPower2(self, number):
        return int(2**round(math.log(number, 2) + 0.5, 0))
        
    # ---------------------------------------------------------------------------
    # Arithmetic operations addition,multiplikation,subtraction,division etc
    # ---------------------------------------------------------------------------

    """
    Adds two nodes, considers the floating point type and rounding mode set in the constructor

    @param dnodeA: the first operand
    @type dnodeA: BoolectorBVNode
    @param dnodeB: the second operand
    @type dnodeB: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the Bitvector of the IEE-conform addition of both nodes
    """
    def fAdd(self, dnodeA, dnodeB):
        return self.fAddBase(dnodeA,dnodeB,True)

    """
    Adds two nodes, considers the floating point type rounding can be enabled or disabled

    @param dnodeA: the first operand
    @type dnodeA: BoolectorBVNode
    @param dnodeB: the second operand
    @type dnodeB: BoolectorBVNode
    @param round_flag: enable or disable rounding
    @type round_flag: bool
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the Bitvector of the IEE-conform addition of both nodes
              where the result is rounded or not rounded according to the round_flag
    """
    def fAddBase(self, dnodeA, dnodeB, round_flag):
        #nodeA > nodeB
        nodeA = super().Cond(self.fGte(self.fAbs(dnodeA), self.fAbs(dnodeB)), dnodeA, dnodeB)
        nodeB = super().Cond(self.fGte(self.fAbs(dnodeA), self.fAbs(dnodeB)), dnodeB, dnodeA)
        
        var = self.fVar(self.FloatSort())
        
        #Sign
        super().Assert(super().Eq(self.fSign(var), self.fSign(nodeA)))
        
        #Exponent difference
        eDiv = super().Sub(self.fExponent(nodeA), self.fExponent(nodeB))
        
        abits = self.nextPower2(2 * self.fptype.value[MAN] + 5)
        bits = abits - (2 * self.fptype.value[MAN] + 5)
        
        #extended mantisse of nodeA and nodeB
        emanA = super().Concat(super().Const(0, 1), super().Concat(self.fMantisseIm(nodeA), super().Const(0, self.fptype.value[MAN] + 3)))
        emanBT = super().Cond(
            super().Ugte(eDiv, super().Const(abits, self.fptype.value[EXP])),
            super().Const(0, 2 * self.fptype.value[MAN] + 5),
            super().Slice(super().Srl(
                super().Concat(
                    super().Const(0, bits),
                    super().Concat(super().Const(0, 1), super().Concat(self.fMantisseIm(nodeB), super().Const(0, self.fptype.value[MAN] + 3)))),
                super().Slice(eDiv, math.log(abits, 2) - 1, 0)), 2 * self.fptype.value[MAN] + 4, 0))
        
        #Indicator if theres a bit not equal to zero which was shifted out of the mantisse
        rem = super().Not(super().Eq(
            self.fMantisse(nodeB),
            super().Slice(super().Sll(
                super().Concat(
                    super().Const(0, bits),
                    emanBT),
                super().Slice(eDiv, math.log(abits, 2) - 1, 0)), 2 * self.fptype.value[MAN] + 2, self.fptype.value[MAN] + 3)))
        
        emanB = super().Cond(
            super().And(rem, super().Xor(self.fSign(nodeA), self.fSign(nodeB))),
            super().Add(emanBT, super().Const(1, 2 * self.fptype.value[MAN] + 5)),
            emanBT)
        
        #Extended mantisse of the result
        man = super().Var(super().BitVecSort(2 * self.fptype.value[MAN] + 5))
        super().Assert(super().Eq(man, super().Cond(
            super().Xor(self.fSign(nodeA), self.fSign(nodeB)),
            super().Sub(emanA, emanB),
            super().Add(emanA, emanB))))
        
        #index of the first one
        smlog = super().Var(super().BitVecSort(math.log(abits, 2)))
        super().Assert(super().Cond(
            super().Eq(super().Const(0, 2 * self.fptype.value[MAN] + 5), man),
            super().Eq(super().Const(0, math.log(abits, 2)), smlog),
            super().Eq(super().Const(1, bits + (2 * self.fptype.value[MAN] + 5)), super().Srl(super().Concat(super().Const(0, bits), man), smlog))))
        mlog = super().Concat(super().Const(0, self.fptype.value[EXP] + 2 - math.log(abits, 2)), smlog)
        
        #extended Exponents
        eV = super().Var(super().BitVecSort(self.fptype.value[EXP]))
        eeA = super().Concat(super().Const(0, 2), self.fExponent(nodeA))
        eeV = super().Concat(super().Var((super().BitVecSort(2))), eV)
        
        #Calculation of the extended exponent of the result
        super().Assert(super().Eq(eeV,
            super().Sub(
                eeA,
                super().Sub(super().Const(2 * self.fptype.value[MAN] + 3, self.fptype.value[EXP] + 2), mlog))))
        
        #Overflow detection
        over = super().Sgte(eeV, super().Const(2**(self.fptype.value[EXP]) - 1, self.fptype.value[EXP] + 2))
        
        #Underflow / Subnormal detection
        under = super().Or(
            super().Slte(eeV, super().Const(0, self.fptype.value[EXP] + 2)),
            super().Eq(super().Const(0, 2 * self.fptype.value[MAN] + 5), man))
        
        #Exponent
        super().Assert(super().Eq(self.fExponent(var), super().Cond(
            over,
            super().Const(-1, self.fptype.value[EXP]),
            super().Cond(
                under,
                super().Const(0, self.fptype.value[EXP]),
                eV))))
        
        smanbits = self.nextPower2(2 * self.fptype.value[MAN] + 5)
        slog = super().Slice(mlog, math.log(smanbits, 2) - 1, 0)
        
        #offset for subnormal numbers
        undero = super().Cond(
            under,
            super().Slice(
                super().Neg(eeV),
                math.log(smanbits, 2) - 1,
                0),
            super().Const(0, math.log(smanbits, 2)))
            
        #mantisse with a one on the highest bit
        shman = super().Slice(super().Cond(
                super().Ugte(super().Const(2 * self.fptype.value[MAN] + 4, math.log(smanbits, 2)), super().Add(slog, undero)),
                super().Sll(
                    super().Concat(super().Const(0, smanbits - (2 * self.fptype.value[MAN] + 5)), man),
                    super().Sub(
                        super().Sub(super().Const(2 * self.fptype.value[MAN] + 4, math.log(smanbits, 2)), slog),
                        undero)),
                super().Srl(
                    super().Concat(super().Const(0, smanbits - (2 * self.fptype.value[MAN] + 5)), man),
                    super().Sub(
                        super().Add(undero, slog),
                        super().Const(2 * self.fptype.value[MAN] + 4, math.log(smanbits, 2))))),
            2 * self.fptype.value[MAN] + 4, 0)
        
        #Mantisse
        super().Assert(super().Eq(self.fMantisse(var), super().Cond(
            over,
            super().Const(0, self.fptype.value[MAN]),
            super().Slice(shman, 2 * self.fptype.value[MAN] + 3, self.fptype.value[MAN] + 4))))
        
        #special case: Not a number
        varNaN = super().Or(
            super().Or(self.fNaN(nodeA), self.fNaN(nodeB)),
            super().Or(
                super().And(self.fPInf(nodeA), self.fNInf(nodeB)),
                super().And(self.fPInf(nodeB), self.fNInf(nodeA))))
        nan = self.fVar(self.FloatSort())
        super().Assert(self.fNaN(nan))
        
        #special case: Infinity
        varInf = super().Or(
            self.fInf(nodeA),
            self.fInf(nodeB))
        inf = self.fVar(self.FloatSort())
        super().Assert(super().Eq(self.fSign(inf), self.fSign(var)))
        super().Assert(self.fInf(inf))
        
        #special case: zero
        varNull = self.fEq(self.fNeg(nodeA), nodeB)
        null = self.fVar(self.FloatSort())
        super().Assert(self.fNull(null))
        
        #rounding bits
        if (round_flag):
            guard = super().Cond(
                over,
                super().Const(False),
                super().Slice(shman, self.fptype.value[MAN] + 3, self.fptype.value[MAN] + 3))
            roundb = super().Cond(
                over,
                super().Const(False),
                super().Slice(shman, self.fptype.value[MAN] + 2, self.fptype.value[MAN] + 2))
            sticky = super().Cond(
                over,
                super().Const(False),
                super().Or(super().Not(super().Eq(
                    super().Const(0, self.fptype.value[MAN] + 2),
                    super().Slice(shman, self.fptype.value[MAN] + 1, 0))),
                    rem))
            return super().Cond(varNaN, nan, super().Cond(varInf, inf, super().Cond(varNull, null, self.fRound(var, guard, roundb, sticky))))
        else:
            return super().Cond(varNaN, nan, super().Cond(varInf, inf, super().Cond(varNull, null, var)))

    """
    Subtracts a node from the other, considers the floating point type and rounding mode set in the constructor

    @param nodeA: the first operand (minuend)
    @type nodeA: BoolectorBVNode
    @param nodeB: the second operand (subtrahend)
    @type nodeB: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the Bitvector of the IEE-conform subtraction of both nodes
    """
    def fSub(self, nodeA, nodeB):
        # create and assert new var to -nodeB
        neg_nodeB = self.fNeg(nodeB)
        # redirect a-b to a+(-b)
        return self.fAdd(nodeA,neg_nodeB)

    """
    Multiplies two nodes, considers the floating point type and rounding mode set in the constructor

    @param nodeA: the first operand
    @type nodeA: BoolectorBVNode
    @param nodeB: the second operand
    @type nodeB: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the Bitvector of the IEE-conform multiplication of both nodes
    """
    def fMul(self, nodeA, nodeB):
        var = self.fVar(self.FloatSort())
        
        #Sign
        super().Assert(super().Eq(self.fSign(var), super().Xor(self.fSign(nodeA), self.fSign(nodeB))))
        
        #Extended mantisse
        man = super().Var(super().BitVecSort(2 * self.fptype.value[MAN] + 3))
        super().Assert(super().Eq(man, super().Mul(
            super().Concat(super().Const(0, self.fptype.value[MAN] + 2), self.fMantisseIm(nodeA)),
            super().Concat(super().Const(0, self.fptype.value[MAN] + 2), self.fMantisseIm(nodeB)))))
        
        abits = self.nextPower2(2 * self.fptype.value[MAN] + 3)
        bits = abits - (2 * self.fptype.value[MAN] + 3)
        
        #index of the highest bit of the mantisse
        smlog = super().Var(super().BitVecSort(math.log(abits, 2)))
        super().Assert(super().Cond(
            super().Eq(super().Const(0, 2 * self.fptype.value[MAN] + 3), man),
            super().Eq(super().Const(0, math.log(abits, 2)), smlog),
            super().Eq(super().Const(1, bits + (2 * self.fptype.value[MAN] + 3)), super().Srl(super().Concat(super().Const(0, bits), man), smlog))))
        mlog = super().Concat(super().Const(0, self.fptype.value[EXP] + 2 - math.log(abits, 2)), smlog)
        
        #Extended exponents
        eV = super().Var(super().BitVecSort(self.fptype.value[EXP]))
        eeA = super().Concat(super().Const(0, 2), self.fExponent(nodeA))
        eeB = super().Concat(super().Const(0, 2), self.fExponent(nodeB))
        eeV = super().Concat(super().Var((super().BitVecSort(2))), eV)
        
        #calculation of the extended exponent of the result
        super().Assert(super().Eq(eeV,
            super().Sub(
                super().Add(eeA, eeB),
                super().Add(
                    super().Const(2**(self.fptype.value[EXP]-1)-1, self.fptype.value[EXP] + 2),
                    super().Sub(super().Const(2 * self.fptype.value[MAN] + 0, self.fptype.value[EXP] + 2), mlog)))))
        
        #Overflow detection
        over = super().Sgte(eeV, super().Const(2**(self.fptype.value[EXP]) - 1, self.fptype.value[EXP] + 2))
        
        #Underflow / Subnormal detection
        under = super().Slte(eeV, super().Const(0, self.fptype.value[EXP] + 2))
        
        #Exponent
        super().Assert(super().Eq(self.fExponent(var), super().Cond(
            over,
            super().Const(-1, self.fptype.value[EXP]),
            super().Cond(
                under,
                super().Const(0, self.fptype.value[EXP]),
                eV))))
        
        smanbits = self.nextPower2(2 * self.fptype.value[MAN] + 3)
        slog = super().Slice(mlog, math.log(smanbits, 2) - 1, 0)
        
        #offset for subnormal numbers
        undero = super().Cond(
            under,
            super().Slice(
                super().Neg(eeV),
                math.log(smanbits, 2) - 1,
                0),
            super().Const(0, math.log(smanbits, 2)))
            
        #mantisse with highest bit one
        shman = super().Slice(super().Cond(
                super().Ugte(super().Const(2 * self.fptype.value[MAN] + 2, math.log(smanbits, 2)), super().Add(slog, undero)),
                super().Sll(
                    super().Concat(super().Const(0, smanbits - (2 * self.fptype.value[MAN] + 3)), man),
                    super().Sub(
                        super().Sub(super().Const(2 * self.fptype.value[MAN] + 2, math.log(smanbits, 2)), slog),
                        undero)),
                super().Srl(
                    super().Concat(super().Const(0, smanbits - (2 * self.fptype.value[MAN] + 3)), man),
                    super().Sub(
                        super().Add(undero, slog),
                        super().Const(2 * self.fptype.value[MAN] + 2, math.log(smanbits, 2))))),
            2 * self.fptype.value[MAN] + 2, 0)
        
        #Mantisse
        super().Assert(super().Eq(self.fMantisse(var), super().Cond(
            over,
            super().Const(0, self.fptype.value[MAN]),
            super().Slice(shman, 2 * self.fptype.value[MAN] + 1, self.fptype.value[MAN] + 2))))
        
        #rounding bits
        guard = super().Cond(
            over,
            super().Const(False),
            super().Slice(shman, self.fptype.value[MAN] + 1, self.fptype.value[MAN] + 1))
        roundb = super().Cond(
            over,
            super().Const(False),
            super().Slice(shman, self.fptype.value[MAN], self.fptype.value[MAN]))
        sticky = super().Cond(
            over,
            super().Const(False),
            super().Not(super().Eq(
                super().Const(0, self.fptype.value[MAN]),
                super().Slice(shman, self.fptype.value[MAN] - 1, 0))))
        
        #special case: Not a number
        varNaN = super().Or(
            super().Or(self.fNaN(nodeA), self.fNaN(nodeB)),
            super().Or(
                super().And(self.fInf(nodeA), self.fNull(nodeB)),
                super().And(self.fInf(nodeB), self.fNull(nodeA))))
        nan = self.fVar(self.FloatSort())
        super().Assert(self.fNaN(nan))
        
        #special case: infinity
        varInf = super().Or(
            self.fInf(nodeA),
            self.fInf(nodeB))
        inf = self.fVar(self.FloatSort())
        super().Assert(super().Eq(self.fSign(inf), self.fSign(var)))
        super().Assert(self.fInf(inf))
        
        #special case: zero
        varNull = super().Or(
            self.fNull(nodeA),
            self.fNull(nodeB))
        null = self.fVar(self.FloatSort())
        super().Assert(self.fNull(null))
        
        return super().Cond(varNaN, nan, super().Cond(varInf, inf, super().Cond(varNull, null, self.fRound(var, guard, roundb, sticky))))
        
    """
    Performs division of two nodes, considers the floating point type and rounding mode set in the constructor

    @param nodeA: the first operand (dividend)
    @type nodeA: BoolectorBVNode
    @param nodeB: the second operand (divisor)
    @type nodeA: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the Bitvector of the IEE-conform division of both nodes
    """
    def fDiv(self, nodeA, nodeB):
        var = self.fVar(self.FloatSort())
        
        #Sign
        super().Assert(super().Eq(self.fSign(var), super().Xor(self.fSign(nodeA), self.fSign(nodeB))))
        
        #extended mantisse
        man = super().Var(super().BitVecSort(3 * self.fptype.value[MAN] + 4))
        super().Assert(super().Eq(man, super().Udiv(
            super().Concat(self.fMantisseIm(nodeA), super().Const(0, 2 * self.fptype.value[MAN] + 3)),
            super().Concat(super().Const(0, 2 * self.fptype.value[MAN] + 3), self.fMantisseIm(nodeB)))))
        
        #Indicator if theres a bit not equal to zero which was shifted out of the mantisse
        rem = super().Not(super().Eq(super().Const(0, 3 * self.fptype.value[MAN] + 4), super().Urem(
            super().Concat(self.fMantisseIm(nodeA), super().Const(0, 2 * self.fptype.value[MAN] + 3)),
            super().Concat(super().Const(0, 2 * self.fptype.value[MAN] + 3), self.fMantisseIm(nodeB)))))
        
        abits = self.nextPower2(3 * self.fptype.value[MAN] + 4)
        bits = abits - (3 * self.fptype.value[MAN] + 4)
        
        #Index of the first one of the mantisse
        smlog = super().Var(super().BitVecSort(math.log(abits, 2)))
        super().Assert(super().Cond(
            super().Eq(super().Const(0, 3 * self.fptype.value[MAN] + 4), man),
            super().Eq(super().Const(0, math.log(abits, 2)), smlog),
            super().Eq(super().Const(1, abits), super().Srl(super().Concat(super().Const(0, bits), man), smlog))))
        mlog = super().Concat(super().Const(0, self.fptype.value[EXP] + 2 - math.log(abits, 2)), smlog)
        
        #Extended exponents
        eV = super().Var(super().BitVecSort(self.fptype.value[EXP]))
        eeA = super().Concat(super().Const(0, 2), self.fExponent(nodeA))
        eeB = super().Concat(super().Const(0, 2), self.fExponent(nodeB))
        eeV = super().Concat(super().Var((super().BitVecSort(2))), eV)
        
        #Calculation of the extended exponent of the result
        super().Assert(super().Eq(eeV,
            super().Add(
                super().Sub(eeA, eeB),
                super().Sub(
                    super().Const(2**(self.fptype.value[EXP]-1)-1, self.fptype.value[EXP] + 2),
                    super().Sub(super().Const(2 * self.fptype.value[MAN] + 3, self.fptype.value[EXP] + 2), mlog)))))
        
        #Overflow detection
        over = super().Sgte(eeV, super().Const(2**(self.fptype.value[EXP]) - 1, self.fptype.value[EXP] + 2))
        
        #Underflow / Subnormal detection
        under = super().Slte(eeV, super().Const(0, self.fptype.value[EXP] + 2))
        
        #Exponent
        super().Assert(super().Eq(self.fExponent(var), super().Cond(
            over,
            super().Const(-1, self.fptype.value[EXP]),
            super().Cond(
                under,
                super().Const(0, self.fptype.value[EXP]),
                eV))))
        
        smanbits = self.nextPower2(3 * self.fptype.value[MAN] + 4)
        slog = super().Slice(mlog, math.log(smanbits, 2) - 1, 0)
        
        #offset for subnormal numbers
        undero = super().Cond(
            under,
            super().Slice(
                super().Cond(
                    self.fSubnormal(nodeA),
                    super().Neg(eeV),
                    super().Add(super().Neg(eeV), super().Const(1, self.fptype.value[EXP] + 2))),
                math.log(smanbits, 2) - 1,
                0),
            super().Const(0, math.log(smanbits, 2)))
            
        #mantisse with highest bit one
        shman = super().Slice(super().Cond(
                super().Ugte(super().Const(3 * self.fptype.value[MAN] + 3, math.log(smanbits, 2)), super().Add(slog, undero)),
                super().Sll(
                    super().Concat(super().Const(0, smanbits - (3 * self.fptype.value[MAN] + 4)), man),
                    super().Sub(
                        super().Sub(super().Const(3 * self.fptype.value[MAN] + 3, math.log(smanbits, 2)), slog),
                        undero)),
                super().Srl(
                    super().Concat(super().Const(0, smanbits - (3 * self.fptype.value[MAN] + 4)), man),
                    super().Sub(
                        super().Add(undero, slog),
                        super().Const(3 * self.fptype.value[MAN] + 3, math.log(smanbits, 2))))),
            3 * self.fptype.value[MAN] + 3, 0)
        
        #Mantisse
        super().Assert(super().Eq(self.fMantisse(var), super().Cond(
            over,
            super().Const(0, self.fptype.value[MAN]),
            super().Slice(shman, 3 * self.fptype.value[MAN] + 2, 2 * self.fptype.value[MAN] + 3))))
        
        #rounding bits
        guard = super().Cond(
            over,
            super().Const(False),
            super().Slice(shman, 2 * self.fptype.value[MAN] + 2, 2 * self.fptype.value[MAN] + 2))
        roundb = super().Cond(
            over,
            super().Const(False),
            super().Slice(shman, 2 * self.fptype.value[MAN] + 1, 2 * self.fptype.value[MAN] + 1))
        sticky = super().Cond(
            over,
            super().Const(False),
            super().Or(
                super().Not(super().Eq(
                    super().Const(0, 2 * self.fptype.value[MAN] + 1),
                    super().Slice(shman, 2 * self.fptype.value[MAN], 0))),
                rem))
        
        #special case: Not a number
        varNaN = super().Or(
            super().Or(self.fNaN(nodeA), self.fNaN(nodeB)),
            super().Or(
                super().And(self.fInf(nodeA), self.fInf(nodeB)),
                super().And(self.fNull(nodeA), self.fNull(nodeB))))
        nan = self.fVar(self.FloatSort())
        super().Assert(self.fNaN(nan))
        
        #special case: Infinity
        varInf = super().Or(
            self.fInf(nodeA),
            self.fNull(nodeB))
        inf = self.fVar(self.FloatSort())
        super().Assert(super().Eq(self.fSign(inf), self.fSign(var)))
        super().Assert(self.fInf(inf))
        
        #special case: zero
        varNull = super().Or(
            self.fNull(nodeA),
            self.fInf(nodeB))
        null = self.fVar(self.FloatSort())
        super().Assert(self.fNull(null))
        
        return super().Cond(varNaN, nan, super().Cond(varInf, inf, super().Cond(varNull, null, self.fRound(var, guard, roundb, sticky))))
    
    
    """
    Calculates the square root of a node with the heron algorithm

    @param node: node
    @type node: BoolectorBVNode
    @param precision: number of steps which are calculated
    @type precision: Integer
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the square root
    """
    def fSqrt(self, node, precision = 5):
        if (precision < 1):
            return node
        
        d = super().Add(
            super().Udiv(
                self.fExponent(node),
                super().Const(2, self.fptype.value[EXP])),
            super().Const(2**(self.fptype.value[EXP] - 2), self.fptype.value[EXP]))
        
        x = self.fVar(self.FloatSort())
        super().Assert(super().And(super().And(
            super().Eq(self.fSign(x), self.fSign(node)),
            super().Eq(self.fMantisse(x), self.fMantisse(node))),
            super().Eq(self.fExponent(x), d)))
        
        for i in range(precision):
            x = self.fDiv(self.fAdd(x, self.fDiv(node, x)), self.fConst("2"))
        
        nan = self.fVar(self.FloatSort())
        super().Assert(self.fNaN(nan))
        
        inf = self.fVar(self.FloatSort())
        super().Assert(self.fPInf(inf))
        
        return super().Cond(self.fSign(node), nan, super().Cond(self.fPInf(node), inf, x))
        
        
    
    # ---------------------------------------------------------------------------
    # Some UNROUNDED arithmetic operations addition,subtraction
    # ---------------------------------------------------------------------------

    """
    Adds two nodes, considers the floating point type from the constructor, but does NOT any rounding

    @param dnodeA: the first operand
    @type dnodeA: BoolectorBVNode
    @param dnodeB: the second operand
    @type dnodeB: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the unrounded Bitvector addition
    """
    def fAddWR(self, dnodeA, dnodeB):
        return self.fAddBase(dnodeA,dnodeB,False)

    """
    Subtracts two nodes, considers the floating point type from the constructor, but does NOT any rounding

    @param nodeA: the first operand (minuend)
    @type nodeA: BoolectorBVNode
    @param nodeB: the second operand (subtrahend)
    @type nodeB: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the unrounded Bitvector subtraction
    """
    def fSubWR(self, nodeA, nodeB):
        # create and assert new var to -nodeB
        neg_nodeB = self.fNeg(nodeB)
        # redirect a-b to a+(-b)
        return self.fAddWR(nodeA,neg_nodeB)

    # ---------------------------------------------------------------------------
    # Methods that handle rounding of the results
    # ---------------------------------------------------------------------------

    """
    TO-DO

    @param node: the node to round
    @type node: BoolectorBVNode
    @param guard: the IEE guard bit
    @type guard: BoolectorBVNode
    @param roundb: the IEE round bit
    @type roundb: BoolectorBVNode
    @param sticky: the IEE sticky bit
    @type sticky: BoolectorBVNode
    @rtype: BoolectorVBNode
    @returns: TO-DO
    """
    def fRound(self, node, guard, roundb, sticky): #TODO special cases
        return super().Cond(
            self.fNaN(node),
            node,
            super().Cond(
                self.fInf(node),
                node,
                self.fRoundN(node, guard, roundb, sticky)))

    """
    TO-DO

    @param node: the node to round
    @type node: BoolectorBVNode
    @param guard: the IEE guard bit
    @type guard: BoolectorBVNode
    @param roundb: the IEE round bit
    @type roundb: BoolectorBVNode
    @param sticky: the IEE sticky bit
    @type sticky: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: TO-DO
    """
    def fRoundN(self, node, guard, roundb, sticky):
        var = self.fVar(self.FloatSort())
        super().Assert(super().Not(self.fSign(var)))
        under = super().Ulte(self.fExponent(node), super().Const(self.fptype.value[MAN], self.fptype.value[EXP]))
        super().Assert(super().Eq(self.fExponent(var), super().Cond(
            under,
            super().Const(0, self.fptype.value[EXP]),
            super().Sub(self.fExponent(node), super().Const(self.fptype.value[MAN], self.fptype.value[EXP])))))
        super().Assert(super().Eq(self.fMantisse(var), super().Cond(
            under,
            super().Const(1, self.fptype.value[MAN]),
            super().Const(0, self.fptype.value[MAN]))))
        
        if self.rmode == RMode.to_zero:
            return node
        elif self.rmode == RMode.to_neg_inf:
            return super().Cond(
                self.fSign(node),
                super().Cond(
                    super().Or(guard,
                    super().Or(roundb,
                    sticky)),
                    self.fSubWR(node, var),
                    node),
                node)
        elif self.rmode == RMode.to_pos_inf:
            return super().Cond(
                self.fSign(node),
                node,
                super().Cond(
                    super().Or(guard,
                    super().Or(roundb,
                    sticky)),
                    self.fAddWR(node, var),
                    node))
        else:
            return super().Cond(
                self.fSign(node),
                super().Cond(
                    super().And(guard,
                    super().Or(roundb,
                    sticky)),
                    self.fSubWR(node, var),
                    node),
                super().Cond(
                    super().And(guard,
                    super().Or(roundb,
                    sticky)),
                    self.fAddWR(node, var),
                    node))

    # ---------------------------------------------------------------------------
    # Methods for compare operators: Eq,Lt,Gt,etc....
    # ---------------------------------------------------------------------------

    """
    Checks the equality of 2 IEE Bitvectors

    @type  nodeA: BoolectorBVNode
    @param nodeA: first operand
    @type  nodeB: BoolectorBVNode
    @param nodeB: second operand
    @rtype: BoolectorBVNode
    @returns: bitvector of length 1
    """
    def fEq(self, nodeA, nodeB):
        return super().Cond(
            #one number equals NaN
            super().Or(self.fNaN(nodeA), self.fNaN(nodeB)),
            super().Const(False),
            super().Cond(
                #both number equals 0
                super().And(self.fNull(nodeA), self.fNull(nodeB)),
                super().Const(True),
                super().Eq(nodeA, nodeB)))

    """
    Checks if one IEE bitvector is greater than the other

    @type  nodeA: BoolectorBVNode
    @param nodeA: first operand
    @type  nodeB: BoolectorBVNode
    @param nodeB: second operand
    @rtype: BoolectorBVNode
    @returns: bitvector of length 1
    """
    def fGt(self, nodeA, nodeB):
        return super().Cond(
            #one number equals NaN
            super().Or(self.fNaN(nodeA), self.fNaN(nodeB)),
            super().Const(False),
            super().Cond(
                #both number equals 0
                super().And(self.fNull(nodeA), self.fNull(nodeB)),
                super().Const(False),
                super().Cond(
                    self.fSign(nodeA),
                    super().Cond(
                        self.fSign(nodeB),
                        super().Ult(nodeA, nodeB),
                        super().Const(False)),
                    super().Cond(
                        self.fSign(nodeB),
                        super().Const(True),
                        super().Ugt(nodeA, nodeB)))))

    """
    Checks if one IEE bitvector is less than the other

    @type  nodeA: BoolectorBVNode
    @param nodeA: first operand
    @type  nodeB: BoolectorBVNode
    @param nodeB: second operand
    @rtype: BoolectorBVNode
    @returns: bitvector of length 1
    """
    def fLt(self, nodeA, nodeB):
        return self.fGt(nodeB, nodeA)

    """
    Checks if one IEE bitvector is greater or equal than the other

    @type  nodeA: BoolectorBVNode
    @param nodeA: first operand
    @type  nodeB: BoolectorBVNode
    @param nodeB: second operand
    @rtype: BoolectorBVNode
    @returns: bitvector of length 1
    """
    def fGte(self, nodeA, nodeB):
        return super().Or(self.fGt(nodeA, nodeB), self.fEq(nodeA, nodeB))

    """
    Checks if one IEE bitvector is less or equal than the other

    @type  nodeA: BoolectorBVNode
    @param nodeA: first operand
    @type  nodeB: BoolectorBVNode
    @param nodeB: second operand
    @rtype: BoolectorBVNode
    @returns: bitvector of length 1
    """
    def fLte(self, nodeA, nodeB):
        return super().Or(self.fLt(nodeA, nodeB), self.fEq(nodeA, nodeB))
