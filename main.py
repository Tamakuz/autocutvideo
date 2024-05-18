import os
import tkinter as tk
from tkinter import filedialog, messagebox, StringVar
from tkinter.ttk import Progressbar, Style
from moviepy.editor import VideoFileClip
from threading import Thread
from ttkthemes import ThemedTk

def choose_input_file(label_video, process_button, input_file_var):
    input_file = filedialog.askopenfilename(title="Pilih Video")
    if input_file:
        label_video.config(text=f"Video input dipilih: {input_file}")
        input_file_var.set(input_file)
        process_button.config(state="normal")

def choose_output_folder(label_output, process_button, output_folder_var):
    output_folder = filedialog.askdirectory(title="Pilih Folder Output")
    if output_folder:
        label_output.config(text=f"Folder output dipilih: {output_folder}")
        output_folder_var.set(output_folder)
        process_button.config(state="normal")

def process_video(input_file_var, output_folder_var, custom_name_var, progress_label, progress_bar, process_button):
    input_file = input_file_var.get()
    output_folder = output_folder_var.get()
    custom_name = custom_name_var.get()

    if not input_file:
        messagebox.showerror("Error", "Silakan pilih file video terlebih dahulu.")
        return

    if not output_folder:
        messagebox.showerror("Error", "Silakan pilih folder output terlebih dahulu.")
        return
    
    # Disable process button
    process_button.config(state="disabled")

    progress_label.config(text="Sedang memproses video...")
    progress_bar["value"] = 0

    # Load video
    video = VideoFileClip(input_file)

    # Define parameters
    cut_interval = 2
    pause_interval = 9

    # Iterate over video frames
    current_time = 0
    clip_number = 1
    try:
        while current_time < video.duration:
            # Define output file path
            output_file = os.path.join(output_folder, f"{custom_name}_{clip_number}.mp4")

            try:
                # Cut clip
                end_time = min(current_time + cut_interval, video.duration)
                clip = video.subclip(current_time, end_time)
                clip.write_videofile(output_file, codec="libx264", fps=video.fps)
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
                return

            # Update progress
            progress = round((current_time / video.duration) * 100, 2)
            progress_label.config(text=f"Proses clip {clip_number} - {progress}% selesai")
            progress_bar["value"] = progress

            # Update current time
            current_time = end_time + pause_interval

            # Increment clip number
            clip_number += 1
    finally:
        # Close the video reader explicitly
        video.close()

    # Update progress label to 100% after completion
    progress_label.config(text="Proses selesai - 100% selesai")
    
    # Show process completion
    messagebox.showinfo("Info", "Proses selesai.")
    
    # Enable process button after completion
    process_button.config(state="normal")

def main():
    root = ThemedTk(theme="equilux")
    root.title("Video Processor")

    label_video = tk.Label(root, text="Pilih file video input")
    label_video.pack(pady=10)

    input_file_var = StringVar()
    output_folder_var = StringVar()
    custom_name_var = StringVar(value="")

    input_button = tk.Button(root, text="Pilih Video", command=lambda: choose_input_file(label_video, process_button, input_file_var))
    input_button.pack(pady=5)

    label_output = tk.Label(root, text="Pilih folder output")
    label_output.pack(pady=10)

    output_button = tk.Button(root, text="Pilih Folder Output", command=lambda: choose_output_folder(label_output, process_button, output_folder_var))
    output_button.pack(pady=5)

    label_custom_name = tk.Label(root, text="Nama Kustom:")
    label_custom_name.pack(pady=5)

    entry_custom_name = tk.Entry(root, textvariable=custom_name_var)
    entry_custom_name.pack(pady=5)

    process_button = tk.Button(root, text="Proses Video", state="disabled")
    process_button.pack(pady=5)

    progress_label = tk.Label(root, text="")
    progress_label.pack(pady=5)

    progress_bar = Progressbar(root, orient="horizontal", length=200, mode="determinate")
    progress_bar.pack(pady=5)

    process_button.config(command=lambda: Thread(target=process_video, args=(input_file_var, output_folder_var, custom_name_var, progress_label, progress_bar, process_button)).start())

    root.mainloop()

if __name__ == "__main__":
    main()
