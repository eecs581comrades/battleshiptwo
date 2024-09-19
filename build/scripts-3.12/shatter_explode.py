import pygame
import random
import platform
import os
import time
import webbrowser

def get_bsod_image():
    # Detect the operating system
    system_name = platform.system()

    # Return the appropriate BSOD image path based on the OS
    if system_name == "Windows":
        return "./bsod.png"
    else:
        return "./otherbsod.png"

def play_explosion_sound():
    # Play explosion sound effect
    explosion_sound = pygame.mixer.Sound("./explosion.mp3")
    explosion_sound.play()

def shutdown_system():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    webbrowser.open(url)


def shatter_and_explode(image_path):
    pygame.init()

    # Initialize the mixer for sound
    pygame.mixer.init()

    # Get the display's resolution
    display_info = pygame.display.Info()
    screen_width, screen_height = display_info.current_w, display_info.current_h
    
    # Load the background (BSOD) image based on the OS
    bsod_image_path = get_bsod_image()
    if bsod_image_path:
        bsod_image = pygame.image.load(bsod_image_path)
        bsod_image = pygame.transform.scale(bsod_image, (screen_width, screen_height))
    
    # Load and scale the exploding image to fit the screen
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (screen_width, screen_height))
    
    # Set up the display
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

    # Play explosion sound effect at the start
    play_explosion_sound()

    # White flash effect: create a white surface the size of the screen
    flash_surface = pygame.Surface((screen_width, screen_height))
    flash_surface.fill((255, 255, 255))  # Fill the surface with white
    flash_alpha = 255  # Set the initial opacity for the white flash

    # Break the image into pieces (grid)
    piece_size = 10  # size of each piece
    pieces = []
    for y in range(0, screen_height, piece_size):
        for x in range(0, screen_width, piece_size):
            piece = image.subsurface((x, y, piece_size, piece_size))
            pieces.append([piece, pygame.Rect(x, y, piece_size, piece_size), [random.uniform(-3, 3), random.uniform(-3, 3)]])

    clock = pygame.time.Clock()
    exploded = False
    speed_factor = 0.1  # Start with a small speed factor
    flash_duration = 30  # Duration of the white flash in frames (adjust as needed)

    frame_count = 0

    while True:
        # Event handling to prevent freezing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                shutdown_system()
                return

        # Fill the screen with the background image (BSOD)
        if bsod_image_path:
            screen.blit(bsod_image, (0, 0))

        # Render the exploding image pieces
        if not exploded:
            for piece in pieces:
                # Move pieces randomly to simulate explosion, and increase the speed factor over time
                piece[1].x += piece[2][0] * speed_factor
                piece[1].y += piece[2][1] * speed_factor
                screen.blit(piece[0], piece[1])
            
            # Gradually increase the speed factor for a progressive acceleration effect
            speed_factor += 0.25  # Adjust this to control how fast the speed increases
            
            # Check if pieces have moved off screen
            exploded = all(
                piece[1].x < -piece_size or piece[1].x > screen_width + piece_size or
                piece[1].y < -piece_size or piece[1].y > screen_height + piece_size
                for piece in pieces
            )
        
        # Show the white flash on top of everything else
        if frame_count < flash_duration:
            # Show the white flash and decrease the opacity gradually
            flash_surface.set_alpha(flash_alpha)
            screen.blit(flash_surface, (0, 0))  # Draw the flash on top of the exploding image
            flash_alpha -= 8  # Decrease the opacity quickly
            if flash_alpha < 0:
                flash_alpha = 0

        pygame.display.update()
        frame_count += 1

        # Once all pieces are off screen, shut down the system
        if exploded:
            pygame.quit()
            shutdown_system()
            break  # Break the loop once shutdown is triggered

        clock.tick(60)  # Limit the frame rate to 60 FPS


if __name__ == "__main__":
    shatter_and_explode("fullscreen_screenshot.png")
