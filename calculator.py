#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox

# ---------------- Circle Button with hover ----------------
class RoundButton(tk.Canvas):
    def __init__(self, parent, text, command=None, diameter=65, bg="#333", fg="white"):
        super().__init__(parent, width=diameter, height=diameter, highlightthickness=0, bg="black")
        self.command = command
        self.bg = bg
        self.hover_bg = "#424242"
        self.diameter = diameter
        self.shrink_factor = 2

        r = diameter // 2
        self.circle = self.create_oval(2, 2, diameter - 2, diameter - 2, fill=bg, outline=bg)
        self.text = self.create_text(r, r, text=text, fill=fg, font=("Arial", 18, "bold"))

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def on_enter(self, event):
        d = self.shrink_factor
        self.coords(self.circle, 2 + d, 2 + d, self.diameter - 2 - d, self.diameter - 2 - d)
        self.itemconfig(self.circle, fill=self.hover_bg)

    def on_leave(self, event):
        self.coords(self.circle, 2, 2, self.diameter - 2, self.diameter - 2)
        self.itemconfig(self.circle, fill=self.bg)

    def on_click(self, event):
        if self.command:
            self.command()


class calculator:
    def __init__(self, master):
        self.master = master

        self.display = tk.Entry(self.master, state='normal', width=20, font=("Arial", 23), justify="right", bg="#000000", foreground="white", borderwidth=0, highlightthickness=0)
        self.display.grid(row=0, column=0, columnspan=4, pady=(75, 25))

        row = 1
        col = 0
        buttons = [
            "AC", "C", "%", "/",
            "7",  "8", "9", "*",
            "4",  "5", "6", "-",
            "1",  "2", "3", "+",
            "^",  "0", ",", "=",
        ]

        for button in buttons:
            self.build_button(button, row, col)
            col += 1
            
            if col > 3:
                col = 0
                row += 1

    # ---------------- Functions ----------------
    def clear_display(self):
        self.display.delete(0, tk.END)

    def delete_last(self):
        texto = self.display.get()
        self.display.delete(0, tk.END)
        self.display.insert(0, texto[:-1])

    def click(self, key):
        self.display.insert("end", key)

    def result(self):
        expr = self.display.get().replace(",", ".").replace("^", "**")
        try:
            result = eval(expr)
            self.clear_display()
            if isinstance(result, float):
                result = round(result, 10)
            self.display.insert(0, str(result).replace(".", ","))
        except ZeroDivisionError:
            self.clear_display()
            self.display.insert(0, "Error: divide by 0")
        except Exception:
            pass

    # ---------------- Construcción de botones ----------------
    def build_button(self, button, row, col):
        if button in "0123456789,^":
            color = "#2E2E2E"
        elif button == "=":
            color = "#8A9390"
        else:
            color = "#1E1E1E"

        if button == "AC":
            b = RoundButton(self.master, text=button, bg=color, command=self.clear_display)
        elif button == "C":
            b = RoundButton(self.master, text=button, bg=color, command=self.delete_last)
        elif button == "=":
            b = RoundButton(self.master, text=button, bg=color, command=self.result)
        else:
            b = RoundButton(self.master, text=button, bg=color, command=lambda b=button: self.click(b))

        b.grid(row=row, column=col, padx=8, pady=8)

# ---------------- Programa principal ----------------
root = tk.Tk()
root.title("calculator")
root.resizable(False, False)
root.configure(background='black')

calculator(root)

root.mainloop()
