import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import os
import pandas as pd

from src.base_analysis import BaseAnalysis

class DataAnalysis(BaseAnalysis):
    """
    Concrete class for Data Analysis that extends BaseAnalysis.
    Includes visualization, outlier detection, and exploratory data analysis.
    """

    def __init__(self, file_path):
        super().__init__(file_path)
        self.numeric_cols = None
        self.outer_flags = None

    def overview(self):
        """
        Provides an overview of the dataset: head, tail, sample, and shape.
        """
        print("\n =================== Dataset Overview:===================================")
        print(self.df.head(10))
        print("\n ============================== Last 5 Rows of the Dataset:========================")
        print(self.df.tail())
        print("\n ================================ Random Sample of 5 Rows:=============================")
        print(self.df.sample(5))
        print("\n =================================== Dataset Shape:=====================================")
        print(self.df.shape)
       

    def describe_numeric(self):
        """
        Provides a description of numeric columns.
        """
        print("\n The description of the numeric columns:")
        print(self.df.describe())

    def describe_categorical_columns(self):
        """
        Provides a description of categorical (object) columns.
        """
        print("\n The description of the categorical columns:")
        print(self.df.describe(include=['object']))
    
    def info(self):
        print("an overview of the dataset: the shape of the dataset")
        print(self.df.info())
    
    def find_missing_value(self):
        # check for missing values 
        print("check for missing values")
        print(self.df.isna().sum())
    
    def drop_column(self, column_name):
        """Drops a column from the DataFrame if it exists."""
        if column_name in self.df.columns:
            self.df.drop(columns=column_name, inplace=True)
            print(f"successfuly dropped {column_name} column")
        else:
            print(f"Column '{column_name}' does not exist in the DataFrame.")
    
    def report_null_columns(self, threshold=5):
        """
        Prints columns with missing data percentage greater than the given threshold.

        :param threshold: Percentage threshold to filter columns with null values.
        """
        missing_percentages = self.df.isna().mean() * 100
        columns_with_nulls = missing_percentages[missing_percentages > threshold]
        print("Columns with missing values > {}%:\n".format(threshold))
        print(columns_with_nulls)
    
    def check_specific_missing_values(self, columns):
        """
        Checks for missing values in the specified list of columns.

        :param columns: List of column names to check.
        :return: Pandas Series of missing value counts for each specified column.
        """
        existing_columns = [col for col in columns if col in self.df.columns]
        missing_values = self.df[existing_columns].isna().sum()
        print(missing_values)

    def detect_outliers(self, numeric_cols):
        print("=== Outlier Detection ===")
        existing_columns = [col for col in numeric_cols if col in self.df.columns]
        if not existing_columns:
            print("No valid numeric columns found in the dataset.")
            return
        self.numeric_cols = existing_columns
        z_scores = np.abs(stats.zscore(self.df[existing_columns].dropna()))
        outlier_flags = (z_scores > 3).any(axis=1)
        self.outlier_flags = outlier_flags

        print(f"Number of outlier samples flagged: {outlier_flags.sum()}")

    def impute_outliers(self):
        """
        Imputes outliers with the median of the respective columns.
        """
        for col in self.numeric_cols:
            self.df.loc[self.outlier_flags, col] = self.df[col].median()
        print("\n Outliers have been replaced with median values.")
    
    def export_cleaned_data(self, export_path, file_name):
        """
        Exports the cleaned DataFrame to the specified directory as a CSV file.
        
        Parameters:
        - export_path (str): The absolute or relative directory to save the CSV file.
        - file_name (str): The name of the file to save. Default is 'benin_clean.csv'.
        """
        os.makedirs(export_path, exist_ok=True)
        full_path = os.path.join(export_path, file_name)
        self.df.to_csv(full_path, index=False)
        print(f"Data exported to {full_path} successfully!")

    def plot_time_series(self):
        """
        Performs time series visualization for selected variables (GHI, DNI, DHI, and Tamb).
        
        - Converts 'Timestamp' column to datetime format.
        - Sets 'Timestamp' as the DataFrame index.
        - Generates subplots showing each variable over time.
        """
        # Ensure Timestamp is in datetime format
        self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'], errors='coerce')

        # Drop rows with invalid timestamps
        self.df.dropna(subset=['Timestamp'], inplace=True)

        # Set Timestamp as index
        self.df.set_index('Timestamp', inplace=True)

        # Plot Time Series
        plt.figure(figsize=(15, 8))

        plt.subplot(2, 2, 1)
        plt.plot(self.df.index, self.df['GHI'], color='orange')
        plt.title('Global Horizontal Irradiance (GHI) Over Time')
        plt.xlabel('Time')
        plt.ylabel('GHI (W/m²)')

        plt.subplot(2, 2, 2)
        plt.plot(self.df.index, self.df['DNI'], color='red')
        plt.title('Direct Normal Irradiance (DNI) Over Time')
        plt.xlabel('Time')
        plt.ylabel('DNI (W/m²)')

        plt.subplot(2, 2, 3)
        plt.plot(self.df.index, self.df['DHI'], color='blue')
        plt.title('Diffuse Horizontal Irradiance (DHI) Over Time')
        plt.xlabel('Time')
        plt.ylabel('DHI (W/m²)')

        plt.subplot(2, 2, 4)
        plt.plot(self.df.index, self.df['Tamb'], color='green')
        plt.title('Ambient Temperature (Tamb) Over Time')
        plt.xlabel('Time')
        plt.ylabel('Temperature (°C)')

        plt.tight_layout()
        plt.show()
    
    def plot_monthly_averages(self):
        """
        Computes and plots the monthly averages of GHI, DNI, DHI, and Tamb.

        Assumes 'Timestamp' is already set as the DataFrame index in datetime format.
        """

        # Extract month (optional if needed later)
        self.df['Month'] = self.df.index.month

        # Compute monthly averages
        monthly_avg = self.df[['GHI', 'DNI', 'DHI', 'Tamb']].resample('ME').mean()

        # Plot the data
        monthly_avg.plot(figsize=(12, 6), title='Monthly Averages of GHI, DNI, DHI, and Tamb')
        plt.xlabel('Month')
        plt.ylabel('Average Value')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_hourly_averages(self):

        """
        Computes and plots the average values of GHI, DNI, DHI, and Tamb for each hour of the day.

        Assumes 'Timestamp' is already set as the DataFrame index and is of datetime type.
        """
        # Extract hour from timestamp
        self.df['Hour'] = self.df.index.hour

        # Compute average for each hour
        hourly_avg = self.df.groupby('Hour')[['GHI', 'DNI', 'DHI', 'Tamb']].mean()

        # Plot
        hourly_avg.plot(figsize=(12, 6), title='Hourly Averages of GHI, DNI, DHI, and Tamb')
        plt.xlabel('Hour of Day')
        plt.ylabel('Average Value')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    
    def analyze_cleaning_impact(self):

        """
        Analyzes the impact of the 'Cleaning' flag on the performance of ModA and ModB.
        It calculates the average values of ModA and ModB grouped by the Cleaning flag.
        """

        # Group by 'Cleaning' and calculate mean
        cleaning_impact = self.df.groupby('Cleaning')[['ModA', 'ModB']].mean().reset_index()

        # Display the result
        print("=== Cleaning Impact on ModA and ModB ===")
        print(cleaning_impact)

        # Optional: Plot the result for better visualization
        cleaning_impact.set_index('Cleaning').plot(kind='bar', figsize=(8, 5))
        plt.title('Effect of Cleaning on ModA and ModB Output')
        plt.ylabel('Average Output')
        plt.xlabel('Cleaning Performed')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    
    def scatter_plot(self):
        """
        Plots the relationship between wind speed (WS and WSgust) and Global Horizontal Irradiance (GHI).
        Color intensity (hue) represents the GHI value in both scatter plots.
        """

        print("=== Wind Speed vs GHI Scatter Plots ===")

        # Scatter plot: WS vs GHI
        sns.scatterplot(data=self.df, x="WS", y="GHI", hue="GHI")
        plt.title("Global vs. Direct Normal Irradiance by Wind Speed")
        plt.show()

        # Scatter plot: WSgust vs GHI
        sns.scatterplot(data=self.df, x="WSgust", y="GHI", hue="GHI")
        plt.title("GHI vs DNI with Cleaning Events")
        plt.show()

    def plot_correlation_heatmap(self, numeric_cols=None):

        """
        Computes and visualizes the correlation matrix for specified numeric columns.
        
        Parameters:
        -----------
        numeric_cols : list of str, optional
            List of numeric column names to include in the correlation matrix.
            If None, defaults to ['GHI', 'DNI', 'DHI', 'TModA', 'TModB'].
        """
        if numeric_cols is None:
            numeric_cols = ["GHI", "DNI", "DHI", "TModA", "TModB"]

        print("=== Correlation Matrix Heatmap ===")
        corr_matrix = self.df[numeric_cols].corr()

        plt.figure(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", square=True, linewidths=0.5)
        plt.title("Correlation Matrix of Solar Features")
        plt.tight_layout()
        plt.show()

    def wind_and_distribution_analysis(self, columns):
        """
        Performs Wind and Distribution Analysis by plotting histograms with KDE
        for 'GHI' (Global Horizontal Irradiance) and 'WS' (Wind Speed) to observe 
        their distributions.
        """
        print("=== Wind & Distribution Analysis ===")
        numeric_cols_selected = columns
        
        for col in numeric_cols_selected:
            sns.histplot(self.df[col], kde=True)
            plt.title(f"{col} Distribution")
            plt.xlabel(col)
            plt.ylabel("count")
            plt.show()
    

    def visualize_histograms(self):
        """
        Plots histograms for each numeric feature.
        """
        print("\n Histograms for Numeric Features:")
        for col in self.numeric_cols:
            sns.histplot(self.df[col], kde=True)
            plt.title(f"{col} Distribution")
            plt.xlabel(col)
            plt.ylabel("Count")
            plt.show()

    def visualize_scatter_plots(self):
        """
        Plots bivariate scatter plots for key features.
        """
        print("\n Scatter Plots:")
        sns.scatterplot(data=self.df, x="GHI", y="DNI", hue="WS")
        plt.title("Global vs. Direct Normal Irradiance by Wind Speed")
        plt.show()

        sns.scatterplot(data=self.df, x="GHI", y="DNI", hue="Cleaning")
        plt.title("GHI vs DNI with Cleaning Events")
        plt.show()

    
    def tempature_analysis(self):
        plt.figure(figsize=(6, 4))
        sns.scatterplot(data=self.df, x="RH", y="Tamb", hue="GHI", palette="coolwarm")
        plt.title("Relative Humidity vs. Temperature (Colored by GHI)")
        plt.xlabel("Relative Humidity (%)")
        plt.ylabel("Temperature (°C)")
        plt.show()

        # Scatter Plot: RH vs. GHI
        plt.figure(figsize=(6, 4))
        sns.scatterplot(data=self.df, x="RH", y="GHI", hue="DNI", palette="coolwarm")
        plt.title("Relative Humidity vs. Global Horizontal Irradiance (Colored by DNI)")
        plt.xlabel("Relative Humidity (%)")
        plt.ylabel("Global Horizontal Irradiance (W/m²)")
        plt.show()

    def bubble_chart(self):
        # Bubble Chart with RH as size
        plt.figure(figsize=(8, 5))
        plt.scatter(self.df["GHI"], self.df["Tamb"], s=self.df["RH"] * 0.5, alpha=0.6, color='teal')
        plt.title("GHI vs. Temperature with Bubble Size = RH")
        plt.xlabel("Global Horizontal Irradiance (GHI)")
        plt.ylabel("Temperature (°C)")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.show()

        # Bubble Chart with BP as size
        plt.figure(figsize=(8, 5))
        plt.scatter(self.df["GHI"], self.df["Tamb"], s=self.df["BP"] * 0.02, alpha=0.5, color='orange')
        plt.title("GHI vs. Temperature with Bubble Size = BP")
        plt.xlabel("Global Horizontal Irradiance (GHI)")
        plt.ylabel("Temperature (°C)")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.show()





