# Logloki
Logloki is a small docker-compose setup, that provides you with a quick and
easy syslog target that ships via promtail to loki and brings a grafana to view the log.

It is mostly based on the docker-compose file from loki, I have added the
container for syslog.

This is very useful if you are in the field and need to debug some infrastructure like switches but don't have a syslog server handy.

# Usage
```bash
docker-compose -f docker-compose.yml up
```
The container provides a syslog target on port 514 udp on localhost. You can use docker, to expose this port. It also starts a grafana on http://localhost:3000. You can login using user "admin" and password "admin". Grafana then let's you change the password. Finally you need to create a new Loki datasource. Just add http://loki:3100 and you are set.

# Testing
There is a small sample script, that sends log lines to a syslog server that is running on localhost:514/udp
```bash
python3 testsyslog.py
```
