from typing import Tuple, List
from pygame import Surface, draw, font, event, K_BACKSPACE, KEYDOWN, K_DELETE, Rect, mouse
from src.definitions import speed_of_light, WIDTH, HEIGHT, draw_arrow, arrow_scale
from src.collisions import calculate_vector
import src.camera as cam

font.init()
base_font = font.SysFont("Helvetica", 15, font.SysFont("Calibri", 15))


class Particle:
    def __init__(
        self, x: int, y: int, x_vel: float, y_vel: float, mass: float,
        color: Tuple[int, int, int], radius: float
    ) -> None:
        self.x: int = x
        self.y: int = y
        self.x_vel: float = x_vel
        self.y_vel: float = y_vel
        self.mass: float = mass
        self.color: Tuple[int, int, int] = color
        self.radius: float = radius
        self.selected: bool = False
        self.dragging: bool = False
        self.shape: draw.Rect | None = None
        self.drag_offset = (0, 0)
        self._last_drag_pos = None
        self._prev_drag_pos = None


    def move(self, screen_pos: Tuple[int, int], mouse_down: bool) -> None:
        world_x = screen_pos[0] / cam.camera_zoom + cam.camera_x_offset
        world_y = screen_pos[1] / cam.camera_zoom + cam.camera_y_offset

        VELOCITY_SCALE = 0.1

        if mouse_down:
            # Check if we're clicking on this particle
            if not self.dragging and self.point_inside_particle(world_x, world_y):
                self.dragging = True
                self.selected = True
                self.drag_offset = (self.x - world_x, self.y - world_y)
                self._prev_drag_pos = (world_x, world_y)
                self.x_vel = 0  # Reset velocity when starting to drag
                self.y_vel = 0

            # If we're dragging this particle, update its position
            if self.dragging:
                self._last_drag_pos = (self.x, self.y)
                self.x = world_x + self.drag_offset[0]
                self.y = world_y + self.drag_offset[1]
                
                if self._prev_drag_pos is not None:
                    dx = (self.x - self._prev_drag_pos[0]) * VELOCITY_SCALE
                    dy = (self.y - self._prev_drag_pos[1]) * VELOCITY_SCALE
                    self.x_vel = dx
                    self.y_vel = dy
                
                self._prev_drag_pos = (world_x, world_y)
        else:
            # Mouse released
            if self.dragging:
                self.dragging = False
                self.selected = False
                self._prev_drag_pos = None
                self._last_drag_pos = None

    def point_inside_particle(self, px: float, py: float) -> bool:
        dx = px - self.x
        dy = py - self.y
        distance_squared = dx * dx + dy * dy
        return distance_squared <= (self.radius * cam.camera_zoom)**2


    def check_delete(self, particles_list: List["Particle"] ) -> None:
        for event_instance in event.get():
            if (event_instance.type == KEYDOWN and 
                event_instance.key == K_BACKSPACE) or (event_instance.type == KEYDOWN and
                                                        event_instance.key == K_DELETE):
                if self in particles_list:
                    print(f"[I] Deleted particle at [{self.x}, {self.y}] with x velocity {str(self.x_vel)} ms-1, y velocity {str(self.y_vel)} ms-1 and mass {self.mass} kg!")
                    particles_list.remove(self)

    def update_position(self, pos: Tuple[int, int], mouse_trajectory: Tuple[float, float], particles_list: List["Particle"]) -> None:
        # Check for deletion if selected
        if self.selected:
            self.check_delete(particles_list)
            return

        self.x += self.x_vel
        self.y += self.y_vel

        # Check boundaries for x-axis
        if self.x - self.radius < 0:
            self.x = self.radius
            self.x_vel *= -1
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.x_vel *= -1

        # Check boundaries for y-axis
        if self.y - self.radius < 0:
            self.y = self.radius
            self.y_vel *= -1
        elif self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.y_vel *= -1

    def draw_attributes(self, screen: Surface) -> None:
        attributes = [
            f"XVel: {self.x_vel:.2f} ms-1",
            f"YVel: {self.y_vel:.2f} ms-1",
            f"Momentum: {self.get_current_momentum():.2f} kgms-1",
            f"Mass: {self.mass:.2f} kg",
        ]
        zoomed_x = int((self.x - cam.camera_x_offset) * cam.camera_zoom)
        zoomed_y = int((self.y - cam.camera_y_offset) * cam.camera_zoom)

        for i, attribute in enumerate(attributes):
            text = base_font.render(attribute, True, (255, 255, 255), (0, 0, 0)) # White text with black background
            text_rect = text.get_rect(center=(zoomed_x, zoomed_y - self.radius* cam.camera_zoom - 20 + i * 20))
            screen.blit(text, text_rect)
    
    def draw_arrows(self, screen:Surface) -> None:
        end_x = int(self.x + self.x_vel * arrow_scale)
        end_y = int(self.y + self.y_vel * arrow_scale)

        draw_arrow(screen, self.color, (int(self.x), int(self.y)), (end_x, end_y), arrow_size=arrow_scale, radius=self.radius)
    
    def draw(self, screen: Surface, zoomed_x: int, zoomed_y: int, zoomed_radius: int) -> None:
        self.shape = draw.circle(screen, self.color, (int(zoomed_x), int(zoomed_y)), zoomed_radius)

    def total_energy(self) -> float:
        """
        Returns the total relativistic energy of the particle.
        Formula: E = sqrt((p*c)^2 + (m*c^2)^2)
        """
        momentum: float = self.get_current_momentum()
        return ((momentum * speed_of_light**2) ** 2 + (self.mass * speed_of_light) ** 2) ** 0.5

    def get_current_momentum(self) -> float:
        return self.mass * (self.x_vel ** 2 + self.y_vel ** 2) ** 0.5

    def rest_mass_energy(self) -> float:
        return self.mass * speed_of_light ** 2

    def get_current_coords(self) -> Tuple[int, int]:
        return self.x, self.y
