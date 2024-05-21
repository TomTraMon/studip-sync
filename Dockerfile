FROM ubuntu:latest

ADD ./config/ /config/studip_config/

RUN apt update && apt upgrade -y
RUN apt install -y openssh-client
RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan gitlab.com >> ~/.ssh/known_hosts
RUN --mount=type=ssh,id=github
RUN apt install -y git
#RUN git clone git@github.com:TomTraMon/studip-sync.git

#RUN apt install -y git python3