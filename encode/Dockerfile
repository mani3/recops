FROM ubuntu:24.04

RUN apt update && apt install -y locales-all
ENV LANG=ja_JP.UTF8
ENV TZ=Asia/Tokyo
ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /root

RUN apt update \
  && apt install -y vim \
  git autoconf python3 python3-pip \
  build-essential cmake automake meson ninja-build texinfo \
  pkg-config nasm yasm gnutls-dev \
  libass-dev \
  libfreetype6-dev \
  libgnutls28-dev \
  libmp3lame-dev \
  libsdl2-dev \
  libtool \
  libva-dev \
  libvdpau-dev \
  libvorbis-dev \
  libxcb1-dev \
  libxcb-shm0-dev \
  libxcb-xfixes0-dev \
  libdvbpsi-dev \
  libaribb24-dev \
  libunistring-dev \
  libaom-dev \
  libdav1d-dev \
  libfdk-aac-dev \
  libopus-dev \
  libsvtav1-dev \
  libx264-dev \
  libx265-dev \
  libnuma-dev \
  libvpx-dev \
  libsvtav1enc-dev

RUN git clone https://git.ffmpeg.org/ffmpeg.git \
  && cd ffmpeg \
  && git checkout -b n6.1.1 n6.1.1 \
  && PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure \
  --prefix="$HOME/ffmpeg_build" \
  --pkg-config-flags="--static" \
  --extra-cflags="-I$HOME/ffmpeg_build/include" \
  --extra-ldflags="-L$HOME/ffmpeg_build/lib" \
  --extra-libs="-lpthread -lm" \
  --ld="g++" \
  --bindir="$HOME/bin" \
  --enable-gpl \
  --enable-gnutls \
  --enable-libaom \
  --enable-libass \
  --enable-libfdk-aac \
  --enable-libfreetype \
  --enable-libmp3lame \
  --enable-libopus \
  --enable-libsvtav1 \
  --enable-libdav1d \
  --enable-libvorbis \
  --enable-libvpx \
  --enable-libx264 \
  --enable-libx265 \
  --enable-nonfree \
  --enable-version3 \
  --enable-libaribb24 \
  --enable-libaom \
  && PATH="$HOME/bin:$PATH" make -j$(nproc) \
  && make install

RUN git clone https://github.com/mkrufky/libdvbtee.git \
  && cd libdvbtee \
  && ./build-auto.sh && make install
RUN git clone https://github.com/Piro77/epgdump.git \
  && cd epgdump \
  && cmake . && make && make install

