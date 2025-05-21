# moonlight-solar-strategy-analysis

Overview

This directory (scripts/) contains documentation for the moonlight-solar-strategy-analysis project, which analyzes solar energy data for Benin, Sierra Leone, and Togo. The project includes Python scripts and a Jupyter Notebook to perform exploratory data analysis (EDA), visualization, and statistical comparisons of solar metrics such as Global Horizontal Irradiance (GHI), Direct Normal Irradiance (DNI), and Diffuse Horizontal Irradiance (DHI).

moonlight-solar-strategy-analysis/
├── app/                      # Streamlit web app
│   ├── main.py
│   └── README.md
├── data/                     # Raw and cleaned solar datasets (ignored via .gitignore)
│   ├── benin_clean.csv
│   ├── sierraleone_clean.csv
│   └── togo_clean.csv
├── src/                      # Source code
│   ├── base_analysis.py      # Abstract base class for EDA and visualization
│   └── solar_analysis.py     # Concrete implementation for solar-specific analysis
├── notebooks/                # Jupyter notebooks for analysis
│   ├── benin_eda.ipynb
│   ├── sierraleone-bumbuna_eda.ipynb
│   ├── togo_eda.ipynb
│   ├── compare_countries.ipynb  # Comparative analysis of countries
│   └── notebook_helpers.py
├── scripts/                  # This folder - contains documentation and helpers
│   ├── __init__.py
│   └── README.md             # You are here
├── .gitignore
└── README.md                 # Main project-level README
```

---

## Directory Descriptions

* **`app/`**: Contains the main Streamlit application code for visualizing solar insights interactively.

* **`data/`**: Contains raw and cleaned solar datasets (`*.csv`). This folder is excluded in `.gitignore` to avoid pushing large or sensitive data to version control.

* **`src/base_analysis.py`**: Defines the `BaseAnalysis` abstract class. It includes common methods for loading data and abstract methods like:

  * `overview`
  * `scatter_plot`
  * `plot_correlation_heatmap`
  * `visualize_histograms`

* **`src/solar_analysis.py`**: Implements the `DataAnalysis` class, which extends `BaseAnalysis` to add:

  * Data cleaning
  * Outlier detection
  * Boxplots, time series, and correlation heatmaps

* **`notebooks/`**: Jupyter Notebooks for in-depth analysis:

  * Country-specific EDA (`benin_eda.ipynb`, `togo_eda.ipynb`, etc.)
  * Cross-country comparisons (`compare_countries.ipynb`) using boxplots and statistical tests (ANOVA, Kruskal-Wallis)


---


