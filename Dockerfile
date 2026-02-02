# ---------- Base image ----------
FROM ubuntu:20.04 AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /code

# System deps + Python 2.7
RUN apt-get update && apt-get install -y --no-install-recommends \
    python2.7 \
    python2.7-dev \
    build-essential \
    curl \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Install pip for Python 2.7
RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py && \
    python2.7 get-pip.py && \
    rm get-pip.py

# Symlinks
RUN ln -s /usr/bin/python2.7 /usr/bin/python && \
    ln -s /usr/local/bin/pip /usr/bin/pip

# Last Python 2 compatible tooling
RUN pip install --upgrade \
    pip==20.3.4 \
    setuptools==44.1.1 \
    wheel==0.37.1

COPY requirements/ /code/requirements/

# ---------- Django image ----------
FROM base AS cropimg

# Build argument with default value
ARG REQUIREMENTS_FILE=requirements/django18/test.txt

# Install dependencies dynamically
RUN pip install -r /code/${REQUIREMENTS_FILE}

COPY . /code/

CMD ["make", "test_with_coverage"]