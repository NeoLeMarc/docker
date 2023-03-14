FROM debian:bullseye
RUN apt update
RUN apt install rsyslog wget -y
COPY rsyslog.conf /etc/rsyslog.conf
COPY /etc/resolv.conf /etc/resolv.conf
CMD /usr/sbin/rsyslogd -n -f /etc/rsyslog.conf
EXPOSE 514/udp
#CMD /bin/bash
