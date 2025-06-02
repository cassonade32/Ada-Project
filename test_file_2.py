import subprocess


r_script_path = "/Users/yashchohan/Desktop/Riaz Lab/ADA_Project/ADA_Project_Test_Script.R"
output_pdf = "/Users/yashchohan/Desktop/Riaz Lab/ADA_Project/forest_plot.pdf"

# Code to run the r script
result = subprocess.run(["Rscript", r_script_path], capture_output=True, text=True)

# This will let me check if my script actually ran properly or not
if result.returncode != 0:
    print("Error running R script!")
else:
    print("R script ran successfully!")

# This will let me display the foresplot as a pdf

subprocess.run(["open", output_pdf])
