import tkinter as tk

def create_window():
    window = tk.Tk()
    window.title("Teste do Tkinter")
    label = tk.Label(window, text="Tkinter está funcionando!")
    label.pack(padx=20, pady=20)
    window.mainloop()

if __name__ == "__main__":
    create_window()
