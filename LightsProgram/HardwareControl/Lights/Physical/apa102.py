"""This is the main driver module for APA102 LEDs"""
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
from math import ceil
import Main.config as config
import numpy as np
import Internals.Utils.wlogger as wlogger

log_buffer = False


RGB_MAP = { 'rgb': [3, 2, 1], 'rbg': [3, 1, 2], 'grb': [2, 3, 1],
            'gbr': [2, 1, 3], 'brg': [1, 3, 2], 'bgr': [1, 2, 3] }

class APA102:
    """
    Driver for APA102 LEDS (aka "DotStar").

    (c) Martin Erzberger 2016-2017

    Public methods are:
     - set_pixel
     - set_pixel_rgb
     - show
     - clear_strip
     - cleanup

    Helper methods for color manipulation are:
     - combine_color
     - wheel

    The rest of the methods are used internally and should not be used by the
    user of the library.

    Very brief overview of APA102: An APA102 LED is addressed with SPI. The bits
    are shifted in one by one, starting with the least significant bit.

    An LED usually just forwards everything that is sent to its data-in to
    data-out. While doing this, it remembers its own color and keeps glowing
    with that color as long as there is power.

    An LED can be switched to not forward the data, but instead use the data
    to change it's own color. This is done by sending (at least) 32 bits of
    zeroes to data-in. The LED then accepts the next correct 32 bit LED
    frame (with color information) as its new color setting.

    After having received the 32 bit color frame, the LED changes color,
    and then resumes to just copying data-in to data-out.

    The really clever bit is this: While receiving the 32 bit LED frame,
    the LED sends zeroes on its data-out line. Because a color frame is
    32 bits, the LED sends 32 bits of zeroes to the next LED.
    As we have seen above, this means that the next LED is now ready
    to accept a color frame and update its color.

    So that's really the entire protocol:
    - Start by sending 32 bits of zeroes. This prepares LED 1 to update
      its color.
    - Send color information one by one, starting with the color for LED 1,
      then LED 2 etc.
    - Finish off by cycling the clock line a few times to get all data
      to the very last LED on the strip

    The last step is necessary, because each LED delays forwarding the data
    a bit. Imagine ten people in a row. When you yell the last color
    information, i.e. the one for person ten, to the first person in
    the line, then you are not finished yet. Person one has to turn around
    and yell it to person 2, and so on. So it takes ten additional "dummy"
    cycles until person ten knows the color. When you look closer,
    you will see that not even person 9 knows its own color yet. This
    information is still with person 2. Essentially the driver sends additional
    zeroes to LED 1 as long as it takes for the last color frame to make it
    down the line to the last LED.
    """
    # Constants
    MAX_BRIGHTNESS = config.MAX_BRIGHTNESS #Safeguard: Max. brightness that can be selected. 
    LED_START = 0b11100000 # Three "1" bits, followed by 5 brightness bits

    def __init__(self, num_led, global_brightness=MAX_BRIGHTNESS,
                 order='rgb', mosi=10, sclk=11, max_speed_hz=2000000):
        """Initializes the library.
        
        """
        self.num_led = num_led  # The number of LEDs in the Strip
        order = order.lower()
        self.rgb = RGB_MAP.get(order, RGB_MAP['rgb'])
        # Limit the brightness to the maximum if it's set higher
        if global_brightness > self.MAX_BRIGHTNESS:
            self.global_brightness = self.MAX_BRIGHTNESS
        else:
            self.global_brightness = global_brightness
            
        print(self.global_brightness)

        self.leds = np.tile([self.LED_START,0,0,0], (self.num_led + 10)) # Pixel buffer number of LEDs plus 10 buffer
        
        # MOSI 10 and SCLK 11 is hardware SPI, which needs to be set-up differently
        if mosi == 10 and sclk == 11:
        	self.spi = SPI.SpiDev(0, 0, max_speed_hz) # Bus 0, chip select 0
        else:
        	self.spi = SPI.BitBang(GPIO.get_platform_gpio(), sclk, mosi)

    def clock_start_frame(self):
        """Sends a start frame to the LED strip.

        This method clocks out a start frame, telling the receiving LED
        that it must update its own color now.
        """
        
        return [0] * 4


    def clock_end_frame(self):
        """Sends an end frame to the LED strip.

        As explained above, dummy data must be sent after the last real colour
        information so that all of the data can reach its destination down the line.
        The delay is not as bad as with the human example above.
        It is only 1/2 bit per LED. This is because the SPI clock line
        needs to be inverted.

        Say a bit is ready on the SPI data line. The sender communicates
        this by toggling the clock line. The bit is read by the LED
        and immediately forwarded to the output data line. When the clock goes
        down again on the input side, the LED will toggle the clock up
        on the output to tell the next LED that the bit is ready.

        After one LED the clock is inverted, and after two LEDs it is in sync
        again, but one cycle behind. Therefore, for every two LEDs, one bit
        of delay gets accumulated. For 300 LEDs, 150 additional bits must be fed to
        the input of LED one so that the data can reach the last LED.

        Ultimately, we need to send additional numLEDs/2 arbitrary data bits,
        in order to trigger numLEDs/2 additional clock changes. This driver
        sends zeroes, which has the benefit of getting LED one partially or
        fully ready for the next update to the strip. An optimized version
        of the driver could omit the "clockStartFrame" method if enough zeroes have
        been sent as part of "clockEndFrame".
        """
        # Reset frame:

        reset_frame = [0] *((self.num_led//4) + 4) 
        return reset_frame



    def clear_strip(self):
        """ Turns off the strip and shows the result right away."""
        self.leds = np.tile([self.LED_START,0,0,0], (self.num_led + 10))
        self.show()
        
    def clear_strip_no_refresh(self, start_index, end_index):
        """ Turns off the strip and shows the result right away."""
        if end_index - start_index == 0:
            return
            
        buffer_start_index = int(4 * start_index)
        buffer_end_index = int(4 * end_index)
        self.leds[buffer_start_index:buffer_end_index] = np.tile([self.LED_START,0,0,0], end_index - start_index)


    def set_pixel(self, led_num, red, green, blue, bright_percent=100):
        """Sets the color of one pixel in the LED stripe.

        The changed pixel is not shown yet on the Stripe, it is only
        written to the pixel buffer. Colors are passed individually.
        If brightness is not set the global brightness setting is used.
        """
        if led_num < 0:
            return  # Pixel is invisible, so ignore
        if led_num >= self.num_led:
            return  # again, invisible

        # Calculate pixel brightness as a percentage of the
        # defined global_brightness. Round up to nearest integer
        # as we expect some brightness unless set to 0
        brightness = ceil(bright_percent*self.global_brightness/100.0)
        brightness = int(brightness)
        brightness = min(self.global_brightness, brightness)
        

        # LED startframe is three "1" bits, followed by 5 brightness bits
        # LED_START = 0b11100000 
        ledstart = (brightness & 0b00011111) | self.LED_START
        
        
        start_index = int(4 * led_num)
        self.leds[start_index] = ledstart
        self.leds[start_index + self.rgb[0]] = int(red)
        self.leds[start_index + self.rgb[1]] = int(green)
        self.leds[start_index + self.rgb[2]] = int(blue)


    def set_pixel_rgb(self, led_num, rgb_color, bright_percent=100):
        """Sets the color of one pixel in the LED stripe.

        The changed pixel is not shown yet on the Stripe, it is only
        written to the pixel buffer.
        Colors are passed combined (3 bytes concatenated)
        If brightness is not set the global brightness setting is used.
        """
       
        
        
        self.set_pixel(led_num, (rgb_color & 0xFF0000) >> 16,
                       (rgb_color & 0x00FF00) >> 8, rgb_color & 0x0000FF,
                        bright_percent)
                        
    def get_pixel(self, led_num):
        """Gets the color of one pixel in the LED stripe.
        """
        

        start_index = int(4 * led_num)

        return self.leds[start_index + self.rgb[0]], self.leds[start_index + self.rgb[1]], self.leds[start_index + self.rgb[2]]
                
                
    def is_led_on(self, led_num):
    
        if led_num < 0:
            return  False # Pixel is invisible, so ignore
        if led_num >= self.num_led:
            return  False # again, invisible
            
        current_colour = self.get_pixel(led_num)
        #print(current_colour)
        
        if current_colour[0] != 0 or current_colour[1] != 0 or current_colour[2] != 0:
            return True
        else:
            return False


    def rotate(self, positions=1):
        """ Rotate the LEDs by the specified number of positions.

        Treating the internal LED array as a circular buffer, rotate it by
        the specified number of positions. The number could be negative,
        which means rotating in the opposite direction.
        """
        cutoff = 4 * (positions % self.num_led)
        self.leds = np.concatenate((self.leds[cutoff:], self.leds[:cutoff]))


    def show(self):
        """Sends the content of the pixel buffer to the strip.

        Todo: More than 1024 LEDs requires more than one xfer operation.
        Done by mikey- needs testing
        """
                  
        start_frame = self.clock_start_frame()
        end_frame = self.clock_end_frame()
        
        led_buffer = np.concatenate((start_frame, self.leds, end_frame))

        packetnum = len(list(led_buffer))
        transfersize = 4096
        transfernum = int(packetnum/transfersize)

        for x in range(0,transfernum):
            
            out_array = led_buffer[x*transfersize:(x+1)*transfersize]
            outArrayAsList = out_array.tolist()
            
            if log_buffer:
                wlogger.log_info(outArrayAsList)

            self.spi.write(outArrayAsList)

        out_array = led_buffer[(transfernum*transfersize):packetnum]
        outArrayAsList = out_array.tolist()
        
        if log_buffer:
            wlogger.log_info(outArrayAsList)
        self.spi.write(outArrayAsList)
        

    def cleanup(self):
        """Release the SPI device; Call this method at the end"""

        self.spi.close()  # Close SPI port

    @staticmethod
    def combine_color(red, green, blue):
        """Make one 3*8 byte color value."""

        return (red << 16) + (green << 8) + blue

    @staticmethod
    def wheel(wheel_pos):
        """Get a color from a color wheel; Green -> Red -> Blue -> Green"""

        if wheel_pos > 255:
            wheel_pos = 255 # Safeguard
        if wheel_pos < 85:  # Green -> Red
            return APA102.combine_color(wheel_pos * 3, 255 - wheel_pos * 3, 0)
        if wheel_pos < 170:  # Red -> Blue
            wheel_pos -= 85
            return APA102.combine_color(255 - wheel_pos * 3, 0, wheel_pos * 3)
        # Blue -> Green
        wheel_pos -= 170
        return APA102.combine_color(0, wheel_pos * 3, 255 - wheel_pos * 3)


    def dump_array(self):
        """For debug purposes: Dump the LED array onto the console."""

        print(self.leds)


x = APA102(3)

print(x)
