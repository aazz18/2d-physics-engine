from typing import List
from .defintions import speed_of_light

class Particle():

    def __init__(self, cords: tuple , mass: int, charge: float, spin: float, momentum: float) -> None:
        self.cords = cords
        self.mass = mass
        self.charge = charge
        self.spin = spin
        self.momentum = momentum

    def get_total_energy(self) -> float:

        """
        This function returns and fetches the total relativistic energy of a subatomic particle.
        Formula: E^2 = (pc)^2 + (mc^2)^2
        Thus, E = sqrt((pc)^2 + (mc^2)^2)

        E is the relativistic energy of the particle
        p is momentum of the particle 
        m is the mass of the particle
        
        Source: https://courses.lumenlearning.com/suny-physics/chapter/28-6-relativistic-energy/
        """

        total_energy  = ((self.momentum * speed_of_light**2 )**2+(self.mass*speed_of_light)**2)**0.5
        
        return total_energy 
    

 
    def rest_mass_energy(self):
                
        pass

    def get_current_cords(self) -> tuple:
        return self.cords
    




    
