django-squatter
===========================

Django multi-tenancy, without any core patches required!

Perfect for SAAS, saving memory, or other insane mad ideas.


Quickstart
----------

    pip install -e 'git+https://github.com/radiosilence/django-squatter.git'

Add these to settings:
    
    DATABASE_ROUTERS = (
        'squatter.routers.TenancyRouter',
        ...
    )

    MIDDLEWARE_CLASSES = (
        ...
        'squatter.middleware.TenancyMiddleware',
    )

    TEMPLATE_LOADERS = (
        'squatter.template.loaders.Loader',
    )

    INSTALLED_APPS = (
        ...
        'squatter',
        ...
    )

Do a migration, etc.

More Docs
=========

These are our more recent internal notes and need editing. But they are better than nothing.


Installing a new Squatter instance
-------------------------------------------
Besides the steps for ordinary projects, we need to create multiple databases for the tenants. 
As there's no way to sync db except for the main tenant, we need to manually copy the database structrue
from main tenant to other tenants. In this case: 
We created mytenant1, mytenant2 etc
And we have existing master db, copy the database into the dbs we just created.

Also we need the media dir and filebrowser dir for each tenant: 
cd /path/to/mytenant/media
mkdir mytenant
mkdir mytenant/documents



Adding a new tenant to a squatter instance
---------------------------------------------------

Say we are adding a new tenant 'mytenant'. 

1. create a mytenant directory under myproject/templates, and put the tenant specific template here. 
  in this case we have base.html for a extra style file, and home.html for different layout from ldevents 
2. put tenant static in myproject/custom_site/static/mytenant. 
  in this case we have css/mytenant.css
3. create media dir 
  create {{ project_dir }}/media/mytenant
4. add site data at /admin/sites/site/add/, and remember the site id. 
  in this case add www.mytenant.com, id is 6, 
5. add the tenant and tenant mapping data at /admin/squatter/
  tenant.alias is the most important, we need to use it in TENANT_SETTINGS of next step.
  in this case we use 'mytenant'
6. add settings to settings_tenants.TENANTS_SETTINGS. For example: 


    
        'mytenant': {
            'SITE_ID': 6,
            'PREPEND_WWW': False or True,
            'SITE_NAME': 'MyTenant',
            'SITE_DOMAIN': 'www.mytenant.com',
            'SITE_MANAGERS' : (('Someone', 'someone@example.org'),),
            'JOHNNY_MIDDLEWARE_KEY_PREFIX':'jp_mytenant',
            'JIMMY_PAGE_CACHE_PREFIX': 'jp_mytenant',        
            'MEDIA_URL': 'http://www.mytenant.com/media/',
            'STATIC_URL': 'http://www.mytenant.com/static/',
            'STATIC_ROOT': '/path/to/mysite/static',
            'MEDIA_ROOT': '/path/to/mysite/media/mytenant',
        },
        
    
Individual Tenant Settings
---------------------------------

The file is settings_tenants.py.

Simply find the entry in TENANTS_SETTINGS i.e.

    'GOOGLE_WEBMASTER_ID' : 'something',
    'GOOGLE_ANALYTICS_ID' : 'UA-101234-56',


Other notes
---------------

Different settings for each tenant?

    step 6 above, we put them in settings_tenants.py

Current issues/bugs?

    Main issue is we can not run cronjobs for the tenants etc.  
    

To-Do
-----

* Docs
* Schemas option
* Tests
* Some way of doing things like migrate/syncdb from the command line.

Inspiration
-----------

 * Neelesh Shastry - The guy who inspired the whole thing with that Posterous article: https://github.com/neeleshs
 * https://github.com/bruth
 * Andy Baker
