import subprocess
from IPython.display import display, IFrame

r_script_path = "/Users/yashchohan/Desktop/Riaz Lab/ADA_Project/ADA_Project_Test_Script.R"
output_pdf = "/Users/yashchohan/Desktop/Riaz Lab/ADA_Project/forest_plot.pdf"

# Run the R script using Rscript command
result = subprocess.run(["Rscript", r_script_path], capture_output=True, text=True)

# Print output and errors for debugging
print("Rscript stdout:")
print(result.stdout)
print("Rscript stderr:")
print(result.stderr)

# Check if R script ran successfully
if result.returncode != 0:
    print("Error running R script!")
else:
    print("R script ran successfully!")

# Display the resulting PDF plot
display(IFrame(output_pdf, width=700, height=600))