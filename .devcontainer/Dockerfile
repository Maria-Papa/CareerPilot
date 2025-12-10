# Base image: Ubuntu 22.04 LTS with Dev Container base
FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV WORKSPACE=/workspace
WORKDIR ${WORKSPACE}

# Install OS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential curl wget git iproute2 procps unzip \
  libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
  libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 \
  libpango-1.0-0 libasound2 libatspi2.0-0 ffmpeg \
  && rm -rf /var/lib/apt/lists/*

# Set up vscode user and workspace
ARG USERNAME=vscode
RUN mkdir -p ${WORKSPACE} && chown -R ${USERNAME}:${USERNAME} ${WORKSPACE}
USER ${USERNAME}

# Default shell
SHELL ["/bin/bash", "-lc"]
CMD ["bash"]
