import tkinter as tk
import math

# Global variables
input_value = ""
history = []

def click_button_action(item):
    global input_value
    input_value += str(item)
    display_text.set(input_value)

def clear_input():
    global input_value
    input_value = ""
    display_text.set("")

def evaluate():
    global input_value, history
    try:
        result = str(eval(input_value))
        history.append(input_value + " = " + result)
        display_text.set(result)
        input_value = result
        update_history()
    except Exception as e:
        display_text.set("Error")
        input_value = ""

def update_history():
    history_box.delete(1.0, tk.END)
    for entry in history[-5:][::-1]:  # Show last 5 in reverse
        history_box.insert(tk.END, entry + '\n')

def keyboard_input(event):
    key = event.char
    if key in '0123456789.+-*/':
        click_button_action(key)
    elif key == '\r':  # Enter key
        evaluate()
    elif key == '\x08':  # Backspace
        backspace()
        
def backspace():
    global input_value
    input_value = input_value[:-1]
    display_text.set(input_value)

# Scientific functions
def apply_function(func):
    global input_value
    try:
        if func == '√':
            result = str(math.sqrt(float(input_value)))
        elif func == 'log':
            result = str(math.log10(float(input_value)))
        elif func == 'sin':
            result = str(math.sin(math.radians(float(input_value))))
        elif func == 'cos':
            result = str(math.cos(math.radians(float(input_value))))
        elif func == 'tan':
            result = str(math.tan(math.radians(float(input_value))))
        display_text.set(result)
        input_value = result
    except:
        display_text.set("Error")
        input_value = ""

# Toggle scientific mode
def toggle_scientific():
    if sci_frame.winfo_ismapped():
        sci_frame.pack_forget()
        sci_button.config(text="Scientific Mode")
    else:
        sci_frame.pack()
        sci_button.config(text="Basic Mode")

# GUI Setup
root = tk.Tk()
root.title("Advanced Calculator")
root.geometry("400x600")
root.resizable(False, False)

display_text = tk.StringVar()

display = tk.Entry(root, textvariable=display_text, font=("Arial", 24), bd=10, relief=tk.RIDGE, justify='right')
display.pack(fill='x', ipadx=8, ipady=15)

btn_frame = tk.Frame(root)
btn_frame.pack()

buttons = [
    ['C', '/', '*', '←'],
    ['7', '8', '9', '-'],
    ['4', '5', '6', '+'],
    ['1', '2', '3', '='],
    ['0', '.', '', '']
]

for row in buttons:
    row_frame = tk.Frame(btn_frame)
    row_frame.pack(expand=True, fill='both')
    for char in row:
        if char:
            action = (
                evaluate if char == '=' else
                clear_input if char == 'C' else
                backspace if char == '←' else
                lambda ch=char: click_button_action(ch)
            )
            tk.Button(row_frame, text=char, font=("Arial", 18), width=6, height=2, command=action).pack(side='left', expand=True, fill='both')
        else:
            tk.Label(row_frame, text="", width=6).pack(side='left', expand=True, fill='both')


# History section with scrollbar
history_label = tk.Label(root, text="History (Last 5)", font=("Arial", 12))
history_label.pack(pady=(10, 0))

history_frame = tk.Frame(root)
history_frame.pack(padx=10, pady=5, fill='both', expand=True)

scrollbar = tk.Scrollbar(history_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

history_box = tk.Text(history_frame, height=5, font=("Arial", 12), yscrollcommand=scrollbar.set, wrap=tk.WORD)
history_box.pack(side=tk.LEFT, fill='both', expand=True)

scrollbar.config(command=history_box.yview)



# Scientific Mode Frame
sci_button = tk.Button(root, text="Scientific Mode", command=toggle_scientific, bg="lightblue")
sci_button.pack(pady=5)

sci_frame = tk.Frame(root)
functions = ['√', 'log', 'sin', 'cos', 'tan']
for func in functions:
    tk.Button(sci_frame, text=func, font=("Arial", 14), width=6, command=lambda f=func: apply_function(f)).pack(side='left', padx=5, pady=5)

# Keyboard binding
root.bind("<Key>", keyboard_input)

root.mainloop()
