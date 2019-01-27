import asyncio

from .const import HEATZY_API_URL, HEATZY_APPLICATION_ID


class HeatzyAPI:
    def __init__(self, session, authenticator):
        self._session = session
        self._authenticator = authenticator

    async def _async_get_token(self):
        """Get authentication token"""
        authentication = await self._authenticator.async_authenticate()
        return authentication.get('token')

    async def async_get_devices(self):
        """Fetch all configured devices"""
        token = await self._async_get_token()
        headers = {
            'X-Gizwits-Application-Id': HEATZY_APPLICATION_ID,
            'X-Gizwits-User-Token': token
        }
        response = await self._session.get(HEATZY_API_URL + '/bindings', headers=headers)
        # API response has Content-Type=text/html, content_type=None silences parse error by forcing content type
        body = await response.json(content_type=None)
        devices = body.get('devices')
        return await asyncio.gather(
            *[self._merge_with_device_data(device) for device in devices]
        )

    async def async_get_device(self, device_id):
        """Fetch device with given id"""
        token = await self._async_get_token()
        headers = {
            'X-Gizwits-Application-Id': HEATZY_APPLICATION_ID,
            'X-Gizwits-User-Token': token
        }
        response = await self._session.get(HEATZY_API_URL + '/devices/' + device_id, headers=headers)
        # API response has Content-Type=text/html, content_type=None silences parse error by forcing content type
        device = await response.json(content_type=None)
        return await self._merge_with_device_data(device)

    async def _merge_with_device_data(self, device):
        """Fetch detailled data for given device and merge it with the device information"""
        device_data = await self._async_get_device_data(device.get('did'))
        return {**device, **device_data}

    async def _async_get_device_data(self, device_id):
        """Fetch detailled data for device with given id"""
        token = await self._async_get_token()
        headers = {
            'X-Gizwits-Application-Id': HEATZY_APPLICATION_ID,
            'X-Gizwits-User-Token': token
        }
        response = await self._session.get(HEATZY_API_URL + '/devdata/' + device_id + '/latest', headers=headers)
        device_data = await response.json()
        return device_data

    async def _async_control_device(self, device_id, payload):
        """Control state of device with given id"""
        token = await self._async_get_token()
        headers = {
            'X-Gizwits-Application-Id': HEATZY_APPLICATION_ID,
            'X-Gizwits-User-Token': token
        }
        response = await self._session.post(HEATZY_API_URL + '/control/' + device_id, json=payload, headers=headers)

    async def async_set_mode(self, device_id, mode):
        """Change device mode. Mode can be 'cft', 'eco', 'fro' or 'stop'."""
        return await self._async_control_device(device_id, {
            'attrs': {
                'mode': mode
            }
        })

    async def async_turn_on(self, device_id):
        """Turn device on"""
        return await self.async_set_mode(device_id, 'cft')

    async def async_turn_off(self, device_id):
        """Turn device off"""
        return await self.async_set_mode(device_id, 'stop')

    async def _async_set_derog_mode(self, device_id, derog_mode):
        """Set device 'derog_mode' (away_mode)"""
        return await self._async_control_device(device_id, {
            'attrs': {
                'derog_mode': derog_mode
            }
        })

    async def async_turn_away_mode_on(self, device_id):
        """Turn device away mode on"""
        return await self._async_set_derog_mode(device_id, 1)

    async def async_turn_away_mode_off(self, device_id):
        """Turn device away mode off"""
        return await self._async_set_derog_mode(device_id, 0)
