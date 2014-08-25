import json

from django.db.utils import load_backend


try:
    import threading
    currentThread = threading.currentThread
except ImportError:
    def currentThread():
        return "no threading"


_sites = {}
_tenants = {}


def set_site(site):
    from django.db import connections
    tenant = site.tenants.all()[0]
    alias = tenant.alias
    from settings_tenants import apply_tenant_settings
    apply_tenant_settings(alias)
    db = {
        'ENGINE': tenant.database_engine,
        'HOST': tenant.database_host,
        'NAME': tenant.database_name,
        'USER': tenant.database_user,
        'PORT': tenant.database_port,
        'PASSWORD': tenant.database_password,
        'OPTIONS': json.loads(tenant.database_options),
        'CONN_MAX_AGE': 0,
        'AUTOCOMMIT': True
    }
    backend = load_backend(db['ENGINE'])
    conn = backend.DatabaseWrapper(db, alias)
    connections[alias] = conn
    _sites[currentThread()] = site
    _tenants[currentThread()] = tenant


def get_site():
    return _sites.get(currentThread(), None)


def get_tenant():
    return _tenants.get(currentThread(), None)


def alias_from_domain(domain):
    """
    This pulls off the port, www, and .local, so if you have a website called
    www.hello.com, you can use hello.com.local:8000 in development.
    """

    alias = ':'.join(domain.split(':')[:-1])
    if alias.endswith('.local'):
        alias = alias[:-6]
    if alias.startswith('www.'):
        alias = alias[4:]
    alias.replace('.', '_')