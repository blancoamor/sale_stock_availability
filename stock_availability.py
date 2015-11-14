# -*- coding    : utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api, fields
import itertools as ii
from math import ceil, log


class stock_availability(models.TransientModel):
    _name = 'stock.availability'

    def read(self, cr, uid, ids, fields, context=None):
        product_pool = self.pool.get('product.product')
        warehouse_pool = self.pool.get('stock.warehouse')
        w_ids = warehouse_pool.search(cr, uid, [])

        res = []
        top = ceil(2**(log(len(w_ids) + 4, 2)))
        for i in ids:
            p_id, w_id = map(int, divmod(i, top))
            product = product_pool.browse(cr, uid, p_id)
            product = product.with_context(warehouse=w_id)
            res.append({
                'id': int(i),
                'product_id': p_id,
                'warehouse_id': w_id,
                'virtual_available': product.virtual_available,
            })
        return res

    def search(self, cr, uid, domain, context=None, offset=0,
               limit=None, order=None, count=False):
        product_pool = self.pool.get('product.product')
        warehouse_pool = self.pool.get('stock.warehouse')
        p_domain = [('id', c, r) for l, c, r in domain if l in ('product_id')]
        p_ids = product_pool.search(cr, uid, p_domain, 0, None, order,
                                    context=context)
        w_domain = [('id', c, r) for rule in domain if l in ('warehouse_id')]
        w_ids = warehouse_pool.search(cr, uid, w_domain, 0, None, order,
                                      context=context)
        top = ceil(2**(log(len(w_ids) + 4, 2)))
        return [c[0]*top + c[1] for c in ii.product(p_ids, w_ids)]

    @api.onchange('product_id', 'warehouse_id')
    def _get_virtual_available(self):
        for line in self:
            product = line.product_id.with_context(
                warehouse=line.warehouse_id.id
            )
            line.virtual_available = product.virtual_available -\
                line.product_uom_qty

    product_id = fields.Many2one('product.product', string='Product')
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    virtual_available = fields.Float(compute="_get_virtual_available",
                                     string='Saldo Stock')

stock_availability()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
