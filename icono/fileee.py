import tkinter as tk
from tkinter import messagebox


class App(tk.Tk):

    def __init__(self):
     tk.Tk.__init__(self)
     self.title("Handling WM_DELETE_WINDOW protocol")
     self.geometry("500x300+500+200")
     self.make_topmost()
     self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def on_exit(self):
     """When you click to exit, this function is called"""
     if messagebox.askyesno("Exit", "Do you want to quit the application?"):
      self.destroy()

    # def center(self):
    #  """Centers this Tk window"""
    #  self.eval('tk::PlaceWindow %s center' % app.winfo_pathname(app.winfo_id()))
    #
    # def make_topmost(self):
    #  """Makes this window the topmost window"""
    #  self.lift()
    #  self.attributes("-topmost", 1)
    #  self.attributes("-topmost", 0)


# if __name__ == '__main__':
#     App().mainloop()
class Geeks:
    def __init__(self):
      self._age = 0



    @property
    def age(self):
     print("getter method called")
     return self._age

    @age.setter
    def age(self, a):
        print("setter method called")
        self._age = a

mark = Geeks()

mark.age = 19778

print(mark.age)
