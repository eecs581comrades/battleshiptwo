import os
import subprocess
import pygame
import random
from PIL import ImageGrab
import platform
import time
import sys

# Function to capture a screenshot of the entire screen
def capture_fullscreen_screenshot():
    screenshot = ImageGrab.grab()  # Capture the entire screen
    screenshot.save("fullscreen_screenshot.png")  # Save the screenshot

# Function to handle shattering and explosion effect
def shatter_and_explode(image_path):
    pygame.init()
    
    # Load the image and set up display
    image = pygame.image.load(image_path)
    width, height = image.get_size()
    screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
    
    # Break image into pieces (grid)
    piece_size = 30  # size of each piece
    pieces = []
    for y in range(0, height, piece_size):
        for x in range(0, width, piece_size):
            piece = image.subsurface((x, y, piece_size, piece_size))
            pieces.append([piece, pygame.Rect(x, y, piece_size, piece_size), [random.uniform(-3, 3), random.uniform(-3, 3)]])
    
    clock = pygame.time.Clock()
    exploded = False
    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        if not exploded:
            for piece in pieces:
                # Move pieces randomly to simulate explosion
                piece[1].x += piece[2][0]
                piece[1].y += piece[2][1]
                screen.blit(piece[0], piece[1])
            
            # Check if pieces have moved off screen
            exploded = all(
                piece[1].x < -piece_size or piece[1].x > width + piece_size or
                piece[1].y < -piece_size or piece[1].y > height + piece_size
                for piece in pieces
            )
        
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()

# Shake window effect based on the platform
def shake_window(duration=3):
    if platform.system() == "Windows":
        import win32gui
        import win32con
        hwnd = win32gui.GetForegroundWindow()
        end_time = time.time() + duration
        while time.time() < end_time:
            rect = win32gui.GetWindowRect(hwnd)
            x, y = rect[0], rect[1]
            new_x = x + random.randint(-10, 10)
            new_y = y + random.randint(-10, 10)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, new_x, new_y, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)
            time.sleep(0.05)

    elif platform.system() == "Darwin":
        os.system('clear')
        ascii_boom = """
        
 ____  _____  _____  __  __       
(  _ \(  _  )(  _  )(  \/  )      
 ) _ < )(_)(  )(_)(  )    (       
(____/(_____)(_____)(_/\/\_)()()()

"""
        print(ascii_boom)
        print("Why are you using a Mac. This is way more epic on Windows.")
        print("\n\nThe nuke killed all the ships. Game over. No one wins.")

        sys.exit()


    elif platform.system() == "Linux":
        from Xlib import X, display
        disp = display.Display()
        root = disp.screen().root
        window = root.query_tree().root
        geom = window.get_geometry()
        end_time = time.time() + duration
        while time.time() < end_time:
            x = geom.x + random.randint(-10, 10)
            y = geom.y + random.randint(-10, 10)
            window.configure(x=x, y=y)
            time.sleep(0.05)

# Main function that ties everything together
def main():
    # Step 1: Shake the window for 3 seconds
    shake_window(3)
    
    # Step 2: Capture full screen screenshot
    capture_fullscreen_screenshot()

    new_process = subprocess.Popen(["python", "./scripts/shatter_explode.py"])

    sys.exit()

# If the script is run directly, execute main()
if __name__ == "__main__":
    main()
