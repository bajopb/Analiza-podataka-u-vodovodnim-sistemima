import tkinter as tk
from tkinter import ttk

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI")

        self.combobox = ttk.Combobox(self.root)
        self.combobox.pack()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.RIGHT)

        self.count_button = tk.Button(self.button_frame, text="Count", cursor="hand2", command=self.count, underline=True)
        self.count_button.pack(anchor=tk.W)

        self.percentage_button = tk.Button(self.button_frame, text="Percentage", cursor="hand2", command=self.percentage, underline=True)
        self.percentage_button.pack(anchor=tk.W)

        self.standard_deviation_button = tk.Button(self.button_frame, text="Standard Deviation", cursor="hand2", command=self.standard_deviation, underline=True)
        self.standard_deviation_button.pack(anchor=tk.W)

    def count(self):
        selected_field = self.combobox.get()

        count = 0
        

    def percentage(self):
        selected_field = self.combobox.get()

        percentage = 0
        

    def standard_deviation(self):
        selected_field = self.combobox.get()

        standard_deviation = 0

      

root = tk.Tk()

gui = GUI(root)

root.mainloop()
