"""
IVirtualBox binding
"""

import logging
import zeep

from .machine import IMachine
from .websession_manager import IWebsessionManager

VBOX_SOAP_BINDING = '{http://www.virtualbox.org/}vboxBinding'


class IVirtualBox(object):
    def __init__(self, location, user, password):
        self.log = logging.getLogger()

        if not location.endswith('/'):
            location = location + '/'

        self.location = location
        self.client = zeep.Client(location + '?wsdl')
        self.service = self.client.create_service(VBOX_SOAP_BINDING,
                                                  self.location)
        self.manager = IWebsessionManager(self.service, user, password)

        self.handle = self.manager.handle

    def get_session_manager(self):
        return self.manager

    def list_machines(self):
        """Lists all machines available"""
        return self.service.IVirtualBox_getMachines(self.handle)

    def get_machine(self, name):
        """Returns IMachine"""
        mid = self.find_machine(name)
        return IMachine(self.service, self.manager, mid)

    def find_machine(self, name):
        """Returns virtual machine identificator by it's name"""
        try:
            return self.service.IVirtualBox_findMachine(self.handle, name)
        except zeep.exceptions.Fault as e:
            logging.error(e)

    def open_machine(self, name):
        """Constructs :class:`IMachine <IMachine>`

        Will check if provided machine exists and return and object

        :param name: virtual machine name
        """

        # return IMachine(self.service.IVirtualBox_openMachine(self.handle, name),
        #                 self.handle)
        pass

    def get_version(self):
        """Returns string with a VirtualBox version"""
        return self.service.IVirtualBox_getVersion(self.handle)