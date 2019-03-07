from homeassistant.components.climate import ClimateDevice
from homeassistant.components.climate.const import (STATE_COOL, STATE_ECO,
                                                    STATE_HEAT,
                                                    SUPPORT_AWAY_MODE,
                                                    SUPPORT_ON_OFF,
                                                    SUPPORT_OPERATION_MODE)
from homeassistant.const import STATE_OFF, TEMP_CELSIUS

HEATZY_TO_HA_STATE = {
    'cft': STATE_HEAT,
    'eco': STATE_ECO,
    'fro': STATE_COOL,
    'stop': STATE_OFF,
}

HA_TO_HEATZY_STATE = {
    STATE_HEAT: 'cft',
    STATE_ECO: 'eco',
    STATE_COOL: 'fro',
    STATE_OFF: 'stop',
}
AWAY_MODE_ON = 1
AWAY_MODE_OFF = 0


class HeatzyPiloteV2Thermostat(ClimateDevice):
    def __init__(self, api, device):
        self._api = api
        self._device = device

    @property
    def temperature_unit(self):
        """Return the unit of measurement which this thermostat uses."""
        return TEMP_CELSIUS

    @property
    def operation_list(self):
        """Return the list of available operation modes."""
        return {
            STATE_HEAT,
            STATE_ECO,
            STATE_COOL
        }

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_OPERATION_MODE | SUPPORT_AWAY_MODE | SUPPORT_ON_OFF

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._device.get('did')

    @property
    def name(self):
        return self._device.get('dev_alias')

    @property
    def current_operation(self):
        """Return current operation ie. heat, cool, idle."""
        return HEATZY_TO_HA_STATE.get(self._device.get('attr').get('mode'))

    @property
    def is_away_mode_on(self):
        """Return true if away mode is on."""
        return self._device.get('attr').get('derog_mode') == AWAY_MODE_ON

    @property
    def is_on(self):
        """Return true if on."""
        return self.current_operation != STATE_OFF

    async def async_set_operation_mode(self, operation_mode):
        """Set new target operation mode."""
        await self._api.async_control_device(self.unique_id, {
            'attrs': {
                'mode': HA_TO_HEATZY_STATE.get(operation_mode),
            },
        })
        await self.async_update()

    async def async_turn_on(self):
        """Turn device on."""
        await self.async_set_operation_mode(STATE_HEAT)

    async def async_turn_off(self):
        """Turn device off."""
        await self.async_set_operation_mode(STATE_OFF)

    async def async_set_away_mode(self, away_mode):
        """Set away mode."""
        await self._api.async_control_device(self.unique_id, {
            'attrs': {
                'derog_mode': away_mode,
            },
        })
        await self.async_update()

    async def async_turn_away_mode_on(self):
        """Turn away mode on."""
        await self.async_set_away_mode(AWAY_MODE_ON)

    async def async_turn_away_mode_off(self):
        """Turn away mode off."""
        await self.async_set_away_mode(AWAY_MODE_OFF)

    async def async_update(self):
        """Retrieve latest state."""
        self._device = await self._api.async_get_device(self.unique_id)
