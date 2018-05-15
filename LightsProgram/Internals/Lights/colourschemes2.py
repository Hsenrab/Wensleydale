class RunOn(ColorCycleTemplate):
        """Paints a the strip starting at the beginning."""
    def update(self, strip, num_led, num_steps_per_cycle, current_step, current_cycle):
        # Comment
        for i in range(num_led):
            if i < num_steps_per_cycle:
                setstrip.set_pixel(led, 255, 255, 255)
        
        return 1 # All pixels are set in the buffer, so repaint the strip now
    
    
    
class Flash(ColorCycleTemplate):
        """Paints a the strip starting at the beginning."""
    def update(self, strip, num_led, num_steps_per_cycle, current_step, current_cycle):
        
        if num_steps_in_cycle % 2 == 0:
            for i in range(num_led):
                setstrip.set_pixel(led, 255, 255, 255)
        else:
            for led in range(strip.num_led):
                strip.set_pixel(led, 0, 0, 0)
        return 1 # All pixels are set in the buffer, so repaint the strip now