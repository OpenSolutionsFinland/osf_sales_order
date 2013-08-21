{'name': 'Sales Order Report by Open solutions',
 'version': '1.1.1',
 'category': 'Reports/Webkit',
 'description': """
Sale order webkit
#################

* Replaces the legacy RML Quotation/Sales Order report by a brand new webkit report.
* Add header and footer notes
* Add HTML note on Sale Order lines

Depends on base_header_webkit community addon available here:
`https://launchpad.net/webkit-utils <https://launchpad.net/webkit-utils>`_
    """,
 'author': 'Open Solutions Finland Ltd',
 'website': 'http://www.opensolutions.fi',
 'depends': ['base', 'report_webkit', 'base_headers_webkit', 'sale'],
 'data': ['security/ir.model.access.csv',
          'sale_report.xml',
          'view/sale_view.xml'],
 'demo_xml': [],
 'test': [],
 'installable': True,
 'active': False,
 }
