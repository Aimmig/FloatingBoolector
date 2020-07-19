from fbtor.BitVecConvert import FPType, RMode, BitVecConvStatic, EXP, MAN, WIDTH
import pyboolector, os
from pyboolector import _BoolectorBitVecSort, BoolectorBVNode, Boolector

os.environ["BTORMODELGEN"] = "1"

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
    

class FBoolector(Boolector):
    
    def __init__(self, fptype, rmode):
        super().__init__()
        self.fptype = fptype
        self.rmode = rmode
    
    def floatSort(self):
        return

    def FloatSort(self):
        #r = FloatSort(self)
        #r._width = self.fptype.value[WIDTH]
        #r._c_sort = btorapi.boolector_bitvec_sort(self._c_btor, width)
        return super().BitVecSort(self.fptype.value[WIDTH])

    def fVar(self, sort, symbol = None):
        #r = FloatNode(self)
        #r._sort = sort
        #r._c_node = btorapi.boolector_var(self._c_btor, sort._c_sort, _ChPtr(symbol)._c_str)
        return super().Var(sort, symbol)

    def fAssert(self, f, var, num: str, debug=False):
        return super().Assert(f(var,self.fConst(num, debug)))
    
    def fConst(self, num: str, debug: bool=False):
        return super().Const(BitVecConvStatic.convertToBinary(num, self.fptype, self.rmode, debug), self.fptype.value[WIDTH])
    
    def fSign(self, node):
        return super().Eq(node[:self.fptype.value[WIDTH]-1],super().Const(1,1))
        #return super().Ugte(node, super().Const(2**(self.fptype.value[WIDTH]-1), self.fptype.value[WIDTH]))
    
    def fMantisse(self, node):
        return super().Slice(node, self.fptype.value[MAN]-1, 0)
    def fMantisseIm(self, node):
        return super().Cond(
            super().Eq(self.Const(0, self.fptype.value[EXP]), self.fExponent(node)),
            super().Concat(Const(0, 1), self.fMantisse(node)),
            super().Concat(Const(1, 1), self.fMantisse(node)))
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
        var = self.fVar(FloatSort())
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
                super().And(self.fInf(nodeB), self.fNull(nodeA)))
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

    #Comparing Operations
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
    
    def fEq(self, nodeA, nodeB):
        return super().Cond(
            super().Or(self.fNaN(nodeA), self.fNaN(nodeB)), #one number equals NaN
            super().Const(False),
            super().Cond(
                super().And(self.fNull(nodeA), self.fNull(nodeB)), #both number equals 0
                super().Const(True),
                super().Eq(nodeA, nodeB)))
    def fGt(self, nodeA, nodeB):
        return super().Cond(
            super().Or(self.fNaN(nodeA), self.fNaN(nodeB)), #one number equals NaN
            super().Const(False),
            super().Cond(
                super().And(self.fNull(nodeA), self.fNull(nodeB)), #both number equals 0
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
    def fLt(self, nodeA, nodeB):
        return self.fGt(nodeB, nodeA)
    def fGte(self, nodeA, nodeB):
        return super().Or(self.fGt(nodeA, nodeB), self.fEq(nodeA, nodeB))
    def fLte(self, nodeA, nodeB):
        return super().Or(self.fLt(nodeA, nodeB), self.fEq(nodeA, nodeB))
