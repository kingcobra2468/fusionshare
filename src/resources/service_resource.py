import logging

from falcon.media.validators import jsonschema
from falcon import HTTPConflict, HTTPNotFound
from schemas import load_schema

logger = logging.getLogger(__name__)


class ServiceResource:
    """Resource that handles the lifecycle of tunnel proxies of various ports. 
    """

    def __init__(self, tunnel_router) -> None:
        """Constructor.

        Args:
            tunnel_router (TunnelRouter): Instance of a tunnel router.
        """
        self._tunnel_router = tunnel_router

    def on_get(self, req, resp, name):
        """Gets the proxy uri for the currently exposed port.
        """
        if not self._tunnel_router.tunnel_exists(name):
            logger.warn(
                'Attempted to access tunnel %s which does not exist', name)
            raise HTTPNotFound(title='Service does not exist',
                               description=f'The service by the name "{name}" does not exist')

        tunnel = self._tunnel_router.get_tunnel(name)

        resp.media = {
            'status': 'success',
            'data': {
                'uri': tunnel
            }
        }

    @jsonschema.validate(load_schema('service_expose'))
    def on_post(self, req, resp, name):
        """Creates a new proxy uri for a given port. This removes
        an existing proxy if one exists.
        """
        if self._tunnel_router.tunnel_exists(name):
            logger.warn(
                'Attempted to create a new tunnel %s under a name that is already active', name)
            raise HTTPConflict(title='Service already defined',
                               description=f'The service by the name "{name}" already exists')

        data = req.get_media()
        tunnel = self._tunnel_router.expose_port(
            name, data['port'], data['proto'], data.get('bind_tls', True))

        resp.media = {
            'status': 'success',
            'data': {
                'uri': tunnel
            }
        }

    def on_delete(self, req, resp, name):
        """Removes a proxy instance for a given port if one is
        active.
        """
        if not self._tunnel_router.tunnel_exists(name):
            logger.warn(
                'Attempted to access tunnel %s which does not exist', name)
            raise HTTPNotFound(title='Service does not exist',
                               description=f'The service by the name "{name}" does not exist')

        status = self._tunnel_router.stop_tunnel(name)
        resp.media = {
            'status': 'success',
            'data': None
        }
