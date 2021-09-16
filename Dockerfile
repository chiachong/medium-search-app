FROM ubuntu:18.04

# install python 3.7
RUN apt-get update && apt-get install -y \
        software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y \
    python3.7 \
    python3-pip
RUN python3.7 -m pip install pip
RUN apt-get update && apt-get install -y \
    python3-distutils \
    python3-setuptools
RUN python3.7 -m pip install pip --upgrade pip

# install google chrome
RUN apt-get update && apt-get install -y curl unzip wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# download chrome driver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/local/bin/ && \
    rm chromedriver_linux64.zip

COPY ./requirements.txt /requirements.txt

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir --upgrade pip setuptools && \
    pip3 install --no-cache-dir -r /requirements.txt

COPY ./srcs /srcs

ENTRYPOINT ["streamlit", "run"]

CMD ["/srcs/streamlit_app/app.py"]

EXPOSE 8501
