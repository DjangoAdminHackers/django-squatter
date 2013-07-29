from django.contrib.sites.models import Site
from squatter.utils import (
    set_site,
    _sites,
)

try:
    import threading
    currentThread = threading.currentThread
except ImportError:
    def currentThread():
        return "no threading"


class TenancyMiddleware:
    def process_request(self, request):
        # Set up the Site model meta option db_table as explained here -
        # http://stackoverflow.com/questions/1160598/how-to-use-schemas-in-django
        # This will make sure that queries on this model will always go to the master schema
        domain = request.get_host()
        site = None
        if Site.objects.filter(domain=domain).exists():
            site = Site.objects.get(domain=domain)
        elif Site.objects.filter(domain=domain.replace('.www', '')).exists():
            site = Site.objects.get(domain=domain.replace('.www', ''))
        if site:
            set_site(site)
        return None

    def process_response(self, request, response):
        _sites.pop(currentThread(), None)
        return response

    def process_exception(self, request, exception):
        _sites.pop(currentThread(), None)
        return None
