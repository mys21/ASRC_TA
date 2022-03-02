#Status

#Importation
from enum import Enum

#Class
class Status(Enum):
   """ Response status from the Aerodiode device. """
   OK = 0x00
   TIMEOUT = 0x01
   UNKNOWN_COMMAND = 0x02
   QUERY_ERROR = 0x04
   BAD_LENGTH = 0x08
   CHECKSUM_ERROR = 0x10

class StatusError(Exception):
    """
    Thrown when an Aerodiode device did not respond with 'OK' status to the last
    command.
    """
    def __init__(self, status):
        """
        :param status: Status code. int.
        """
        super().__init__()
        self.status = status

    def __str__(self):
        return str(Status(self.status))

class ChecksumError(Exception):
    """ Thrown if a communication checksum error is detected. """
    pass


class ProtocolError(Exception):
    """ Thrown if an unexpected response from the device is received. """
    pass


class ConnectionFailure(Exception):
    pass


class ProtocolVersionNotSupported(Exception):
    """
    Thrown when a PDM protocol version is not (yet) supported by the library.
    """
    def __init__(self, version):
        """
        :param version: Version string.
        """
        super().__init__()
        self.version = version

    def __str__(self):
        return self.version

