from pynput.keyboard import Key, Controller
import numpy as np
import sys
sys.path.append('../')
from model.lda import LDAHandler

keyboard = Controller()
X = np.load('../data/processed/X.npy')
y = np.load('../data/processed/y.npy')
train_size = 0.8
shuffle = np.random.permutation(len(X))
X, y = X[shuffle], y[shuffle]
X_train, y_train, X_test, y_test = X[:int(train_size * len(X))], y[:int(train_size * len(X))], X[int(train_size * len(X)):], y[int(train_size * len(X)):]
lda = LDAHandler({0:'LEFT', 1:'RIGHT'})
lda.fit(X_train, y_train)

def trigger_key(key: str):
    """Triggers a left or right arrow keyboard press.

    Args:
        key (str): Key to press. Input not in {'LEFT', 'RIGHT'} is ignored.
    """
    if key == 'LEFT':
        keyboard.press(Key.left)
    elif key == 'RIGHT':
        keyboard.press(Key.right)

def load_example_data(direction: str, test=False) -> np.array:
    data = X_test if test else X_train
    labels = y_test if test else y_train
    sample_idx = np.argwhere(labels == int(direction == 'RIGHT')).flatten()
    return np.array([data[np.random.choice(sample_idx)]])

def predict_direction(data: np.ndarray) -> str:
    return lda.predict(data)[0]