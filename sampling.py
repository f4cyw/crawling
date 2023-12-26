import os
import zipfile
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def zip_files(files, zip_name, extract_dir):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in files:
            abs_path = os.path.join(extract_dir, file)
            if not os.path.exists(abs_path):
                print(f"File not found, skipping: {abs_path}")
                continue
            print(f"Zipping file: {abs_path}")
            zipf.write(abs_path, os.path.basename(file))
            os.remove(abs_path)


def extract_first_image(zip_dir, extract_dir):
    image_formats = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    extracted_files = []

    for filename in os.listdir(zip_dir):
        if filename.endswith('.zip'):
            zip_path = os.path.join(zip_dir, filename)
            if not zipfile.is_zipfile(zip_path):
                print(f"Skipping non-ZIP file: {filename}")
                continue
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file in zip_ref.namelist():
                    if file.lower().endswith(image_formats):
                        abs_path = os.path.join(extract_dir, file)
                        print(f"Extracting file: {abs_path}")  # Diagnostic print
                        zip_ref.extract(file, extract_dir)
                        extracted_files.append(file)
                        break

    if extracted_files:
        # Extract the folder name from the extract_dir path
        folder_name = os.path.basename(os.path.normpath(zip_dir))
        zip_file_name = f"{folder_name}_sampling.zip"
        zip_files(extracted_files, os.path.join(extract_dir, zip_file_name), extract_dir)
        print("완료 되었습니다. 오정훈님")


def select_zip_folder():
    zip_dir = filedialog.askdirectory(title="Select ZIP Folder")
    if zip_dir:
        extract_dir = filedialog.askdirectory(title="Select samling Folder")
        if extract_dir :
            extract_first_image(zip_dir, extract_dir)

# GUI setup
root = tk.Tk()
root.title("ZIP Extractor")

select_button = tk.Button(root, text="Select ZIP Folder and Extract", command=select_zip_folder)
select_button.pack(pady=20)

root.mainloop()
