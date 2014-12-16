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

ODOO_ROOT_DIR = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR', '.'), 'odoo')
if ODOO_ROOT_DIR not in sys.path:
    sys.path.append(ODOO_ROOT_DIR)

os.environ['XDG_DATA_HOME'] = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR', '.'),'.local/share')
os.environ['XDG_CACHE_HOME'] = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR', '.'),'.cache')
os.environ['XDG_CONFIG_HOME'] = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR', '.'),'.config')


import openerp

#----------------------------------------------------------
# Common
#----------------------------------------------------------
openerp.multi_process = True # Nah!

# Equivalent of --load command-line option
openerp.conf.server_wide_modules = ['web']
conf = openerp.tools.config

# Path to the ODOO Addons repository (comma-separated for
# multiple locations)

conf['addons_path'] = ','.join([os.path.join(ODOO_ROOT_DIR,'openerp' ,'addons'),os.path.join(ODOO_ROOT_DIR, 'addons'),os.path.join(os.environ.get('OPENSHIFT_REPO_DIR', '.'), 'addons')])
#conf['addons_path'] = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR', '.'), 'addons')

# Optional database config if not using local socket
conf['db_host']     = os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']
conf['db_port']     = int(os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'])
conf['db_user']     = os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME']
conf['db_name']     = os.environ['OPENSHIFT_APP_NAME']
conf['db_password'] = os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD']

conf['logfile'] = os.path.join(os.environ.get('OPENSHIFT_LOG_DIR', '.') , 'odoo.log')

#----------------------------------------------------------
# Generic WSGI handlers application
#----------------------------------------------------------
application = openerp.service.wsgi_server.application
openerp.service.server.load_server_wide_modules()

#----------------------------------------------------------
# Gunicorn
#----------------------------------------------------------
# Standard ODOO XML-RPC port is 8069
#bind = '127.0.0.1:8069'
#pidfile = ODOO_ROOT_DIR+'.gunicorn.pid'
#workers = 4
#timeout = 240
#max_requests = 2000

#
# Below for testing only
#
#if __name__ == '__main__':
#    from wsgiref.simple_server import make_server
#    httpd = make_server('localhost', 8051, application)
#    # Wait for a single request, serve it and quit.
#    httpd.handle_request()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
