from pygame import Surface, Vector2, draw
from math import cos, sin, pi, atan2
from typing import Tuple
import src.camera as cam

speed_of_light = 300000000 # speed of light in a vacuum - C
WIDTH, HEIGHT = 700, 700 # width and height of the window
MASS_RATIO = 2.5

arrow_scale = 20

is_stats_shown = False
is_simulator_paused = False

def draw_walls(screen: Surface, width: int, height: int):
    """Draws a world-space box that stays fixed relative to world coordinates"""

    color = 'white'
    thickness = max(1, int(5 * cam.camera_zoom))

    world_x0 = 0
    world_y0 = 0

    world_x1 = world_x0 + width
    world_y1 = world_y0 + height

    # Converts camera coordinates into real world coordinates
    x0 = int((world_x0 - cam.camera_x_offset) * cam.camera_zoom)
    y0 = int((world_y0 - cam.camera_y_offset) * cam.camera_zoom)
    x1 = int((world_x1 - cam.camera_x_offset) * cam.camera_zoom)
    y1 = int((world_y1 - cam.camera_y_offset) * cam.camera_zoom)

    draw.line(screen, color, (x0, y0), (x1, y0), thickness)  # Upper wall
    draw.line(screen, color, (x0, y1), (x1, y1), thickness)  # Bottom wall
    draw.line(screen, color, (x0, y0), (x0, y1), thickness)  # Left left
    draw.line(screen, color, (x1, y0), (x1, y1), thickness)  # Right wall


def draw_arrow(surface: Surface, color: str,start: Tuple[float, float],end: Tuple[float, float],arrow_size: int,radius: int,thickness=2):
    """Draws an arrow from start to end (in world space), scaled and offset correctly for camera view."""

    start_vec_world = Vector2(start)
    end_vec_world = Vector2(end)

    start_vec_screen = (start_vec_world - Vector2(cam.camera_x_offset, cam.camera_y_offset)) * cam.camera_zoom
    end_vec_screen = (end_vec_world - Vector2(cam.camera_x_offset, cam.camera_y_offset)) * cam.camera_zoom

    direction = end_vec_screen - start_vec_screen
    distance = direction.length()

    if distance == 0:
        return

    screen_radius = radius * cam.camera_zoom
    if distance > screen_radius and distance != 0:
        direction.scale_to_length(distance - screen_radius)
        adjusted_end = start_vec_screen + direction
    else:
        return

    draw.line(surface, color, start_vec_screen, adjusted_end, max(1, int(thickness)))


    angle = atan2(direction.y, direction.x)
    arrow_len = arrow_size * cam.camera_zoom

    point1 = (
        adjusted_end.x - arrow_len * cos(angle - pi / 6),
        adjusted_end.y - arrow_len * sin(angle - pi / 6),
    )
    point2 = (
        adjusted_end.x - arrow_len * cos(angle + pi / 6),
        adjusted_end.y - arrow_len * sin(angle + pi / 6),
    )

    draw.polygon(surface, color, [adjusted_end, point1, point2])



