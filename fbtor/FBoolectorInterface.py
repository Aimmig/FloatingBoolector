"""The FBoolector class extends Boolector such that floating point formulas
   can be generated and solved using the Boolector bitvector logic.

   This is done by overring the following functionality.

   -The choosen rounding mode and concrete floating point type can be set
    once in the constructor and are fixed for all operations.
   -Rounding modes are implemented according to IEE 754.
   -The 'floating point nodes' are actually just bitvector nodes of the
    appropriate length.
   -Basic arithmetic operatores for addition, multiplication etc, which
    simulate these IEE 754 operations on bitvector nodes, are implemented
   -The usual comparision operators are implemented.
   -Converting methods between integer bitvectors and floating point bitvectors
    are implemented
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
class FBoolectorInterface():
    
    """
    Creates an FBoolector object that extends Boolector object

    @param fptype: the floating point type to use
    @type fptype: FPType
    @param rmode: the rounding mode to use
    @type rmode: RMode
    @rtype: FBoolector
    @returns: a new boolector object, that additionally holds fptype
    """
    def __init__(self, fptype, rmode):
        pass
    """
    Create a BitVecSort of the corresponding length for the floating point type.
    This 'sort' is used as a 'FloatSort'

    @rtype: BitVecSort
    @returns: the BitVecSort of appropriate length
    """
    def FloatSort(self):
        pass

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
        pass

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
        pass
    
    """
    Gets the sign of a node

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode (length 1) that indicates the sign of the node
    """
    def fSign(self, node):
        pass

    """
    Gets the mantisse of a node

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the mantissa
    """
    def fMantisse(self, node):
        pass

    """
    Gets the mantisse including the implicit leading bit

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: new BoolectorBVNode with implicit leading bit & mantisse
    """
    def fMantisseIm(self, node):
        pass

    """
    Gets the exponent of a node

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the exponent
    """
    def fExponent(self, node):
        pass

    """
    Checks if node represents NaN

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: new BoolectorBVNode (length 1) that indicates wether node is NaN or not
    """
    def fNaN(self, node):
        pass

    """
    Checks if node represents infinity

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: new BoolectorBVNode (length 1) that indicates wether node is infinity or not
    """
    def fInf(self,node):
        pass

    """
    Checks if node represents positiv infinity

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: new BoolectorBVNode (length 1) that indicates wether node is +infinity or not
    """
    def fPInf(self, node):
        pass

    """
    Checks if node represents negative infinity

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: new BoolectorBVNode (length 1) that indicates wether node is -infinity or not
    """
    def fNInf(self, node):
        pass

    """
    Checks if node represents the number 0

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: new BoolectorBVNode (length 1) that indicates wether node is 0
    """
    def fNull(self, node):
        pass

    """
    Checks if node is a subnormal number

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: new BoolectorBVNode (length 1) that indicates wether node is subnormal
    """
    def fSubnormal(self,node):
        pass

    """
    Converts a floating point number to a BitVectorNode

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the same number as the input node
              interpreted as integer
    """
    def Convert(self, width, node):
        pass

    """
    Converts a BitVectorNode to a floating point number

    @param node: the node representing a integer number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the same number as the input node
              interpreted as floating point number
    """
    def fConvert(self, node):
        pass

    """
    Compute node that has that represents negative floating point number

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the same number as the input node
              but with inverted sign-bit
    """
    def fNeg(self, node):
        pass

    """
    Gets the absolute value of a node

    @param node: the node representing a floating point number
    @type node: BoolectorBVNode
    @rtype: BoolectorBVNode
    @returns: a new BoolectorBVNode that contains the same number as the input node
              but with sign-bit always set to 0
    """
    def fAbs(self, node):
        pass

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
        pass

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
        pass

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
        pass

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
        pass

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
        pass

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
         pass
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
         pass
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
        pass
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
        pass
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
        pass
