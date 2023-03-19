import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

class LDAHandler:
    """
    Wrapper class for sklearn.discriminant_analysis.LinearDiscriminantAnalysis to
    convert EEG data to left/right movement predictions.
    """

    def __init__(self, class_mapping: dict, **model_params) -> None:
        """Instantiates Linear Discriminant Analysis model and class mapping. 

        Args:
            class_mapping (dict): Mapping of truth values to directions.
        """
        self.__clf = LDA(**model_params)
        self.__class_mapping = class_mapping
    
    def fit(self, X: np.ndarray, y: np.array) -> None:
        """Fits the Linear Discriminant Analysis model to point data and class truth labels.

        Args:
            X (np.ndarray): Point data.
            y (np.array): Class truth labels.
        """
        self.__clf.fit_transform(X, y)
    
    def predict(self, X: np.ndarray, direction=True) -> np.array:
        """Predicts class/direction of passed points.

        Args:
            X (np.ndarray): Point data.
            direction (bool, optional): If True, return predicted direction, return class label otherwise. 
                                        Defaults to True.

        Returns:
            np.array: Predictions.
        """
        predictions = self.__clf.predict(X)
        if not direction:
            return predictions
        return np.array([self.__class_mapping[p] for p in predictions])

    def score(self, X: np.ndarray, y: np.array) -> float:
        """Calculates prediction accuracy for given data.

        Args:
            X (np.ndarray): Point data.
            y (np.array): Class truth labels.

        Returns:
            float: Propotion of correct predictions according to given truth.
        """
        return self.__clf.score(X, y)
