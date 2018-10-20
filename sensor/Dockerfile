FROM resin/raspberrypi3-debian:stretch

ENV INITSYSTEM on

RUN apt-get update && apt-get install -yq \
  python3 \
  python3-sense-hat \
  python3-influxdb \
  python3-pip \
  python3-setuptools\
  vim \
  wget && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . /usr/src/app
WORKDIR /usr/src/app
RUN pip3 install -r /usr/src/app/requirements.txt

# Finally, start our app
CMD ["python3", "/usr/src/app/measure.py"]
