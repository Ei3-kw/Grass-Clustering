import random
import uuid
import copy

# constants
BEST_GROWTH_RATE = 1
BEST_SPREAD_RATE = 0.5
BEST_DEATH_RATE = 0
LIVE_GROWTH_RATE = 0.8
LIVE_SPREAD_RATE = 0
LIVE_DEATH_RATE = 0.3
DEATH_RATE = 0.8

class Plant(object):

    def __init__(
        self, 
        name: str, 
        plant_id: str, 
        best_lv: tuple, 
        live_lv: tuple, 
        max_stage: int, 
        mature_stage: int, 
        multi_season: bool):
        self.name = name
        self.plant_id = plant_id
        self.best_lv = best_lv
        self.live_lv = live_lv
        self.max_stage = max_stage
        self.mature_stage = mature_stage
        self.current_stage = 0
        self.multi_season = multi_season
        self.dead = False

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

    def get_dead(self):
        return self.dead

    def grow(self, env_lv):
        """
        advance to next stage if suitable 

        Args:
            env_lv (int): lv of the environment
        """
        if random.uniform(0, 1) < self.get_growth_rate(self, env_lv):
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
        return random.uniform(0, 1) < self.get_growth_rate(self, env_lv)\
            and self.current_stage >= self.mature_stage

    def end(self, env_lv, num_plants):
        """
        decide to die or not
        due to old age (not multi season) or unsuitable env_lv
        
        Args:
            env_lv (int): lv of the environment
            num_plants (int): number of plants on the same grid
        """
        self.dead = random.uniform(0, 1)/num_plants < self.get_death_rate(self, env_lv)\
            or (self.current_stage > self.max_stage and not self.multi_season)

    def __str__(self):
        return self.name[0]


class Tile(object):

    def __init__(self, lv, coord: tuple, plants=[]):
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

    def add_plants(self, plant):
        self.plants.append(plant)

    def remove_dead_plants(self):
        plants = copy.deepcopy(self.plants)
        for p in plants:
            if p.get_dead():
                self.plants.remove(p)

    def compare(self, p1, p2):
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

    def get_most_mature_plant(self):
        try:
            return self.plants.sort(key=self.compare, reverse=True)[0]
        except IndexError as e:
            pass


class Grid(object):

    def __init__(self, file_name):
        self.file_name = file_name

        

        
        

