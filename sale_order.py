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

from openerp.osv import fields, osv

class sale_order_line_stock(osv.osv):
    _name = 'sale.order.line'
    _inherit = "sale.order.line"

    def _fnct_line_stock(self, cr, uid, ids, field_name, args, context=None):

        location_obj = self.pool.get('stock.location')
        product_obj = self.pool.get('product.product')

        if context is None:
            context = {}
        stock_available = 0
        res = {}
        quant_obj = self.pool.get('stock.quant')
        for line in self.browse(cr, uid, ids, context=context):
        # location_id = line.order_id.warehouse_id.lot_stock_id.id
            product_id = line.product_id.id
            quant_ids = quant_obj.search(cr,uid,[('product_id','=',product_id)])
            inventory = 0
            for quant in quant_obj.browse(cr,uid,quant_ids):
                inventory += quant.qty
                if inventory < 0:
                       res[line.id] = 0 - line.product_uom_qty
                else:
                    res[line.id] = inventory - line.product_uom_qty
        return res

    _columns = {
        'virtual_available': fields.function(_fnct_line_stock, string='Saldo Stock'),
    }

sale_order_line_stock()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
