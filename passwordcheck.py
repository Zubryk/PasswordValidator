from tkinter import *
import tkinter.ttk as ttk
from password_validation import PasswordCheck

def strength_bar(pwd):
    s = ttk.Style()
    s.theme_use('clam')

    if pwd.get_score() < 20:
        s.configure("red.Horizontal.TProgressbar", text='{:g} %'.format(pwd.get_score()) , foreground='red', background='red')
        progress.configure(style="red.Horizontal.TProgressbar")
    elif pwd.get_score() < 40:
        s.configure("orange.Horizontal.TProgressbar", foreground='orange', background='orange')
        progress.configure(style="orange.Horizontal.TProgressbar")
    elif pwd.get_score() < 60:
        s.configure("yellow.Horizontal.TProgressbar", foreground='yellow', background='yellow')
        progress.configure(style="yellow.Horizontal.TProgressbar")
    elif pwd.get_score() < 80:
        s.configure("yellowgreen.Horizontal.TProgressbar", foreground='yellowgreen', background='yellowgreen')
        progress.configure(style="yellowgreen.Horizontal.TProgressbar")
    else:
        s.configure("green.Horizontal.TProgressbar", foreground='green', background='green')
        progress.configure(style="green.Horizontal.TProgressbar")

def hide_password():
    if check_var.get() == 1:
        pwdtxt.configure(show = "#")
    else:
        pwdtxt.configure(show = "")


def callback(sv):
    output.delete("1.0", END)
    output.configure(bg = "grey")

    pwd = PasswordCheck(sv.get())

    if pwd.password_length < 8:
        output.insert(END, "Пароль занадто короткий")
        lengthlabel.configure(fg = 'red')
    elif pwd.password in pwd.password_dictionary:
        output.insert(END, "Пароль виявлено у відкритому словнику")
        output.configure(bg = "red")
    else:
        output.insert(END, str(pwd.get_complexity()))

    u, s, d, p = pwd.check_requirements()

    if pwd.password_length > 8:
        lengthlabel.configure(fg = 'green')
    if u == 0 :
        ulabel.configure(fg = "red")
    else:
        ulabel.configure(fg = "green")
    if s == 0 :
        slabel.configure(fg = "red")
    else:
        slabel.configure(fg = "green")
    if d == 0 :
        dlabel.configure(fg = "red")
    else:
        dlabel.configure(fg = "green")
    if p == 0 :
        plabel.configure(fg = "red")
    else:
        plabel.configure(fg = "green")
    if u + s + d + p < 3 :
        symblabel.configure(fg = "red")
    else:
        symblabel.configure(fg = "green")

    progress['value'] = pwd.get_score()
    strength_bar(pwd)
    score.set(str(pwd.get_score()) + " %")

root = Tk()

root['bg'] = 'grey'
root.title('Перевірка паролів')
root.geometry('750x400')

root.geometry("+350+200")
root.resizable(width = False, height = False)

pwdlabel = Label(root, background = "grey", text = "Введіть та перевірте свій пароль:")
pwdlabel.place(x = 50, y = 50, width = 300, height = 30)
pwdlabel.configure(font='Helvetica 12 bold', anchor='w')

sv = StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
pwdtxt = Entry(root, textvariable=sv)
pwdtxt.place(x = 50, y = 100, width = 300, height = 30)

check_var = IntVar()
cb = Checkbutton(root, text = "Приховати пароль", font='Helvetica 10',
 command = hide_password,  background = "grey", variable = check_var, onvalue = 1, offvalue = 0)
cb.place(x = 50, y = 150, height = 30)

output = Text(root, background = "grey", font = 'Helvetica 10 bold')
output.place(x = 50, y = 200, width = 300, height = 30)

progress = ttk.Progressbar(root, orient = HORIZONTAL, length = 100, mode = 'determinate')
progress.place(x = 50, y = 250, width = 250, height = 30)

score = StringVar()
score.set("0 %")
score_label = Label(root, background = "grey", textvariable = score)
score_label.place(x = 310, y = 250, width = 40, height = 30)

label1 = Label(root, background = "grey", text = "Основні вимоги до паролю:")
label1.place(x = 400, y = 50, width = 300, height = 30)
label1.configure(font='Helvetica 12 bold', anchor='w')

lengthlabel = Label(root, background = "grey", text = "Довжина паролю більша 8")
lengthlabel.place(x = 400, y = 100, width = 320, height = 30)
lengthlabel.configure(font='Helvetica 10 bold', anchor='w')

symblabel = Label(root, background = "grey", text = "Повинні виконуватися 3 з 4 наступних пунктів:")
symblabel.place(x = 400, y = 125, width = 320, height = 30)
symblabel.configure(font='Helvetica 10 bold', anchor='w')

ulabel = Label(root, background = "grey", text = "\t- Великі букви")
ulabel.place(x = 400, y = 150, width = 320, height = 30)
ulabel.configure(font='Helvetica 10 bold', anchor='w')

slabel = Label(root, background = "grey", text = "\t- Малі букви")
slabel.place(x = 400, y = 175, width = 320, height = 30)
slabel.configure(font='Helvetica 10 bold', anchor='w')

dlabel = Label(root, background = "grey", text = "\t- Цифри")
dlabel.place(x = 400, y = 200, width = 320, height = 30)
dlabel.configure(font='Helvetica 10 bold', anchor='w')

plabel = Label(root, background = "grey", text = "\t- Спеціальні символи")
plabel.place(x = 400, y = 225, width = 320, height = 30)
plabel.configure(font='Helvetica 10 bold', anchor='w')

root.mainloop()