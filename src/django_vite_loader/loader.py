import json
from typing import List, Optional, Set
from urllib.parse import urljoin

from django.contrib.staticfiles.storage import staticfiles_storage

from .settings import (
    VITE_DEV_MODE,
    VITE_DEV_SERVER_URL,
    VITE_MANIFEST_PATH,
    VITE_STATIC_URL_BASE,
    VITE_WS_CLIENT_URL,
)


class ViteLoader:
    _instance: Optional["ViteLoader"] = None

    def __init__(self) -> None:
        raise RuntimeError("Use the instance() method instead.")

    def _parse_manifest(self) -> None:
        try:
            with open(VITE_MANIFEST_PATH, "r") as manifest:
                self._manifest = json.load(manifest)
        except Exception as error:
            raise RuntimeError(
                f"Cannot read Vite manifest file at {VITE_MANIFEST_PATH} : {str(error)}"
            )

    @classmethod
    def instance(cls) -> "ViteLoader":
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance._manifest = None

            # Manifest is only used in production.
            if not VITE_DEV_MODE:
                cls._instance._parse_manifest()

        return cls._instance

    @classmethod
    def get_asset_url(cls, asset_relative_path: str) -> str:
        return staticfiles_storage.url(asset_relative_path)

    def get_css_deps_for_asset(
        self, asset_name: str, already_processed: Set[str]
    ) -> List[str]:
        manifest_entry = self._manifest[asset_name]
        dependents = []
        for entry in manifest_entry.get("imports", []):
            dependents += self.get_css_deps_for_asset(entry, already_processed)

        for entry in manifest_entry.get("css", []):
            if entry not in already_processed:
                dependents.append(entry)
                already_processed.add(entry)

        return dependents

    def _generate_vite_dev_server_url(self, path: str) -> str:
        return urljoin(
            VITE_DEV_SERVER_URL,
            urljoin(VITE_STATIC_URL_BASE, path),
        )

    def _generate_vite_style_tag(self, url: str) -> str:
        return f'<link rel="stylesheet" href="{url}" type="text/css"/>'

    def _generate_vite_script_tag(self, url: str, script_async=False, **kwargs) -> str:
        attrs = " ".join([f'{key}="{value}"' for key, value in kwargs.items()])
        if not script_async:
            return f'<script {attrs} src="{url}"></script>'
        else:
            return f'<script {attrs} src="{url}" defer></script>'

    def generate_vite_asset_tags(
        self, asset_name: str, script_async=False
    ) -> List[str]:
        if VITE_DEV_MODE:
            return [
                self._generate_vite_script_tag(
                    self._generate_vite_dev_server_url(asset_name), type="module"
                )
            ]
        else:
            scripts_attrs = {"type": "module", "crossorigin": ""}

            manifest_entry = self._manifest[asset_name]
            css_imports = self.get_css_deps_for_asset(asset_name, set())
            css_imports = [
                staticfiles_storage.url(rel_path) for rel_path in css_imports
            ]
            css_imports = [self._generate_vite_style_tag(url) for url in css_imports]
            # TODO: Split if style vs script
            script_tag = self._generate_vite_script_tag(
                staticfiles_storage.url(manifest_entry["file"]),
                script_async=script_async,
                **scripts_attrs,
            )
            return css_imports + [script_tag]

    def generate_vite_hmr_client_tag(self) -> str:
        if not VITE_DEV_MODE:
            return ""
        else:
            return self._generate_vite_script_tag(
                self._generate_vite_dev_server_url(VITE_WS_CLIENT_URL), type="module"
            )
