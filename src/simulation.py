from drone import Drone

class simulation:
    def schedule(nb: int, drone: Drone):
        if drone.finished is False:
            if drone.waiting > 0:
                continue
        if drone.current == len(drone.path):
            drone.finished = True 
            return
