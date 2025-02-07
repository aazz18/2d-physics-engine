from pygame import init, display, mouse, event, QUIT, KEYDOWN, K_SPACE, time, draw, K_c, key, KMOD_CTRL, K_ESCAPE, K_s, K_m, K_a
from random import randint
from src.particles import Particle
from src.collisions import check_collision
from src.definitions import HEIGHT, WIDTH, MASS_RATIO, is_stats_shown, is_simulator_paused, draw_walls
from os import system, name




init()

system('cls' if name == 'nt' else 'clear')
system('title 2D Particle Physics Simulator')

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
""")


screen = display.set_mode((WIDTH, HEIGHT))

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
                    
            elif event_instance.key == K_ESCAPE:
                is_running = False    
                print("[I] Exiting simulator!")
            elif event_instance.key == K_c and key.get_mods() & KMOD_CTRL:
                is_running = False
                print("[I] Exiting simulator!")

    # Show particle count
    if is_simulator_paused:
        display.set_caption(f'2D Particle Physics Simulator - Total particles: {len(particles_list)} - PAUSED')
    else:
        display.set_caption(f'2D Particle Physics Simulator - Total particles: {len(particles_list)}')

    display.update()

display.quit()
