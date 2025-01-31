from typing import Tuple
from pygame import Surface, draw
from .definitions import speed_of_light, WIDTH, HEIGHT, draw_arrow, arrow_scale
from .collisions import calculate_vector

class Particle:
    def __init__(
        self, x: int, y: int, x_vel: float, y_vel: float, mass: float,
        color: str, radius: float, friction: float
    ) -> None:
        self.x: int = x
        self.y: int = y
        self.x_vel: float = x_vel
        self.y_vel: float = y_vel
        self.mass: float = mass
        self.color: str = color
        self.radius: float = radius
        self.friction: float = friction
        self.selected: bool = False
        self.shape: draw.Rect | None = None

    def move(self, pos: Tuple[int, int], mouse_down: bool) -> None:
        if self.shape and self.shape.collidepoint(pos) and mouse_down:
            self.selected = True
        elif not mouse_down:
            self.selected = False

    def update_position(self, pos: Tuple[int, int], mouse_trajectory: Tuple[float, float]) -> None:
        if not self.selected:
            # Check boundaries for x-axis
            if self.x - self.radius + self.x_vel < 0 or self.x + self.radius + self.x_vel > WIDTH:
                self.x_vel *= -1

            # Check boundaries for y-axis
            if self.y - self.radius + self.y_vel < 0 or self.y + self.radius + self.y_vel > HEIGHT:
                self.y_vel *= -1

            self.x += self.x_vel
            self.y += self.y_vel
        else:
            res = calculate_vector(mouse_trajectory)
            self.x_vel = res[0]
            self.y_vel = res[1]
            self.x = pos[0]
            self.y = pos[1]



    def draw(self, screen: Surface) -> None:
        self.shape = draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius)) 
        end_x = int(self.x + self.x_vel * arrow_scale)
        end_y = int(self.y + self.y_vel * arrow_scale)

        # Draw velocity vector arrow
        self.arrow = draw_arrow(screen, self.color, (int(self.x), int(self.y)), (end_x, end_y), arrow_size=arrow_scale, radius=self.radius)
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

