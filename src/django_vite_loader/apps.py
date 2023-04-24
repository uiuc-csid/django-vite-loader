from json import JSONDecodeError
from json import load as load_json
from os import path
from typing import List

from django.apps import AppConfig
from django.conf import settings
from django.core.checks import Error, register

from .settings import VITE_MANIFEST_PATH


@register()
def check_config(app_configs, **kwargs):
    errors: List[Error] = []

    # TODO: Check that VITE_BUILD_OUT_DIR is in STATICFILES_DIRS?
    # TODO: Only error in dev mode? Or just check that you can reach the static files

    if not hasattr(settings, "VITE_BUILD_OUT_DIR"):
        errors.append(
            Error(
                "Error finding the vite output directory",
                hint="Set the VITE_BUILD_OUT_DIR setting",
                obj="django.conf.settings.VITE_BUILD_OUT_DIR",
                id="django_vite_loader.E001",
            )
        )

    if not path.exists(VITE_MANIFEST_PATH):
        errors.append(
            Error(
                "Vite file manifest does not exist",
                hint="Set the VITE_MANIFEST_PATH setting",
                obj="django_vite_loader.settings.VITE_MANIFEST_PATH",
                id="django_vite_loader.E002",
            )
        )
    else:
        try:
            with open(VITE_MANIFEST_PATH, "r") as manifest:
                load_json(manifest)
        except JSONDecodeError:
            errors.append(
                Error(
                    "Error parsing vite manifest",
                    hint="Ensure the file at VITE_MANIFEST_PATH is a valid json document",
                    obj="django_vite_loader.settings.VITE_MANIFEST_PATH",
                    id="django_vite_loader.E003",
                )
            )

    return errors


class DVLConfig(AppConfig):
    name = "django_vite_loader"
    default_auto_field = "django.db.models.AutoField"
    verbose_name = "Django Vite Loader"
    default = True
