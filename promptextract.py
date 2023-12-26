import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, Button, ttk
import pandas as pd
import re
import pyperclip
# 숫자 제거 함수 정의

df = None



def remove_numbers_and_split(text):
    # <>로 둘러싸인 부분을 보존하기 위한 임시 치환
    protected_parts = re.findall(r'<[^>]+>', text)
    for i, part in enumerate(protected_parts):
        text = text.replace(part, f'{{REPLACEMENT{i}}}')

    text = re.sub(r'parameters:|Negative prompt:', '', text)
    # 괄호 제거
    text = text.replace('(', '').replace(')', '')

    # :숫자 형식 제거
    text = re.sub(r':\d+|\.\d+', '', text)

    # 임시 치환된 부분을 원래대로 복구
    for i, part in enumerate(protected_parts):
        text = text.replace(f'{{REPLACEMENT{i}}}', part)

    # 쉼표를 구분자로 사용하여 분할
    return text.split(',')

def flatten_list(nested_list):
    flattened_list = [value for sublist in nested_list for value in sublist]
    return flattened_list

# 결과 출력 테이블 클릭 시 텍스트 박스에 추가
def add_result_to_textbox(event):
    selected_item = result_tree.selection()
    if selected_item:
        value = result_tree.item(selected_item)['values'][0]  # "Value" 열 값만 가져오기
        if value not in result_text.get("1.0", tk.END):
            result_text.insert(tk.END, value + ', ')

# 클립보드에 텍스트 복사
def copy_to_clipboard():
    result = result_text.get("1.0", tk.END).strip()
    if result:
        pyperclip.copy(result)
        messagebox.showinfo("클립보드 복사", "텍스트가 클립보드에 복사되었습니다.")

# 엑셀 파일 선택
def select_excel_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx ; *.xls')])
    if file_path:
        load_excel_data(file_path)

# 선택한 컬럼의 데이터 불러오기
def load_excel_data(file_path):
    global df  # Use the global DataFrame
    df = pd.read_excel(file_path)
    column_headers = df.columns.tolist()
    column_combobox['values'] = column_headers
    if column_headers:
        column_combobox.current(0)
        update_column_data(column_headers[0])

def update_column_data(selected_column):
    global df
    column_data = df[selected_column].astype(str).tolist()
    processed_data = [remove_numbers_and_split(value) for value in column_data]
    flattened_data = [item.strip() for sublist in processed_data for item in sublist if item.strip()]  # 공백 제거 및 빈 셀 제거

    # 데이터와 카운트를 함께 정렬
    unique_data = list(set(flattened_data))
    data_count = [flattened_data.count(data) for data in unique_data]
    sorted_data = sorted(zip(unique_data, data_count), key=lambda x: x[1], reverse=True)  # 사용 횟수에 따라 내림차순 정렬

    # Treeview 업데이트
    result_tree.delete(*result_tree.get_children())
    for data, count in sorted_data:
        result_tree.insert("", "end", values=(data, count))


def on_column_selected(event):
    selected_column = column_var.get()
    if selected_column:
        update_column_data(selected_column)

# GUI 생성
root = tk.Tk()
root.title("Excel Data Loader")

# 엑셀 파일 선택 버튼
select_button = tk.Button(root, text="엑셀 파일 선택", command=select_excel_file)
select_button.pack(pady=10)

# 컬럼 선택 라벨 및 콤보박스
column_label = tk.Label(root, text="컬럼 선택:")
column_label.pack()
column_var = tk.StringVar()
column_combobox = ttk.Combobox(root, textvariable=column_var, state="readonly")
column_combobox.bind("<<ComboboxSelected>>", on_column_selected)  
column_combobox.pack()


# 결과 출력 테이블
result_tree = ttk.Treeview(root, columns=("Value", "Count"), show="headings")
result_tree.heading("Value", text="값")
result_tree.heading("Count", text="사용 횟수")
result_tree.pack(pady=10)

# 결과 출력 테이블 클릭 시 텍스트 박스에 추가
result_tree.bind("<ButtonRelease-1>", add_result_to_textbox)

# 결과 출력 텍스트 박스
result_text = tk.Text(root, height=10, width=50)
result_text.pack(pady=10)

# 클립보드에 복사 버튼
copy_button = tk.Button(root, text="클립보드에 복사", command=copy_to_clipboard)
copy_button.pack(pady=10)

root.mainloop()
