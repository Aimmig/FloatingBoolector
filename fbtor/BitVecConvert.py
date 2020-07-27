import re
from fbtor.FBoolectorTypes import FPType, RMode

# TO-DO: look at remaining TO-DOs or remove them ...
# TO-DO: remove this fixed bit-precision
additional_bits = 3
""" Class that contains functionality to convert a decimal number to IEE-754 floating-point bitvector.

    The first step is to convert the given number in scientifc notation, into a more
    standardized scientifc notation, where there is no dot in the number and no unnecessary 0s at the
    end. The basic idead is then to distinguish two cases.
    One case where the number to convert is actually an integer and another where the number to convert
    has an absolute value less than 1. Converting these cases seperatly and combining the results allows
    to converty any number.
    This class also contains some utility functions that help actually compute the IEE-754 floating-point bitvector
    representation and can handle different rounding modes as well as different floating point sizes. 
"""

class BitVecConvStatic:

    """ Adds 1 to binary list

    @type x: list[int]
    @param x: the binary number to add 1 to
    @rtype: list[int]
    @returns: result of binary addition from x with 1
    """
    def addOne(x:[int]):
            maxlen = len(x)
            y = [0]*(maxlen-1) + [1]        
            result = [0]*maxlen
            carry = 0
            i = maxlen-1
            while i>=0:
                r = carry
                r += 1 if x[i] == 1 else 0
                r += 1 if y[i] == 1 else 0

                # r can be 0,1,2,3 (carry + x[i] + y[i])
                # and among these, for r==1 and r==3 you will have result bit = 1
                # for r==2 and r==3 you will have carry = 1

                result[i] = (1 if r % 2 == 1 else 0) 
                carry = 0 if r < 2 else 1       
                i = i-1
            return result

    """Rounds the given number according to the given rounding mode

    @type s: int
    @param s: the sign bit
    @type m: list[int]
    @param m: the mantissa_bits
    @type mantissa_bits: int
    @param mantissa_bits: the amount of bits available for the mantissa
    @tpye rmode: RMode
    @param rmode: the rouding mode to use, default is no rounding mode
    @rtype: list[int]
    @returns the correctly rounded mantissa
    """
    # TO-DO: remove static fixed bit-precision (beginning of file!!)
    # TO-DO?? Rounding mode (e.g. to nearest) might need another look at
    # not sure if subnormal numbers round correctly??
    def round(s: int, m: [int], mantissa_bits: int, rmode=None):
            
            # nothing to round
            if rmode == None or len(m) <=mantissa_bits:
                return m
            
            # Truncate rest bits$
            elif rmode == RMode.to_zero:
                return m[:mantissa_bits]
            
            # to pos inf truncates only neg numbers
            elif rmode == RMode.to_pos_inf:
                if s == 1:
                    return m[:mantissa_bits]
                else:
                    return BitVecConvStatic.addOne(m[:mantissa_bits])
            
            # to neg inf truncates only pos numbers
            elif rmode == RMode.to_neg_inf:
                if s == 0:
                    return m[:mantissa_bits]
                else:
                    return BitVecConvStatic.addOne(m[:mantissa_bits])
            
            # to nearest$ 
            elif rmode == RMode.to_nearest:
                # guard=0 -> round down
                if m[mantissa_bits] == 0:
                    return m[0:mantissa_bits]
                # guard=1 and there is another bit 1 after that
                elif 1 in m[mantissa_bits+1:]:
                    return BitVecConvStatic.addOne(m[:mantissa_bits])
                # ties to even case e.g. guard=1 and all other bits after that 0
                elif m[mantissa_bits-1] == 0:
                    return m[:mantissa_bits]
                else:
                    return BitVecConvStatic.addOne(m[:mantissa_bits])

    """Infinity check for exponent

    @type exp: [int]
    @param exp: binary exponent to check
    @type exp_bits: int
    @param exp_bits: the number of allowed bits
    """
    def checkInf(exp, exp_bits):
        if (len(exp) == exp_bits and any(i == 0 for i in exp)):
            return exp
        else:
            return [1]*exp_bits

    """Computes the binary biased exponent

    @type exp: int
    @param exp: the actual decimal exponent to encode
    @type num_bits: int
    @param num_bits: available bits for biased exponent default is -1
    @rtype: list[int]
    @returns: the binary representation of the biased exponent
    """
    def getBiasedExponent(exp: int,num_bits=-1):
        bias = 2**(num_bits-1)-1
        binary, leng = BitVecConvStatic.getBinary(bias+exp, num_bits)
        return binary

    """Convertes the given number to binary

    @type exp: int
    @param exp: the number to convert
    @tpye num_bits: int
    @param num_bits: available bits
    @type insert_after: bool
    @param insert_after:flag wether to fill up with 0 at the end or front if number is shorter
    @rtype: (list[int],int)
    @returns: the binary representation of the given number and
            the amount of bits actually needed
    """
    def getBinary(exp: int,num_bits=-1,insert_after=False):
        q = exp
        exp_binary = []
        i=-1
        # repeat division by to to get bits (in reversed order)
        while q!= 0:
            (q,r) = divmod(q,2)
            exp_binary.insert(0,r)
            i+=1
        #fill remaining bits with zeros from front
        if num_bits > 0:
            pos = 0
            if not insert_after:
                while len(exp_binary) < num_bits:
                    exp_binary.insert(0,0)
            else:
                while len(exp_binary) < num_bits:
                    exp_binary.append(0)
        return exp_binary, i

    """ Convertes the given number to IEE-bitvector assuming the number is acutally an integer

    @type  num10: int
    @param num10: the mantissa part of the decimal number
    @type  exp10: int
    @param exp10: the exponent of the decimal number. exp10 must be larger or equal to 0 to work
    @type  mantissa_bits: int
    @param mantissa_bits: available bits for the mantissa, default to -1
    @type  exp_bits: int
    @param exp_bits: available bits for the exponent, defaults to -1
    @rtype: (list[int],list[int])
    @returns: the exponent and the mantissa of the coresponding IEE-754 floating point number
    """
    def convertInteger(num10: int, exp10: int, mantissa_bits=-1, exp_bits=-1):
        num10 = int(str(num10)+ exp10*"0")
        binary, exp = BitVecConvStatic.getBinary(num10, mantissa_bits+1, True)
        if exp != -1:
            binary = binary[1:]
            exp = BitVecConvStatic.getBiasedExponent(exp,exp_bits)
            exp = BitVecConvStatic.checkInf(exp, exp_bits)
            # exponent is too large
            if (all(i == 1 for i in exp)):
                return exp, ['0']*mantissa_bits
            return exp,binary
        elif exp == -1:
            return ['0']*exp_bits, binary[1:]

    """Converts the given number to IEE-bitvector assuming the absolut value is less than 1

    @type num10: int
    @param num10: the mantissa part of the decimal number
    @type exp10: int
    @param exp10: the exponent part of the decimal number, must be strictly negative to work
    @type exp_bits: int
    @param exp_bits: available bits for the exponent
    @type mantissa_bits: int
    @param mantissa_bits: available bits for the mantissa
    @type dropLeading1: bool
    @param dropLeading1: flag wether the leading 1 should be discarded (implicit leading 1)
    @rtype: (list[int],list[int])
    @returns: the exponent and the mantissa of the coresponding IEE-754 floating point number
    """
    def convertNumberLT1(num10: int, exp10: int, exp_bits: int , mantissa_bits: int, dropLeading1=True):
        num = num10
        comp = 10**-exp10
        leading_zeros = 0
        leading_one = not dropLeading1
        binary = []
        while len(binary) < mantissa_bits:
            if 2*num >= comp:
                num = num*2-comp
                if not leading_one:
                    leading_one = True
                    leading_zeros+=1
                else:
                    binary.append(1)
            else:
                num*=2
                if leading_one:
                    binary.append(0)
                else:
                    leading_zeros +=1
        unbiased_exp = -leading_zeros
        min_exp = -(2**(exp_bits-1)-1)
        # check for subnormal number
        if unbiased_exp <= min_exp:
            if dropLeading1:
                binary = [1] + binary
            numZerosFront = min_exp - unbiased_exp
            # TO-DO: not sure if this might cause problems if converting e.g 1+e where e is subnormal
            #propably should not cause problems because these bits wont ever make it into the signficant
            #might use test case to check that
            return exp_bits*[0], numZerosFront*[0] + binary
        return BitVecConvStatic.getBiasedExponent(unbiased_exp,exp_bits),binary

    """Formats the binary number into a bitvector string

    @type sign: int
    @param: the sign bit of the number
    @type exp: list[int]
    @param exp: the exponent bits of the number
    @type mant: list[int]
    @param mant: the mantissa bits of the number
    @rtype: str
    @returns concatenation of sign, exp, mant as string
    """
    def getFinalBitString(sign: int, exp:[int], mant:[int]) -> str:
        return str(sign)+''.join(map(str,exp ))+''.join(map(str,mant))


    """ Converts a decimal number into IEE-754 conform bitvector-string

    IMPORTANT: This method (for good reasons) only supports the conversion of strings,
               as the implicit conversion of int/float might bring problems, that are not obvious.
               Therefore it is considered a conversion of other types should be done
               explictly beforehand, such that a user is aware of the possible problems.
               Pyton defaults to double precision floats, such that a choosen fptypes
               would sometimes not be immideatly compatible when doing an implicit conversion.

    @type num: str
    @param num: the decimal number to convert
    @type fptype: FPType
    @param fptype: the floating point type to use
    @tpye rmode: RMode
    @param rmode: the rounding mode to use
    @type debug: bool
    @param debug: enables debugging by printing the bitvector value
    @rtype: str
    @returns: bitwise IEE-754 conform floating point representation
    """
    def convertToBinary(num: str, fptype, rmode=None, debug=False):
        if not isinstance(num,str):
            raise TypeError("This methods only supports conversion of strings."
                           +"If needed consider converting your number to string beforehand."
                           +"But be aware that this approach might bring problems e.g. when using non-double precision,"
                           +"because python defaults to double precision for its floats", num)
        exp_bits = fptype.value[0]
        mantissa_bits =fptype.value[1]
        result = ''

        if 'inf' in num:
            if '-' in num:
                s = 1
            else:
                s = 0
            result = BitVecConvStatic.getFinalBitString(s,['1']*exp_bits,['0']*mantissa_bits)
            if debug:
                print(result)
            return result

        s,num10, exp10 = BitVecConvStatic.convertToScientificNotation(num)

        if num10 == 0 and exp10 == 0:
            result = BitVecConvStatic.getFinalBitString(s,['0']*exp_bits,['0']*mantissa_bits)
        
        # integer case: Add necessary zeros & get binary format, exponent
        # ignore first 1 and compute biased exponent
        if exp10 >= 0:
            e,m = BitVecConvStatic.convertInteger(num10, exp10, mantissa_bits, exp_bits)
            result = BitVecConvStatic.getFinalBitString(s,e, BitVecConvStatic.round(s, m,mantissa_bits,rmode))
        elif -exp10 >= len(str(num10)):
            # problem: how to get enought bits for checking the to nearest case??
            e,m = BitVecConvStatic.convertNumberLT1(num10, exp10, exp_bits,mantissa_bits+additional_bits)
            result = BitVecConvStatic.getFinalBitString(s,e, BitVecConvStatic.round(s, m,mantissa_bits,rmode))
        # Splitt number appart and convert each one seperatly 
        # merge result together ..
        else:
            num_intpart = str(num10)[:exp10] + "0"*-exp10
            exp_intpart = str(exp10)
            sign, num, exp = BitVecConvStatic.convertToScientificNotation(num_intpart+"e"+exp_intpart)
            expbinary, intpartbinary = BitVecConvStatic.convertInteger(num, exp, -1, exp_bits)

            num_fract = int(str(num10)[exp10:])
            # same problem as above with number of bits for rounding
            remaining_bits = mantissa_bits -len(intpartbinary)
            #safety check for infinty
            if (remaining_bits == 0 and all(i == 1 for i in expbinary) and all(j == 0 for j in intpartbinary)):
                result = s, expbinary, intpartbinary
            remaining_bits += additional_bits
            expfract, fractbinary = BitVecConvStatic.convertNumberLT1(num_fract, exp10, exp_bits,remaining_bits,False)
            result = BitVecConvStatic.getFinalBitString(s, expbinary, BitVecConvStatic.round(s, intpartbinary + fractbinary,mantissa_bits,rmode))
        if debug:
            print(result)
        return result

    """Normalizes the decimal input number such that no dots are included, e.g.
    pulling these digits out of the exponent. Remainings 0 from the decimal
    are put into exponent

    @type item: str
    @param item: the decimal number to convert
    @rtype: list[int]
    @returns: an equivalent representation of the input number as sign, mant, exp
    """
    @staticmethod
    def convertToScientificNotation(item: str) -> [int]:
        if not 'e' in item:
            return BitVecConvStatic.convertToScientificNotation(item+'e0')
        item = item.replace(" ", "")
        splitted = re.split('e|E',item)
        preexp   = splitted[0]
        afterexp  = splitted[1]
        dotloc = preexp.find(".")
        # there is a dot in the number
        if dotloc > -1:
            x = preexp.split(".")
            afterdot = x[1]
            #shift number accordingly, remove dot and trailing zeros
            new_exp = int(afterexp)- len(afterdot)
            # make sure to also remove remaining zeros at the end
            return BitVecConvStatic.convertToScientificNotation(preexp.replace(".","").lstrip('0')+"e"+str(new_exp))
        # no dot in number then only remove remaining zeros at the end
        else:
            # default sign is +
            sign = 0
            # set and remove negative sign
            if preexp[0] == '-':
                sign = 1
                preexp = preexp.replace("-","")
            # always remove + sign
            preexp = preexp.replace("+","")
            # remaining zeros
            if all(i == '0' for i in preexp):
                return [sign, 0, 0]
            rightzeros = len(preexp) - len(preexp.rstrip('0'))
            if rightzeros > 0:
                return[sign, int(preexp.rstrip('0')), int(afterexp)+rightzeros]
            else:
                return[sign, int(preexp), int(afterexp)]
