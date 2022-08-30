import tkinter as tk
from tkinter import filedialog, Text
import os

root = tk.Tk()

canvas= tk.Canvas(root, height=700, width=700, bg="#ff66aa")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight= 0.8, relx=0.1, rely=0.1)

openAccuracy = tk.Button(root, text="Accuracy", padx=10, pady=5, fg="white", bg="#ff66aa")
openAccuracy.pack()

openHistory = tk.Button(root, text="History", padx=10, pady=5, fg="white", bg="#ff66aa")
openHistory.pack()

root.mainloop()
