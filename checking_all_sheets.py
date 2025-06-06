import pandas as pd
import subprocess #subprocess allows you to call other scripts 
import os
from PyPDF2 import PdfFileMerger  

excel_file = "/Users/yashchohan/Desktop/Riaz Lab/ADA_Project/PWMA_06.24_PARPi.xlsx"
r_script_path_hazard_ratio = "/Users/yashchohan/Desktop/Riaz Lab/ADA_Project/ADA_Project_Test_Script.R"
r_script_path_binary_data = "/Users/yashchohan/Desktop/Riaz Lab/ADA_Project/ADA_Bin_Script.R"
output_dir = "/Users/yashchohan/Desktop/Riaz Lab/ADA_Project/"
total_combined_outputs = os.path.join(output_dir, "total_combined_outputs.pdf")

df_dict = pd.read_excel(excel_file, sheet_name=None)

pdfs = [] #creates an empty list of the pdf documents which I can append as the program runs

for sheet_name, df in df_dict.items():
    cols = df.columns
    
    if "lowerci" in cols:
        output_pdf = os.path.join(output_dir, f"{sheet_name}_HR.pdf")
        #creates a path for the newly created pdf
        result = subprocess.run(
            ["Rscript", r_script_path_hazard_ratio, sheet_name, output_pdf],
            capture_output=True, text=True
        )
        #"Rscript" tells subprocess that you are calling, then you give it the path to the R script, sheet_name and output_pdf are the arguments you pass onto the R script
        #capture_output=True allows you to capture the standard output and standard error and text=True ensures that the output is returned as a string
        if result.returncode == 0:
            print(f"Successfully ran hazard ratio script on {sheet_name}")
            pdfs.append(output_pdf) #adds the newly created pdf to the pdf list
        else:
            print(f"Error in hazard ratio script for {sheet_name}")
            print("stderr:", result.stderr)
            print("stdout:", result.stdout)

    elif "Nt" in cols:
        output_pdf = os.path.join(output_dir, f"{sheet_name}_Bin.pdf")
        result = subprocess.run(
            ["Rscript", r_script_path_binary_data, sheet_name, output_pdf],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"Successfully ran binary data script on {sheet_name}")
            pdfs.append(output_pdf)
        else:
            print(f"Error in binary script for {sheet_name}")
            print("stderr:", result.stderr)
            print("stdout:", result.stdout)

    else:
        print(f"Sheet {sheet_name} does not have data for analysis")

merger = PdfFileMerger() #creates a new pdf file merger object in the PdfFileMerger lib

for pdf in pdfs:
    if os.path.exists(pdf): #checks if the file exists
        merger.append(pdf) #if it does, adds it to the total outputs pdf
    else:
        print(f" missing file: {pdf}")

merger.write(total_combined_outputs) #creates the total combined outputs pdf from the merged pdfs
merger.close() #closes the merger 

for pdf in pdfs:
    try:
        os.remove(pdf)
    except:
        total_combined_outputs

print("total output pdf created")
