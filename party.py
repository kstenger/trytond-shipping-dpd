# -*- encoding: utf-8 -*-
"""
    Customizes party address to have address in correct format for DPD API 

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import Pool, PoolMeta

__all__ = ['Address']
__metaclass__ = PoolMeta


class Address:
    '''
    Address
    '''
    __name__ = 'party.address'

    def to_dpd_address(self, shipment_service_client):
        """
        Converts the address to a complex type: address defined in the WSDL.
        """
        address = shipment_service_client.factory.create('ns0:address')

        address.name1 = (self.name or self.party.name)
        address.street = self.street
        address.zipCode = self.zip
        address.city = self.city
        if self.subdvision:
            address.state = self.subdivision.code[3:]
        if self.country:
            address.country = self.country.code

        address.customerNumber = address.party.code
        address.phone = address.party.phone
        address.fax = address.party.fax
        address.email = address.party.email

        return address
