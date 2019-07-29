from homeassistant.components.climate import ClimateDevice
from homeassistant.components.climate.const import (HVAC_MODE_AUTO,
                                                    PRESET_AWAY,
                                                    PRESET_COMFORT, PRESET_ECO,
                                                    PRESET_NONE,
                                                    SUPPORT_PRESET_MODE)
from homeassistant.const import TEMP_CELSIUS

HEATZY_TO_HA_STATE = {
    'cft': PRESET_COMFORT,
    'eco': PRESET_ECO,
    'fro': PRESET_AWAY,
    'stop': PRESET_NONE,
}

HA_TO_HEATZY_STATE = {
    PRESET_COMFORT: 'cft',
    PRESET_ECO: 'eco',
    PRESET_AWAY: 'fro',
    PRESET_NONE: 'stop',
}


class HeatzyPiloteV2Thermostat(ClimateDevice):
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
            'attrs': {
                'mode': HA_TO_HEATZY_STATE.get(preset_mode),
            },
        })
        await self.async_update()

    async def async_update(self):
        """Retrieve latest state."""
        self._device = await self._api.async_get_device(self.unique_id)
