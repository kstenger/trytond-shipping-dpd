# -*- coding: utf-8 -*-
"""
    carrier

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.transaction import Transaction
from trytond.pool import PoolMeta, Pool
from trytond.model import fields

__all__ = ['Carrier']
__metaclass__ = PoolMeta


class Carrier:
    "Carrier"
    __name__ = 'carrier'

    # TODO: All should be required if carrier_cost_method is DPD
    dpd_url = fields.Char('Base URL', help="Ex. https://public-ws-stage.dpd.com")
    dpd_login_service_wsdl = fields.Char('Login Service URL')
    dpd_shipment_service_wsdl = fields.Char('Shipment Service URL')
    dpd_username = fields.Char('Username/DelisID')
    dpd_password = fields.Char('Password')

    @classmethod
    def __setup__(cls):
        super(Carrier, cls).__setup__()
        selection = ('dpd', 'DPD')
        if selection not in cls.carrier_cost_method.selection:
            cls.carrier_cost_method.selection.append(selection)

    @fields.depends('carrier_cost_method', 'dpd_url')
    def on_change_dpd_url(self):
        """
        Set the login_service and shipment_service URL on change of dpd_url
        """
        if self.carrier_cost_method != 'dpd':
            return {}
        if not self.dpd_url:
            return {}
        return {
            'dpd_login_service_wsdl': (
                self.dpd_url + '/services/LoginService/V2_0?wsdl'),
            'dpd_shipment_service_wsdl': (
                self.dpd_url + '/services/ShipmentService/V3_2?wsdl'),
        }

    def get_dpd_client(self):
        """
        Return the DPD client with the username and password set
        """
        return DPDClient(
            self.dpd_login_service_wsdl,
            self.dpd_shipment_service_wsdl,
            self.dpd_username,
            self.dpd_password,
            message_language=Transaction().context.get('language', 'en_US')
        )

    # TODO: Add this button to the view
    def test_dpd_credentials(self):
        """
        Tests the connection. If there is a WebFault, raises an UserError
        """
        client = self.get_dpd_client()
        try:
            client.get_auth()
        except WebFault, exc:
            self.raise_user_error(exc.fault)
