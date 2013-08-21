from openerp.osv import orm, fields
from openerp import netsvc


class SaleConditionText(orm.Model):
    """Sale order Textual information"""
    _name = "sale.condition_text"
    _description = "sale conditions"

    _columns = {
        'name': fields.char('Condition summary', required=True, size=128),
        'type': fields.selection([('header', 'Top condition'),
                                  ('footer', 'Bottom condition')],
                                 'type', required=True),
        'text': fields.html('Condition', translate=True, required=True)}


class SaleOrder(orm.Model):
    """Adds condition to SO"""

    _inherit = "sale.order"
    _description = 'Sale Order'

    _columns = {'text_condition1': fields.many2one('sale.condition_text', 'Header',
                                                   domain=[('type', '=', 'header')]),
                'text_condition2': fields.many2one('sale.condition_text', 'Footer',
                                                   domain=[('type', '=', 'footer')]),
                'note1': fields.html('Header'),
                'note2': fields.html('Footer')}

    def _set_condition(self, cursor, uid, inv_id, commentid, key):
        """Set the text of the notes in invoices"""
        if not commentid:
            return {}
        try:
            lang = self.browse(cursor, uid, inv_id)[0].partner_id.lang
        except Exception as exc:
            lang = 'en_US'
        cond = self.pool.get('sale.condition_text').browse(cursor, uid,
                                                           commentid, {'lang': lang})
        return {'value': {key: cond.text}}

    def set_header(self, cursor, uid, inv_id, commentid):
        return self._set_condition(cursor, uid, inv_id, commentid, 'note1')

    def set_footer(self, cursor, uid, inv_id, commentid):
        return self._set_condition(cursor, uid, inv_id, commentid, 'note2')

    def print_quotation(self, cursor, uid, ids, context=None):
        '''
        This function prints the sales order and mark it as sent,
        so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time'
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(uid, 'sale.order', ids[0], 'quotation_sent', cursor)
        datas = {'model': 'sale.order',
                 'ids': ids,
                 'form': self.read(cursor, uid, ids[0], context=context),
                 }
        return {'type': 'ir.actions.report.xml',
                'report_name': 'osf.sales.order',
                'datas': datas, 'nodestroy': True}


class SaleOrderLine(orm.Model):
    """ADD HTML note to sale order lines"""

    _inherit = "sale.order.line"

    _columns = {'formatted_note': fields.html('Formatted Note')}
