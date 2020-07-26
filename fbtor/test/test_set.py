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

set_fSign=[ ('-inf',"1",t,r), ("-5.12e3","1",t,r), ("-2.17e-4","1",t,r), ("-0","1",t,r), ("-3.72E-40","1",t,r),
            ("+inf","0",t,r), ("+5.12e3","0",t,r), ("+2.17e-4","0",t,r), ("+0","0",t,r), ("+3.72E-40","0",t,r)
          ]

set_fAdd= [ ("0","0","0",t,r), ("1","0","1",t,r), ("0","1","1",t,r), ("-1","0","-1",t,r), ("0","-1","-1",t,r), ("1","-1","0",t,r), ("-1","1","0",t,r),
            ("1","1e-40","1",t,r), ("5","-2","3",t,r)
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
