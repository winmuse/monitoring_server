# Run main.py!!!
import tkinter
from tkinter import *

def on_closing():
    global running
    running = False

# GUI
root = tkinter.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.resizable(False, False)
root.title("Frame Recorder Server")
root.geometry("800x400+500+100")
canvas = Canvas(root, bg="#4392F1", height=400, width=800, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
background_img = PhotoImage(file=f"assets/background.png")
background = canvas.create_image(400.0, 200.0, image=background_img)

# menubar.add_cascade(label="About", menu=about)
start_img = PhotoImage(file=f"assets/start.png")
start = Button(image=start_img, borderwidth=0, highlightthickness=0, relief="flat")
end_img = PhotoImage(file=f"assets/end.png")
end = Button(image=end_img, borderwidth=0, highlightthickness=0, relief="flat")
info = canvas.create_text(400.0, 142.5, text="Frame Recording Server", fill="#ECE8EF", font=("Roboto-Medium", int(16.0)))
# When started
end["state"] = "disabled"
# pause["state"] = "disabled"

