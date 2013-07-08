from django.contrib.sites.models import Site
from django.db import models


DATABASE_ENGINE_CHOICES = (
    ('django.db.backends.postgresql_psycopg2', 'PostgreSQL'),
    ('django.db.backends.mysql', 'MySQL'),
    ('django.db.backends.sqlite3', 'SQLite'),
)


class TenantMapping(models.Model):
    site = models.ForeignKey(Site, unique=True)
    tenant = models.ForeignKey('Tenant')


class Tenant(models.Model):
    sites = models.ManyToManyField(Site, related_name='tenants',
        through=TenantMapping)
    database_engine=models.CharField(max_length=255,
        choices=DATABASE_ENGINE_CHOICES, default=DATABASE_ENGINE_CHOICES[0][0])
    alias = models.CharField(max_length=255)
    database_name=models.CharField(max_length=128)
    database_host=models.CharField(max_length=128, blank=True)
    database_port=models.CharField(max_length=128, blank=True)
    database_user=models.CharField(max_length=128)
    database_password=models.CharField(max_length=128)
    database_options=models.TextField(default='{}')

    def __unicode__(self):
        return u'{} ({}) {}'.format(self.database_name, self.alias,
            self.database_host)

    class Meta:
        verbose_name=u'Tenant'
        verbose_name_plural=u'Tenants'
