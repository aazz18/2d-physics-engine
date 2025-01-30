from pygame import Surface, Vector2, draw
from math import cos, sin, pi, atan2, sqrt, asin
from typing import Tuple

speed_of_light = 300000000 # speed of light in a vacuum - C
WIDTH, HEIGHT = 700, 700
arrow_scale = 30

def draw_arrow(surface: Surface, color: str, start: Tuple[float, float], end: Tuple[float, float], 
               arrow_size: int, radius: int, thickness=2):
    """Draws an arrow from start to end, ensuring it does not phase into a particle."""

    limit = radius + 10  # The minimum distance the arrow should stop before reaching the particle

    # Compute total distance between start and end
    distance = sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
    
    # Prevent division by zero
    if distance == 0:
        return  

    # Adjust the endpoint so that the arrow stops at `limit` distance before the actual end
    if distance > limit:
        scale = (distance - limit) / distance
        new_end_x = start[0] + (end[0] - start[0]) * scale
        new_end_y = start[1] + (end[1] - start[1]) * scale
    else:
        return  # If the arrow is too short, don't draw it at all

    # Draw the main arrow shaft
    draw.line(surface, color, start, (new_end_x, new_end_y), thickness)

    # Compute the angle of the arrow
    angle = atan2(end[1] - start[1], end[0] - start[0])

    # Position the arrowhead just at `new_end_x, new_end_y` (so it does not phase into the particle)
    arrow_point1 = (new_end_x - arrow_size * cos(angle - pi / 6),
                    new_end_y - arrow_size * sin(angle - pi / 6))
    arrow_point2 = (new_end_x - arrow_size * cos(angle + pi / 6),
                    new_end_y - arrow_size * sin(angle + pi / 6))

    # Draw the arrowhead at the new endpoint
    draw.polygon(surface, color, [(new_end_x, new_end_y), arrow_point1, arrow_point2])