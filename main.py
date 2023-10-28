import tkinter as tk
from tkinter import ttk
from tkinter import messagebox



def say_hello():
   # print("Dies ist ein Info")
   tk.messagebox.showinfo(title="Info", message="Dieses Tool wurde von Cihan Tayiz programmiert. Es werden keinerlei Haftungen für die Auswirkung übernommen.")

def print_entry_input():
    print(entry1.get())

root = tk.Tk()
root.title("CCW MigrationsTool")
# set windowsize
root.geometry("600x600")
root.minsize(width=400, height=400)
root.maxsize(width=800, height=800)


label1 = tk.Label(root, text="MigrationsTool")
label1.pack()

button1 = ttk.Button (root, text="Info", padding=10, command=say_hello)
button1.pack()

quit_button = ttk.Button (root, text="Cancel", command=root.destroy)
quit_button.pack(side="left")

button2 = ttk.Button (root, text="Eingabe", command=print_entry_input)
button2.pack(side="left")

entry1 = ttk.Entry (root)
entry1.pack()

checkbox1 = ttk.Checkbutton(root)
checkbox1.pack()

root.mainloop()

