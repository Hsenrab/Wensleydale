import Main.enums as enums



class WBlock:
    """ Holds information for each sub block of LEDs """
    def __init__(self, start_index, end_index, invert_direction = False):
        
        self._start_index = start_index
        self._end_index = end_index
        self._colour = enums.WColour.Blue
        self._speed = enums.WSpeed.Hare
        self._pattern = enums.WPattern.Singles
        self._invert_direction = invert_direction
        self._pattern_index = 0
        self.colour_change = False
        
    def get_start_index(self):
        return self._start_index
        
    def get_end_index(self):
        return self._end_index
        
    def set_variables(self, colour, speed, pattern):
        if self._colour is not colour:
            self._colour = colour
            self.colour_change = True
        else:
            self.colour_change = False
            
        self._speed = speed
        
        # Update and reset if the pattern changes.
        if self._pattern is not pattern:
            self._pattern = pattern
            self._pattern_index = 0
        
    def set_colour(self, colour):
        
        if self._colour is not colour:
            self._colour = colour
            self.colour_change = True
        else:
            self.colour_change = False
        
    def get_colour(self):
        return self._colour
    
    def set_speed(self, speed):
        self._speed = speed
        
    def get_speed(self):
        return self._speed
    
    def set_pattern(self, pattern):
        # Update and reset if the pattern changes.
        if self._pattern is not pattern:
            self._pattern = pattern
            self._pattern_index = 0
            
    def get_pattern(self):
        # Return pattern.
        return self._pattern
        
    def set_pattern_index(self, pattern_index):
        self._pattern_index = pattern_index
        
    def get_pattern_index(self):
        return self._pattern_index
        
    def get_direction(self):
        return self._invert_direction

    def invert_direction(self):
        self._invert_direction = True
        
    def dont_invert_direction(self):
        self._invert_direction = False
        
    def increment_pattern_index(self, increment):
        self._pattern_index += increment
