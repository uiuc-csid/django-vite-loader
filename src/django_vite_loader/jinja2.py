from jinja2.ext import Extension
from jinja2.runtime import Context
from jinja2.utils import pass_context

from django_vite_loader.templatetags.vite_loader import vite_bundle, vite_hmr_bundle


@pass_context
def _vite_bundle(context: Context, *args, **kwargs):
    return vite_bundle(context, *args, **kwargs)


@pass_context
def _vite_hmr_bundle(context: Context, *args, **kwargs):
    return vite_hmr_bundle(context, *args, **kwargs)


class ViteExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.globals["vite_bundle"] = _vite_bundle
        environment.globals["vite_hmr"] = _vite_hmr_bundle
