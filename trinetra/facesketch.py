from tkinter import *
 
ws = Tk()
ws.geometry('400x300')
ws.title('PythonGuides')
ws['bg']='#ffbf00'
 
f = ("Times bold", 14)
  
 
Label(
    ws,
    text="This is Second page",
    padx=20,
    pady=20,
    bg='#ffbf00',
    font=f
).pack(expand=True, fill=BOTH)
 
 
