'''
Excel to PDF Converter

This program utilizes Tkinter, FPDF, and Pandas modules to convert Excel files to PDF.

Modules:
- `tkinter`: Provides the GUI for selecting Excel files and generating PDFs.
- `fpdf`: Enables PDF generation from Excel data.
- `pandas`: Used for reading and processing Excel data efficiently.

Functions:
- `generate_pdf()`: Initiates PDF generation from the selected Excel file.
- `choose_file()`: Opens a file dialog to select an Excel file.
'''
# Imports for GUI
import tkinter as tk
from tkinter import filedialog

# Import for PDF
from fpdf import FPDF
# Import to read Excel
import pandas as pd
import os

# Generate PDF from selected Excel file
def generate_pdf():
    excel_file_path = file_entry.get()
    pdf_name = pdf_name_entry.get()

    if excel_file_path == '':
        status_label.config(text="Please choose an Excel file.", fg="red")
        return

    if pdf_name == '':
        status_label.config(text="Please enter a PDF name.", fg="red")
        return

    try:
        df = pd.read_excel(excel_file_path)
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial","I",8)

        for _, row in df.iterrows():
            for value in row:
                pdf.cell(40, 10, str(value), ln=True)

        excel_directory = os.path.dirname(excel_file_path)
        pdf.output(os.path.join(excel_directory, f"{pdf_name}.pdf"))
        status_label.config(text="PDF generated successfully.", fg="green")
        root.after(1000, root.quit)  # Exit after 2000 milliseconds (2 seconds)
    except Exception as e:
        status_label.config(text=f"Error: {e}", fg="red")

def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

# Create the main window
root = tk.Tk()
root.title("Excel to PDF Converter")

# Styles
background_color = "#f0f0f0"
font_style = ("Arial", 10)
button_bg_color = "#4caf50"
button_fg_color = "white"
button_hover_color = "#388e3c"

root.config(bg=background_color)

# File Selection
file_frame = tk.Frame(root, bg=background_color)
file_frame.pack(pady=20)

file_label = tk.Label(file_frame, text="Select Excel file:", bg=background_color, font=font_style)
file_label.grid(row=0, column=0, padx=10)

file_entry = tk.Entry(file_frame, width=50, font=font_style)
file_entry.grid(row=0, column=1, padx=10)

browse_button = tk.Button(file_frame, text="Browse", command=choose_file, bg=button_bg_color, fg=button_fg_color, 
                          activebackground=button_hover_color, activeforeground="white", font=font_style)
browse_button.grid(row=0, column=2, padx=10)

# PDF Name
pdf_frame = tk.Frame(root, bg=background_color)
pdf_frame.pack(pady=20)

pdf_name_label = tk.Label(pdf_frame, text="Enter PDF name:", bg=background_color, font=font_style)
pdf_name_label.grid(row=0, column=0, padx=10)

pdf_name_entry = tk.Entry(pdf_frame, width=50, font=font_style)
pdf_name_entry.grid(row=0, column=1, padx=10)

# Generate PDF button
generate_button = tk.Button(root, text="Generate PDF", command=generate_pdf, bg=button_bg_color, fg=button_fg_color,
                            activebackground=button_hover_color, activeforeground="white", font=font_style)
generate_button.pack(pady=20)

# Status Label
status_label = tk.Label(root, text="", bg=background_color, font=font_style)
status_label.pack()

root.mainloop()
