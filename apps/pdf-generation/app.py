'''
This program generates a PDF file from an Excel file using a graphical user interface (GUI) built with CustomTkinter.

Dependencies:
- CustomTkinter: A custom-themed interface built on top of Tkinter for GUI design.
- fpdf: A Python library used for PDF generation.
- pandas: A library used for data manipulation with Excel files.
- os: A standard Python library used for file operations.

Methods/Functions:
- choose_file():  Opens a file dialog window to choose an Excel file.
- generate_pdf(): Generates a PDF file from the selected Excel file and user-provided PDF name.

Usage:
1. Run the program.
2. Use the 'Browse' button to select an Excel file (*.xlsx).
3. Enter the desired name for the resulting PDF file.
4. Click 'Generate PDF' to create the PDF file from the Excel data.

Note: 
- Ensure that the selected Excel file contains data in a readable format.
- The generated PDF file will be saved in the SAME directory as the selected Excel file.
'''
# Import tkinter and CustomTkinter for GUI design
from tkinter import filedialog
from tkinter import CENTER
import customtkinter

# Import fpdf for pdf generation, pandas for reading Excel file, os to manage file-paths
from fpdf import FPDF
import pandas as pd
import os

# Define window width and height
WIDTH = 400
HEIGHT = 340

# Set theme and default color
customtkinter.set_appearance_mode("dark")

# Init. window
root = customtkinter.CTk()

# Set properties of window
root.geometry(str(WIDTH)+"x"+str(HEIGHT)) 
root.title("PDF Generator")
root.resizable(False, False)

# Choose Excel file to be converted
def choose_file():
    '''Opens a file dialog window to select an Excel file (*.xlsx).'''
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    file_entry.delete(0, customtkinter.END)
    file_entry.insert(0, file_path)

# Generate PDF
def generate_pdf():
    '''Generates a PDF file from the selected Excel file and user-provided PDF name.'''
    excel_file_path = file_entry.get()
    pdf_name = pdf_name_entry.get()

    # Check if excel file is selected
    if excel_file_path == '':
        status_label.configure(text="Please choose an Excel file.", text_color="red")
        return

    # Check if pdf name has been inputted
    if pdf_name == '':
        status_label.configure(text="Please enter a PDF name.", text_color="red")
        return

    # Go through excel sheet, and generate PDF at same location
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
        status_label.configure(text="PDF generated successfully.", text_color="green")
        root.after(1000, root.quit)  # Exit after 2000 milliseconds (2 seconds)
    
    except Exception as e:
        status_label.configure(text=f"Error: {e}", text_color="red")


# File select UI components
file_frame = customtkinter.CTkFrame(master=root, width=int(0.9*WIDTH), height=80) #, fg_color="transparent"
file_frame.place(relx=0.5, rely=0.20, anchor=CENTER)

file_entry = customtkinter.CTkEntry(master=file_frame,placeholder_text="Choose file...", width=int(0.85*WIDTH), height=30)
file_entry.place(relx=0.5, rely=0.3, anchor=CENTER)

# Create browse/select button
selectButton = customtkinter.CTkButton(master=file_frame, text="Browse", command=choose_file)
selectButton.place(relx=0.5, rely=0.75, anchor=CENTER)

# PDF name UI components
pdf_frame = customtkinter.CTkFrame(master=root, width=int(0.9*WIDTH), height=80) #, fg_color="transparent"
pdf_frame.place(relx=0.5, rely=0.5, anchor=CENTER) 

pdf_name_entry = customtkinter.CTkEntry(master=pdf_frame,placeholder_text="Enter PDF Name...", width=int(0.85*WIDTH), height=30)
pdf_name_entry.place(relx=0.5, rely=0.3, anchor=CENTER)

# Create generate button
generateButton = customtkinter.CTkButton(master=pdf_frame, text="Generate PDF", fg_color="green", hover_color="#154406", command=generate_pdf)
generateButton.place(relx=0.5, rely=0.75, anchor=CENTER)

# Status Label
status_label = customtkinter.CTkLabel(master=root, text="", font=("Arial",15)) #, fg_color="transparent"
status_label.place(relx=0.5, rely=0.8, anchor=CENTER)

# run the app
root.mainloop()