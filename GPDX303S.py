""" Driver for GPD-X303S powersupply for COM """

import serial

class PowerSupply:
    """
    A class used to control and communicate with the GPD-X303S power supply.

    Attributes:
    ----------
    port : str
        The serial port connected to the power supply.
    baudrate : int
        The baudrate of the serial communication (default is 9600).
    timeout : int
        The timeout for the serial communication in seconds (default is 1).
    ser : serial.Serial
        The serial object used for communication.

    Methods:
    -------
    open()
        Opens the serial port for communication.
    close()
        Closes the serial port.
    write_command(command: str)
        Writes a command to the power supply.
    read_response()
        Reads a response from the power supply.
    set_voltage(channel: int, voltage: float)
        Sets the output voltage for a specific channel.
    get_setvoltage(channel: int)
        Returns the output voltage setting for a specific channel.
    measure_voltage(channel: int)
        Returns the actual output voltage for a specific channel.
    set_current(channel: int, current: float)
        Sets the output current for a specific channel.
    get_setcurrent(channel: int)
        Returns the output current setting for a specific channel.
    measure_current(channel: int)
        Returns the actual output current for a specific channel.
    set_output(output_status: int)
        Turns on or off the output.
    set_remote_mode()
        Exits local mode and sets the instrument to remote mode.
    set_local_mode()
        Exits remote mode and sets the instrument to local mode.
    set_beep(status: int)
        Sets the beep sound from the device.
    get_idn()
        Returns the instrument identification.
    """
    def __init__(self, port: str, baudrate: int=9600, timeout:int=1):
        """
        Initializes the PowerSupply object.

        Parameters:
        ----------
        port : str
            The serial port connected to the power supply.
        baudrate : int
            The baudrate of the serial communication (default is 9600).
        timeout : int
            The timeout for the serial communication in seconds (default is 1).
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def open(self):
        """
        Open the serial port.
        """
        if self.ser is None:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)

    def close(self):
        """
        Close the serial port.
        """
        if self.ser is not None:
            self.ser.close()
            self.ser = None
        
    def write_command(self, command: str):
        """
        Write a command to the power supply.
        
        Args:
        command (str): The command string to send.
        """
        self.ser.write((command + '\n').encode())

    def read_response(self):
        """
        Read a response from the power supply.
        
        Returns:
        str: The response string from the power supply.
        """
        return self.ser.readline().decode().strip()

    def set_voltage(self, channel: int, voltage:float):
        """
        Sets the output voltage.

        Args:
        channel (int): The channel to set. 1 = CH1, 2 = CH2, 3 = CH3, 4 = CH4.
        voltage (float): The voltage value to set, in volts. Range: 0 ~ 32V.
        """
        command = f'VSET{channel}:{voltage}'
        self.write_command(command)

    def get_setvoltage(self, channel: int):
        """
        Returns the output voltage setting.
        
        Args:
        channel (int): The channel to set. 1 = CH1, 2 = CH2, 3 = CH3, 4 = CH4.
        
        Returns:
        str: The voltage setting.
        """
        command = f'VSET{channel}?'
        self.write_command(command)
        return self.read_response()
    
    def measure_voltage(self, channel: int):
        """
        Returns the actual output voltage.
        
        Args:
        channel (int): The channel to set. 1 = CH1, 2 = CH2, 3 = CH3, 4 = CH4.
        
        Returns:
        str: The measured output voltage.
        """
        command = f'VOUT{channel}?'
        self.write_command(command)
        return self.read_response()

    def set_current(self, channel: int, current: float):
        """
        Sets the output current for the selected channel.

        Args:
        channel (int): The channel to set. 1 = CH1, 2 = CH2, 3 = CH3, 4 = CH4.
        current (float): The current value to set, in ampers. Range: 0 ~ 3.2A.
        """
        command = f'ISET{channel}:{current}'
        self.write_command(command)

    def get_setcurrent(self, channel: int):
        """
        Returns the output current setting.
        
        Args:
        channel (int): The channel to set. 1 = CH1, 2 = CH2, 3 = CH3, 4 = CH4.
        
        Returns:
        str: The current setting.
        """
        command = f'ISET{channel}?'
        self.write_command(command)
        return self.read_response()

    def measure_current(self, channel: int):
        """
        Returns the actual output current.
        
        Args:
        channel (int): The channel to set. 1 = CH1, 2 = CH2, 3 = CH3, 4 = CH4.
        
        Returns:
        str: The measured output current.
        """
        command = f'IOUT{channel}?'
        self.write_command(command)
        return self.read_response()

    def set_output(self, output_status:int = 0):
        """
        Turns on or off the output. 
        
        Args:
        output_status (int): Output status. 0 = off, 1 = on.
        """
        command = f'OUT{output_status}'
        self.write_command(command)

    def set_remote_mode(self):
        """
        Exits local mode and sets the instrument to remote mode. 
        """
        command = 'REMOTE'
        self.write_command(command)

    def set_local_mode(self):
        """
        Exits remote mode and sets the instrument to local mode. 
        """
        command = 'LOCAL'
        self.write_command(command)
        
    def set_beep(self, status: int):
        """
        Set the beep sound from the device.

        Args:
            status (int): Beep status. 0 = off, 1 = on.
        """
        command = f'BEEP{status}'
        self.write_command(command)

    def get_idn(self):
        """
        Returns the instrument identification.
        
        Returns:
        str: The instrument identification from the device.
        """
        command = '*IDN?'
        self.write_command(command)
        return self.read_response()
    
if __name__ == "__main__":
    ps = PowerSupply('COM12')
    ps.open()
    ps.set_voltage(1, 5)
    ps.set_voltage(2, 30)
    ps.set_current(1, 0.5)
    ps.set_current(2, 0.5)
    ps.set_output(1)
    ps.close()