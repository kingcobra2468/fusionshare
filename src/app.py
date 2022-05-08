from wsgiref.simple_server import make_server
import falcon

from resources.service_resource import ServiceResource

service = ServiceResource()

app = falcon.App()
app.add_route('/service', service)

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')

        # Serve until process is killed
        httpd.serve_forever()
