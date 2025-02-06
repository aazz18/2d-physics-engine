from pygame import init, display, mouse, event, QUIT, KEYDOWN, K_SPACE, time, draw, K_c
from random import randint
from src.particles import Particle
from src.collisions import check_collision
from src.definitions import HEIGHT, WIDTH

init()

def draw_walls(screen, width, height):
    """Draws the boundary walls of the simulator"""
    
    color = 'white'
    thickness = 5
    draw.line(screen, color, (0, 0), (width, 0), thickness)  # Upper wall
    draw.line(screen, color, (0, height), (width, height), thickness)  # Lower wall
    draw.line(screen, color, (0, 0), (0, height), thickness)  # Left wall
    draw.line(screen, color, (width, 0), (width, height), thickness)  # Right wall

screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption('2D Physics Simulator')

# Global variables
particles_list = []
clock = time.Clock()
mouse_positions = []
is_stats_shown = False  # Toggle for stats display

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
    for index, particle in enumerate(particles_list):
        particle.draw(screen)
        particle.update_position(mouse_position, mouse_positions, particles_list)  # Pass particles_list here
        particle.move(mouse_position, is_mouse_pressed)

        # Check collisions
        for other_index in range(index + 1, len(particles_list)):
            check_collision(particle, particles_list[other_index])

        # Draw attributes if stats mode is enabled
        if is_stats_shown:
            particle.draw_attributes(screen)

    # Event handling
    for event_instance in event.get():
        if event_instance.type == QUIT:
            is_running = False
        
        elif event_instance.type == KEYDOWN:
            if event_instance.key == K_SPACE:
                
                mass =  randint(1, 20)
                radius = mass * 2.5
                new_particle = Particle(
                    randint(50, WIDTH - 50),
                    randint(50, HEIGHT // 2),
                    randint(-5, 5),  # Reduced random speed range for better control
                    randint(-5, 5),
                    mass,
                    (randint(100, 255), randint(100, 255), randint(100, 255)),
                    radius,
                    0.05
                )
                particles_list.append(new_particle)

            elif event_instance.key == K_c:
                is_stats_shown = not is_stats_shown  # Toggle the stats display

    # Show particle count
    display.set_caption(f'2D Physics Simulator - Total particles: {len(particles_list)}')

    display.update()

display.quit()
