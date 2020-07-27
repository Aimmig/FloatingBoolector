import enum

#Some constants for indexing the FPTypes
EXP = 0
MAN = 1
WIDTH = 2

#enum type for floating point type
class FPType(enum.Enum):
    single = [8,23,32]
    double = [11,52,64]
    extended = [15,64,80]

#enum type for rounding mode
class RMode(enum.Enum):
    to_zero = 0
    to_neg_inf = -1
    to_pos_inf = 1
    to_nearest = 2
