from numpy import sign
import numpy as np
import tkinter as tk
import customtkinter


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

A = [[-18, -10, -1, 0, 2, 1], [27, 1, 1, 3, 1, -1], [-32, -6, -1, -2, 0, -1]]

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

    if np.count_nonzero(A.T[column] != 0) == 0:
        print("Невозможно выбрать псевдобазис")
        return 1
    if A[row][column] == 0:
        for i in range(m):
            if A[i][column] != 0:
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
        return 1

    basis = np.array([-1] * 3, int)
    for i in range(1, n + 1):
        if C[i] == 0:
            if (
                np.count_nonzero(A.T[i] == 0) == m - 1
                and np.count_nonzero(A.T[i] == 0) == 1
            ):
                for j in range(m):
                    if A[i][j] == 1:
                        basis[j] == i
                        break

    for i in range(1, n + 1):
        if C[i] == 0:
            if np.count_nonzero(A.T[i] > 0) != 0:
                for j in range(m):
                    if basis[j] == -1:
                        r = make_basis(j, i)
                        if r == 0:
                            basis[j] = i
                        else:
                            return 1
                        break
    return 0


def choose_new():
    min_b = 0
    for i in range(m):
        if A[i][0] < A[min_b][0]:
            min_b = i
    min_s = -1
    for i in range(1, n + 1):
        if (A[min_b][i] < 0) and (
            min_s == -1 or scores[min_s] / A[min_b][min_s] < scores[i] / A[min_b][i]
        ):
            min_s = i

    return min_b, min_s


def check_end():
    return all(A.T[0] >= 0)


def calc_scores():
    global scores
    scores = (
        np.array(list(map(lambda x: C[x], basis)), Drob).reshape(1, 3) @ A - C
    ).reshape(-1)
    # print(*map(str, *scores))


def get_answer():
    x = []
    for i in range(n):
        x.append(0)
    for i in range(m):
        x[basis[i] - 1] = A[i][0]
    
    return x, scores[0]


def print_table():
    length = 7
    print("".join(list(map(lambda x: str(x) + " " * (length - len(str(x))), C))))
    print()
    print(
        "\n".join(
            map(
                lambda row: "".join(
                    map(lambda el: str(el) + " " * (length - len(str(el))), row)
                ),
                A,
            )
        )
    )
    print()
    print("".join(list(map(lambda x: str(x) + " " * (length - len(str(x))), scores))))
    print()
    print()


def draw_table(canvas, x, y):
    height, width = 20, 40
    pady, padx = 7, 7
    for i in range(m + 4):
        canvas.create_line(x, y + i * height, x + (n + 3) * width, y + i * height)
    for i in range(n + 4):
        canvas.create_line(x + i * width, y, x + i * width, y + (m + 3) * height)
    canvas.create_text(
        x + width / 2, y + height / 2, text="Базис", font="TimesNewRoman 10"
    )
    canvas.create_text(
        x + width * 1 + width / 2, y + height / 2, text="Cбаз", font="TimesNewRoman 10"
    )
    canvas.create_text(
        x + width * 2 + width / 2, y + height / 2, text="A0", font="TimesNewRoman 10"
    )
    canvas.create_text(
        x + width + width / 2,
        y + height * (m + 2) + height / 2,
        text="Δ",
        font="TimesNewRoman 10",
    )

    for i in range(n):
        canvas.create_text(
            x + width * (3 + i) + width / 2,
            y + height + height / 2,
            text="A" + str(i + 1),
            font="TimesNewRoman 10",
        )
        canvas.create_text(
            x + width * (3 + i) + width / 2,
            y + height / 2,
            text=str(C[i + 1]),
            font="TimesNewRoman 10",
        )

    for i in range(m):
        canvas.create_text(
            x + width / 2,
            y + height * (2 + i) + height / 2,
            text="A" + str(basis[i]),
            font="TimesNewRoman 10",
        )
        canvas.create_text(
            x + width + width / 2,
            y + height * (2 + i) + height / 2,
            text=str(C[basis[i]]),
            font="TimesNewRoman 10",
        )

    row, column = choose_new()
    if check_end():
        row = -1
    for i in range(m):
        for j in range(n + 1):
            if row == i and column == j:
                canvas.create_text(
                    x + width * (2 + j) + width / 2,
                    y + height * (2 + i) + height / 2,
                    text=f'"{A[i][j]}"',
                    font="TimesNewRoman 10",
                    fill="red",
                )
            else:
                canvas.create_text(
                    x + width * (2 + j) + width / 2,
                    y + height * (2 + i) + height / 2,
                    text=str(A[i][j]),
                    font="TimesNewRoman 10",
                )

    for i in range(n + 1):
        canvas.create_text(
            x + width * (2 + i) + width / 2,
            y + height * (2 + m) + height / 2,
            text=str(scores[i]),
            font="TimesNewRoman 10",
        )
    
    return height * (m + 4)


def solve():
    # make_task(A, C)
    choose_pseudobasis()
    calc_scores()
    print_table()

    while not (check_end()):
        # row, column = choose_new()
        make_basis(*choose_new())
        calc_scores()
        print_table()


def error_root(err):
    root = tk.Tk()
    root.geometry("240x40")
    root.title("Ошибка")
    customtkinter.CTkLabel(
        master=root, text=err, text_color="red", anchor="w"
    ).pack()


def solve_root():
    root = tk.Tk()
    root.geometry("720x480")
    root.title("Решение")

    canvas = tk.Canvas(root, width=30, height=600)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scroll_canv = tk.Scrollbar(root, orient=tk.VERTICAL)
    scroll_canv.pack(side=tk.LEFT, fill=tk.Y)
    scroll_canv.config(command=canvas.yview)
    canvas.config(yscrollcommand=scroll_canv.set)

    x, y = 50, 50

    r = choose_pseudobasis()
    if r:
        error_root("Невозможно выбрать псевдобазис")
        root.destroy()
        return
        
    calc_scores()
    y += draw_table(canvas, x, y)

    while not (check_end()):
        row, column = choose_new()
        r = make_basis(row, column)
        if r or column == -1:
            canvas.create_text(x, y, anchor="nw", text="Задача не имеет решений")
            break
        calc_scores()
        y += draw_table(canvas, x, y)
    
    if not(r or column == -1):
        x_, l_ = get_answer()

        canvas.create_text(x, y, text=f"x* = ({', '.join(list(map(str, x_)))}); l* = {l_}", anchor="nw")
    
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    root.mainloop()


def get_task():
    a = []
    for i in range(m):
        a.append([])
        for j in range(n + 1):
            try:
                a[i].append(int(a_entryes[i][j].get()))
            except:
                error_root("Данные некорректны")
                return

    c = []
    for i in range(n):
        try:
            c.append(int(c_entryes[i].get()))
        except:
            error_root("Данные некорректны")
            return

    make_task(a, c)
    solve_root()


# solve()

root = tk.Tk()
root.geometry("720x480")
root.title("Двойственный симплекс-метод")
customtkinter.CTkLabel(master=root, text="   ").grid(row=0, column=0, ipadx=10)
customtkinter.CTkLabel(
    master=root,
    text="Двойственный симпекс-метод",
    text_color="black",
    font=("Times New Roman", 40),
).grid(row=0, column=1, columnspan=15, pady=20, ipadx=10, sticky="W")

a_entryes = []
c_entryes = []
n_entry = None
m_entry = None
equal_labels = []
a_label = None
c_label = None


def shape_validation():
    global c_entryes, a_entryes, equal_labels, n, m

    if n != int(n_entry.get()) or m != int(m_entry.get()):
        for i in range(m):
            equal_labels[i].destroy()
            for j in range(n + 1):
                a_entryes[i][j].destroy()

        for i in range(n):
            c_entryes[i].destroy()

        a_entryes.clear()
        c_entryes.clear()
        equal_labels.clear()

        n = int(n_entry.get())
        m = int(m_entry.get())

        form_drawing_target()
        form_drawing_rest()

    n_entry.configure(validate="focusout", validatecommand=shape_validation)
    m_entry.configure(validate="focusout", validatecommand=shape_validation)


def form_drawing():
    global a_entryes, c_entryes, n_entry, m_entry, equal_labels, a_label, c_label

    customtkinter.CTkLabel(
        master=root,
        text="Параметры",
        text_color="black",
        font=("Times New Roman", 18),
    ).grid(row=2, column=1, columnspan=2, pady=5, sticky="W")
    customtkinter.CTkLabel(
        master=root,
        text="n:",
        text_color="black",
        font=("Times New Roman", 18),
    ).grid(row=3, column=1)
    customtkinter.CTkLabel(
        master=root,
        text="m:",
        text_color="black",
        font=("Times New Roman", 18),
    ).grid(row=3, column=3)
    n_entry = customtkinter.CTkEntry(
        master=root,
        width=30,
        fg_color="#EAEAEA",
        text_color="black",
        validate="focusout",
        validatecommand=shape_validation,
    )
    n_entry.grid(row=3, column=2)
    n_entry.insert(0, "5")
    m_entry = customtkinter.CTkEntry(
        master=root,
        width=30,
        fg_color="#EAEAEA",
        text_color="black",
        validate="focusout",
        validatecommand=shape_validation,
    )
    m_entry.insert(0, "3")
    m_entry.grid(row=3, column=4)
    customtkinter.CTkLabel(master=root, text="").grid(row=4, column=0, ipadx=10)
    c_label = customtkinter.CTkLabel(
        master=root,
        text="Целевая функция",
        text_color="black",
        font=("Times New Roman", 18),
    )
    c_label.grid(row=4, column=1, columnspan=3, pady=5, sticky="W")
    a_label = customtkinter.CTkLabel(
        master=root,
        text="Ограничения",
        text_color="black",
        font=("Times New Roman", 18),
    )
    a_label.grid(row=6, column=1, columnspan=2, pady=5, sticky="W")

    form_drawing_target()
    form_drawing_rest()
    customtkinter.CTkButton(master=root, text="Решить", command=get_task).grid(
        row=10, column=1
    )


def form_drawing_target():
    global c_entryes

    xs = 1
    ys = 5

    for i in range(n):
        c_entryes.append(
            customtkinter.CTkEntry(
                master=root, width=30, fg_color="#EAEAEA", text_color="black"
            )
        )
        c_entryes[i].grid(row=ys, column=xs + i)
        c_entryes[i].insert(0, "0")


def form_drawing_rest():
    global a_entryes

    xs = 1
    ys = 7

    for i in range(m):
        a_entryes.append([])
        for j in range(n):
            a_entryes[i].append(
                customtkinter.CTkEntry(
                    master=root, width=30, fg_color="#EAEAEA", text_color="black"
                )
            )
            a_entryes[i][j].grid(row=i + ys, column=j + xs, padx=3, pady=3)
            a_entryes[i][j].insert(0, "0")
    for i in range(m):
        equal_labels.append(
            customtkinter.CTkLabel(
                master=root,
                width=30,
                height=25,
                text="=",
                text_color="black",
                font=("Arial", 20),
            )
        )
        equal_labels[i].grid(row=i + ys, column=n + xs, padx=0)
        a_entryes[i].insert(
            0,
            customtkinter.CTkEntry(
                master=root, width=30, fg_color="#EAEAEA", text_color="black"
            ),
        )
        a_entryes[i][0].grid(row=i + ys, column=n + xs + 1, padx=3, pady=3)
        a_entryes[i][0].insert(0, "0")


form_drawing()

# solve_root()

root.mainloop()
