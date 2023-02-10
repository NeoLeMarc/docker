FROM mqtt-controller
#FROM tensorflow/tensorflow:latest-gpu
#RUN apk --update add bash nano vim
#RUN apk add make automake gcc g++ subversion python3-dev
COPY ./requirements.txt /var/www/requirements.txt
RUN apt-get update
RUN apt-get install python3-pip build-essential -y
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /var/www/requirements.txt
WORKDIR /app/app
EXPOSE 5002
CMD ["python3", "-m", "flask", "--app", "main", "run", "--host=0.0.0.0"]
