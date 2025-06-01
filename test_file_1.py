import pandas as pd
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import pandas2ri
from IPython.display import display, IFrame

# Import R packages
utils = importr('utils')
dplyr = importr('dplyr')
readxl = importr('readxl')
meta = importr('meta')

# Read the Excel sheet
r_df = robjects.r('readxl::read_excel("/Users/yashchohan/Desktop/Riaz Lab/ADA_Project/PWMA_05.25_PARPi.xlsx", sheet = "COMBO_OS_OVERALL")')

# Assign to global R variable
robjects.globalenv['ada_data'] = r_df

# Run analysis and plot using R code
robjects.r('''
ada_data$TE <- log(ada_data$TE)
ada_data$lowerci <- log(ada_data$lowerci)
ada_data$upperci <- log(ada_data$upperci)
ada_data$SE <- (ada_data$upperci - ada_data$lowerci) / 3.92

results <- metagen(
  TE,
  SE,
  data = ada_data,
  studlab = ada_data$study,
  sm = "HR",
  common = FALSE,
  random = TRUE,
  method.tau = "DL",
  method.random.ci = "classic"
)

# Save forest plot as PDF
pdf("/Users/yashchohan/Desktop/Riaz Lab/ADA_Project/forest_plot.pdf", width = 8, height = 6)
forest(results,
       col.square = "black",
       col.diamond = "red",
       col.diamond.lines.random = "black",
       print.pval = TRUE,
       smlab = "Hazard Ratio (95% CI)",
       weight.study = "random",
       label.right = "Favors ADT",
       label.left = "Favors Doublet")
dev.off()
''')


display(IFrame("/Users/yashchohan/Desktop/Riaz Lab/ADA_Project/forest_plot.pdf", width=700, height=600))

