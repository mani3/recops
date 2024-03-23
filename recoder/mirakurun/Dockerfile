ARG ARCH=
FROM ${ARCH}node:18.15.0-buster AS build
WORKDIR /app
ENV DOCKER=YES NODE_ENV=production
ADD . .
RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y --no-install-recommends build-essential && \
  npm install --production=false && \
  npm run build && \
  npm install -g --unsafe-perm --production

FROM ${ARCH}node:18.15.0-buster-slim
WORKDIR /app
RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y --no-install-recommends \
  ca-certificates \
  cmake \
  make \
  gcc \
  g++ \
  pkg-config \
  pcscd \
  libpcsclite-dev \
  libccid \
  libdvbv5-dev \
  pcsc-tools \
  dvb-tools \
  build-essential \
  libtool \
  autoconf \
  git \
  automake \
  && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*
COPY --from=build /usr/local/lib/node_modules/mirakurun /app

RUN git clone https://github.com/stz2012/libarib25.git && \
  cd libarib25 && \
  cmake . && \
  make && \
  make install && \
  ldconfig

RUN git clone https://github.com/stz2012/recpt1.git && \
  cd recpt1/recpt1/ && \
  ./autogen.sh && \
  ./configure --enable-b25 && \
  make && \
  make install && \
  install -m 755 recpt1 recpt1ctl checksignal /usr/local/bin


CMD ["./docker/container-init.sh"]
EXPOSE 40772 9229
