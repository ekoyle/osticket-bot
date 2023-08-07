FROM ghcr.io/bhnoc/python3:latest
RUN dnf -y update && \
        dnf -y install findutils


RUN dnf install -y dnf-utils
RUN dnf install -y cronie && crond -V

#project setup
RUN mkdir -p /opt/env/live/app
COPY . /opt/env/live/.
run source /opt/env/live/bin/activate && pip install -r /opt/env/live/app/requirements.txt

COPY build/start-up.sh start-up.sh
RUN chmod +x start-up.sh
CMD ["/start-up.sh"]
