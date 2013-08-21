'''

'''
import time

from openerp.report import report_sxw
from openerp import pooler


class SaleOrderReport(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(SaleOrderReport, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({'time': time,
                                  'company_vat': self._get_company_vat})

    def _get_company_vat(self):
        res_users_obj = pooler.get_pool(self.cr.dbname).get('res.users')
        company_vat = res_users_obj.browse(self.cr, self.uid, self.uid).company_id.partner_id.vat
        return company_vat

report_sxw.report_sxw('report.osf.sales.order',
                      'sale.order',
                      'addons/osf_sales_order/report/sale_order.mako',
                      parser=SaleOrderReport)