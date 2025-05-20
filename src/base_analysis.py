from abc import ABC, abstractmethod
import pandas as pd

class BaseAnalysis(ABC):
    """
    Abstract Base Class for data profeling and EDA
    """

    def __init__(self, file_path: str):
        """
        Initialize the class with the file path.
        """
        self.file_path = file_path
        self.df = None

    def load_data(self):
        """
        Loads the dataset into a DataFrame.
        """
        self.df = pd.read_csv(self.file_path)
        print("Dataset loaded successfully.")

    @abstractmethod
    def overview(self):
        pass

    @abstractmethod
    def scatter_plot(self):
        pass

    @abstractmethod
    def plot_correlation_heatmap(self):
        pass

    @abstractmethod
    def visualize_histograms(self):
        pass
