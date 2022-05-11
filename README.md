# FusionShare
A simple RESTful microservice for exposing local ports to the world through
tunneling. Built on top of Ngrok.

## Use Cases
FusionShare is designed to provide programmatic exposure of local ports through
a REST API. This might be needed for a variety of purposes such as:
- Exposing microservices to the world temporary.
- Exposing system services such as SSH.
  
## REST API
The REST API is documented through Swagger and can be analyzed by importing
the yaml file (found in `docs/swagger` directory) into Swagger. To setup Swagger, follow
the docs found [here](https://swagger.io/docs/open-source-tools/swagger-editor/).

## Configuration
Configuration for FusionShare lives within an env file. Copy/rename the template.env
file into `.env`. Then, the following options can be configured:
- **FUSIONSHARE_NGROK_AUTH_TOKEN=** The auth token for Ngrok. The token becomes accessible
  after an Ngrok account is created. Only a free tier account is needed for FusionShare.  
- **FUSIONSHARE_PORT=** The port on which FusionShare runs on.

## Installation
1. Ensure that Python 3.6+ is on the system.
2. Install dependencies with with `pip3 install -r requirements.txt`.
3. Setup the `.env` file as described in the [config](#configuration) section.
4. Once inside `/src`, run FusionShare with `python3 app.py`.