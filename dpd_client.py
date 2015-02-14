# -*- coding: utf-8 -*-
from suds import WebFault
from suds.client import Client


class DPDException(WebFault):
    """
    A generic exception type that can be handled by API consumers
    """
    pass


class DPDClient(object):
    """
    A DPD client API

    :param username: DPD Username (Also known as DelisId)
    :param password: DPD Password
    """

    # Caches for properties
    _login_service_client = None
    _shipment_service_client = None

    def __init__(self, login_wsdl, shipment_service_wsdl,
                 username, password,
                 message_language='en_US', lazy=True):
        self.login_wsdl = login_wsdl
        self.shipment_service_wsdl = shipment_service_wsdl

        self.username = username
        self.password = password

        self.message_language = message_language

        if not lazy:
            self.token = self.get_auth().auth_token

    @property
    def login_service_client(self):
        """
        Returns a login service client
        """
        if self._login_service_client is None:
            self._login_service_client = Client(self.login_wsdl)
        return self._login_service_client

    @property
    def shipment_service_client(self):
        """
        Returns a shipment service client
        """
        if self._shipment_service_client is None:
            self._shipment_service_client = Client(self.shipment_service_wsdl)
        return self._shipment_service_client

    def get_auth(self):
        """
        Creates an authentication token for the committed user
        if user name and password are valid.

        The authentication token is needed for accessing other
        DPD Web Services.

        Returns an object with the ``auth_code`` attribute and ``depot``
        """
        try:
            response = self.login_service_client.service.getAuth(
                self.username, self.password, self.message_language
            )
        except WebFault, exc:
            raise DPDException(exc.fault, exc.document)
        else:
            return response
