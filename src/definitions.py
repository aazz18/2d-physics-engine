from pygame import Surface, Vector2, draw
from math import cos, sin, pi, atan2
from typing import Tuple
speed_of_light = 300000000 # speed of light in a vacuum - C
WIDTH, HEIGHT = 700, 700 # width and height of the window
MASS_RATIO = 2.5

arrow_scale = 20

is_stats_shown = False  # Toggle for stats display
is_simulator_paused = False


def draw_walls(screen, width, height):
    """Draws the boundary walls of the simulator"""
    
    color = 'white'
    thickness = 5
    draw.line(screen, color, (0, 0), (width, 0), thickness)  # Upper wall
    draw.line(screen, color, (0, height), (width, height), thickness)  # Lower wall
    draw.line(screen, color, (0, 0), (0, height), thickness)  # Left wall
    draw.line(screen, color, (width, 0), (width, height), thickness)  # Right wall


def draw_arrow(surface: Surface, color: str, start: Tuple[float, float], end: Tuple[float, float],
              arrow_size: int, radius: int, thickness=2):
    """Draws an arrow from start to end, ensuring it does not phase into a particle."""
    
    limit = radius + 1  # Adjusted limit
    start_vec = Vector2(start)
    end_vec = Vector2(end)

    # Compute the direction vector
    direction = end_vec - start_vec
    distance = direction.length()

    # Prevent division by zero and avoid drawing when the particle is selected
    if distance == 0:
        return    
    
    # Ensure the arrow stops before hitting the particle
    if distance > radius:
        new_end_vec = start_vec + direction.normalize() * (distance + radius)
    else:
        return

    # Draw the main arrow line only if it's long enough
    if distance > limit:
        draw.line(surface, color, start, (new_end_vec.x, new_end_vec.y), thickness)

    # Compute the angle of the arrow
    angle = atan2(direction.y, direction.x)

    # Position the arrowhead at `new_end_vector
    arrow_point1 = (new_end_vec.x - arrow_size * cos(angle - pi / 6),
                    new_end_vec.y - arrow_size * sin(angle - pi / 6))
    arrow_point2 = (new_end_vec.x - arrow_size * cos(angle + pi / 6),
                    new_end_vec.y - arrow_size * sin(angle + pi / 6))

    # Always draw the arrowhead
    draw.polygon(surface, color, [(new_end_vec.x, new_end_vec.y), arrow_point1, arrow_point2])
