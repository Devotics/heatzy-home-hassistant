from homeassistant.components.climate import ClimateDevice
from homeassistant.components.climate.const import (STATE_COOL, STATE_ECO,
                                                    STATE_HEAT, SUPPORT_ON_OFF,
                                                    SUPPORT_OPERATION_MODE)
from homeassistant.const import STATE_OFF, TEMP_CELSIUS

HEATZY_TO_HA_STATE = {
    '\u8212\u9002': STATE_HEAT,
    '\u7ecf\u6d4e': STATE_ECO,
    '\u89e3\u51bb': STATE_COOL,
    '\u505c\u6b62': STATE_OFF,
}

HA_TO_HEATZY_STATE = {
    STATE_HEAT: [1, 1, 0],
    STATE_ECO: [1, 1, 1],
    STATE_COOL: [1, 1, 2],
    STATE_OFF: [1, 1, 3],
}


class HeatzyPiloteV1Thermostat(ClimateDevice):
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
        return SUPPORT_OPERATION_MODE | SUPPORT_ON_OFF

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
    def is_on(self):
        """Return true if on."""
        return self.current_operation != STATE_OFF

    async def async_set_operation_mode(self, operation_mode):
        """Set new target operation mode."""
        await self._api.async_control_device(self.unique_id, {
            'raw': HA_TO_HEATZY_STATE.get(operation_mode),
        })
        await self.async_update()

    async def async_turn_on(self):
        """Turn device on."""
        await self.async_set_operation_mode(STATE_HEAT)

    async def async_turn_off(self):
        """Turn device off."""
        await self.async_set_operation_mode(STATE_OFF)

    async def async_update(self):
        """Retrieve latest state."""
        self._device = await self._api.async_get_device(self.unique_id)
