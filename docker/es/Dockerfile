FROM docker.elastic.co/elasticsearch/elasticsearch:8.13.4

USER root
RUN apt-get update && apt-get install -y sudo tmux software-properties-common
RUN apt-get install -y wget
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
RUN mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
RUN wget --progress=bar:force:noscroll https://developer.download.nvidia.com/compute/cuda/12.4.1/local_installers/cuda-repo-wsl-ubuntu-12-4-local_12.4.1-1_amd64.deb
RUN dpkg -i cuda-repo-wsl-ubuntu-12-4-local_12.4.1-1_amd64.deb
RUN cp /var/cuda-repo-wsl-ubuntu-12-4-local/cuda-*-keyring.gpg /usr/share/keyrings/
RUN echo 'APT::Acquire::Retries "3";' > /etc/apt/apt.conf.d/80-retries
RUN apt-get update && apt-get -y install cuda-toolkit-12-4

USER 1000:0
