FROM python:3.10.6
RUN mkdir /bot && chmod 777 /bot
WORKDIR /bot
ENV DEBIAN_FRONTEND=noninteractive
RUN apt -qq update && apt -qq install -y git wget pv jq python3-dev ffmpeg mediainfo
RUN apt-get install neofetch wget -y -f

COPY . .
RUN pip3 install -r requirements.txt
CMD ["bash","run.sh"]
