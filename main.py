from pygame import init, display, mouse, event, QUIT, KEYDOWN, K_SPACE, time, draw
from random import randint
from src.particles import Particle
from src.collisions import check_collision
from src.definitions import HEIGHT, WIDTH
init()

def draw_walls(screen, width, height):
    """Draws the boundary walls of the simulation."""
    color = 'white'
    thickness = 5

    draw.line(screen, color, (0, 0), (width, 0), thickness)      # Upper wall
    draw.line(screen, color, (0, height), (width, height), thickness)  # Lower wall
    draw.line(screen, color, (0, 0), (0, height), thickness)     # Left wall
    draw.line(screen, color, (width, 0), (width, height), thickness)  # Right wall

screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption('2D Physics Simulator')

# Global variables
particles = []
clock = time.Clock()
mouse_positions = []

# Main loop flag
is_running = True

while is_running:
    clock.tick(60)
    screen.fill((0, 0, 0))
    
    # Draw walls
    draw_walls(screen, WIDTH, HEIGHT)

    # Get mouse input
    mouse_position = mouse.get_pos()
    is_mouse_pressed = mouse.get_pressed()[0]
    
    if is_mouse_pressed:
        mouse_positions.append(mouse_position)
        mouse_positions = mouse_positions[-20:]  # Keep only the last 20 positions

    # Update and draw particles
    for index, particle in enumerate(particles):
        particle.draw(screen)
        particle.update_position(mouse_position, mouse_positions)
        particle.move(mouse_position, is_mouse_pressed)
        for other_index in range(index + 1, len(particles)):
            check_collision(particle, particles[other_index])

    # Event handling
    for event_instance in event.get():
        if event_instance.type == QUIT:
            is_running = False
        
        if event_instance.type == KEYDOWN and event_instance.key == K_SPACE:
            new_particle = Particle(
                randint(50, WIDTH - 50),
                randint(50, HEIGHT // 2),
                randint(-5, 5),   # Reduced random speed range for better control
                randint(-5, 5),
                10,
                (randint(100, 255), randint(100, 255), randint(100, 255)),
                20,
                0.05
            ) # 
            particles.append(new_particle)

    display.update()

display.quit()

