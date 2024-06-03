import pyautogui
import keyboard
import cv2
import numpy as np
import time
import argparse

# Global variable to control the work state
work = False

def change():
    """Toggle the work state"""
    global work
    work = not work

def find(template_path, click_template_path='coin.bmp', threshold=0.9, interval=1):
    """
    Continuously search for a template in the screenshot and perform an action when found.
    
    Parameters:
    - template_path: Path to the template image.
    - click_template_path: Path to the image for clicking action (default is 'coin.bmp').
    - threshold: Matching threshold (default is 0.9).
    - interval: Time interval between searches (default is 1 second).
    """
    keyboard.add_hotkey('`', change)  # Assign hotkey to toggle work state
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]

    try:
        while True:
            if work:
                screenshot = pyautogui.screenshot()
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
                result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
                location = np.where(result >= threshold)
                for _ in zip(*location[::-1]):
                    click(click_template_path)
                    break
                time.sleep(interval)
    except KeyboardInterrupt:
        print('\nExit')

def click(template_path, threshold=0.8):
    """
    Perform a double-click action at the center of the matched template in the screenshot.
    
    Parameters:
    - template_path: Path to the template image.
    - threshold: Matching threshold (default is 0.8).
    """
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
    location = np.where(result >= threshold)
    for pt in zip(*location[::-1]):
        center_x = pt[0] + w // 2
        center_y = pt[1] + h // 2
        pyautogui.doubleClick(center_x, center_y)
        break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Automate template matching and clicking.')
    parser.add_argument('template_path', type=str, help='Path to the template image to find.')
    parser.add_argument('--click_template_path', type=str, default='coin.bmp', help='Path to the image for clicking action (default is "coin.bmp").')
    parser.add_argument('--interval', type=float, default=1, help='Time interval between searches in seconds (default is 1 second).')
    args = parser.parse_args()

    find(args.template_path, args.click_template_path, interval=args.interval)
