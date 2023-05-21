#!/usr/bin/env python3

from sympy import *
import numpy

class ElepticalArray:
    def __init__(self, indexes, negative=False):
        self.indexes = indexes
        self.negative = negative

    def __str__(self):
        return "ElepticalArray({},{})".format(self.indexes, "negative" if self.negative else "positive")

    def reorder_with_last(self, index, drop=False):
        return self.reorder_with_moving(index, len(self.indexes) - 1, drop)

    def reorder_with_first(self, index, drop=False):
        return self.reorder_with_moving(index, 0, drop)

    def reorder_with_moving(self, index, position, drop=False):
        if not index in self.indexes:
            raise Exception("Index not found")

        new_indexes = self.indexes.copy()
        new_indexes.remove(index)
        if not drop:
            new_indexes.insert(position, index)
        need_to_negate = (self.indexes.index(index) - position) % 2 == 1

        return ElepticalArray(new_indexes, not self.negative if need_to_negate else self.negative)

    def copy(self):
        return ElepticalArray(self.indexes.copy(), self.negative)

    def is_sorted(self):
        for i in range(len(self.indexes) - 1):
            if self.indexes[i] > self.indexes[i + 1]:
                return False
        return True

    def sorted(self):
        return self.sorted_as_template(sorted(self.indexes))

    def sorted_as_template(self, template):
        c = self.copy()
        sorted_indexes = template
        for idx in range(len(sorted_indexes)):
            c = c.reorder_with_moving(sorted_indexes[idx], idx)
        return c


class CliffordMulter:
    def __init__(self, eleptical_ones=[], dual_ones=[],  total_elipse=[], total_dual=[], negative=False, null=False):
        self.dual_ones = dual_ones
        self.eleptical_ones = ElepticalArray(eleptical_ones, negative)
        self.total_elipse = total_elipse
        self.total_dual = total_dual
        self.null = null

    def real(self):
        return CliffordMulter(self.eleptical_ones.indexes, [], self.total_elipse, self.total_dual, self.eleptical_ones.negative)

    def is_null(self):
        return self.null

    def sign(self):
        return -1 if self.eleptical_ones.negative else 1

    def grade(self):
        return len(self.dual_ones) + len(self.eleptical_ones.indexes)

    def antigrade(self):
        return len(self.total_elipse) + len(self.total_dual) - self.grade()

    def reverse(self):
        gr = self.grade()
        s = gr*(gr-1)/2
        sign = (-1)**s
        neg = sign == -1
        negative = neg != self.eleptical_ones.negative
        return CliffordMulter(self.eleptical_ones.indexes, self.dual_ones, self.total_elipse, self.total_dual, negative)

    # def left_complement(self):

    def prod(self, other):
        for x in self.dual_ones:
            for y in other.dual_ones:
                return CliffordMulter(null=True)

        dual_ones = self.dual_ones + other.dual_ones

        indexes_common = set(self.eleptical_ones.indexes).intersection(
            set(other.eleptical_ones.indexes))

        a_eleptical = self.eleptical_ones
        b_eleptical = other.eleptical_ones

        for x in indexes_common:
            a_eleptical = a_eleptical.reorder_with_last(x, drop=True)
            b_eleptical = b_eleptical.reorder_with_first(x, drop=True)

        eleptical_ones = a_eleptical.indexes + b_eleptical.indexes
        negative = a_eleptical.negative != b_eleptical.negative

        eleptical_array = ElepticalArray(eleptical_ones, negative)
        eleptical_array = eleptical_array.sorted()
        eleptical_array_as_tuple = tuple(eleptical_array.indexes)
        canonical_form = CliffordAlgebra301.canonical_formes[eleptical_array_as_tuple]
        eleptical_array = eleptical_array.sorted_as_template(canonical_form)

        return CliffordMulter(eleptical_array.indexes, dual_ones, self.total_elipse, self.total_dual, negative=eleptical_array.negative)

    def antiprod(self, other):
        return self.prod(other).reverse()

    def __str__(self):
        if len(self.dual_ones) == 0 and len(self.eleptical_ones.indexes) == 0:
            return "e"

        es = "".join(f"{i}" for i in self.eleptical_ones.indexes)
        base = "e_"
        ds = "".join(f"{i}" for i in self.dual_ones)

        sign = "-" if self.eleptical_ones.negative else ""
        return sign+base + ds + es

    def __repr__(self):
        return self.__str__()

    def symbol_name(self):
        if len(self.dual_ones) == 0 and len(self.eleptical_ones.indexes) == 0:
            return "e"

        es = "".join(f"{i}" for i in self.eleptical_ones.indexes)
        base = "e_"
        ds = "".join(f"{i}" for i in self.dual_ones)

        return base + ds + es

    def symbol(self):
        a = self.symbol_name()
        sign = -1 if self.eleptical_ones.negative else +1
        return CliffordAlgebra301.canonical_symbols[f"{a}"] * sign


class CliffordGeometrySymbol(Symbol):
    def __new__(cls, name, *args, **kwargs):
        return super().__new__(cls, name, commutative=False)

    def __init__(self, name, ellipse, dual, total_elipse, total_dual, negative=False):
        super().__init__()
        self.multer = CliffordMulter(
            ellipse, dual,  total_elipse, total_dual, negative)

    @staticmethod
    def from_multer(multer, eones, dones):
        return multer.symbol()

    @staticmethod
    def clifford_product(a, b):
        aname = a.name
        bname = b.name

        name_to_index = { "e" : 0,
                            "e_1" : 1,
                            "e_2" : 2,
                            "e_3" : 3,
                            "e_4" : 4,
                            "e_23" : 5,
                            "e_31" : 6,
                            "e_12" : 7,
                            "e_43" : 8,
                            "e_42" : 9,
                            "e_41" : 10,
                            "e_321" : 11,
                            "e_412" : 12,
                            "e_431" : 13,
                            "e_423" : 14,
                            "e_4321" : 15}

        e, e_1, e_2, e_3, e_4, e_23, e_31, e_12, e_43, e_42, e_41, e_321, e_412, e_431, e_423, e_4321 = CliffordAlgebra301.basis

        table = [
            [     e,     e_1,     e_2,     e_3,     e_4,   e_23,   e_31,    e_12,    e_43,     e_42,    e_41,  e_321,   e_412,   e_431,  e_423, e_4321],
            [   e_1,       e,    e_12,   -e_31,   -e_41, -e_321,   -e_3,     e_2,   e_431,   -e_412,    -e_4,  -e_23,   -e_42,    e_43, e_4321,  e_423],
            [   e_2,   -e_12,       e,    e_23,   -e_42,    e_3, -e_321,    -e_1,  -e_423,     -e_4,   e_412,  -e_31,    e_41,  e_4321,  -e_43,  e_431], 
            [   e_3,    e_31,   -e_23,       e,   -e_43,   -e_2,     e_1,  -e_321,   -e_4,    e_423,  -e_431,  -e_12,  e_4321,   -e_41,   e_42,  e_412],
            [   e_4,    e_41,    e_42,    e_43,       0,  e_423,   e_431,   e_412,      0,        0,       0, e_4321,       0,       0,      0,      0],
            [  e_23,  -e_321,    -e_3,     e_2,   e_423,     -1,   -e_12,    e_31,    e_42,   -e_43, -e_4321,    e_1,   e_431,  -e_412,   -e_4,   e_41],
            [  e_31,     e_3,  -e_321,    -e_1,   e_431,   e_12,      -1,   -e_23,   -e_41, -e_4321,    e_43,    e_2,  -e_423,    -e_4,  e_412,   e_42],
            [  e_12,    -e_2,     e_1,  -e_321,   e_412,  -e_31,    e_23,      -1, -e_4321,    e_41,   -e_42,    e_3,    -e_4,   e_423, -e_431,   e_43],
            [  e_43,   e_431,  -e_423,     e_4,       0,  -e_42,    e_41, -e_4321,       0,       0,       0, -e_412,       0,       0,      0,      0],
            [  e_42,  -e_412,     e_4,   e_423,       0,   e_43, -e_4321,   -e_41,       0,       0,       0, -e_431,       0,       0,      0,      0], 
            [  e_41,     e_4,   e_412,  -e_431,       0, -e_4321,  -e_43,    e_42,       0,       0,       0, -e_423,       0,       0,      0,      0],
            [ e_321,   -e_23,   -e_31,   -e_12, -e_4321,     e_1,    e_2,     e_3,   e_412,   e_431,   e_423,     -1,   -e_43,   -e_42,  -e_41,    e_4],
            [ e_412,   -e_42,    e_41, -e_4321,       0,  -e_431,  e_423,    -e_4,       0,       0,       0,   e_43,       0,       0,      0,      0],
            [ e_431,    e_43, -e_4321,   -e_41,       0,   e_412,   -e_4,  -e_423,       0,       0,       0,   e_42,       0,       0,      0,      0],
            [ e_423, -e_4321,   -e_43,    e_42,       0,    -e_4, -e_412,   e_431,       0,       0,       0,   e_41,       0,       0,      0,      0],
            [e_4321,  -e_423,  -e_431,  -e_412,       0,    e_41,   e_42,    e_43,       0,       0,       0,   -e_4,       0,       0,      0,      0]
        ]
        a_index = name_to_index[aname]
        b_index = name_to_index[bname]
        return Mul(table[a_index][b_index])

    def __mul__(self, other):
        if isinstance(other, CliffordGeometrySymbol):
            return self.clifford_product(self, other)
        else:
            return super().__mul__(other)

    def __div__(self, other):
        if isinstance(other, CliffordGeometrySymbol):
            multer = self.multer.proddiv(other.multer)
            if multer.is_null():
                return Add()
            return multer.symbol()
        else:
            return super().__div__(other)

    def __pow__(self, power, modulo=None):
        if power == 0:
            return self * 0
        if power == 2:
            return self * self
        else:
            raise Exception("Not implemented")

    def grade(self):
        return self.multer.grade()

    def reverse(self):
        return self.multer.reverse().symbol()

    def is_dual(self):
        return len(self.multer.dual_ones) > 0

    def real(self):
        multer = self.multer.real()
        if multer.is_null():
            return Add()
        return multer.symbol()


class CliffordAlgebra301:
    eleptical_ones = [1, 2, 3]
    dual_ones = [4]
    e = CliffordGeometrySymbol("e", [], [], eleptical_ones, dual_ones)
    e_1 = CliffordGeometrySymbol("e_1", [1], [], eleptical_ones, dual_ones)
    e_2 = CliffordGeometrySymbol("e_2", [2], [], eleptical_ones, dual_ones)
    e_3 = CliffordGeometrySymbol("e_3", [3], [], eleptical_ones, dual_ones)
    e_4 = CliffordGeometrySymbol("e_4", [], [4], eleptical_ones, dual_ones)
    e_23 = CliffordGeometrySymbol(
        "e_23", [2, 3], [], eleptical_ones, dual_ones)
    e_31 = CliffordGeometrySymbol(
        "e_31", [3, 1], [], eleptical_ones, dual_ones)
    e_12 = CliffordGeometrySymbol(
        "e_12", [1, 2], [], eleptical_ones, dual_ones)

    e_41 = CliffordGeometrySymbol("e_41", [1], [4], eleptical_ones, dual_ones)
    e_42 = CliffordGeometrySymbol("e_42", [2], [4], eleptical_ones, dual_ones)
    e_43 = CliffordGeometrySymbol("e_43", [3], [4], eleptical_ones, dual_ones)

    e_321 = CliffordGeometrySymbol(
        "e_321", [3, 2, 1], [], eleptical_ones, dual_ones)

    e_423 = CliffordGeometrySymbol(
        "e_423", [2, 3], [4], eleptical_ones, dual_ones)
    e_431 = CliffordGeometrySymbol(
        "e_431", [3, 1], [4], eleptical_ones, dual_ones)
    e_412 = CliffordGeometrySymbol(
        "e_412", [1, 2], [4], eleptical_ones, dual_ones)

    e_4321 = CliffordGeometrySymbol(
        "e_4321", [3, 2, 1], [4], eleptical_ones, dual_ones)

    canonical_formes = {
        (1, 2, 3): (3, 2, 1),
        (2, 3): (2, 3),
        (1, 3): (3, 1),
        (1, 2): (1, 2),
        (1,): (1,),
        (2,): (2,),
        (3,): (3,),
        (): ()
    }
    
    canonical_symbols = {
        "e_321": e_321,
        "e_23": e_23,
        "e_12": e_12,
        "e_31": e_31,
        "e_1": e_1,
        "e_2": e_2,
        "e_3": e_3,
        "e_4": e_4,
        "e": e,
        "e_4321": e_4321,
        "e_423": e_423,
        "e_412": e_412,
        "e_431": e_431,
        "e_41": e_41,
        "e_42": e_42,
        "e_43": e_43
    }

    index_to_pos = {
        0: 0,
        1: 1,
        2: 2,
        3: 3,
        4: 4,
        23 : 5,
        31 : 6,
        12 : 7,
        43 : 8,
        42 : 9,
        41 : 10,
        321 : 11,
        412 : 12,
        431 : 13,
        423 : 14,
        4321 : 15}

    canonical_symbols_ordered = [ e, e_1, e_2, e_3, e_4, e_23, e_31, e_12, e_43, e_42, e_41, e_321, e_412, e_431, e_423, e_4321] 

    basis = canonical_symbols_ordered

var("a a_1 a_2 a_3 a_4 a_12 a_23 a_31 a_41 a_42 a_43 a_412 a_423 a_431 a_321 a_4321")
var("b b_1 b_2 b_3 b_4 b_12 b_23 b_31 b_41 b_42 b_43 b_412 b_423 b_431 b_321 b_4321")

a1 = a_1
a2 = a_2
a3 = a_3
a4 = a_4
a12 = a_12
a23 = a_23
a31 = a_31
a41 = a_41
a42 = a_42
a43 = a_43
a412 = a_412
a423 = a_423
a431 = a_431
a321 = a_321
a4321 = a_4321

b1 = b_1
b2 = b_2
b3 = b_3
b4 = b_4
b12 = b_12
b23 = b_23
b31 = b_31
b41 = b_41
b42 = b_42
b43 = b_43
b412 = b_412
b423 = b_423
b431 = b_431
b321 = b_321
b4321 = b_4321

e = CliffordAlgebra301.e
e1 = CliffordAlgebra301.e_1
e2 = CliffordAlgebra301.e_2
e3 = CliffordAlgebra301.e_3
e4 = CliffordAlgebra301.e_4
e12 = CliffordAlgebra301.e_12
e23 = CliffordAlgebra301.e_23
e31 = CliffordAlgebra301.e_31
e41 = CliffordAlgebra301.e_41
e42 = CliffordAlgebra301.e_42
e43 = CliffordAlgebra301.e_43
e412 = CliffordAlgebra301.e_412
e423 = CliffordAlgebra301.e_423
e431 = CliffordAlgebra301.e_431
e321 = CliffordAlgebra301.e_321
e4321 = CliffordAlgebra301.e_4321

AS = a*e
AV = a1*e1 + a2*e2 + a3*e3 + a4*e4
AB = a12*e12 + a23*e23 + a31*e31 + a41*e41 + a42*e42 + a43*e43
AT = a412*e412 + a423*e423 + a431*e431 + a321*e321
AP = a4321*e4321
AAA = AS + AV + AB + AT + AP

BS = b*e
BV = b1*e1 + b2*e2 + b3*e3 + b4*e4
BB = b12*e12 + b23*e23 + b31*e31 + b41*e41 + b42*e42 + b43*e43
BT = b412*e412 + b423*e423 + b431*e431 + b321*e321
BP = b4321*e4321
BBB = BS + BV + BB + BT + BP

def eval_ga(M):
    def ga_eval_mul(M):
            symbols = M.args
            symbols = [s for s in symbols if isinstance(s, CliffordGeometrySymbol)]
            nonsymbols = [s for s in M.args if not isinstance(s, CliffordGeometrySymbol)]

            if len(symbols) == 0:
                return M

            else:
                val = CliffordAlgebra301.e
                for s in symbols:
                    val *= s
                val *= Mul(*nonsymbols)
                return val
            
    
    # get list of sum parts:
    S = expand(M)
    
    ret = []
    if isinstance(S, Mul):
        ret.append(ga_eval_mul(S))
    elif isinstance(S, Add):
        parts = S.args
        for part in parts:
            if isinstance(part, Mul):
                ret.append(ga_eval_mul(part))
            else:
                ret.append(part)

    #create new sum
    return Add(*ret)

def ga_eval(M):
    return eval_ga(M)

def args_with_ga(M, symbol):
    S = expand(M)
    parts = S.args

    ret = []
    for part in parts:
        if isinstance(part, Mul):
            mul_parts = part.args
            if symbol in mul_parts:
                mul_parts_without_symbol = [s for s in mul_parts if s != symbol]
                if len(mul_parts_without_symbol) > 0:
                    ret.append(Mul(*mul_parts_without_symbol))
                else:
                    ret.append(1)

    return Add(*ret) * symbol
            
def ga_grade(M, grade):
    S = expand(M)
    parts = S.args

    ret = []
    for part in parts:
        if isinstance(part, Mul):
            mul_parts = part.args
            for mul_part in mul_parts:
                if isinstance(mul_part, CliffordGeometrySymbol):
                    if mul_part.grade() == grade:
                        ret.append(part)
               

    return Add(*ret)

def ga_as_dict(M):
    def ga_as_dict_mul(M, ret):
            mul_parts = M.args
            for mul_part in mul_parts:
                if isinstance(mul_part, CliffordGeometrySymbol):
                    part_removed = ga_remove_clifford_geometry_symbol(M)
                    if mul_part in ret:
                        ret[mul_part] += part_removed
                    else:
                        ret[mul_part] = part_removed

    S = expand(M)
    parts = S.args

    ret = {}
    if isinstance(M, Add):
        for part in parts:
            if isinstance(part, Mul):
                ga_as_dict_mul(part, ret)
    else:
        ga_as_dict_mul(M, ret)

    return ret

def ga_remove_clifford_geometry_symbol(mul):
    parts = mul.args
    ret = []
    for part in parts:
        if isinstance(part, CliffordGeometrySymbol):
            continue
        else:
            ret.append(part)
    return Mul(*ret)


def ga_as_vector(M, grades=[0,1,2,3,4]):
    dct = ga_as_dict(M)
    ret = []
    order_grade_0 = [e]
    order_grade_1 = [e1, e2, e3, e4]
    order_grade_2 = [e23, e31, e12, e43, e42, e41]
    order_grade_3 = [e321, e412, e431, e423]
    order_grade_4 = [e4321]

    order_grades = {0: order_grade_0, 1: order_grade_1, 2: order_grade_2, 3: order_grade_3, 4: order_grade_4}

    for grade in grades:
        order = order_grades[grade]
        for o in order:
            if o in dct:
                val = dct[o]
                ret.append(val)
            else:
                ret.append(0)
    return ret

A = ga_grade(AAA,0) + ga_grade(AAA,2) + ga_grade(AAA,4)
B = ga_grade(BBB,0) + ga_grade(BBB,2) + ga_grade(BBB,4)

C = eval_ga(A * B)

C = ga_as_dict(C)
print("A*B")
for s,c in C.items():
    print("{:7} : {}".format(str(s), str(c)))

B_vect = ga_as_vector(B, grades=[0,2,4])
A_vect = ga_as_vector(A, grades=[0,2,4])
print("B")
for i,l in enumerate(B_vect):
    if l != 0:
        print("{:7} : {}".format(i, str(l)))

Amat = Matrix([
    [    a,   a_23,   a_31,   a_12,      0,    0,      0,    0],
    [ a_23,      a,   a_12,  -a_31,      0,    0,      0,    0],
    [ a_31,  -a_12,      a,   a_23,      0,    0,      0,    0],
    [ a_12,   a_31,  -a_23,      a,      0,    0,      0,    0],
    [ a_41, a_4321,   a_43,  -a_42,      a, a_12,  -a_31, a_23],
    [ a_42,  -a_43, a_4321,   a_41,  -a_12,    a,   a_23, a_31],
    [ a_43,   a_42,  -a_41, a_4321,   a_31, -a_23,     a, a_12],
    [a_4321, -a_41,  -a_42,  -a_43,  -a_23, -a_31, -a_12,    a]
])

#print(eval_ga(CliffordAlgebra301.e_1 * CliffordAlgebra301.e_23.reverse()))
#exit()

#Amat = Matrix([[0]*16]*16)
""" for i in range(5,11):
    for j in range(5,11):
        i_symbol = CliffordAlgebra301.canonical_symbols_ordered[i]
        j_symbol = CliffordAlgebra301.canonical_symbols_ordered[j]
        j_symbol_is_dual = j_symbol.is_dual()
        i_symbol_is_dual = i_symbol.is_dual()

        if j_symbol_is_dual and not i_symbol_is_dual:
            continue
            
        j_symbol = j_symbol.reverse()
        
        Amat[i,j] = eval_ga(i_symbol / j_symbol)

pprint(Amat) """

#exit()

Amat_conjugate = Matrix([
    [    a,   -a_23,   -a_31,   -a_12,      0,    0,      0,    0],
    [ -a_23,      a,   -a_12,  a_31,      0,    0,      0,    0],
    [ -a_31,  a_12,      a,   -a_23,      0,    0,      0,    0],
    [ -a_12,   -a_31,  a_23,      a,      0,    0,      0,    0],
    [ -a_41, a_4321,   -a_43,  a_42,      a, -a_12,  a_31, -a_23],
    [ -a_42,  a_43, a_4321,   -a_41,  a_12,    a,   -a_23, -a_31],
    [ -a_43,   -a_42,  a_41, a_4321,   -a_31, a_23,     a, -a_12],
    [a_4321, a_41,  a_42,  a_43,  a_23, a_31, a_12,    a]
])

Bvect = Matrix(B_vect).reshape(8,1)
Avect = Matrix(A_vect).reshape(8,1)
Bvect_reverse = Matrix(B_vect).reshape(1,8)

print("C1")
C1 = Amat*Bvect
pprint(C1)

Bmat_reverse = Matrix([
    [b,     b_23,  b_31,  b_12,    b_41,    b_42,   b_43, b_4321],
    [b_23,     b,  b_12, -b_31,  b_4321,    b_43,  -b_42,  -b_41],
    [b_31, -b_12,     b,  b_23,   -b_43,  b_4321,   b_41,  -b_42],
    [b_12,  b_31,  -b_23,    b,    b_42,   -b_41, b_4321,  -b_43],
    [0,        0,     0,     0,       b,    b_12,  -b_31,  -b_23],
    [0,        0,     0,     0,   -b_12,       b,   b_23,  -b_31],
    [0,        0,     0,     0,    b_31,   -b_23,      b,  -b_12],
    [0,        0,     0,     0,    b_23,    b_31,   b_12,      b]
]).transpose()

Amat_reverse = Matrix([
    [a,     a_23,  a_31,  a_12,    a_41,    a_42,   a_43, a_4321],
    [a_23,     a,  a_12, -a_31,  a_4321,    a_43,  -a_42,  -a_41],
    [a_31, -a_12,     a,  a_23,   -a_43,  a_4321,   a_41,  -a_42],
    [a_12,  a_31,  -a_23,    a,    a_42,   -a_41, a_4321,  -a_43],
    [0,        0,     0,     0,       a,    a_12,  -a_31,  -a_23],
    [0,        0,     0,     0,   -a_12,       a,   a_23,  -a_31],
    [0,        0,     0,     0,    a_31,   -a_23,      a,  -a_12],
    [0,        0,     0,     0,    a_23,    a_31,   a_12,      a]
]).transpose()

Reverse = Matrix([
    [1,     0,  0,  0,    0,    0,   0, 0],
    [0,     -1,  0,  0,    0,    0,   0, 0],
    [0,     0,  -1,  0,    0,    0,   0, 0],
    [0,     0,  0,  -1,    0,    0,   0, 0],
    [0,     0,  0,  0,    -1,    0,   0, 0],
    [0,     0,  0,  0,    0,    -1,   0, 0],
    [0,     0,  0,  0,    0,    0,   -1, 0],
    [0,     0,  0,  0,    0,    0,   0, 1]
])


Reverse16 = Matrix.diag([1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 1])

Avect_reverse = Matrix(A_vect).reshape(1,8)


C = Amat * Bvect - Bmat_reverse * Avect
print(C)
print("C")
for i,l in enumerate(C):
    print("{:7} : {}".format(i, str(l)))

print("A")
pprint(Amat)
print("AUUUU")
pprint(Reverse * Amat_conjugate * Reverse - Amat)
pprint(Amat_reverse - Amat)

pprint(Reverse * Amat_conjugate * Reverse - Amat_reverse)
pprint(Reverse * Amat_conjugate * Reverse - Amat_reverse)

Ab = Amat* Reverse
Abin = Ab * Ab 

Abb = Amat* Reverse
Abbin = Abb * Abb 
#ABbin = Abin * Bvect

pprint(Abbin)

Ab = Abbin * Bvect

#pprint(Amat - Amat_reverse)
pprint(Amat_conjugate*Amat_reverse)

#pprint(Amat.subs([
 #   (a, 0), 
  #  (a41, 0), 
   # (a42, 0), 
    #(a43, 0), 
    #(a4321, 0)]))


def ga_multivector_to_matrix(A, left=True):
    Amat = Matrix([[0]*16]*16)
    B = ga_grade(BBB, 0) + ga_grade(BBB, 1) + ga_grade(BBB, 2) + ga_grade(BBB, 3) + ga_grade(BBB, 4)
    
    if left:
        C = eval_ga(expand(A * B))
    else:
        C = eval_ga(expand(B * A))
    Cvect = ga_as_vector(C)
    
    for i,val in enumerate(Cvect):
        for mul in val.args:
            sign = 1
            a_arg = mul.args[0]
            if a_arg == -1:
                sign = -1
                a_arg = mul.args[1]
                b_arg = mul.args[2]
            else:
                b_arg = mul.args[1]

            #if left == False:
            #    a_arg, b_arg = b_arg, a_arg

            b_index = b_arg.name[2:]

            if b_index == '':
                b_index = 0
            b_pos = CliffordAlgebra301.index_to_pos[int(b_index)]
            Amat[i, b_pos] += sign * a_arg

    return Amat

def ga_vector_to_multivector(vect):
    return sum([a*b for a,b in zip(vect, CliffordAlgebra301.basis)])

def ga_reverse(M):
    vect = ga_as_vector(M)
    reversed_vect = Reverse16 * Matrix(vect).reshape(16,1)
    return ga_vector_to_multivector(reversed_vect)
    

A = ga_grade(AAA, 0) + ga_grade(AAA, 1) + ga_grade(AAA, 2) + ga_grade(AAA, 3) + ga_grade(AAA, 4)
Amat_left =  ga_multivector_to_matrix(A)
pprint(Amat_left)

A_conjugate_mat_left =  ga_multivector_to_matrix(ga_reverse(A))
pprint(A_conjugate_mat_left)


Amat_right =  ga_multivector_to_matrix(A, False)
pprint(Amat_right)


#pprint(Reverse16 * A_conjugate_mat_left * Reverse16)


pprint(Reverse16 * A_conjugate_mat_left * Reverse16 - Amat_right)


A = AAA#ga_grade(AAA, 4)
B = BBB#ga_grade(BBB, 2)

ArBr = eval_ga(expand(ga_reverse(A) * ga_reverse(B)))

# print("A", ga_reverse(A))
# print("B", ga_reverse(B))

# C = ga_reverse(eval_ga(expand(ArBr)))
# print("C", C)
# Cvect = ga_as_vector(C)

# for c in Cvect:
#     print(c)

# C = ga_eval(A*B) - ga_eval(ga_reverse(ga_eval(ga_reverse(B)*ga_reverse(A))))

# pprint(C)
# Cvect = ga_as_vector(C)

# print()
# for i, c in enumerate(Cvect):
#     print(i, c)