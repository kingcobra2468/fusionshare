from os import getenv
import logging
import sys

from wsgiref.simple_server import make_server
from dotenv import load_dotenv
import falcon

from resources.service_resource import ServiceResource
from proxy.tunnel_router import TunnelRouter


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
load_dotenv()


def error_serializer(req, resp, exception):
    """Serializes a given error to follow the conventions defined
    here https://github.com/omniti-labs/jsend .
    """
    resp.content_type = falcon.MEDIA_JSON

    resp.media = {
        'status': 'error',
        'data': exception.to_dict()
    }


if __name__ == '__main__':
    service_proxy = TunnelRouter(getenv('NGROK_AUTH_TOKEN'))
    service = ServiceResource(service_proxy)

    app = falcon.App(cors_enable=True)
    app.add_route('/services/{name}', service)
    app.set_error_serializer(error_serializer)

    port = int(getenv('FUSIONSHARE_PORT'))
    with make_server('0.0.0.0', port, app) as httpd:
        logging.info(f'Serving on port {port}...')

        # Serve until process is killed
        httpd.serve_forever()
