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



import logging
_logger = logging.getLogger(__name__)

class sale_order(models.Model):
    _inherit = "sale.order"

    def stock_availability_onchange_sale_warehouse_id(self, cr, uid, ids, warehouse_id, order_lines,context=None):
       # res = super(sale_order, self).onchange_warehouse_id( cr, uid, ids, warehouse_id, context=context) 
        res={}
        if not order_lines or order_lines == [(6, 0, [])]:
            return res

        lines=[]
        order_line_obj = self.pool.get('sale.order.line')

        for order_line in order_lines:
            #si esta grabada la linea
            if order_line[0]==6 :
                for line in order_line_obj.browse(cr, uid,order_line[2]):
                    product = line.product_id.with_context(
                        warehouse=warehouse_id
                    )
                    #state=line['state'] | u'draft'
                    lines.append((1,line.id,{'virtual_available':product.virtual_available}))                    

            #si la linea es nueva y no esta creada e la DB
            if order_line[0]==0 :
                line=order_line[2]
                product=self.pool.get('product.product').browse(cr, uid, line['product_id'], context={'warehouse': warehouse_id})
                order_line[2]['virtual_available']=product.virtual_available
                order_line[2]['state']=u'draft'

                lines.append( order_line)                    


        _logger.info("lines %r" , lines)

        value={}
        value['order_line']=lines   
        return { 'value': value}

        return res


class sale_order_line(models.Model):
    _inherit = "sale.order.line"

    def _get_virtual_available(self):
        for line in self:
            product = line.product_id.with_context(
                warehouse=line.order_id.warehouse_id.id
            )
            line.virtual_available = product.virtual_available

    @api.multi
    def view_availability(self):
        
        return {
            "type": "ir.actions.act_window",
            "res_model": "stock.availability",
            "views": [[False, "tree"]],
            "target": "new", 
            "domain": [["product_id", "=", self.product_id.id]]
        }

    virtual_available = fields.Float(compute="_get_virtual_available",
                                     string="Stock")


    def product_id_change_with_wh(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, warehouse_id=False, context=None):

        if not product:
            return {'value': {'th_weight' : 0, 'product_packaging': False,
                'product_uos_qty': qty}, 'domain': {'product_uom': [],
                   'product_uos': []}}
        product_obj = self.pool.get('product.product')
        product_info = product_obj.browse(cr, uid, product).with_context(
            warehouse=warehouse_id
        )

        result =  super(sale_order_line, self).product_id_change_with_wh( cr, uid, ids, pricelist, product, qty,
            uom, qty_uos, uos, name, partner_id,
            lang, update_tax, date_order, packaging, fiscal_position, flag, warehouse_id=warehouse_id, context=context)

        result['value'].update({'virtual_available': product_info['virtual_available']})

        #self.pool.get('sale.order').message_post(cr, uid, ids, body="Task Created", subtype='mail.mt_comment', context=context)

        return result


sale_order_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
