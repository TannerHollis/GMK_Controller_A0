import serial
import serial.tools.list_ports as list_ports
from ConfigClasses import *

VID = 1155
PID = 22336

BAUDRATE = 38400
TIMEOUT = 2

CMD_READ_ID = 0x00
CMD_READ_CONFIG = 0x10
CMD_WRITE_CONFIG_RAM = 0x20
CMD_ERASE_FLASH = 0x30
CMD_WRITE_CONFIG_FLASH = 0x40
CMD_AUTO_CALIBRATE = 0x50
CMD_CONTROLLER_DATA = 0x60
CMD_PING = 0x70
CMD_CHANGE_CONFIG = 0x80

class SerialController(serial.Serial):
    def __init__(self):
        super().__init__()
        self.parity = "N"
        self.baudrate = BAUDRATE
        self.timeout = TIMEOUT
        self.ports = SerialController.getDevices()

    def getDevices():
        l = []
        for device in list_ports.comports():
            if device.vid == VID and device.pid == PID:
                l.append(device.usb_description())
        return l

    def connectWithPort(self, port):
        self.port = port
        try:
            self.open()
        except:
            print("Could not open device on port: {}".format(self.port))

    def ping(self):
        if self.checkConnection():
            self.write(bytes([CMD_PING]))
            if self.read(1) == b"":
                self.close()

    def getConfiguration(self, config):
        if self.checkConnection():
            self.write(bytes([CMD_READ_CONFIG | config]))
            bytesOut = self.read(CONFIGURATION_SIZE)
            return ControllerConfiguration.from_bytes(bytesOut)
        
    def checkConnection(self):
        if self.port in SerialController.getDevices():
            return True
        else:
            self.close()
            return False

if __name__ == "__main__":
    commPorts = SerialController.getDevices()
    if commPorts: 
        serialController = SerialController()
        print("Available ports:")
        for port in SerialController.getDevices():
            print(" {}".format(port))    
        port = input("PORT: ")
        serialController.connectWithPort(port)
    else:
        print("No devices available to connect to. Please check cable and try again.")
