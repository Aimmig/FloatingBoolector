from fbtor.BitVecConvert import FPType, RMode, BitVecConvStatic, EXP, MAN, WIDTH
from pyboolector import _BoolectorBitVecSort, Boolector


#TO-DO: Remove this code below

"""

class FloatSort(_BoolectorBitVecSort):
    def __init__(self, fbtor):
        super().__init__(fbtor)
class FloatNode(BoolectorBVNode):
    def __init__(self, fbtor):
        super().__init__(fbtor)
    def fSign(self):
        return btor.fSign(self)
    def fMantisse(self, node):
        return btor.fMantisse(self)
    def fExponent(self, node):
        return btor.fExponent(self)
    def fNaN(self):
        return btor.fNaN(self)
    def fNull(self):
        return btor.fNull(self)
    def fInf(self):
        return btor.fInf(self)
    def fSubnormal(self):
        return btor.fSubnormal(self)
    def fRound(self, guard, round, sticky):
        return btor.fRound(self, guard, round, sticky)
    def fEq(self, node):
        return btor.fEq(self, node)
    def fGt(self, node):
        return btor.fGt(self, node)
    def fLt(self, node):
        return btor.fLt(self, node)
    def fGte(self, node):
        return btor.fGte(self, node)
    def fLte(self, node):
        return btor.fLte(self, node)
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
    #TO-DO: Remove non working c btorapi-stuff ....
    def FloatSort(self):
        #r = FloatSort(self)
        #r._width = self.fptype.value[WIDTH]
        #r._c_sort = btorapi.boolector_bitvec_sort(self._c_btor, width)
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
    #TO-DO: Remove non working c btorapi-stuff ....
    def fVar(self, sort, symbol = None):
        #r = FloatNode(self)
        #r._sort = sort
        #r._c_node = btorapi.boolector_var(self._c_btor, sort._c_sort, _ChPtr(symbol)._c_str)
        return super().Var(sort, symbol)

    """
    Helper method to assert a property to a variable based on a binary function and a value.
    E.g. asserts that var is equal/less/greater etc. than the given value

    @param f: function that is applied to var,num
    @type f: BoolectorBVNode x BoolectorBVNode -> BoolectorNode (length 1)
    @param var: the variable that shall be asserted
    @type var: BoolectorNode
    @param num: number that is converted to BoolectorNode
    @type num: str
    @param debug: debug flag for conversion
    @type debug: bool
    """
    def fAssert(self, f, var, num: str, debug=False):
        super().Assert(f(var,self.fConst(num, debug)))
    
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
    #TO-DO: This is way to complicated ... should be the first bit ??
    def fSign(self, node):
        return super().Eq(node[:self.fptype.value[WIDTH]-1],super().Const(1,1))
        #return node[0]

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
    Gets the mantisse including the sign bit of a node

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the sign bit and the mantisse
    """
    def fMantisseIm(self, node):
        return super().Cond(
            super().Eq(self.Const(0, self.fptype.value[EXP]), self.fExponent(node)),
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
    
    def fNaN(self, node):
        return super().And(
            super().Eq(self.fExponent(node), super().Const(2**self.fptype.value[EXP]-1, self.fptype.value[EXP])),
            super().Not(super().Eq(self.fMantisse(node), super().Const(0, self.fptype.value[MAN]))))

    def fInf(self, node):
        return super().Or(self.fPInf(node), self.fNInf(node))

    def fPInf(self, node):
        return super().And(
            super().Not(self.fSign(node)), super().And(
            super().Eq(self.fMantisse(node), super().Const(0, self.fptype.value[MAN])),
            super().Eq(self.fExponent(node), super().Const(2**self.fptype.value[EXP]-1, self.fptype.value[EXP]))))

    def fNInf(self, node):
        return super().And(
            self.fSign(node), super().And(
            super().Eq(self.fMantisse(node), super().Const(0, self.fptype.value[MAN])),
            super().Eq(self.fExponent(node), super().Const(2**self.fptype.value[EXP]-1, self.fptype.value[EXP]))))

    def fNull(self, node):
        return super().And(
            super().Eq(self.fExponent(node), super().Const(0, self.fptype.value[EXP])),
            super().Eq(self.fMantisse(node), super().Const(0, self.fptype.value[MAN])))

    def fInf(self,node):
        return super().And(
            super().Eq(self.fExponent(node), super().Const(2**self.fptype.value[EXP]-1, self.fptype.value[EXP])),
            super().Eq(self.fMantisse(node), super().Const(0, self.fptype.value[MAN])))

    def fSubnormal(self,node):
        return super().And(
            super().Eq(self.fExponent(node), super().Const(0, self.fptype.value[EXP])),
            super().Not(super().Eq(self.fMantisse(node), super().Const(0, self.fptype.value[MAN]))))

    def Convert(self, sort, node): #TODO special cases, rounding
        var = super().Var(sort)
        tshift = super().Add(super().Sub(self.fExponent(node), super().Sll(super().Const(1, self.fptype.value[EXP]), self.fptype.value[EXP]-1)), super().Const(1, self.fptype.value[EXP]))
        tres = super().Cond(
            super().Gte(tshift, super().Const(0, self.fptype.value[EXP])),
            super().Sll(
                super().Concat(super().Const(1, sort._width-self.fptype.value[MAN]), self.fMantisse(node)),
                tshift),
            super().Const(0, sort._width))
        super().Assert(super().Eq(var, super().Cond(
            self.fSign(node),
            tres,
            super().Neg(tres))))
        return var

    def fConvert(self, node):
        var = self.fVar(FloatSort())
        super().Assert(super().Cond(
            super().Gte(node, super().Const(0, node._sort._width)),
            super().Not(self.fSign(var)),
            self.fSign(var)))
        pos = super().Cond(
            super().Gte(node, super().Const(0, node._sort._width)),
            node,
            super().Neg(node))
        log = super().Var(node._sort)
        super().Assert(super().Eq(super().Const(1, node._sort._width), super().Srl(pos, log)))
        super().Assert(super().Cond(
            super().Ugte(log, super().Const(2**fbtype[0]-3, fbtype[0])), #enough Exponent bits
            super().And(
                super().Eq(self.fExponent(var), super().Const(2**fbtype[0]-1, fbtype[0])),
                super().Eq(self.fMantisse(var), super().Const(0, fbtype[0]))),
            super().And(
                super().Eq(self.fExponent(var), log),
                super().Eq(self.fMantisse(var), super().Slice(pos, super().Sub(log, super().Const(1, node._sort._width)), super().Cond(
                    super().Ugt(log, super().Const(fbtype[1], node._sort._width)), #enough Mantisse bits
                    super().Sub(log, super().Const(fbtype[1], node._sort._width)),
                    super().Const(0, node._sort._width)))))))
        guard = super().Cond(
            super().Ugt(super().Add(log, super().Const(1, node._sort._width)), super().Const(fbtype[1], node._sort._width)), #enough Mantisse bits
            super().Eq(super().Slice(pos, super().Sub(log, super().Const(fbtype[1]+1, node._sort._width)), super().Sub(log, super().Const(fbtype[1]+1, node._sort._width))), super().Const(1)),
            super().Const(False))
        round = super().Cond(
            super().Ugt(super().Add(log, super().Const(2, node._sort._width)), super().Const(fbtype[1], node._sort._width)), #enough Mantisse bits
            super().Eq(super().Slice(pos, super().Sub(log, super().Const(fbtype[1]+2, node._sort._width)), super().Sub(log, super().Const(fbtype[1]+2, node._sort._width))), super().Const(1)),
            super().Const(False))
        sticky = super().Cond(
            super().Ugt(super().Add(log, super().Const(3, node._sort._width)), super().Const(fbtype[1], node._sort._width)), #enough Mantisse bits
            super().Not(super().Eq(super().Slice(pos, super().Sub(log, super().Const(fbtype[1]+3, node._sort._width)), super().Const(0, node._sort._width)), super().Const(0, node._sort._width))),
            super().Const(False))
        
        return self.fRound(var, guard, round, sticky)
    
    # checks if a has the given property and returns b if so otherwise returns
    # value of the elseCondition
    def fPropElse(self, nodeA,nodeB, fProp, elseCond):
        return Cond(
                   fProp(nodeA),
                   nodeB,
                   elseCond
               )

    def fInfElse(nodeA, nodeB, elseCond):
        return fProp(nodeA, nodeA, fInf,
                     fProp(nodeB, nodeB, fInf,
                           elseCond
                     )
                )

    def fNanElse(nodeA, nodeB, elseCond):
        return fProp(nodeA, nodeA, fNaN,
                     fProp(nodeB, nodeB, fNaN,
                           elseCond
                     )
                )

    def fNullElse(nodeA, nodeB, elseCond):
        return fProp(nodeA, nodeB, fNull,
                     fProp(nodeB, nodeA, fNull,
                           elseCond
                     )
                )

    def fNeg(self, node):
        var = self.fVar(self.FloatSort())
        super().Assert(super().And(super().And(
            super().Eq(self.fMantisse(node), self.fMantisse(var)),
            super().Eq(self.fExponent(node), self.fExponent(var))),
            super().Eq(self.fSign(node), super().Not(self.fSign(var)))))
        return var
    
    #Arithmetic Operations
    def fAdd(self, nodeA, nodeB):
        #TO-DO determine order of Nan, Inf, Null checks
        #return fNanElse(nodeA, nodeB,
        #                fInfElse(nodeA, nodeB,
        #                         fNullElse(nodeA,nodeB,
        #                                  nodeA
        #                                  #TO-DO Cond(.....
        #                                   #)
        #                         )
        #                )
        #       )
        var = self.fVar(super().BitVecSort(self.fptype.value[EXP]))
        #super().Cond(super().Eq(self.fSign(nodeA),self.fSign(nodeB)),
        super().Assert(super().Eq(var,super().Sub(self.fExponent(nodeA),self.fExponent(nodeB))))
        newExp = self.fVar(super().BitVecSort(self.fptype.value[EXP]))
        super().Assert(super().Eq(newExp, super().Add(super().Const(2**(self.fptype.value[EXP]-1)-1,self.fptype.value[EXP]),var)
                                 )
                      )
                                 #)
                    #)
        return newExp 

    def fSub(self, nodeA, nodeB):
        # create and assert new var to -nodeB
        neg_nodeB = self.fNeg(nodeB)
        # redirect a-b to a+(-b)
        return neg_nodeB
        #return self.fAdd(nodeA,neg_nodeB)

    def fMul(self, nodeA, nodeB):
        var = self.fVar(self.FloatSort())
        super().Assert(super().Eq(self.fSign(var), super().Xor(self.fSign(nodeA), self.fSign(nodeB))))
        
        man = super().Var(super().BitVecSort(2 * self.fptype.value[MAN] + 3))
        super().Assert(super().Eq(man, super().Mul(
            super().Concat(super().Const(0, self.fptype.value[MAN] + 2), self.fMantisseIm(nodeA)),
            super().Concat(super().Const(0, self.fptype.value[MAN] + 2), self.fMantisseIm(nodeB)))))
        
        log = super().Var(super().BitVecSort(self.fptype.value[EXP] + 2))
        super().Assert(super().Eq(super().Const(1, self.fptype.value[EXP] + 2), super().Srl(man, log)))
        
        eV = super().Var(super().BitVecSort(self.fptype.value[EXP]))
        eeA = super().Concat(super().Const(0, 2), self.fExponent(nodeA))
        eeB = super().Concat(super().Const(0, 2), self.fExponent(nodeB))
        eeV = super().Concat(super().Var((super().BitVecSort(2)), eeV))
        
        super().Assert(super().Eq(eeV,
            super().Sub(
                super().Add(eeA, eeB),
                super().Add(
                    super().Const(2**(self.fptype.value[EXP]-1)-1, self.fptype.value[EXP] + 2),
                    super().Sub(log, super().Const(self.fptype.value[MAN], self.fptype.value[EXP] + 2))))))
        
        over = super().Sgte(eeV, super().Const(2**(self.fptype.value[EXP]) - 1, self.fptype.value[EXP] + 2))
        under = super().Slte(eeV, super().Const(0, self.fptype.value[EXP] + 2))
        
        #Exponent
        super().Assert(super().Eq(self.fExponent(var), super().Cond(
            over,
            super().Const(-1, self.fptype.value[EXP]),
            super().Cond(
                under,
                super().Const(0, self.fptype.value[EXP]),
                eV))))
        
        upper = super().Cond(
            under,
            super().Add(super().Sub(log, super().Const(1, self.fptype.value[EXP] + 2)), eeV),
            super().Sub(log, super().Const(1, self.fptype.value[EXP] + 2)))
        lower = super().Sub(upper, super().Const(self.fptype.value[MAN], self.fptype.value[EXP] + 2))
        
        #Mantisse
        super().Assert(super().Eq(self.fMantisse(var), super().Cond(
            over,
            super().Const(0, self.fptype.value[MAN]),
            super().Concat(
                super().Slice(man,
                    super().Cond(
                        super().Slt(upper, super().Const(0, self.fptype.value[EXP] + 2)),
                        super().Const(0, self.fptype.value[EXP] + 2),
                        upper),
                    super().Cond(
                        super().Slt(lower, super().Const(0, self.fptype.value[EXP] + 2)),
                        super().Const(0, self.fptype.value[EXP] + 2),
                        lower)),
                super().Slice( #Add zeros to fill mantisse
                    super().Const(0, self.fptype.value[EXP] + 2),
                    super().Cond(
                        super().Slt(lower, super().Const(0, self.fptype.value[EXP] + 2)),
                        super().Cond(
                            super().Slt(upper, super().Const(0, self.fptype.value[EXP] + 2)),
                            super().Sub(super().Neg(lower), super().Neg(upper)),
                            super().Neg(lower)),
                        super().Const(0, self.fptype.value[EXP] + 2)),
                    super().Const(0, self.fptype.value[EXP] + 2))))))
        
        guard = super().Cond(
            super().Slt(lower, super().Const(1, self.fptype.value[EXP] + 2)),
            super().Const(False),
            super().Eq(super().Slice(man,
                super().Sub(lower, super().Const(1, self.fptype.value[EXP] + 2)),
                super().Sub(lower, super().Const(1, self.fptype.value[EXP] + 2))), super().Const(1)))
        round = super().Cond(
            super().Slt(lower, super().Const(2, self.fptype.value[EXP] + 2)),
            super().Const(False),
            super().Eq(super().Slice(man,
                super().Sub(lower, super().Const(2, self.fptype.value[EXP] + 2)),
                super().Sub(lower, super().Const(2, self.fptype.value[EXP] + 2))), super().Const(1)))
        sticky = super().Cond(
            super().Slt(lower, super().Const(3, self.fptype.value[EXP] + 2)),
            super().Const(False),
            super().Eq(super().Slice(man,
                super().Sub(lower, super().Const(3, self.fptype.value[EXP] + 2)),
                super().Sub(lower, super().Const(3, self.fptype.value[EXP] + 2))), super().Const(1)))
        
        varNaN = super().Or(
            super().Or(self.fNaN(nodeA), self.fNaN(nodeB)),
            super().Or(
                super().And(self.fInf(nodeA), self.fNull(nodeB)),
                super().And(self.fInf(nodeB), self.fNull(nodeA))))
        nan = self.fVar(self.FloatSort())
        super().Assert(self.fNaN(nan))
        
        return super().Cond(varNaN, nan, var) #fRound(var, guard, round, sticky)
        
    def fDiv(self, nodeA, nodeB):
        return
    
    #Without rounding
    def fAddWR(self, nodeA, nodeB):
        # assume both are normalized
        nan = self.fVar(self.FloatSort())
        super().Assert(self.fNaN(nan))
        notNan = self.fVar(self.FloatSort())
        super().Assert(super().Not(self.fNaN(notNan)))
        
        return super().Cond(super().Or(self.fNaN(nodeA),self.fNaN(nodeB)),
                            nan,
                            super().Cond(super().Or(super().And(self.fPInf(nodeA),self.fNInf(nodeB)),super().And(self.fPInf(nodeB),self.fNInf(nodeA))),
                                nan,
                                # Here comes actual addition
                                notNan
                                )
                    )
        #exp_diff = super.Sub(self.fExponent(nodeA),self.fExponent(nodeB))

    def fMulWR(self, nodeA, nodeB):
        return

    def fDivWR(self, nodeA, nodeB):
        return

# ---------------------------------------------------------------------------
# Methods that handle rounding of the results
# ---------------------------------------------------------------------------

    def fRound(self, node, guard, round, sticky): #TODO special cases
        return super().Cond(
            self.fNaN(node),
            node,
            super().Cond(
                self.fInf(node),
                node,
                self.fRoundN(self, node, guard, round, sticky)))

    def fRoundN(self, node, guard, round, sticky):
        if self.rmode == RMode.to_zero:
            return node
        elif self.rmode == RMode.to_neg_inf:
            return super().Cond(
                self.fSign(node),
                super().Cond(
                    super().Or(guard,
                    super().Or(round,
                    sticky)),
                    node, #TODO subtract 1
                    node),
                node)
        elif self.rmode == RMode.to_pos_inf:
            return super().Cond(
                self.fSign(node),
                node,
                super().Cond(
                    super().Or(guard,
                    super().Or(round,
                    sticky)),
                    node, #TODO add 1
                    node))
        else:
            return super().Cond(
                self.fSign(node),
                super().Cond(
                    super().And(guard,
                    super().Or(round,
                    sticky)),
                    node, #TODO subtract 1
                    node),
                super().Cond(
                    super().And(guard,
                    super().Or(round,
                    sticky)),
                    node, #TODO add 1
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
