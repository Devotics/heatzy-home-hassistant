import logging

from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers import aiohttp_client, storage

from .api import HeatzyAPI
from .authenticator import HeatzyAuthenticator
from .const import (HEATZY_PILOTE_V1_PRODUCT_KEY, HEATZY_PILOTE_V2_PRODUCT_KEY,
                    STORAGE_KEY, STORAGE_VERSION)
from .pilote_v1 import HeatzyPiloteV1Thermostat
from .pilote_v2 import HeatzyPiloteV2Thermostat

PRODUCT_KEY_TO_DEVICE_IMPLEMENTATION = {
    HEATZY_PILOTE_V1_PRODUCT_KEY: HeatzyPiloteV1Thermostat,
    HEATZY_PILOTE_V2_PRODUCT_KEY: HeatzyPiloteV2Thermostat,
}

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, add_devices, discovery_info=None):
    """Configure Heatzy API using Home Assistant configuration and fetch all Heatzy devices."""
    # retrieve platform config
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)

    session = aiohttp_client.async_get_clientsession(hass)
    store = storage.Store(hass, STORAGE_VERSION, STORAGE_KEY)

    authenticator = HeatzyAuthenticator(session, store, username, password)
    api = HeatzyAPI(session, authenticator)

    # fetch configured Heatzy devices
    devices = await api.async_get_devices()
    # add all Heatzy devices with HA implementation to home assistant
    add_devices(filter(None.__ne__, map(setup_heatzy_device(api), devices)))
    return True


def setup_heatzy_device(api):
    def find_heatzy_device_implementation(device):
        """Find Home Assistant implementation for the Heatzy device.
        Implementation search is based on device 'product_key'.
        If the implementation is not found, returns None.
        """
        DeviceImplementation = PRODUCT_KEY_TO_DEVICE_IMPLEMENTATION.get(
            device.get('product_key'))
        if DeviceImplementation is None:
            _LOGGER.warn('Device %s with product key %s is not supported',
                         device.get('did'), device.get('product_key'))
            return None
        return DeviceImplementation(api, device)
    return find_heatzy_device_implementation
