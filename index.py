from numpy import sign


def nod(a, b):
    if type(a) != int or type(b) != int or a < 1 or b < 1:
        return 0
    a, b = max(a, b), min(a, b)
    while b != 0:
        a, b = b, a % b
    return a


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
        if drob1 == drob2 or drob1 < drob2:
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
