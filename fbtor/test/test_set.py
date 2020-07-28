from fbtor.BitVecConvert import BitVecConvStatic
from fbtor.FBoolectorTypes import FPType, RMode, WIDTH
from pyboolector import Boolector

# TO-DO: Thinking about more test cases and check if existings are actually correct
# TO-DO: Test cases right now don't consider that fptype & rmode might have an influence!!

t = FPType.single
d = FPType.double
r = RMode.to_zero
n = RMode.to_nearest

set_fEq=  [ ("-0","+0",Boolector.SAT,t,r), ("-1","+1",Boolector.UNSAT,t,r), ("5e17","5e17",Boolector.SAT,t,r), ("5e17","5.000001e17",Boolector.UNSAT,t,r),
           ("2.0000001","2",Boolector.SAT,t,r),("3.403E38","inf",Boolector.SAT,t,r),("3.4025E38","inf",Boolector.UNSAT,t,r),
           ("1.5e-45","0",Boolector.UNSAT,t,n),("1e-46","0",Boolector.SAT,t,n)
          ]

set_fGtE= [ ("-0","+0",Boolector.SAT,t,r), ("-1","+1",Boolector.UNSAT,t,r), ("5e17","5e17",Boolector.SAT,t,r), ("5e17","5.000001e17",Boolector.UNSAT,t,r),
            ("2.0000001","2",Boolector.SAT,t,r),("1.797693e308","inf",Boolector.UNSAT,d,r), ("1.797694e308","inf",Boolector.SAT,d,r)
          ]

set_fLtE= [ ("+0","-0",Boolector.SAT,d,r), ("-1","+1",Boolector.SAT,d,r), ("5e17","5e17",Boolector.SAT,d,r), ("5e17","5.000001e17",Boolector.SAT,d,r),
            ("2.0000001","2",Boolector.UNSAT,d,r),("-1.797693e308","-inf",Boolector.UNSAT,d,r), ("-1.797694e308","-inf",Boolector.SAT,d,r)
          ]

set_fGt=  [ ("-0","0",Boolector.UNSAT,d,r), ("-1","+1",Boolector.UNSAT,d,r), ("5e17","5e17",Boolector.UNSAT,d,r), ("5e17","5.000001e17",Boolector.UNSAT,d,r),
            ("2.0000001","2",Boolector.SAT,d,r), ("-3","-8",Boolector.SAT,d,r), ("-123","-123",Boolector.UNSAT,d,r), ("-25.1","-25.11",Boolector.SAT,d,r), ("1.797693e308","inf",Boolector.UNSAT,d,r), ("inf","inf",Boolector.UNSAT,d,r),("-inf","inf",Boolector.UNSAT,d,r)
          ]

set_fLt=  [ ("0","0",Boolector.UNSAT,t,r), ("-1","+1",Boolector.SAT,t,r), ("5e17","5e17",Boolector.UNSAT,t,r), ("5e17","5.000001e17",Boolector.SAT,t,r),
            ("2.0000001","2",Boolector.UNSAT,t,r), ("-1.797693e308","-inf",Boolector.UNSAT,d,r), ("-inf","-inf",Boolector.UNSAT,d,r),
            ("-inf","inf",Boolector.SAT,d,r),("3.724e-40","3.74e-40",Boolector.SAT,t,n),("1e-40","4",Boolector.SAT,t,n),
            ("3.724e-40","-3.74e-40",Boolector.UNSAT,t,n),("1e-40","-4",Boolector.UNSAT,t,n)
          ]

set_fSign=[ ('-inf',"1",t,r), ("-5.12e3","1",t,r), ("-2.17e-4","1",t,r), ("-0","1",t,r), ("-3.72E-40","1",t,r),("-1.75E308","1",d,n),
            ("+inf","0",t,r), ("+5.12e3","0",t,r), ("+2.17e-4","0",t,r), ("+0","0",t,r), ("+3.72E-40","0",t,r),("+1.75E308","0",d,n)
          ]

set_fExponent=[ ('-inf',"11111111",t,r),("-5.12e3","10001011",t,r),("-2.17e-4","01110010",t,r), ("-0","00000000",t,r), ("-3.72E-40","00000000",t,r),
                ("+inf","11111111",t,r),("+5.12e3","10001011",t,r),("+2.17e-4","01110010",t,r), ("+0","00000000",t,r), ("+3.72E-40","00000000",t,r),
                ("-1.75E308","11111111110",d,n), ("+1.75E308","11111111110",d,n),
                ("1e-40"    ,"011111101111010",FPType.extended,r),
                ("-1.25e200","100001010010111",FPType.extended,r),
              ]

set_fMantisse=[ ('-inf',"00000000000000000000000",t,n), ("-5.12e3"  ,"01000000000000000000000",t,n), ("-2.17e-4","11000111000101001111110",t,n),
                ("-0"  ,"00000000000000000000000",t,n), ("-3.72E-40","00001000000110011111100",t,n),
                ("+inf","00000000000000000000000",t,n), ("+5.12e3"  ,"01000000000000000000000",t,n), ("+2.17e-4","11000111000101001111110",t,n),
                ("+0"  ,"00000000000000000000000",t,n), ("+3.72E-40","00001000000110011111100",t,n),
                ("-1.75E308","1111001001101010101000101010010111001001111100011000",d,n),
                ("+1.75E308","1111001001101010101000101010010111001001111100011000",d,n),
                ("1e-40"    ,"0001011011000010011000100111011101110101011110011100010110001100",FPType.extended,n),
                ("-1.25e200","1010001000001101111100001101110011010011101011110000101110010000",FPType.extended,n),
              ]

set_fAdd= [ ("0","0","0",t,r), ("1","0","1",t,r), ("0","1","1",t,r), ("-1","0","-1",t,r), ("0","-1","-1",t,r), ("1","-1","0",t,r), ("-1","1","0",t,r),
            ("1","1e-40","1",t,r), ("5","-2","3",t,r), ("1","1e-15","1.000000000000001",t,r), ("1","-1e-15","0.999999999999999",t,r), ("1","0.5","1.5",t,RMode.to_pos_inf)
            ,("1","3e-8","1.00000003",t,RMode.to_nearest)
            ]

set_fSub= [ ("1","1","0",t,r)
          ]

set_fMul= [ ("1","1","1",t,r), ("1","-1","-1",t,r), ("-1","1","-1",t,r), ("-1","-1","1",t,r),
            ("2","1","2",t,r), ("1","2","2",t,r), ("2","2","4",t,r), ("3","3","9",t,r), ("0.5","2","1",t,r),
            ("1e-40","1","1e-40",t,r), ("1e-40","1e-20","1e-60",t,r), ("1e-20","1e-40","1e-60",t,r)
          ]

set_fDiv= [ ("1","1","1",t,r), ("1","-1","-1",t,r), ("-1","1","-1",t,r), ("-1","-1","1",t,r),
            ("2","1","2",t,r), ("1","2","0.5",t,r), ("2","2","1",t,r), ("3","3","1",t,r), ("0.5","2","0.25",t,r),
            ("1e-40","1","1e-40",t,r), ("1e-40","1e20","1e-60",t,r), ("1e-20","1e40","1e-60",t,r)
          ]

set_fConvert = [ 
            
          ]