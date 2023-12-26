

import os
import face_recognition
from PIL import Image, ExifTags
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import textwrap

VALID_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"]

def get_image_metadata(image_path):
    image = Image.open(image_path)
    metadata = {}

    if image.format == 'JPEG' and hasattr(image, '_getexif'):
        raw_metadata = image._getexif()
        if raw_metadata:
            for tag, value in raw_metadata.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                metadata[tag_name] = value
    else:
        metadata = image.info

    return metadata or None

def find_matching_keyword(metadata, keywords):
    for key, value in metadata.items():
        if isinstance(value, str):
            for keyword in keywords:
                if keyword.lower() in value.lower():  # 대소문자를 구분하지 않고 검색합니다.
                    return keyword
    return None


def classify_by_keywords(image_folder, sorted_folder, keywords):
    if not os.path.exists(sorted_folder):
        os.makedirs(sorted_folder)

    for filename in os.listdir(image_folder):
        if not is_valid_image(filename):  # 이미지 파일만 처리
            continue
        
        image_path = os.path.join(image_folder, filename)
        exif_data = get_image_metadata(image_path)
        
        matched_keyword = find_matching_keyword(exif_data, keywords)
        folder_name = matched_keyword if matched_keyword else "Unknown"

        sorted_path = os.path.join(sorted_folder, folder_name)
        if not os.path.exists(sorted_path):
            os.makedirs(sorted_path)
        
        os.rename(image_path, os.path.join(sorted_path, filename))


def start_classification():
    image_folder = folder_entry.get()
    sorted_folder = sorted_folder_entry.get()
    keywords = [k.strip() for k in keywords_entry.get().split(",")]

    classify_by_keywords(image_folder, sorted_folder, keywords)
    messagebox.showinfo("Info", "분류 완료!")



def is_valid_image(filename):
    """지정된 파일이 이미지인지 확인합니다."""
    extension = os.path.splitext(filename)[1].lower()
    return extension in VALID_IMAGE_EXTENSIONS


def classify_by_face(image_folder, sorted_folder):
    known_faces = []
    known_face_names = []
    
    # 알려진 얼굴 로드
    for filename in os.listdir(sorted_folder):
        if is_valid_image(filename):
            person_name = os.path.splitext(filename)[0]
            person_image = face_recognition.load_image_file(os.path.join(sorted_folder, filename))
            person_face_encoding = face_recognition.face_encodings(person_image)[0]
            known_faces.append(person_face_encoding)
            known_face_names.append(person_name)

    # 폴더 내의 모든 이미지에 대한 얼굴 분류
    for filename in os.listdir(image_folder):
        if not is_valid_image(filename):
            continue

        print(f"Processing {filename}")
        unknown_image_path = os.path.join(image_folder, filename)
        unknown_image = face_recognition.load_image_file(unknown_image_path)
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            person_dir = os.path.join(sorted_folder, name)
            if not os.path.exists(person_dir):
                os.makedirs(person_dir)

            os.rename(unknown_image_path, os.path.join(person_dir, filename))
            break  # 이미지가 한번 분류되면 루프에서 나옵니다.


def start():
    image_folder = folder_entry.get()
    sorted_folder = sorted_folder_entry.get()
    mode = mode_combobox.get()
    
    if mode == "EXIF 키워드":
        keywords = [k.strip() for k in keywords_entry.get().split(",")]
        classify_by_keywords(image_folder, sorted_folder, keywords)
    elif mode == "얼굴 인식":
        classify_by_face(image_folder, sorted_folder)

    messagebox.showinfo("Info", "분류 완료!")


def select_image_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_path)
        
        # '분류될 폴더'의 기본값을 '이미지 폴더'와 동일하게 설정
        sorted_folder_entry.delete(0, tk.END)
        sorted_folder_entry.insert(0, folder_path)

def view_metadata():
    file_types = [("PNG files", "*.png"), ("All files", "*.*")]
    image_path = filedialog.askopenfilename(filetypes=file_types)
    if image_path:
        metadata = get_image_metadata(image_path)
        if metadata:
            viewer = MetadataViewer(root)
            viewer.show(metadata)
        else:
            messagebox.showwarning("Warning", "이 이미지에는 메타데이터가 없습니다.")

class MetadataViewer:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Image Metadata")

        self.text_widget = tk.Text(self.top, wrap=tk.NONE)
        self.text_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.scrollbar_x = tk.Scrollbar(self.top, orient=tk.HORIZONTAL, command=self.text_widget.xview)
        self.scrollbar_x.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.scrollbar_y = tk.Scrollbar(self.top, orient=tk.VERTICAL, command=self.text_widget.yview)
        self.scrollbar_y.pack(fill=tk.Y, side=tk.RIGHT)

        self.text_widget.config(xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)

    # def show(self, metadata):
    #     print(metadata)
    #     # 대분류를 나타내는 키워드 목록
    #     categories = ['Parameters', 'Negative Prompt', 'Steps']

    #     # 대분류별로 메타데이터를 저장할 딕셔너리 초기화
    #     categorized_data = {category: [] for category in categories}

    #     # 메타데이터를 대분류별로 분류
    #     for key, value in metadata.items():
    #         for category in categories:
    #             if category in key:
    #                 categorized_data[category].append(f"{key}: {value}")

    #     # 대분류별로 정보 출력
    #     display_data = ""
    #     for category, items in categorized_data.items():
    #         if items:  # 해당 대분류에 해당하는 항목이 있을 경우만 출력
    #             display_data += f"{category}:\n"  # 대분류 이름 출력
    #             display_data += '\n'.join(items)  # 해당 대분류에 해당하는 항목들 출력
    #             display_data += "\n\n"  # 대분류 간에 공백 줄 추가
        
    #     self.text_widget.delete(1.0, tk.END)
    #     self.text_widget.insert(tk.END, metadata)
    
    def show(self, metadata):
        # display_data = ""
        # for key, value in metadata.items():
        #     wrapped_value = textwrap.fill(str(value), width=50)  # 긴 문자열을 50자리에서 줄 바꿈
        #     display_data += f"{key}: {wrapped_value}\n\n"

        # self.text_widget.delete(1.0, tk.END)
        # self.text_widget.insert(tk.END, display_data)
        # print(self.format_metadata(metadata))
        formatted_metadata = self.format_metadata(metadata)
        # print(formatted_metadata)
    # 포맷팅된 메타데이터를 Text 위젯에 표시
        self.text_widget.delete(1.0, tk.END)
        # self.text_widget = tk.Text(wrap='word')
        self.text_widget.insert(tk.END, formatted_metadata)

    def format_metadata(self, metadata):
        # 'parameters' 키의 값을 가져와서 줄바꿈
        parameters_text = "parameters: " + metadata.get('parameters', '').replace(',', ',')
        # wrap_length = 50  
        # parameters_text = "parameters:\n" + '\n'.join(textwrap.wrap(parameters_text, wrap_length))
        lines = parameters_text.split('\n')
        print(len(lines))
        # 'Negative prompt' 키의 값을 가져와서 줄바꿈
        negative_prompt_text = "\nNegative prompt:\n\n" + metadata.get('Negative prompt', '').replace(',', ',')
        
        # 나머지 키들에 대한 정보를 줄바꿈하여 가져옴
        remaining_keys = [
            "Steps"
        ]
        # remaining_text = ",".join([f"{key}:\n{metadata.get(key, '')}" for key in remaining_keys])
        remaining_text = ""
        # return f"{parameters_text}\n{negative_prompt_text}\n{remaining_text}"
        return f"{parameters_text}\n"
    # def format_metadata(self, metadata):
    #     # metadata 딕셔너리를 텍스트로 변환
    #     text_representation = str(metadata)
        
    #     # 'parameters:', 'negative prompt:', 'steps:' 를 기준으로 줄바꿈 처리
    #     for keyword in ["'parameters:'", "'negative prompt:'", 'steps:']:
    #         text_representation = text_representation.replace(keyword, '\n' + keyword + '\n')
        
    #     return text_representation
    
root = tk.Tk()
root.title("이미지 분류기")

folder_entry = tk.Entry(root, width=50)
folder_entry.pack(padx=20, pady=(0,10))

folder_select_button = tk.Button(root, text="폴더 선택", command=select_image_folder)
folder_select_button.pack(pady=(0,20))

sorted_folder_label = tk.Label(root, text="정렬될 폴더:")
sorted_folder_label.pack(padx=20, pady=(0,0))

sorted_folder_entry = tk.Entry(root, width=50)
sorted_folder_entry.pack(padx=20, pady=(0,20))


mode_label = tk.Label(root, text="분류 모드:")
mode_label.pack(padx=20, pady=(20,0))

mode_combobox = ttk.Combobox(root, values=["EXIF 키워드", "얼굴 인식"], state="readonly")
mode_combobox.set("EXIF 키워드")
mode_combobox.pack(padx=20, pady=(0,20))

keywords_label = tk.Label(root, text="키워드 (쉼표로 구분, EXIF 모드에서만 사용):")
keywords_label.pack(padx=20, pady=(0,0))

keywords_entry = tk.Entry(root, width=50)
keywords_entry.pack(padx=20, pady=(0,20))

start_button = tk.Button(root, text="시작", command=start)
start_button.pack(pady=20)


metadata_button = tk.Button(root, text="이미지 메타데이터 보기", command=view_metadata)
metadata_button.pack(pady=10)



root.mainloop()

