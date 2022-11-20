import random
import copy
import json
from uuid import uuid4
from functools import cmp_to_key
from itertools import filterfalse
from numpy import sqrt
import cProfile
# import pandas as pd

# constants
BEST_GROWTH_RATE = 1
BEST_SPREAD_RATE = 0.5
BEST_DEATH_RATE = 0
LIVE_GROWTH_RATE = 0.8
LIVE_SPREAD_RATE = 0
LIVE_DEATH_RATE = 0.3
DEATH_RATE = 0.8

# colors
PREFIX = "\033["
RESET = f"{PREFIX}0m"
BLACK = f"{PREFIX}30m"
RED = f"{PREFIX}31m"        
GREEN = f"{PREFIX}32m"      
YELLOW = f"{PREFIX}33m"
BLUE = f"{PREFIX}34m"
MAGENTA = f"{PREFIX}35m"
CYAN = f"{PREFIX}36m"
WHITE = f"{PREFIX}37m"


# Grid display elements
HORIZONTAL_WALL = f"{WHITE}-"
VERTICAL_WALL = f"{WHITE}|"
CORNER = f"{WHITE}+"
EMPTY = f"{WHITE} "
CELL_SIZE = 3

class Plant(object):

    def __init__(
        self, 
        name: str, 
        plant_id: str, 
        best_lv: tuple, 
        live_lv: tuple, 
        max_stage: int, 
        mature_stage: int, 
        multi_season: bool,
        color):
        self.name = name
        self.plant_id = plant_id
        self.best_lv = best_lv
        self.live_lv = live_lv
        self.max_stage = max_stage
        self.mature_stage = mature_stage
        self.current_stage = 0
        self.multi_season = multi_season
        self.color = color
        # self.dead = False

    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.plant_id

    def get_best_lv(self):
        return self.best_lv

    def get_live_lv(self):
        return self.live_lv

    def get_max_stage(self):
        return self.max_stage

    def get_mature_stage(self):
        return self.mature_stage

    def get_current_stage(self):
        return self.current_stage

    def get_multi_season(self):
        return self.multi_season

    def get_growth_rate(self, env_lv):
        """  
        Args:
            env_lv (int): lv of the environment
        
        Returns:
            growth rate
        """
        if self.best_lv[0] <= env_lv <= self.best_lv[1]:
            return BEST_GROWTH_RATE
        if self.best_lv[0] <= env_lv <= self.best_lv[1]:
            return LIVE_GROWTH_RATE
        return 0

    def get_spread_rate(self, env_lv):
        """  
        Args:
            env_lv (int): lv of the environment
        
        Returns:
            spread rate
        """
        if self.best_lv[0] <= env_lv <= self.best_lv[1]:
            return BEST_SPREAD_RATE
        if self.best_lv[0] <= env_lv <= self.best_lv[1]:
            return LIVE_SPREAD_RATE
        return 0

    def get_death_rate(self, env_lv):
        """  
        Args:
            env_lv (int): lv of the environment
        
        Returns:
            growth rate
        """
        if self.best_lv[0] <= env_lv <= self.best_lv[1]:
            return BEST_DEATH_RATE
        if self.best_lv[0] <= env_lv <= self.best_lv[1]:
            return LIVE_DEATH_RATE
        return DEATH_RATE

    # def get_dead(self):
    #     return self.dead

    def grow(self, env_lv):
        """
        advance to next stage if suitable 

        Args:
            env_lv (int): lv of the environment
        """
        if random.uniform(0, 1) < self.get_growth_rate(env_lv):
            self.current_stage += 1

    def spread(self, env_lv):
        """
        decide to spread to neighbor (consider competition later?)
        might spread if mature 
        
        Args:
            env_lv (int): lv of the environment
        
        Returns:
            [bool]: spread or not
        """
        # if self.current_stage >= self.mature_stage:
        #     return random.uniform(0, 1) < self.get_growth_rate(env_lv)
        return random.uniform(0, 1) < self.get_growth_rate(env_lv)\
            and self.current_stage >= self.mature_stage

    def end(self, env_lv, num_plants):
        """
        decide to die or not
        due to old age (not multi season) or unsuitable env_lv
        
        Args:
            env_lv (int): lv of the environment
            num_plants (int): number of plants on the same grid

        Returns:
            [bool]: end or not
        """
        return random.uniform(0, 1)/sqrt(num_plants) < self.get_death_rate(env_lv)\
            or (self.current_stage > self.max_stage and not self.multi_season)

    def clone(self):
        """
        create a plant with identical features except new uuid
        
        Returns:
            Plant: a plant with identical features except new uuid
        """
        return Plant(
            self.name,
            uuid4(),
            self.best_lv,
            self.live_lv,
            self.max_stage,
            self.mature_stage,
            self.multi_season,
            self.color
            )

    def __str__(self):
        # colored first char of plant name
        return self.color + self.name[0]

    def __eq__(self, other):
        if (other is None):
            return False
        return self.plant_id == other.plant_id


class Tile(object):

    def __init__(self, lv, coord: int, plants=None):
        if plants is None:
            plants = []
        self.lv = lv
        self.coord = coord
        self.plants = plants

    def get_lv(self):
        return self.lv

    def set_lv(self, lv):
        self.lv = lv

    def get_coord(self):
        return self.coord

    def get_num_plants(self):
        return len(self.plants)

    def get_plants(self):
        return self.plants

    def add_plant(self, plant):
        self.plants.append(plant)

    def remove_dead_plants(self):
        """
        iterate over the plants on the grid
        and remove those who are dead
        """
        # plants = copy.deepcopy(self.plants)
        # for p in plants:
        #     if p.end(self.lv, self.get_num_plants()):
        #         self.plants.remove(p)
                
        # self.plants[:] = filterfalse(determine, self.plants)
        
        # remove copy to save time
        self.plants[:] = [p for p in self.plants if not p.end(self.lv, self.get_num_plants())]

    def get_most_mature_plant(self):
        try:
            return sorted(self.plants, key=cmp_to_key(compare), reverse=True)[0]
        except IndexError as e:
            pass

    def grow(self):
        for p in self.plants:
            p.grow(self.lv)

    def __str__(self):
        if self.get_most_mature_plant() is None:
            return EMPTY
        return str(self.get_most_mature_plant())


class Grid(object):

    def __init__(self, file_name):
        # file = pd.read_json(file_name)
        with open(file_name) as file:
            data = json.load(file)
            self.step = 0
            self.dim_x = int(data["dim_x"])
            self.dim_y = int(data["dim_y"])

            p1 = data["plant1"]
            p2 = data["plant2"]

            # plant randomly initially
            self.tiles = []
            for i in range(len(data["grid"])):
                t = Tile(data["grid"][i], i)
                # 20% covered by plant1
                if random.uniform(0, 1) < 0.2:
                    t.add_plant(
                        Plant(p1["name"], 
                            uuid4(), 
                            tuple((p1["best_low"], p1["best_high"])), 
                            tuple((p1["live_low"], p1["live_high"])),
                            p1["max_stage"],
                            p1["mature_stage"],
                            p1["multi_season"],
                            WHITE))
                # 20% covered by plant2
                elif random.uniform(0, 1) < 0.4:
                    t.add_plant(
                        Plant(p2["name"], 
                            uuid4(), 
                            tuple((p2["best_low"], p2["best_high"])), 
                            tuple((p2["live_low"], p2["live_high"])),
                            p2["max_stage"],
                            p2["mature_stage"],
                            p2["multi_season"],
                            CYAN))
                self.tiles.append(t)

    def render(self):


        grid_repr = f"current step: {self.step}\n"
        # horizontal coord
        for i in range(self.dim_x):
            grid_repr += f"{VERTICAL_WALL} {i+1} "
        grid_repr += VERTICAL_WALL
        horizontal_border = (CORNER + HORIZONTAL_WALL * CELL_SIZE) * self.dim_x\
                            + CORNER + "\n"
        grid_repr += f"\n{horizontal_border}"

        for row in range(self.dim_y):
            grid_repr += VERTICAL_WALL
            for col in range(self.dim_x):
                index = col + row * self.dim_x
                grid_repr += f" {str(self.tiles[index])} {VERTICAL_WALL}"
            grid_repr += f" {row+1}\n{horizontal_border}"
        print(grid_repr)


    def next_step(self):
        self.step += 1
        for tile in self.tiles:
            # grow
            tile.grow()
            
            # find nbhd that's inbound
            coord = tile.get_coord()
            nbhd = []
            if coord - self.dim_x >= 0:
                nbhd.append(coord-self.dim_x)
            if coord + self.dim_x < self.dim_x*self.dim_y:
                nbhd.append(coord+self.dim_x)
            if coord%self.dim_x != 0:
                nbhd.append(coord-1)
            if coord%self.dim_x != self.dim_x-1:
                nbhd.append(coord+1)
            # spread
            for p in tile.get_plants():
                for c in nbhd:
                    if p.spread(tile.get_lv()):
                        self.tiles[c].add_plant(p.clone())
            
            # end
            tile.remove_dead_plants()

def compare(p1, p2):
    """
    Comparing two plants by their maturity then if multiseason

    more mature > less mature
    multi season > single season
    
    Args:
        p1 (Plant): [description]
        p2 (Plant): [description]
    
    Returns:
        number: 
        -1: p1 < p2
        1: p1 > p2
        0: p1 = p2
    """
    p1_maturity = p1.get_current_stage()/p1.get_max_stage()
    p2_maturity = p2.get_current_stage()/p2.get_max_stage()
    if p1_maturity < p2_maturity:
        return -1
    elif p1_maturity > p2_maturity:
        return 1
    else:
        if not p1.get_multi_season() and p2.get_multi_season():
            return -1
        if p1.get_multi_season() and not p2.get_multi_season():
            return 1
        return 0

def main():
    grid = Grid(input("map:"))
    grid.render()
    N = 20

    for i in range(N):
        grid.next_step()
        grid.render()

if __name__ == '__main__':
    cProfile.run('main()')





