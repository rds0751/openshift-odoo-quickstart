#!/usr/bin/python
import os

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass
#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#


import sys

ODOO_ROOT_DIR = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR', '.'), 'odoo')
if ODOO_ROOT_DIR not in sys.path:
    sys.path.append(ODOO_ROOT_DIR)

import openerp

#----------------------------------------------------------
# Common
#----------------------------------------------------------
odoo.multi_process = True # Nah!

# Equivalent of --load command-line option
odoo.conf.server_wide_modules = ['web']
conf = odoo.tools.config

# Path to the ODOO Addons repository (comma-separated for
# multiple locations)

conf['addons_path'] = os.path.join(ODOO_ROOT_DIR, 'openerp/addons')

# Optional database config if not using local socket
conf['db_host']     = os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']
conf['db_port']     = int(os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'])
conf['db_user']     = os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME']
conf['db_name']     = os.environ['OPENSHIFT_APP_NAME']
conf['db_password'] = os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD']

#----------------------------------------------------------
# Generic WSGI handlers application
#----------------------------------------------------------
application = openerp.service.wsgi_server.application

#----------------------------------------------------------
# Gunicorn
#----------------------------------------------------------
# Standard ODOO XML-RPC port is 8069
#bind = '127.0.0.1:8069'
#pidfile = '.gunicorn.pid'
#workers = 4
#timeout = 240
#max_requests = 2000

#
# Below for testing only
#
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
    # Wait for a single request, serve it and quit.
    httpd.handle_request()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
