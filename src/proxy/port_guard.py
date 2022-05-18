class PortGuard:
    def __init__(self, config):
        self._accepted_ports = config.get('allowed', None)
        self._denied_ports = config.get('denied', None)

    def allowed(self, port):
        if self._denied_ports and port in self._denied_ports:
            return False
        elif self._accepted_ports and port not in self._accepted_ports:
            return False

        return True
