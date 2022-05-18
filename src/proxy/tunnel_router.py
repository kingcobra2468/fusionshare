import logging
from proxy.exceptions import RestrictedPortError

from pyngrok import ngrok


logger = logging.getLogger(__name__)
logging.getLogger('pyngrok').setLevel(logging.ERROR)


class TunnelRouter:
    """Router that manages the proxy tunnel between an internal port and
    its corresponding tunnel endpoint. 
    """

    def __init__(self, port_guard, auth_token=None):
        """Constructor.

        Args:
            port_guard (proxy.port_guard.PortGuard): An instance of port guard for determining
            the allowed and denied ports.
            auth_token (str, optional): The auth token for Ngrok. With this token,
            more features are unlocked as part of Ngrok's free plan. Without it,
            certain features might not work. Defaults to None.
        """
        if auth_token:
            ngrok.set_auth_token(auth_token)
        self._port_guard = port_guard
        self._cache = {}

    def expose_port(self, name, port, proto, bind_tls=True):
        """Exposes a given port on the host machine and binds a proxy tunnel to it.

        Args:
            name (str): Name to give to the port being exposed.
            port (int): The port that is being exposed.
            proto (str): The protocol to use (e.g. http, tcp, udp, ...)
            bind_tls (bool, optional): Whether to only create a TLS tunnel. Defaults to True.

        Raises:
            RestrictedPortError: Thrown when there was an attempt to open a port that has
            been marked as restricted.
            
        Returns:
            str: The uri for the corresponding tunnel.
        """
        if not self._port_guard.allowed(port):
            raise RestrictedPortError(port)
        
        logger.info(
            'Created a new tunnel called "%s" on port %i using %s protocol', name, port, proto)
        tunnel = ngrok.connect(addr=port, name=name, proto=proto,
                               bind_tls=bind_tls)
        self._cache[tunnel.name] = tunnel.public_url

        return tunnel.public_url

    def tunnel_exists(self, name):
        """Checks whether a tunnel already exists under a given name.

        Args:
            name (str): Name of the tunnel.

        Returns:
            bool: Whether such a tunnel exists. True if exists, False otherwise.
        """
        return name in self._cache

    def get_tunnel(self, name):
        """Retrieves the tunnel uri under the given name.

        Args:
            name (str): Name of the tunnel.

        Raises:
            ValueError: Raised if no such tunnel exists for the given name.

        Returns:
            str: The uri for the corresponding tunnel.
        """
        if name not in self._cache:
            raise ValueError('Service doesnt exist')

        return self._cache[name]

    def stop_tunnel(self, name):
        """Stops a given tunnel under a given name.

        Args:
            name (str): Name of the tunnel.

        Returns:
            bool: Whether the tunnel was closed. True if success, False otherwise.
        """
        if name not in self._cache:
            return False

        logger.info('Stopped tunnel session for "%s"', name)

        ngrok.disconnect(self._cache[name])
        del self._cache[name]

        return True
