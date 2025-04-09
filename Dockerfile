FROM mambaorg/micromamba:2-ubuntu22.04

COPY environment.yml /tmp/environment.yml

RUN micromamba create -y -f /tmp/environment.yml

WORKDIR /app

COPY . /app/

RUN mkdir -p /app/data /app/results

ARG MAMBA_DOCKERFILE_ACTIVATE=1
ENV MAMBA_DEFAULT_ENV=bio-agent

CMD ["micromamba", "run", "-n", "bio-agent", "python", "biotools_server.py"]