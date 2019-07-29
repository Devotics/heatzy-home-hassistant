from homeassistant.components.climate import ClimateDevice
from homeassistant.components.climate.const import (HVAC_MODE_AUTO,
                                                    PRESET_AWAY,
                                                    PRESET_COMFORT, PRESET_ECO,
                                                    PRESET_NONE,
                                                    SUPPORT_PRESET_MODE)
from homeassistant.const import TEMP_CELSIUS

HEATZY_TO_HA_STATE = {
    '\u8212\u9002': PRESET_COMFORT,
    '\u7ecf\u6d4e': PRESET_ECO,
    '\u89e3\u51bb': PRESET_AWAY,
    '\u505c\u6b62': PRESET_NONE,
}

HA_TO_HEATZY_STATE = {
    PRESET_COMFORT: [1, 1, 0],
    PRESET_ECO: [1, 1, 1],
    PRESET_AWAY: [1, 1, 2],
    PRESET_NONE: [1, 1, 3],
}


class HeatzyPiloteV1Thermostat(ClimateDevice):
    def __init__(self, api, device):
        self._api = api
        self._device = device

    @property
    def temperature_unit(self):
        """Return the unit of measurement used by the platform."""
        return TEMP_CELSIUS

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_PRESET_MODE

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._device.get('did')

    @property
    def name(self):
        return self._device.get('dev_alias')

    @property
    def hvac_modes(self):
        """Return the list of available hvac operation modes.

        Need to be a subset of HVAC_MODES.
        """
        return [
            HVAC_MODE_AUTO
        ]

    @property
    def hvac_mode(self):
        """Return hvac operation ie. heat, cool mode.

        Need to be one of HVAC_MODE_*.
        """
        return HVAC_MODE_AUTO

    @property
    def preset_modes(self):
        """Return a list of available preset modes.

        Requires SUPPORT_PRESET_MODE.
        """
        return [
            PRESET_NONE,
            PRESET_COMFORT,
            PRESET_ECO,
            PRESET_AWAY
        ]

    @property
    def preset_mode(self):
        """Return the current preset mode, e.g., home, away, temp.

        Requires SUPPORT_PRESET_MODE.
        """
        return HEATZY_TO_HA_STATE.get(self._device.get('attr').get('mode'))

    async def async_set_preset_mode(self, preset_mode):
        """Set new preset mode."""
        await self._api.async_control_device(self.unique_id, {
            'raw': HA_TO_HEATZY_STATE.get(preset_mode),
        })
        await self.async_update()

    async def async_update(self):
        """Retrieve latest state."""
        self._device = await self._api.async_get_device(self.unique_id)
