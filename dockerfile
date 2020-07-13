FROM debian:buster-slim

ARG EMAIL
ARG PASSWORD
ARG PORT=5059

RUN mkdir /code
WORKDIR /code

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip git && \
    pip3 install flask && \
    pip3 install flask-jsonpify && \
    git clone https://github.com/bdwilson/raincloudy && \
    git clone https://github.com/bdwilson/raincloudy-flask && \
    sed -i "s/EMAIL/${EMAIL}/" /code/raincloudy-flask/raincloudy_flask.py && \
    sed -i "s/PASSWORD/${PASSWORD}/" /code/raincloudy-flask/raincloudy_flask.py && \
    sed -i "s/PORT/${PORT}/" /code/raincloudy-flask/raincloudy_flask.py

#ADD . /code/
WORKDIR /code/raincloudy
RUN /usr/bin/python3 setup.py install
EXPOSE ${PORT}
CMD [ "python3", "/code/raincloudy-flask/raincloudy_flask.py" ]
