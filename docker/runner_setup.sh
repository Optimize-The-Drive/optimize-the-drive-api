#!/bin/bash

apt update

# Install docker if not on runner already
if [ ! -x "$(command -v docker)" ]; then
    apt install apt-transport-https curl gnupg-agent ca-certificates software-properties-common -y
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
    apt install docker-ce docker-ce-cli containerd.io -y
    systemctl enable docker
    systemctl start docker
fi