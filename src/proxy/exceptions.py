class RestrictedPortError(ValueError):
    """Thrown when there is an attempt to open a port that has
    ben marked as restricted.
    """

    def __init__(self, port) -> None:
        self.port = port
        super().__init__(f'An error occurred when trying to open restricted port {port}')
