FROM ubuntu:18.04

RUN apt-get clean &&  \
    apt-get update && \
    apt-get install -yq --no-install-recommends python3-pip \
                        python3-dev \
                        python3-setuptools \
                        python3-wheel \
						build-essential \
                        locales \
                        wget \
                        gunicorn3
RUN pip3 install --upgrade setuptools

# Download and install Elastic Search
RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.9.2-linux-x86_64.tar.gz
RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.9.2-linux-x86_64.tar.gz.sha512
RUN shasum -a 512 -c elasticsearch-7.9.2-linux-x86_64.tar.gz.sha512 
RUN tar -xzf elasticsearch-7.9.2-linux-x86_64.tar.gz
RUN cd elasticsearch-7.9.2

# Run Elastoic Search
# RUN bin/elasticsearch

## Locale information
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen
ENV LANG=en_US.UTF-8   \
    LANGUAGE=en_US.UTF-8   \
    LC_ALL=en_US.UTF-8

## Create User and switch to user space
ENV APP_USER="mattar" \
    APP_DIR="/app"
RUN adduser --disabled-password --gecos "" "$APP_USER"

# Add Watson API key to use the tone analyzer
ENV WATSON_TONE_ANALYZER_API_KEY=""

# Install APP
WORKDIR "$APP_DIR"
COPY reviews_tone_api "$APP_DIR/reviews_tone_api"
COPY ["README.md", "run.sh", "setup.*", "dock.run.vars", "requirements*.txt", "$APP_DIR/"]

RUN pip3 install --no-cache-dir --upgrade --requirement "$APP_DIR/requirements.txt"

# RUN APP
CMD /bin/bash run.sh
