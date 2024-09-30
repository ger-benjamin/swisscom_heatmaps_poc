FROM debian:bullseye-slim
LABEL maintainer="Camptocamp <info@camptocamp.com>"

WORKDIR /app

COPY requirements.txt /app/

RUN DEV_PACKAGES="libpq-dev python3.9-dev python3-pip python3.9-distutils build-essential" && \
    apt update && \
    DEBIAN_FRONTEND=noninteractive apt install --yes --no-install-recommends ${DEV_PACKAGES} && \
    pip -V && \
    pip install --upgrade pip && \
    pip install --disable-pip-version-check --no-cache-dir -r requirements.txt && \
    apt remove --purge --autoremove --yes ${DEV_PACKAGES} binutils && \
    apt-get clean && \
    rm --force --recursive /var/lib/apt/lists/*

COPY . /app

# Generate the version file, black and compile.
ARG GIT_HASH
RUN pip3 install --no-cache-dir -e . && \
    c2cwsgiutils-genversion $GIT_HASH && \
    black swisscom_heatmap_geoproxy --check && \
    python3 -m compileall -q .

CMD ["gunicorn", "--paste=/app/production.ini"]

# Default values for the environment variables
ENV \
  DEVELOPMENT=0 \
  SQLALCHEMY_POOL_RECYCLE=30 \
  SQLALCHEMY_POOL_SIZE=5 \
  SQLALCHEMY_MAX_OVERFLOW=25 \
  SQLALCHEMY_SLAVE_POOL_RECYCLE=30 \
  SQLALCHEMY_SLAVE_POOL_SIZE=5 \
  SQLALCHEMY_SLAVE_MAX_OVERFLOW=25\
  LOG_TYPE=console \
  OTHER_LOG_LEVEL=WARNING \
  GUNICORN_LOG_LEVEL=WARNING \
  SQL_LOG_LEVEL=WARNING \
  C2CWSGIUTILS_LOG_LEVEL=WARNING \
  LOG_LEVEL=INFO
