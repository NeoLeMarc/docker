# Logloki
Logloki is a small docker-compose setup, that provides you with a quick and
easy syslog target that ships via promtail to loki and brings a grafana to view the log.

It is mostly based on the docker-compose file from loki, I have added the
container for syslog.

This is very useful if you are in the field and need to debug some infrastructure like switches but don't have a syslog server handy.