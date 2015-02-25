# -*- coding: utf-8 -*-
"""
    sale.py

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: see LICENSE for more details.
"""
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Eval, Bool, And

__all__ = ['Sale']
__metaclass__ = PoolMeta

STATES = {
    'readonly': Eval('state') == 'done',
    'required': Bool(Eval('is_dpd_shipping')),
}

DPD_PRODUCTS = [
    (None, ''),
    ('CL', 'DPD CLASSIC'),
    ('E830', 'DPD 8:30'),
    ('E10', 'DPD 10:00'),
    ('E12', 'DPD 12:00'),
    ('E18', 'DPD 18:00'),
    ('IE2', 'DPD EXPRESS'),
    ('PL', 'DPD PARCELLetter'),
    ('PL+', 'DPD PARCELLetterPlus'),
    ('MAIL', 'DPD International Mail'),
]


class Sale:
    "Sale"
    __name__ = 'sale.sale'

    is_dpd_shipping = fields.Function(
        fields.Boolean('Is Shipping', readonly=True),
        'get_is_dpd_shipping'
    )

    dpd_product = fields.Selection(
        DPD_PRODUCTS, 'DPD Product', states=STATES, depends=[
            'state', 'is_dpd_shipping'
        ]
    )
    dpd_customs_terms = fields.Selection(
        [
            (None, ''),
            ('01', 'DAP, cleared'),
            ('02', 'DDP, delivered duty paid (incl. duties and excl. Taxes'),
            (
                '03',
                'DDP, delivered duty paid (incl duties and taxes) 05 = ex '
                'works (EXW)'
            ),
            ('06', 'DAP'),
        ], 'DPD customs terms', states={
            'readonly': Eval('state') == 'done',
            'invisible': ~Eval('is_international_shipping'),
            'required': And(
                Bool(Eval('is_dpd_shipping')),
                Bool(Eval('is_international_shipping'))
            ),
        }, depends=['state', 'dpd_product']
    )

    @fields.depends('is_dpd_shipping', 'carrier')
    def on_change_carrier(self):
        """
        Show/Hide DPD Tab in view on change of carrier
        """
        res = super(Sale, self).on_change_carrier()

        res['is_dpd_shipping'] = self.carrier and \
            self.carrier.carrier_cost_method == 'dpd'

        return res

    def get_is_dpd_shipping(self, name):
        """
        Check if shipping is from DPD
        """
        return self.carrier and self.carrier.carrier_cost_method == 'dpd'
