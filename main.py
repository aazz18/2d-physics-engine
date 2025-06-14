from pygame import init, display, mouse, event, QUIT, KEYDOWN, K_SPACE, time, draw, K_c, key, KMOD_CTRL, K_ESCAPE, K_s, K_m, K_a, MOUSEWHEEL, K_UP, K_DOWN, K_LEFT, K_RIGHT
from random import randint
from src.particles import Particle
from src.collisions import check_collision
from src.definitions import HEIGHT, WIDTH, MASS_RATIO, is_stats_shown, is_simulator_paused, draw_walls
from os import system, name
import src.camera as cam
from sys import stdout

init()

system('cls' if name == 'nt' else 'clear')
if name == 'nt':  
    system('title 2D Particle Physics Simulator')
else:
    stdout.write("\x1b]0;2D Particle Physics Simulator\x07")
    stdout.flush()

print("""   ___   ____                      __  _      __                __               _                   _                 __      __            
  |__ \ / __ \   ____  ____ ______/ /_(_)____/ /__       ____  / /_  __  _______(_)_________   _____(_)___ ___  __  __/ /___ _/ /_____  _____
  __/ // / / /  / __ \/ __ `/ ___/ __/ / ___/ / _ \     / __ \/ __ \/ / / / ___/ / ___/ ___/  / ___/ / __ `__ \/ / / / / __ `/ __/ __ \/ ___/
 / __// /_/ /  / /_/ / /_/ / /  / /_/ / /__/ /  __/    / /_/ / / / / /_/ (__  ) / /__(__  )  (__  ) / / / / / / /_/ / / /_/ / /_/ /_/ / /    
/____/_____/  / .___/\__,_/_/   \__/_/\___/_/\___/    / .___/_/ /_/\__, /____/_/\___/____/  /____/_/_/ /_/ /_/\__,_/_/\__,_/\__/\____/_/     
             /_/                                     /_/          /____/
      
                Written by Ethan Barnard & Andy Zeng
      """)
print("""[I] Welcome to a 2D Particle Physics simulator by Ethan Barnard & Andy Zeng""")
print("""[I] Key-binds:
    ESC / CTRL C: EXIT SIMULATOR
    SPACE: PAUSE SIMULATOR
    M: SPAWN PARTICLE INTO SIMULATOR
    S: TOGGLE STATISTICS MODE
    A: TOGGLE ARROWS
    HOLD + DEL/ HOLD + BACKSPACE: DELETE PARTICLE IF HOLDING
    HOLD: DRAG AND MOVE PARTICLE
    ARROW KEYS: PAN CAMERA
    SCROLL WHEEL / TOUCHPAD: ZOOM
""")


screen = display.set_mode((WIDTH,HEIGHT))

# Global variables
particles_list = []
clock = time.Clock()
mouse_positions = []
# Main loop flag
is_running = True
is_drawing_arrows = True


while is_running:
    if not is_simulator_paused:
        clock.tick(60)
        screen.fill((0, 0, 0))
        
        # Draw walls
        draw_walls(screen, WIDTH, HEIGHT)

        # Get mouse input
        mouse_position = mouse.get_pos()
        mouse_world_x = mouse_position[0] / cam.camera_zoom + cam.camera_x_offset
        mouse_world_y = mouse_position[1] / cam.camera_zoom + cam.camera_y_offset
        is_mouse_pressed = mouse.get_pressed()[0]
        
        if is_mouse_pressed:
            mouse_positions.append(mouse_position)
            mouse_positions = mouse_positions[-20:]  # Keep only the last 20 positions
        else:
            mouse_positions = []  # Clear positions when mouse is released

        # Update and draw particles
        for index, particle in enumerate(particles_list):
            # Needs to convert the camera coordinate into a real world coordinate
            zoomed_x = int((particle.x - cam.camera_x_offset) * cam.camera_zoom)
            zoomed_y = int((particle.y - cam.camera_y_offset) * cam.camera_zoom)
            zoomed_radius = int(particle.radius) * cam.camera_zoom
            
            particle.move(mouse_position, is_mouse_pressed)

            particle.update_position((mouse_world_x, mouse_world_y), mouse_positions, particles_list)

            particle.draw(screen, zoomed_x, zoomed_y, zoomed_radius)

            # Check collisions
            for other_index in range(index + 1, len(particles_list)):
                check_collision(particle, particles_list[other_index])

            # Draw attributes if stats mode is enabled
            if is_stats_shown:
                particle.draw_attributes(screen)
            if is_drawing_arrows:
                particle.draw_arrows(screen)

    # Event handling
    for event_instance in event.get():
        if event_instance.type == QUIT:
            is_running = False
            print("[I] Exiting simulator!")

        elif event_instance.type == KEYDOWN:
            if event_instance.key == K_m:

                mass =  randint(3, 20) # mass between 3 and 20kg
                radius = mass * MASS_RATIO
                x = randint(50, WIDTH - 50)
                y = randint(50, HEIGHT // 2)
                x_velocity = randint(-5, 5)
                y_velocity = randint(-5, 5)
                colour_rgb = (randint(100, 255), randint(100, 255), randint(100, 255))


                new_particle = Particle(
                    x=x, # x
                    y=y, # y
                    x_vel=x_velocity,  # x_velocity
                    y_vel=y_velocity, # y_velocity
                    mass=mass, # mass
                    color=colour_rgb, # colour RGB
                    radius=radius, # radius
                )

                # Particle (x, y, x_velocity, y_velocity, mass, colour, radius, friction)
                particles_list.append(new_particle)
                print(f"[I] Spawned a particle into position [{x},{y}] with x velocity {str(x_velocity)} ms-1, y velocity {str(y_velocity)} ms-1 and mass {str(mass)} kg!")

            elif event_instance.key == K_s:
                is_stats_shown = not is_stats_shown  # Toggle the stats display
                if is_stats_shown == True:
                    print(f"[I] Turned on Statistics Mode!")
                else:
                    print(f"[I] Turned off Statistics Mode!")

            elif event_instance.key == K_SPACE:
                is_simulator_paused = not is_simulator_paused
                if is_simulator_paused == True:
                    print(f"[I] Paused simulator!")
                else:
                    print(f"[I] UnPaused simulator!")

            elif event_instance.key == K_a:
                is_drawing_arrows = not is_drawing_arrows
                if is_drawing_arrows == True:
                    print(f"[I] Turned on arrows!")
                else:
                    print(f"[I] Turned off arrows!")

            # Pan camera
            elif event_instance.key == K_LEFT:
                cam.camera_x_offset -= cam.camera_pan_speed / cam.camera_zoom
            elif event_instance.key == K_RIGHT:
                cam.camera_x_offset += cam.camera_pan_speed / cam.camera_zoom
            elif event_instance.key == K_UP:
                cam.camera_y_offset -= cam.camera_pan_speed / cam.camera_zoom
            elif event_instance.key == K_DOWN:
                cam.camera_y_offset += cam.camera_pan_speed / cam.camera_zoom


                
            elif event_instance.key == K_ESCAPE:
                is_running = False    
                print("[I] Exiting simulator!")
            elif event_instance.key == K_c and key.get_mods() & KMOD_CTRL:
                is_running = False
                print("[I] Exiting simulator!")

        # Zoom control
        elif event_instance.type == MOUSEWHEEL:
            if event_instance.y > 0:
                cam.camera_zoom += cam.zoom_speed
            elif event_instance.y < 0 and cam.camera_zoom > cam.zoom_speed:
                cam.camera_zoom -= cam.zoom_speed

    # Show particle count
    if is_simulator_paused:
        display.set_caption(f'2D Particle Physics Simulator - Total particles: {len(particles_list)} - PAUSED')
    else:
        display.set_caption(f'2D Particle Physics Simulator - Total particles: {len(particles_list)}')

    display.update()

display.quit()
