# Import libraries
import RPi.GPIO as GPIO
from PyQt5.QtWidgets import QWidget, QGridLayout, QRadioButton, QApplication
from enum import IntEnum
import sys
import atexit

class Pin(IntEnum): # GPIO pin numbers
    RED = 15
    GREEN = 13
    BLUE = 11
    OFF = 0

class MyWidget(QWidget):
    """
    A class to represent a PyQt widget
    """
    
    def __init__(self):
        """
        Constructs a new widget
        """
    
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)
        self.initUI(layout)
        self.setWindowTitle("Toggle LEDs")

    def addRadio(self, text, pin, checked, layout):
        """
        Adds a radio button to a layout
        
        Parameters
        ----------
        text : str
            text displayed on the Radio Button
        pin : int
            GPIO pin controlled by the Radio Button
        checked : bool
            if the Radio Button is selected or not
        layout : QGridLayout
            layout to attach the Radio Button to
        """
    
        radio = QRadioButton(text)
        radio.pin = pin
        radio.setChecked(checked)
        radio.toggled.connect(self.toggleLED)
        layout.addWidget(radio)

    def toggleLED(self):
        """
        Turns an LED on or off after a Radio Button status has changed
        """
    
        radio = self.sender()
        pin = radio.pin
        if pin != Pin.OFF:
            GPIO.output(pin, radio.isChecked())

    def initUI(self, layout):
        """
        Sets up the Radio Buttons on a layout
        
        Parameters
        ----------
        layout : QGridLayout
            the layout to set up
        """
        
        self.addRadio("Red LED", Pin.RED, False, layout)
        self.addRadio("Green LED", Pin.GREEN, False, layout)
        self.addRadio("Blue LED", Pin.BLUE, False, layout)
        self.addRadio("Off", Pin.OFF, True, layout)

# Run program
if __name__ == "__main__":
    
    # Register GPIO cleanup on exit
    atexit.register(GPIO.cleanup)
    
    # Setup GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Pin.RED, GPIO.OUT)
    GPIO.setup(Pin.GREEN, GPIO.OUT)
    GPIO.setup(Pin.BLUE, GPIO.OUT)
    
    # Setup GUI
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    
    # Close program when GUI closes
    sys.exit(app.exec_())