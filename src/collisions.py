from pygame import draw

def calculate_vector(mouse_trajectory, scaling_factor=20, min_length=10):
    """Calculates the vector for mouse movement based on trajectory."""
    if len(mouse_trajectory) < min_length:
        return 0, 0
    
    start_x, start_y = mouse_trajectory[0][0], mouse_trajectory[1][1]
    end_x, end_y = mouse_trajectory[-1][0], mouse_trajectory[-1][1]
    
    return (end_x - start_x) / scaling_factor, (end_y - start_y) / scaling_factor

def check_collision(obj1, obj2):
    """Checks and handles collision between two objects."""
    dx, dy = obj2.x - obj1.x, obj2.y - obj1.y
    distance = (dx**2 + dy**2) ** 0.5
    min_distance = obj1.radius + obj2.radius
    
    if distance >= min_distance:
        return
    
    normal = [dx / distance, dy / distance] if distance != 0 else [1, 0]
    tangent = [-normal[1], normal[0]]
    
    v1n, v1t = obj1.x_vel * normal[0] + obj1.y_vel * normal[1], obj1.x_vel * tangent[0] + obj1.y_vel * tangent[1]
    v2n, v2t = obj2.x_vel * normal[0] + obj2.y_vel * normal[1], obj2.x_vel * tangent[0] + obj2.y_vel * tangent[1]
    
    v1n_after = (v1n * (obj1.mass - obj2.mass) + 2 * obj2.mass * v2n) / (obj1.mass + obj2.mass)
    v2n_after = (v2n * (obj2.mass - obj1.mass) + 2 * obj1.mass * v1n) / (obj1.mass + obj2.mass)
    
    obj1.x_vel = v1n_after * normal[0] + v1t * tangent[0]
    obj1.y_vel = v1n_after * normal[1] + v1t * tangent[1]
    obj2.x_vel = v2n_after * normal[0] + v2t * tangent[0]
    obj2.y_vel = v2n_after * normal[1] + v2t * tangent[1]
    
    overlap = min_distance - distance
    obj1.x -= overlap * normal[0] / 2
    obj1.y -= overlap * normal[1] / 2
    obj2.x += overlap * normal[0] / 2
    obj2.y += overlap * normal[1] / 2