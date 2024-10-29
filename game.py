from tkinter import *
# class Application(Frame):
#     def __init__(self, master=None):
#         Frame.__init__(self, master)
#         self.msg = Label(self, text="Hello World")
#         self.msg.pack ()
#         self.bye = Button (self, text="Bye", command=self.quit)
#         self.bye.pack ()
#         self.pack()

# app = Application()
# app.master.title("Hello World")
# app.master.geometry("200x100+100+100")



# top = Frame()
# top.pack()

# rotulo = Label(top, text="Hello World", foreground="blue")
# rotulo.pack()

# rotulo.configure(relief="ridge", font="Arial 24 bold", border=10, background="yellow")

# mainloop()



# top = Frame() ; top.pack()
# a = Label (top, text="A") ; a.pack (side="left", fill="y")
# b = Label (top, text="B") ; b.pack (side="bottom", fill="x")
# c = Label (top, text="C") ; c.pack (side="right")
# d = Label (top, text="D") ; d.pack (side="top")
# for widget in (a,b,c,d):
#     widget.configure(relief="groove", border=10, font="Times 24 bold")

# top.mainloop()




# def inc():
#     n=int(rotulo.configure("text")[4])+1
#     rotulo.configure(text=str(n))

# b = Button(text="Incrementa",command=inc)
# b.pack()
# rotulo = Label(text="0")
# rotulo.pack()
# mainloop()



##TODO: PRA PEGAR CLIQUE:

# <Motion> : mouse arrastado sobre o widget
#<Enter>: O mouse entrou na área do widget
# <Leave>: O mouse saiu da área do widget
#PRA COLORIR, POR EXEMPLO

def clica (e):
    txt = "Mouse clicado em\n%d,%d"%(e.x,e.y)
    r.configure(text=txt)

def tecla(e):
    txt="Keysym=%s\nKeycode=%s\nChar=%s"\
    %(e.keysym,e.keycode,e.char)
    r.configure(text=txt)

r = Label()
r.pack(expand=True, fill="both")
r.master.geometry("400x400")
r.bind("<Button-1>", clica)
r.bind("<Key>", tecla)
mainloop()