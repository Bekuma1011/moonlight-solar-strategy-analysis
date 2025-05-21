# moonlight-solar-strategy-analysis

Overview

This directory (scripts/) contains documentation for the moonlight-solar-strategy-analysis project, which analyzes solar energy data for Benin, Sierra Leone, and Togo. The project includes Python scripts and a Jupyter Notebook to perform exploratory data analysis (EDA), visualization, and statistical comparisons of solar metrics such as Global Horizontal Irradiance (GHI), Direct Normal Irradiance (DNI), and Diffuse Horizontal Irradiance (DHI).

moonlight-solar-strategy-analysis/
|-- app
|   |--main.py
|   |--README.md
├── data/                    # Ignored in .gitignore; contains cleaned CSV files
│   ├── benin_clean.csv
│   ├── sierraleone_clean.csv
│   ├── togo_clean.csv
├── src/                     # Python source code
│   ├── base_analysis.py     # Abstract base class for data analysis
│   ├── solar_analysis.py    # Concrete class for solar data analysis
├── notebooks/               # Jupyter Notebooks
│   ├── compare_countries.ipynb   # Notebook for comparing solar metrics across countries
|   |-- benin_eda.ipynb
|   |-- compare_countries.ipynb
|   |-- notebook_helpers.py
|   |-- sierraleone-bumbuna_eda.ipynb 
|   |-- togo_eda.ipynb
|   |           
├── scripts/                 # Documentation and scripts
│   ├── __init__.py
│   ├── README.md            # This file
├── .gitignore
├── README.md                # Project-level README (assumed to exist)



app/:  

data/: Contains cleaned CSV files (benin_clean.csv, sierraleone_clean.csv, togo_clean.csv), ignored in .gitignore to prevent committing sensitive or large data files. and also contains raw data files 

src/base_analysis.py: Defines the BaseAnalysis abstract base class with methods for loading data and required abstract methods (overview, scatter_plot, plot_correlation_heatmap, visualize_histograms).


src/solar_analysis.py: Defines the DataAnalysis class, which extends BaseAnalysis to provide solar-specific analysis, including data cleaning, outlier detection, and visualizations like boxplots, time series, and correlation heatmaps.


notebooks/:  A Jupyter Notebook that compares GHI, DNI, and DHI across Benin, Sierra Leone, and Togo using boxplots and statistical tests (ANOVA and Kruskal-Wallis). 