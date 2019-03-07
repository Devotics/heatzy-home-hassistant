import logging
import time

from .const import HEATZY_API_URL, HEATZY_APPLICATION_ID

_LOGGER = logging.getLogger(__name__)


class HeatzyAuthenticator:
    def __init__(self, session, store, username, password):
        self._session = session
        self._store = store
        self._username = username
        self._password = password

    async def async_authenticate(self):
        """Get Heatzy stored authentication if it exists or authenticate against Heatzy API"""
        stored_auth = await self._async_load_authentication()
        # check if there is a stored authentication and if it is not expired
        if stored_auth is not None and stored_auth.get('expire_at') > time.time():
            # return stored authentication
            return stored_auth
        # refresh authentication
        headers = {
            'X-Gizwits-Application-Id': HEATZY_APPLICATION_ID
        }
        payload = {
            'username': self._username,
            'password': self._password
        }
        response = await self._session.post(HEATZY_API_URL + '/login', json=payload, headers=headers)

        if response.status != 200:
            _LOGGER.error("Heatzy API returned HTTP status %d, response %s",
                          response.status, response)
            return None

        authentication = await response.json()
        await self._async_save_authentication(authentication)
        return authentication

    async def _async_load_authentication(self):
        """Load stored authentication"""
        return await self._store.async_load()

    async def _async_save_authentication(self, authentication):
        """Save authentication to store"""
        return await self._store.async_save(authentication)
