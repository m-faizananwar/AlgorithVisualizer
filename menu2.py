import pygame
import math
import os
import itertools

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Algorithm Visualizer")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ICON_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), 
               (0, 255, 255), (255, 0, 255), (128, 128, 128), (255, 128, 0)]

# Center coordinates
CENTER = (WIDTH // 2, HEIGHT // 2)

# Font
pygame.font.init()
heading_font = pygame.font.Font(None, 80)
font = pygame.font.Font(None, 50)

# Gradient Animation for Heading
gradient_colors = list(itertools.cycle([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]))
gradient_index = 0

# Radius and angles for the radial layout
ICON_RADIUS_START = 30
ICON_RADIUS_TARGET = 150
ICON_SIZE = 40
NUM_ICONS = 8
angles = [i * (2 * math.pi / NUM_ICONS) for i in range(NUM_ICONS)]

# State
hovering_plus = False
clicked_plus = False
animation_progress = 0  # For animating the circles
plus_thickness = 2
show_radial_icons = False

# Load Icons (replace with SVG or use dummy colored circles)
def load_icons():
    icons = []
    for color in ICON_COLORS:
        icon_surface = pygame.Surface((ICON_SIZE, ICON_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(icon_surface, color, (ICON_SIZE//2, ICON_SIZE//2), ICON_SIZE//2)
        icons.append(icon_surface)
    return icons

icons = load_icons()

# Draw animated heading
def draw_animated_heading():
    global gradient_index
    gradient_index = (gradient_index + 1) % len(gradient_colors)
    gradient_color = gradient_colors[gradient_index]
    heading_surface = heading_font.render("Algorithm Visualizer", True, gradient_color)
    heading_rect = heading_surface.get_rect(center=(WIDTH // 2, 100))
    screen.blit(heading_surface, heading_rect)

# Draw "+" sign
def draw_plus():
    global plus_thickness
    line_width = plus_thickness
    pygame.draw.line(screen, WHITE, (CENTER[0] - 10, CENTER[1]), (CENTER[0] + 10, CENTER[1]), line_width)
    pygame.draw.line(screen, WHITE, (CENTER[0], CENTER[1] - 10), (CENTER[0], CENTER[1] + 10), line_width)

# Animate radial icons
def draw_radial_icons(progress):
    for i, angle in enumerate(angles):
        # Smoothly animate radius
        radius = ICON_RADIUS_START + (ICON_RADIUS_TARGET - ICON_RADIUS_START) * progress
        x = CENTER[0] + radius * math.cos(angle)
        y = CENTER[1] + radius * math.sin(angle)
        icon_size = int(ICON_SIZE * progress)  # Icons grow smoothly
        icon = pygame.transform.scale(icons[i], (icon_size, icon_size))
        screen.blit(icon, (x - icon_size // 2, y - icon_size // 2))

# Main loop
running = True
while running:
    screen.fill(BLACK)
    
    mouse_pos = pygame.mouse.get_pos()
    hovering_plus = abs(mouse_pos[0] - CENTER[0]) < 15 and abs(mouse_pos[1] - CENTER[1]) < 15
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and hovering_plus and not clicked_plus:
            clicked_plus = True
            show_radial_icons = True
    
    # Handle animations
    if hovering_plus and not clicked_plus:
        plus_thickness = min(plus_thickness + 1, 5)  # Gradually bold the "+"
    else:
        plus_thickness = max(plus_thickness - 1, 2)  # Reset thickness
    
    if clicked_plus:
        animation_progress = min(animation_progress + 0.02, 1)  # Smooth animation progress
    else:
        animation_progress = 0
    
    # Draw elements
    draw_animated_heading()
    if show_radial_icons:
        draw_radial_icons(animation_progress)
    else:
        draw_plus()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
