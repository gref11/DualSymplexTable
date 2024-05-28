from numpy import sign
import numpy as np


def nod(a, b):
    if type(a) != int or type(b) != int or a < 1 or b < 1:
        return 0
    a, b = max(a, b), min(a, b)
    while b != 0:
        a, b = b, a % b
    return a


# дроби
class Drob:
    __type = "Drob"
    __num = 1
    __den = 1

    def __init__(self, num, den=1):
        if type(num) != int or int(num) != num:
            return
        if type(den) != int or den < 1 or int(den) != den:
            return
        if num == 0:
            self.__num = 0
            self.__den = 1
        else:
            nod_drob = nod(abs(num), den)
            self.__num = int(num / nod_drob)
            self.__den = int(den / nod_drob)

    def __del__(self):
        # print(f'Дробь {str(self)} удалена')
        pass

    def __str__(self):
        return f"{self.__num}/{self.__den}" if (self.__den != 1) else str(self.__num)

    def reduce(self):
        nod_drob = nod(abs(self.__num), self.__den)
        if nod_drob == 0:
            self.__num = 0
            self.__den = 1
        else:
            self.__num = int(self.__num / nod_drob)
            self.__den = int(self.__den / nod_drob)
        return self

    def __add__(drob1, drob2):
        if type(drob2) == int:
            drob2 = Drob(drob2, 1)
        res_num = drob1.__num * drob2.__den + drob2.__num * drob1.__den
        res_den = drob1.__den * drob2.__den
        res = Drob(res_num, res_den).reduce()
        return res

    def __iadd__(self, other):
        res = self + other
        self.__num = res.__num
        self.__den = res.__den
        return self

    def __mul__(drob1, drob2):
        if type(drob2) == int:
            drob2 = Drob(drob2, 1)
        res_num = drob1.__num * drob2.__num
        res_den = drob1.__den * drob2.__den
        res = Drob(res_num, res_den).reduce()
        return res

    def __imul__(self, other):
        res = self * other
        self.__num = res.__num
        self.__den = res.__den
        return self

    def __sub__(drob1, drob2):
        if type(drob2) == int:
            drob2 = Drob(drob2, 1)
        res_num = drob1.__num * drob2.__den - drob2.__num * drob1.__den
        res_den = drob1.__den * drob2.__den
        res = Drob(res_num, res_den).reduce()
        return res

    def __isub__(self, other):
        res = self - other
        self.__num = res.__num
        self.__den = res.__den
        return self

    def __truediv__(drob1, drob2):
        if type(drob2) == int:
            drob2 = Drob(drob2, 1)
        res_num = drob1.__num * drob2.__den * int(sign(drob2.__num))
        res_den = drob1.__den * abs(drob2.__num)
        res = Drob(res_num, res_den).reduce()
        return res

    def __itruediv__(self, other):
        res = self / other
        self.__num = res.__num
        self.__den = res.__den
        return self

    def __lt__(drob1, drob2):
        if type(drob2) == int:
            drob2 = Drob(drob2, 1)
        if drob1.__num * drob2.__den < drob2.__num * drob1.__den:
            return True
        else:
            return False

    def __le__(drob1, drob2):
        if drob1 == drob2 or drob1 < drob2:
            return True
        else:
            return False

    def __gt__(drob1, drob2):
        if type(drob2) == int:
            drob2 = Drob(drob2, 1)
        if drob1.__num * drob2.__den > drob2.__num * drob1.__den:
            return True
        else:
            return False

    def __ge__(drob1, drob2):
        if drob1 == drob2 or drob1 > drob2:
            return True
        else:
            return False

    def __eq__(drob1, drob2):
        if type(drob2) == int:
            drob2 = Drob(drob2, 1)
        if drob1.__num == drob2.__num and drob1.__den == drob2.__den:
            return True
        else:
            return False


# A = [
#     [-115, 5, 0, -1, -10, -1],
#     [63, 12, 1, -1, -1, 1], 
#     [-27, -6, 1, 1, -1, -1]
# ]

# C = [0, -6, -1, 0, 0]

A = [
    [-18, -10, -1, 0, 2, 1],
    [27, 1, 1, 3, 1, -1], 
    [-32, -6, -1, -2, 0, -1]
]

C = [0, 0, 0, -4, -1]

basis = []

scores = np.array([Drob(0)] * 6, Drob)

n = 5
m = 3


# решение задачи
def make_task(a, c):
    global A, C, n, m

    # A = np.array(list(map(lambda row: np.array(list(map(Drob, row)), Drob), a)))

    A = np.array(a, Drob)
    for i in range(m):
        for j in range(n + 1):
            A[i][j] = Drob(A[i][j])
    
    c.insert(0, 0)
    C = np.array(c, Drob)
    for i in range(n + 1):
        C[i] = Drob(C[i])
    
def make_basis(row, column):
    global A, basis

    if (np.count_nonzero(A.T[column] != 0) == 0):
        print("Невозможно выбрать псевдобазис1")
        return 1
    if (A[row][column] == 0):
        for i in range(m):
            if (A[i][column] != 0):
                A[row] += A[i]
    A[row] /= A[row][column]
    for i in range(m):
        if row == i:
            continue
        A[i] -= A[row] * A[i][column]
    basis[row] = column
    return 0

def choose_pseudobasis():
    global basis

    if m + 1 > np.count_nonzero((C == 0)):
        print("Невозможно выбрать псевдобазис")
    
    basis = np.array([-1] * 3, int)
    for i in range(1, n + 1):
        if C[i] == 0:
            if (np.count_nonzero(A.T[i] == 0) == m - 1 and np.count_nonzero(A.T[i] == 0) == 1):
                for j in range(m):
                    if (A[i][j] == 1):
                        basis[j] == i
                        break
    
    for i in range(1, n + 1):
        if C[i] == 0:
            if (np.count_nonzero(A.T[i] > 0) != 0):
                for j in range(m):
                    if (basis[j] == -1):
                        r = make_basis(j, i)
                        if (r == 0):
                            basis[j] = i
                        break

def choose_new():
    min_b = 0
    for i in range(m):
        if (A[i][0] < A[min_b][0]):
            min_b = i
    min_s = -1
    for i in range(1, n + 1):
        if (A[min_b][i] < 0) and (min_s == -1 or scores[min_s] / A[min_b][min_s] < scores[i] / A[min_b][i]):
            min_s = i
    
    return min_b, min_s

def check_end():
    return all(A.T[0] >= 0)


def calc_scores():
    global scores
    scores = (np.array(list(map(lambda x: C[x], basis)), Drob).reshape(1, 3) @ A - C).reshape(-1)
    # print(*map(str, *scores))


def print_table():
    length = 7
    print("".join(list(map(lambda x : str(x) + " " * (length - len(str(x))), C))))
    print()
    print("\n".join(map(lambda row: "".join(map(lambda el: str(el) + " " * (length - len(str(el))), row)), A)))
    print()
    print("".join(list(map(lambda x : str(x) + " " * (length - len(str(x))), scores))))
    print()
    print()

def solve():
    make_task(A, C)
    choose_pseudobasis()
    calc_scores()
    print_table()

    while(not(check_end())):
        # row, column = choose_new()
        make_basis(*choose_new())
        calc_scores()
        print_table()


solve()