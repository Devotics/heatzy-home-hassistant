import logging

import async_timeout
from homeassistant.components.climate import (STATE_COOL, STATE_ECO,
                                              STATE_HEAT, SUPPORT_AWAY_MODE,
                                              SUPPORT_ON_OFF,
                                              SUPPORT_OPERATION_MODE,
                                              ClimateDevice)
from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, TEMP_CELSIUS
from homeassistant.helpers import aiohttp_client, storage

from .api import HeatzyAPI
from .authenticator import HeatzyAuthenticator
from .const import STORAGE_KEY, STORAGE_VERSION

_LOGGER = logging.getLogger(__name__)

HA_TO_HEATZY_STATE = {
    STATE_HEAT: 'cft',
    STATE_ECO: 'eco',
    STATE_COOL: 'fro'
}
HEATZY_TO_HA_STATE = {
    'cft': STATE_HEAT,
    'eco': STATE_ECO,
    'fro': STATE_COOL,
}


async def async_setup_platform(hass, config, add_devices, discovery_info=None):
    # retrieve platform config
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)

    session = aiohttp_client.async_get_clientsession(hass)
    store = storage.Store(hass, STORAGE_VERSION, STORAGE_KEY)

    authenticator = HeatzyAuthenticator(session, store, username, password)
    api = HeatzyAPI(session, authenticator)

    # fetch configured Heatzy devices
    devices = await api.async_get_devices()
    # add all Heatzy devices to home assistant
    add_devices(HeatzyPilotThermostat(api, device) for device in devices)
    return True


class HeatzyPilotThermostat(ClimateDevice):
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
        return self._device.get('attr').get('derog_mode') == 1

    @property
    def is_on(self):
        """Return true if on."""
        return self._device.get('attr').get('mode') != 'stop'

    async def set_operation_mode(self, operation_mode):
        """Set new target operation mode."""
        _LOGGER.debug("Setting operation mode '%s' for device '%s'...",
                      operation_mode, self.unique_id)
        await self._api.async_set_mode(self.unique_id, HA_TO_HEATZY_STATE.get(operation_mode))
        await self.async_update()
        _LOGGER.info("Operation mode set to '%s' for device '%s'",
                     operation_mode, self.unique_id)

    async def async_turn_on(self):
        """Turn device on."""
        _LOGGER.debug("Turning device '%s' on...", self.unique_id)
        await self._api.async_turn_on(self.unique_id)
        await self.async_update()
        _LOGGER.info("Device '%s' turned on (%s)", self.unique_id)

    async def async_turn_off(self):
        """Turn device off."""
        _LOGGER.debug("Turning device '%s' off...", self.unique_id)
        await self._api.async_turn_off(self.unique_id)
        await self.async_update()
        _LOGGER.info("Device '%s' turned off (%s)", self.unique_id)

    async def async_turn_away_mode_on(self):
        """Turn away mode on."""
        _LOGGER.debug("Turning device '%s' away mode on...", self.unique_id)
        await self._api.async_turn_away_mode_on(self.unique_id)
        await self.async_update()
        _LOGGER.info("Device '%s' away mode turned on", self.unique_id)

    async def turn_away_mode_off(self):
        """Turn away mode off."""
        _LOGGER.debug("Turning device '%s' away mode off...", self.unique_id)
        await self._api.async_turn_away_mode_off(self.unique_id)
        await self.async_update()
        _LOGGER.info("Device '%s' away mode turned off", self.unique_id)

    async def async_update(self):
        """Retrieve latest state."""
        _LOGGER.debug("Updating device '%s'... Current state is: %s",
                      self.unique_id, {'is_on': self.is_on, 'is_away_mode_on': self.is_away_mode_on, 'current_operation': self.current_operation})
        self._device = await self._api.async_get_device(self.unique_id)
        _LOGGER.debug("Device '%s' updated. New state is: %s",
                      self.unique_id, {'is_on': self.is_on, 'is_away_mode_on': self.is_away_mode_on, 'current_operation': self.current_operation})
