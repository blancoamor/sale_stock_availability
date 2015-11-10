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


class stock_availability(osv.osv_memory):
    _name = 'stock.availability'

    def _get_virtual_available(self, cr, uid, ids, field_name, attrs,
                               context=None):
        return {}

    _columns = {
        'product_id': fields.one2many('product.template', 'Product'),
        'location_id': fields.one2many('stock.location', 'Location'),
        'virtual_available': fields.function(_get_virtual_available,
                                             'Saldo Stock'),
    }

stock_availability()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
