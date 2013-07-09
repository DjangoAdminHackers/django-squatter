"""
Wrapper for loading templates from "templates" directories in INSTALLED_APPS
packages.
"""

import os
import sys

from django.template import TemplateDoesNotExist
from django.template.loader import BaseLoader
from django.template.loaders.app_directories import app_template_dirs
from django.template.loaders.app_directories import Loader as BaseLoader
from django.utils._os import safe_join

from django.conf import settings

from squatter.utils import (
    get_tenant,
)


class Loader(BaseLoader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        """
        Returns the absolute paths to "template_name", when appended to each
        directory in "template_dirs". Any paths that don't lie inside one of the
        template dirs are excluded from the result set, for security reasons.
        """
        tenant = get_tenant()
        if tenant:
            alias = tenant.alias
            if not template_dirs:
                template_dirs = app_template_dirs
            for template_dir in template_dirs:
                try:
                    yield safe_join(template_dir, alias, template_name)
                except UnicodeDecodeError:
                    # The template dir name was a bytestring that wasn't valid UTF-8.
                    raise
                except ValueError:
                    # The joined path was located outside of template_dir.
                    pass

