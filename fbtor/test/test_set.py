from fbtor.BitVecConvert import FPType, RMode, BitVecConvStatic, WIDTH
from pyboolector import Boolector

# TO-DO: Thinking about more test cases and check if existings are actually correct
# TO-DO: Test cases right now don't consider that fptype & rmode might have an influence!!

t = FPType.single
d = FPType.double
r = RMode.to_zero

set_fEq=  [ ("-0","+0",Boolector.SAT,t,r), ("-1","+1",Boolector.UNSAT,t,r), ("5e17","5e17",Boolector.SAT,t,r), ("5e17","5.000001e17",Boolector.UNSAT,t,r),
           ("2.0000001","2",Boolector.SAT,t,r)
          ]

set_fGtE= [ ("-0","+0",Boolector.SAT,t,r), ("-1","+1",Boolector.UNSAT,t,r), ("5e17","5e17",Boolector.SAT,t,r), ("5e17","5.000001e17",Boolector.UNSAT,t,r),
            ("2.0000001","2",Boolector.SAT,t,r)
          ]

set_fLtE= [ ("+0","-0",Boolector.SAT,d,r), ("-1","+1",Boolector.SAT,d,r), ("5e17","5e17",Boolector.SAT,d,r), ("5e17","5.000001e17",Boolector.SAT,d,r),
            ("2.0000001","2",Boolector.UNSAT,d,r)
          ]

set_fGt=  [ ("-0","0",Boolector.UNSAT,d,r), ("-1","+1",Boolector.UNSAT,d,r), ("5e17","5e17",Boolector.UNSAT,d,r), ("5e17","5.000001e17",Boolector.UNSAT,d,r),
            ("2.0000001","2",Boolector.SAT,d,r), ("-3","-8",Boolector.SAT,d,r), ("-123","-123",Boolector.UNSAT,d,r), ("-25.1","-25.11",Boolector.SAT,d,r)
          ]

set_fLt=  [ ("0","0",Boolector.UNSAT,t,r), ("-1","+1",Boolector.SAT,t,r), ("5e17","5e17",Boolector.UNSAT,t,r), ("5e17","5.000001e17",Boolector.SAT,t,r),
            ("2.0000001","2",Boolector.UNSAT,t,r)
          ]

set_fSign=[ ('-inf',"1",t,r), ("-5.12e3","1",t,r), ("-2.17e-4","1",t,r), ("-0","1",t,r), ("-3.72E-40","1",t,r),
            ("+inf","0",t,r), ("+5.12e3","0",t,r), ("+2.17e-4","0",t,r), ("+0","0",t,r), ("+3.72E-40","0",t,r)
          ]

set_fMul= [ ("1","1","1",t,r), ("1","-1","-1",t,r), ("-1","1","-1",t,r), ("-1","-1","1",t,r),
            ("2","1","2",t,r), ("1","2","2",t,r), ("2","2","4",t,r), ("3","3","9",t,r)
          ]
