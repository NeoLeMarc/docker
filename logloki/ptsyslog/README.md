# ptsyslog
A very simple container that provides a syslog target and writes the received
loglines to separate filess - depending on the host sending the logs.

This is meant to be used together with promtail to ship to loki.

# Usage
There is a whole docker-compose setup that uses ptsyslog togehter with
promtail and loki. See: [Logloki](https://github.com/NeoLeMarc/docker/tree/main/logloki)
