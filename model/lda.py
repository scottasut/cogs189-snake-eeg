import numpy as np

class LDA:
    def fit(self, X: np.ndarray, y: np.array) -> None:
        """Fit the Linear Discriminant Analysis model to given data.
        
        Calculates the optimal projection vector 'w' and optimal class threshold 'c'

        Args:
            X (np.ndarray): point data
            y (np.array): class truth values
        """
        # Calculate covariance matrix
        u = np.mean(X, axis=0).reshape(-1, 1)
        scatter = np.zeros((X.shape[1], X.shape[1]))
        for x in X:
            diff = x - u
            scatter += diff @ diff.T
        cov = scatter / X.shape[0]

        # Calculate optimal projection vector
        left, right = X[y == 0], X[y == 1]
        u_l, u_r = np.mean(left, axis=0).reshape(-1, 1), np.mean(right, axis=0).reshape(-1, 1)
        self.w = np.linalg.inv(cov) @ (u_r - u_l)

        # Calculate optimal threshold
        self.c = self.w.T @ ((u_r + u_l) / 2)
    
    def predict(self, X: np.ndarray) -> np.array:
        """Classify all points in given data.

        Args:
            X (np.ndarray): point data

        Returns:
            np.array: classification predictions for each point {0, 1}
        """
        X_proj = X @ self.w
        return X_proj.flatten() > self.c

    def score(self, X: np.ndarray, y: np.array) -> float:
        """Calculates accuracy of predictions on given point data compared to given class truth labels.

        Args:
            X (np.ndarray): point data
            y (np.array): class truth values 

        Returns:
            float: classification accuracy [0, 1]
        """
        return np.mean(self.predict(X) == y)
