import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from converter import convert_sequence_to_video

class ImageToVideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Sequence to Video Converter")
        self.root.geometry("600x360")
        self.root.configure(bg="white")

        self.input_pattern = None
        self.output_folder = None

        tk.Label(root, text="Drag & Drop the First Image of Your Sequence Below", bg="white", font=("Arial", 12)).pack(pady=10)

        self.drop_frame = tk.Label(root, text="⬇ Drop Image File Here ⬇", bg="#f0f0f0", width=60, height=5, relief="groove")
        self.drop_frame.pack(pady=10)
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.drop)

        # tk.Button(root, text="Or Click to Select Image", command=self.select_input_image).pack(pady=5)
        tk.Button(root, text="Select Output Folder", command=self.select_output_folder).pack(pady=5)

        self.fps = tk.IntVar(value=24)
        tk.Label(root, text="Frames per Second:", bg="white").pack()
        tk.Entry(root, textvariable=self.fps).pack()

        self.output_filename_var = tk.StringVar(value="output.mp4")
        tk.Label(root, text="Output Video Filename:", bg="white").pack(pady=(10, 0))
        tk.Entry(root, textvariable=self.output_filename_var).pack()

        tk.Button(root, text="Convert to Video", command=self.convert).pack(pady=15)

    def select_input_image(self):
        file_path = filedialog.askopenfilename(title="Select First Image")
        if file_path:
            self.process_input_file(file_path)

    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder = folder
            print("Selected output folder:", folder)

    def drop(self, event):
        files = self.root.tk.splitlist(event.data)
        if files:
            file_path = files[0]
            self.process_input_file(file_path)

    def process_input_file(self, file_path):
        print("Selected/Dropped file:", file_path)
        dir_name = os.path.dirname(file_path)
        filename = os.path.basename(file_path)

        match = re.match(r"(.*?)(\d+)(\.\w+)$", filename)
        if match:
            prefix, digits, ext = match.groups()
            pattern = f"{prefix}%0{len(digits)}d{ext}"
            self.input_pattern = os.path.join(dir_name, pattern)
            print("Detected input pattern:", self.input_pattern)
            self.drop_frame.config(text=f"✅ Pattern: {self.input_pattern}")
            if not self.output_folder:
                self.output_folder = dir_name
        else:
            messagebox.showerror("Invalid File", "Could not detect a numeric sequence in the filename.")

    def convert(self):
        if not self.input_pattern:
            messagebox.showerror("Error", "Please drop or select a valid image file first.")
            return
        if not self.output_folder:
            messagebox.showerror("Error", "Please select an output folder.")
            return

        output_filename = self.output_filename_var.get().strip()
        if not output_filename:
            messagebox.showerror("Error", "Please enter a valid output filename.")
            return

        output_path = os.path.join(self.output_folder, output_filename)

        # Overwrite if exists
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
                print(f"Deleted existing file: {output_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Cannot overwrite existing file:\n{e}")
                return

        fps_value = self.fps.get()

        success, error = convert_sequence_to_video(self.input_pattern, output_path, fps_value)
        if success:
            messagebox.showinfo("Success", f"Video created:\n{output_path}")
        else:
            messagebox.showerror("Error", error)


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageToVideoApp(root)
    root.mainloop()
