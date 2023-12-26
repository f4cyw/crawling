import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, Button
import pandas as pd

class ExcelFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel Filter")

        self.sheet_listbox = Listbox(root, selectmode="single")
        self.sheet_listbox.pack(side="left", fill="both", expand=True)

        self.column_listbox = Listbox(root, selectmode="single")
        self.column_listbox.pack(side="left", fill="both", expand=True)

        self.value_listbox = Listbox(root, selectmode="multiple")
        self.value_listbox.pack(side="left", fill="both", expand=True)

        Button(root, text="Select File", command=self.filter_excel_file).pack()
        Button(root, text="Confirm Sheet", command=self.on_sheet_selected).pack()
        Button(root, text="Confirm Column", command=self.on_column_selected).pack()
        Button(root, text="Confirm Values", command=self.on_value_selected).pack()
        Button(root, text="Select All", command=lambda: self.value_listbox.select_set(0, tk.END)).pack()

    def filter_excel_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not self.file_path:
            return

        try:
            xls = pd.ExcelFile(self.file_path)
            sheet_names = xls.sheet_names

            self.sheet_listbox.delete(0, tk.END)
            for sheet in sheet_names:
                self.sheet_listbox.insert(tk.END, sheet)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_sheet_selected(self):
        selected_sheet_index = self.sheet_listbox.curselection()[0]
        selected_sheet = self.sheet_listbox.get(selected_sheet_index)
        self.df = pd.read_excel(self.file_path, sheet_name=selected_sheet, header=4)
        column_headers = self.df.columns.tolist()

        self.column_listbox.delete(0, tk.END)
        for header in column_headers:
            self.column_listbox.insert(tk.END, header)

    def on_column_selected(self):
        selected_column_index = self.column_listbox.curselection()[0]
        self.selected_column = self.df.columns[selected_column_index]
        unique_values = self.df[self.selected_column].unique().tolist()

        self.value_listbox.delete(0, tk.END)
        for value in unique_values:
            self.value_listbox.insert(tk.END, value)

    def on_value_selected(self):
        selected_items = [self.value_listbox.get(i) for i in self.value_listbox.curselection()]
        if not selected_items:
            messagebox.showwarning("No Selection", "No value selected.")
            return

        filtered_data = self.df[self.df[self.selected_column].isin(selected_items)]

        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not save_path:
            return

        with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
            for value in selected_items:
                filtered_sheet_data = filtered_data[filtered_data[self.selected_column] == value]
                filtered_sheet_data.to_excel(writer, index=False, sheet_name=str(value)[:31])

        messagebox.showinfo("Success", "Data has been filtered and saved successfully!")

# GUI 실행
root = tk.Tk()
app = ExcelFilterApp(root)
root.mainloop()
