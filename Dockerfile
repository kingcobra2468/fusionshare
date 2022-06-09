FROM python:3.7

ARG fusionshare_ngrok_auth_token
ARG fusionshare_port
ARG fusionshare_config_path=/fusionshare/config

ENV FUSIONSHARE_NGROK_AUTH_TOKEN=${fusionshare_ngrok_auth_token}
ENV FUSIONSHARE_PORT=${fusionshare_port}
ENV FUSIONSHARE_CONFIG_PATH=${fusionshare_config_path}

COPY src/ /opt/fusionshare/
COPY requirements.txt /tmp

RUN mkdir -p /fusionshare/config
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /opt/fusionshare

VOLUME /fusionshare/config

ENTRYPOINT ["python3", "main.py"]