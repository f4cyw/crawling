import os
from tkinter import Tk, Label, Button, filedialog
from PIL import Image

class MetadataViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("PNG Metadata Viewer")

        self.select_button = Button(self.root, text="Select Image", command=self.load_image)
        self.select_button.pack(pady=20)

        self.metadata_label = Label(self.root, text="", justify='left')
        self.metadata_label.pack(pady=20, padx=20)

    def load_image(self):
        file_types = [("PNG files", "*.png"), ("All files", "*.*")]
        file_path = filedialog.askopenfilename(filetypes=file_types)

        if file_path:
            try:
                with Image.open(file_path) as img:
                    formatted_metadata = "\n".join([f"{key}: {value}" for key, value in img.info.items()])
                    self.metadata_label.config(text=formatted_metadata)
            except Exception as e:
                self.metadata_label.config(text=f"Error loading image: {e}")

if __name__ == "__main__":
    root = Tk()
    viewer = MetadataViewer(root)
    root.mainloop()
