from pynput.keyboard import Key, Controller

keyboard = Controller()

def trigger_key(key: str):
    """Triggers a left or right arrow keyboard press.

    Args:
        key (str): Key to press. Input not in {'left', 'right'} is ignored.
    """
    if key.lower() == 'left':
        keyboard.press(Key.left)
    elif key.lower() == 'right':
        keyboard.press(Key.right)
