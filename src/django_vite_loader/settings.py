from pathlib import Path

from django.conf import settings

VITE_BUILD_OUT_DIR = Path(getattr(settings, "VITE_BUILD_OUT_DIR", "dist"))
VITE_DEV_MODE = getattr(settings, "VITE_DEV_MODE", getattr(settings, "DEBUG"))

VITE_DEV_SERVER_PROTOCOL = getattr(settings, "VITE_DEV_SERVER_PROTOCOL", "http")
VITE_DEV_SERVER_HOST = getattr(settings, "VITE_DEV_SERVER_HOST", "localhost")
VITE_DEV_SERVER_PORT = getattr(settings, "VITE_DEV_SERVER_PORT", 3000)
VITE_DEV_SERVER_URL = (
    f"{VITE_DEV_SERVER_PROTOCOL}://" f"{VITE_DEV_SERVER_HOST}:{VITE_DEV_SERVER_PORT}"
)

VITE_WS_CLIENT_URL = getattr(settings, "VITE_WS_CLIENT_URL", "@vite/client")

VITE_STATIC_URL_BASE = getattr(settings, "VITE_STATIC_URL_BASE", "")

VITE_MANIFEST_NAME = getattr(settings, "VITE_MANIFEST_NAME", "manifest.json")
VITE_MANIFEST_PATH = Path(
    getattr(settings, "VITE_MANIFEST_PATH", VITE_BUILD_OUT_DIR / VITE_MANIFEST_NAME)
)
