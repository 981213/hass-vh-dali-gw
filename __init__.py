"""The VUNHO Dali Gateway integration."""
from __future__ import annotations

import asyncio
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .vunho_daligw import VunhoDaliGW

from .const import DOMAIN

PLATFORMS = ["light"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up VUNHO Dali Gateway from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hub = VunhoDaliGW(entry.data["host"], entry.data["port"])
    retry = 0
    while not await hass.async_add_executor_job(hub.connect):
        if retry > 5:
            return False
        await asyncio.sleep(10)
        retry = retry + 1
    hass.data[DOMAIN][entry.unique_id] = hub
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.unique_id)

    return unload_ok
