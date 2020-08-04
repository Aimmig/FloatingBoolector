from fbtor.BitVecConvert import BitVecConvStatic
from fbtor.FBoolectorTypes import FPType, RMode, WIDTH
from pyboolector import Boolector

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

set_fNeg = [("-0","+0"),("+1","-1"), ("5e17","-5e17"), ("-inf","+inf")]

set_fAdd= [ ("0","0","0",t,r), ("1","0","1",t,r), ("0","1","1",t,r), ("-1","0","-1",t,r), ("0","-1","-1",t,r), ("1","-1","0",t,r), ("-1","1","0",t,r),
            ("1","1e-40","1",t,r), ("5","-2","3",t,r), ("1","1e-15","1.000000000000001",t,r), ("1","-1e-15","0.999999999999999",t,r),
            ("1e-40","1e-40","2e-40",t,r),
            ("1","0.5","1.5",t,RMode.to_pos_inf),
            ("1","3e-8","1.00000003",t,RMode.to_nearest)
            ]

set_fSub= [ ("1","1","0",t,r)
          ]

set_fMul= [ ("1","1","1",t,r), ("1","-1","-1",t,r), ("-1","1","-1",t,r), ("-1","-1","1",t,r),
            ("2","1","2",t,r), ("1","2","2",t,r), ("2","2","4",t,r), ("3","3","9",t,r), ("0.5","2","1",t,r),
            ("1e-40","1","1e-40",t,r), ("1e-40","1e-2","1e-42",t,r), ("1e-2","1e-40","1e-42",t,r)
          ]

set_fDiv= [ ("1","1","1",t,r), ("1","-1","-1",t,r), ("-1","1","-1",t,r), ("-1","-1","1",t,r),
            ("2","1","2",t,r), ("1","2","0.5",t,r), ("2","2","1",t,r), ("3","3","1",t,r), ("0.5","2","0.25",t,r),
            ("1e-40","1","1e-40",t,r), ("1e-40","1e2","1e-42",t,r), ("1e-41","0.25","4e-41",t,r), ("1","1e-40","1e40",t,r),
            ("1e-20","1e20","1e-40",t,r), ("1e-40","1e-40","1",t,r)
          ]

set_fSqrt=[ ("1",1,"1",t,r), ("2",5,"1.41421356237",t,r), ("0.25",1,"0.5",t,r), ("0.5",5,"0.70710678118",t,r), ("100",5,"10",t,r)
          ]

set_fConvert= [ (0,8,"0",t,r), (0,8,"-0",t,r), (1,8,"1",t,r), (-1,8,"-1",t,r), (127,8,"127",t,r), (-128,8,"-128",t,r),
            (4096,16,"4096",t,r)
          ]
          
set_Convert= [ ("0",8,0,t,r), ("-0",8,0,t,r), ("1",8,1,t,r), ("-1",8,-1,t,r),
            ("127",8,127,t,r), ("128",8,0,t,r), ("-127",8,-127,t,r), ("-128",8,-128,t,r), ("-129",8,0,t,r)
          ]