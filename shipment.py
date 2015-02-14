# -*- coding: utf-8 -*-
"""
    shipping_dpd.py

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

__all__ = ['ShipmentOut', 'GenerateShippingLabel']
__metaclass__ = PoolMeta


STATES = {
    'readonly': Eval('state') == 'done',
}


class ShipmentOut:
    "Shipment Out"
    __name__ = 'stock.shipment.out'

    # TODO: required if carrier is DPD
    dpd_product = fields.Selection(
        DPD_PRODUCTS, 'DPD Product', states=STATES, depends=['state']
    )

    def _get_weight_uom(self):
        UOM = Pool().get('product.uom')
        if self.carrier and self.carrier.carrier_cost_method == 'dpd':
            return UOM.search([('symbol', '=', 'g')])[0]
        return super(ShipmentOut, self)._get_weight_uom()

    def get_dpd_general_shipment_data(self, shipment_service_client):
        """
        Returns a DPD shipment object
        """
        general_shipment_data = shipment_service_client.factory.create(
            'ns0:generalShipmentData'
        )

        general_shipment_data.identificationNumber = self.code
        general_shipment_data.mpsCustomerReferenceNumber1 = self.reference
        general_shipment_data.product = self.dpd_product

        # Weight should be rounded 10Gram units
        general_shipment_data.mpsWeight = int(round(self.package_weight / 10))

        general_shipment_data.sender = self.warehouse.address.to_dpd_address(
            shipment_service_client
        )
        general_shipment_data.recipient = self.delivery_address.to_dpd_address(
            shipment_service_client
        )
        return general_shipment_data


    def get_dpd_print_options(self, shipment_service_client):
        # Set the printing options
        # TODO: This should be configurable
        print_options =  shipment_service_client.factory.create(
            'ns0:printOptions')
        print_options.printerLanguage = 'PDF'
        print_options.paperFormat = 'A6'

        return shipment_service_data

    def make_dpd_labels(self):
        """
        Make labels for the shipment using DPD

        :return: Tracking number as string
        """
        # TODO: Assert that the carrier is DPD
        client = self.carrier.get_dpd_client()

        shipment_service_data = client.shipment_service_client.factory.create(
            'ns0:shipmentServiceData'
        )
        shipment_service_data.generalShipmentData = \
                self.get_dpd_general_shipment_data(
                    client.shipment_service_client
                )
        # XXX: Not sure if parcel is needed here
        # TODO: Make the label here
