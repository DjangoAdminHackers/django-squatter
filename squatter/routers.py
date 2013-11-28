from squatter.utils import (
    get_tenant,
)


class TenancyRouter(object):
    def _name(self, model, **hints):
        tenant = get_tenant()
        if tenant is None:
            alias = 'default'
        else:
            alias = tenant.alias
        return alias
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label in ['squatter', 'sites', 'robots']:
            return 'default'
        return self._name(model, **hints)

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label in ['squatter', 'sites']:
            return 'default'
        return self._name(model, **hints)
