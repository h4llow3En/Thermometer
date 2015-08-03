__author__ = 'h4llow3En'

from collections import namedtuple
import RPi.GPIO as GPIO
import time
import re

cgram_address = 0x40
rs_command = False
rs_data = True

custom_char = re.compile("\\cg:[0-7]")


def e_wait():
    time.sleep(0.00005)


PinConfig = namedtuple('PinConfig', 'disp_rs disp_e data4 data5 data6 data7')
LCDConfig = namedtuple('LCDConfig', 'rows cols')


class HD44780(object):

    line = []

    def __init__(self, disp_rs=7, disp_e=8, data_lines=[25, 24, 23, 18], cols=20, rows=4, breaklines=True):

        """
        HD44780 controller.

        The pins are based on GPIO.BCM

        Args:
            disp_rs:
                Register select (RS). Default: 7.
            disp_e:
                Enable (E). Default: 8.
            data_lines:
                List of data lines pins in 4 bit mode only. Default: [25, 24, 23, 18].
            rows:
                Number of display rows. Default: 4.
            cols:
                Number of columns per row. Default 20.
            breaklines:
                Break line if end of line. Defaulf True
        Returns:
            A :class:`HD44780` instance.
        """

        #  Split data_lines into single vars an
        if len(data_lines) == 4:
            self.pins = PinConfig(disp_rs=disp_rs, disp_e=disp_e, data4=data_lines[0],
                                  data5=data_lines[1], data6=data_lines[2],
                                  data7=data_lines[3])
        else:
            raise ValueError('Only 4Bit mode supported')

        self.breaklines = breaklines

        self.config = LCDConfig(rows=rows, cols=cols)

        #  Seting up the data connections for the RPi
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        for pin in list(filter(None, self.pins)):
            GPIO.setup(pin, GPIO.OUT)

        #  Setting up
        if rows >= 1:
            self.line.append(0x80)
        if rows >= 2:
            self.line.append(0xC0)
        if rows >= 3:
            self.line.append(0x94)
        if rows == 4:
            self.line.append(0xD4)

        #  Initialize display
        time.sleep(0.0005)
        for bits in [0x33, 0x32, 0x28, 0x0C, 0x06]:
            self.command(bits)

        #  Clean display
        self.clean()

    def close(self, clean=False):
        """Clean the GPIO

        Args:
            clean:
                Clean the display before reseting GPIO. Default: False
        """
        if clean:
            self.clean()
        GPIO.cleanup()

    def clean(self):
        """Overwrite display with blank characters."""
        self.command(0x01)

    def command(self, bits):
        self._send_byte(bits, rs_command)

    def send_string(self, text, row=None, ):
        message = []
        col = self.config.cols
        row = 0 if row is None else row
        custom = custom_char.finditer(text)

        if custom is not None:
            taken = 0
            for cust_char in custom:
                for char in text[:cust_char.start() - 1 - taken]:
                    message.append(ord(char))
                message.append(ord(unichr(int(text[cust_char.end() - 1 - taken]))))
                try:
                    text = text[cust_char.end() - taken:]
                except IndexError:
                    pass
                taken = cust_char.end()

        self._select_row(row)
        if self.breaklines:
            while len(message) > col:
                self._write(message[:col])
                message = message[col:]
                if not row >= self.config.rows:
                    row += 1
                    self._select_row(row)
                else:
                    return
            self._write(message)
        else:
            length = col if len(message) > col else len(message)
            self._write(message[:length])


    def create_char(self, address, bitmap):
        """Create a new character.

        HD44780 has a cgram of 64Bytes for own characters (address 0-7).

        Args:
            address:
                The place in memory where the character is stored. Values need
                to be integers between 0 and 7.
            bitmap:
                The bitmap containing the character. This should be a tuple of
                8 numbers, each representing a 5 pixel row.
        Raises:
            AssertionError:
                Raised when an invalid location is passed in or when bitmap
                has an incorrect size.
        """
        assert address in range(8), 'Address have to be between 0 to 7.'
        assert len(bitmap) == 8, 'Bitmap must have exactly 8 rows.'

        #  Write character to CGRAM
        self.command(cgram_address | address << 3)
        for row in bitmap:
            self._send_byte(row, rs_data)

        return address

    def _select_row(self, row):
        self._send_byte(self.line[row], rs_command)

    def _write(self, charlist):
        for i in range(len(charlist)):
            self._send_byte(charlist[i], rs_data)

    def _send_byte(self, bits, mode):
        """Send the specified value to the display as rs_command or as rs_data"""
        GPIO.output(self.pins.disp_rs, mode)
        GPIO.output(self.pins.data4, False)
        GPIO.output(self.pins.data5, False)
        GPIO.output(self.pins.data6, False)
        GPIO.output(self.pins.data7, False)
        if bits & 0x10 == 0x10:
            GPIO.output(self.pins.data4, True)
        if bits & 0x20 == 0x20:
            GPIO.output(self.pins.data5, True)
        if bits & 0x40 == 0x40:
            GPIO.output(self.pins.data6, True)
        if bits & 0x80 == 0x80:
            GPIO.output(self.pins.data7, True)
        e_wait()
        GPIO.output(self.pins.disp_e, True)
        e_wait()
        GPIO.output(self.pins.disp_e, False)
        e_wait()
        GPIO.output(self.pins.data4, False)
        GPIO.output(self.pins.data5, False)
        GPIO.output(self.pins.data6, False)
        GPIO.output(self.pins.data7, False)
        if bits & 0x01 == 0x01:
            GPIO.output(self.pins.data4, True)
        if bits & 0x02 == 0x02:
            GPIO.output(self.pins.data5, True)
        if bits & 0x04 == 0x04:
            GPIO.output(self.pins.data6, True)
        if bits & 0x08 == 0x08:
            GPIO.output(self.pins.data7, True)
        e_wait()
        GPIO.output(self.pins.disp_e, True)
        e_wait()
        GPIO.output(self.pins.disp_e, False)
        e_wait()
