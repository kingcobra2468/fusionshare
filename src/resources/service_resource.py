from schemas import load_schema
from falcon.media.validators import jsonschema


class ServiceResource:
    """Resource that handles the lifecycle of the exposure
    of a service via a proxy channel.
    """
    def on_get(self, req, resp):
        """Gets the proxy uri for the currently exposed port.
        """
        resp.media = {'url': '...'}

    @jsonschema.validate(load_schema('service_expose'))
    def on_post(self, req, resp):
        """Creates a new proxy uri for a given port. This removes
        an existing proxy if one exists.
        """
        print(req.get_media())

    def on_delete(self, req, resp):
        """Removes a proxy instance for a given port if one is
        active.
        """
        resp.media = {'success': True}
