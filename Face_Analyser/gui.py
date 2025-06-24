import tkinter as tk
from tkinter import filedialog
from main import analyse_image, analyse_video, analyse_webcam

# Create main tkinter window
root = tk.Tk()
root.title('Face Analyzer')
root.geometry('400x300')
root.configure(bg='#1e1e1e')

# Title label
label = tk.Label(root, text='Face Analyser GUI', font=('Helvetica', 18), bg='#1e1e1e', fg='white')
label.pack(pady=20)

# Funtion to handle image button
def run_image():
    filepath = filedialog.askopenfilename(filetypes=[('Image File', '*.jpg *.jpeg *.png')])
    if filepath:
        analyse_image(filepath)
        
# Funtion to handle video button
def run_video():
    filepath = filedialog.askopenfilename(filetypes=[('Video Files', '*.mp4 *.avi *.mov')])
    if filepath:
        analyse_video(filepath)

# Funtion to run webcam button
def run_webcam():
    analyse_webcam()

# Buttons for GUI
tk.Button(root, text='Analyse Image', command=run_image, width=20, height=2, bg='#4CAF50', fg='white').pack(pady=10)
tk.Button(root, text='Analyse Video', command=run_video, width=20, height=2, bg='#2196F3', fg='white').pack(pady=10)
tk.Button(root, text='Live Camera (Webcam)', command=run_webcam, width=20, height=2, bg='#FF5722', fg='white').pack(pady=10)

# Start the GUI event loop
root.mainloop()