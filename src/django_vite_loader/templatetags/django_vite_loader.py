from django.template import Library
from django.utils.safestring import mark_safe

from django_vite_loader.loader import ViteLoader

register = Library()


@mark_safe
def vite_bundle(context, entry_name, script_async=False):
    tags = ViteLoader.instance().generate_vite_asset_tags(
        entry_name, script_async=script_async
    )
    return "".join(tags)


@mark_safe
def vite_hmr_bundle(context):
    return ViteLoader.instance().generate_vite_hmr_client_tag()
