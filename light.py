from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    COLOR_MODE_BRIGHTNESS,
    LightEntity
)
from .const import DOMAIN
from .vunho_daligw import VunhoDaliGW

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    hub = hass.data[DOMAIN][entry.unique_id]
    hubmac = await hass.async_add_executor_job(hub.read_mac_addr)
    hubprefix = hubmac.replace(":", "")
    devlist = await hass.async_add_executor_job(hub.read_dev_list)
    devs = []
    for devaddr, devtype in devlist:
        if devtype == 6:
            devs.append(DaliDT6(hub, devaddr, hubprefix))
    async_add_entities(devs)

class DaliDT6(LightEntity):

    _attr_should_poll = True
    _attr_supported_color_modes = {COLOR_MODE_BRIGHTNESS}
    _attr_color_mode = COLOR_MODE_BRIGHTNESS

    def __init__(self, gw : VunhoDaliGW, addr, prefix):
        self._gw = gw
        self._addr = addr
        self._brightness = 0
        self._attr_unique_id = prefix + ".dt6." + str(addr)

    @property
    def name(self):
        return "DALI Light %d" % self._addr

    @property
    def brightness(self):
        return self._brightness

    @property
    def is_on(self):
        return self._brightness > 0

    def turn_on(self, **kwargs):
        self._brightness = kwargs.get(ATTR_BRIGHTNESS, 255)
        self._gw.set_brightness(self._addr, self._brightness)

    def turn_off(self, **kwargs):
        self._brightness = 0
        self._gw.set_brightness(self._addr, 0)

    def update(self):
        self._brightness = self._gw.get_brightness(self._addr)