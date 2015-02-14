# -*- coding: utf-8 -*-
"""
    tests/test_client.py

    :copyright: (C) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import sys
import os
import unittest

from trytond.modules.shipping_dpd.dpd_client import DPDClient, DPDException


class TestClientAPI(unittest.TestCase):
    '''
    Test Client API
    '''

    def setUp(self):
        """
        Set up data used in the tests.
        this method is called before each test function execution.
        """
        self.server = os.environ.get(
            'DPD_SERVER', 'https://public-ws-stage.dpd.com'
        )
        self.login_service_wsdl = self.server + '/services/LoginService/V2_0?wsdl'
        self.shipment_service_wsdl = self.server + '/services/ShipmentService/V3_2?wsdl'
        self.username = os.environ['DPD_USERNAME']
        self.password = os.environ['DPD_PASSWORD']

    def test_0010_correct_auth(self):
        """
        Test if the auth works!
        """
        client = DPDClient(
            self.login_service_wsdl, self.shipment_service_wsdl,
            self.username, self.password
        )
        result = client.get_auth()
        self.assert_(result.authToken)
        self.assert_(result.depot)

    def test_0020_correct_auth(self):
        """
        Test if the wrong auth fails!
        """
        client = DPDClient(
            self.login_service_wsdl, self.shipment_service_wsdl,
            self.username, 'not' + self.password
        )
        with self.assertRaises(DPDException):
            client.get_auth()


def suite():
    """
    Define suite
    """
    test_suite = trytond.tests.test_tryton.suite()
    test_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestClientAPI)
    )
    return test_suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())

