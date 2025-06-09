import os

inputfile = input("please enter your excel file name: ")
inputfilexlsx = inputfile + ".xlsx"


project_dir = "/Users/yashchohan/Desktop/Riaz Lab/ADA_Project/"
os.chdir(project_dir)

excel_file_dir_path = project_dir
excel_file_abs_path = os.path.abspath(inputfilexlsx)


while True:
    directory = input(f"do you want to save the pdf in the directory {excel_file_dir_path}? (yes/no): ")
    if directory == "yes":
        output_dir = os.path.dirname(excel_file_abs_path)
        break
    elif directory == "no":
        while True:
            output_loc = input("please enter the directory path you would like to save the pdf to")
            if os.path.exists(output_loc):
                output_dir = output_loc
                break
            else:
                print("this directory does not exist")
        break
    else:
        print("please respond with \"yes\" or \"no\"")
    

def sheet_checker(excel_file_abs_path, output_dir):
    
    import pandas as pd
    import subprocess #subprocess allows you to call other scripts 
    import os
    from PyPDF2 import PdfFileMerger  

    r_script_path_hazard_ratio = "/Users/yashchohan/Desktop/Riaz Lab/ADA_Project/ADA_Project_Test_Script.R"
    r_script_path_binary_data = "/Users/yashchohan/Desktop/Riaz Lab/ADA_Project/ADA_Bin_Script.R"
    total_combined_outputs = os.path.join(output_dir, "total_combined_outputs.pdf")

    df_dict = pd.read_excel(excel_file_abs_path, sheet_name=None)
    pdfs = []

    for sheet_name, df in df_dict.items():
        cols = df.columns
    
        if "lowerci" in cols:
            output_pdf = os.path.join(output_dir, f"{sheet_name}_HR.pdf")
            result = subprocess.run(
                ["Rscript", r_script_path_hazard_ratio, sheet_name, output_pdf, excel_file_abs_path],
                capture_output=True, text=True
            )

            if result.returncode == 0:
                print(f"Successfully ran hazard ratio script on {sheet_name}")
                pdfs.append(output_pdf) 
            else:
                print(f"Error in hazard ratio script for {sheet_name}")
                print("stderr:", result.stderr)
                print("stdout:", result.stdout)
        
        elif "Nt" in cols:
            output_pdf = os.path.join(output_dir, f"{sheet_name}_Bin.pdf")
            result = subprocess.run(
                ["Rscript", r_script_path_binary_data, sheet_name, output_pdf, excel_file_abs_path],
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
    
    merger = PdfFileMerger() 

    for pdf in pdfs:
        if os.path.exists(pdf): 
            merger.append(pdf) 
        else:
            print(f" missing file: {pdf}")

    merger.write(total_combined_outputs) 
    merger.close()  

    for pdf in pdfs:
        try:
            os.remove(pdf)
        except:
            total_combined_outputs

    print("total output pdf created")

sheet_checker(excel_file_abs_path, output_dir)

#file name PWMA_06.24_PARPi
#output directory /Users/yashchohan/Desktop/Riaz Lab/ADA_Project/
