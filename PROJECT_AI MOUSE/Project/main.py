import tkinter as tk
from subprocess import call

# function to call the main file
def open_py_file():
    call(["python", "PROJECT_AI_MOUSE\\Project\\AI_MOUSE.py"])

root = tk.Tk()
root.overrideredirect(True)

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

x = width / 2 - 200
y = height / 2 - 50

root.geometry(f'200x200+{int(x+120)}+{int(y-50)}')
#root.geometry(f'200x200+{int(x)}+{int(y)}')
root.attributes('-alpha', 0.0) # Set the initial opacity to 0.0

image = tk.PhotoImage(file="PROJECT_AI_MOUSE\\Splash_Screen\\logo.png")
label = tk.Label(root, image=image, bg="#4a4a4a")
label.pack(fill="both", expand=True)

#label.pack(fill="both", expand=True)
# Fade-in function to gradually increase the opacity of the window
def fade_in():
    alpha = root.attributes('-alpha')
    if alpha < 1.0:
        alpha += 0.01
        root.attributes('-alpha', alpha)
        root.after(10, fade_in)

# Call the fade-in function after a delay of 500 milliseconds
root.after(500, fade_in)
root.after(4000, root.destroy)
root.mainloop()

# Start the main file after the splash screen is over
open_py_file() 