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


class sale_order_line_stock(models.Model):
    _inherit = "sale.order.line"

    @api.depends('product_id', 'product_uom_qty', 'order_id.warehouse_id')
    def _get_virtual_available(self):
        for line in self:
            product = line.product_id.with_context(
                warehouse=line.order_id.warehouse_id.id
            )
            line.virtual_available = product.virtual_available -\
                line.product_uom_qty

    @api.multi
    def view_availability(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "stock.availability",
            "views": [[False, "tree"]],
            "domain": [["product_id", "=", self.product_id.id]]
        }

    virtual_available = fields.Float(compute="_get_virtual_available",
                                     string="Saldo Stock")

sale_order_line_stock()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
