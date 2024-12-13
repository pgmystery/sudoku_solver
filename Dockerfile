FROM python:3.12-bookworm AS buildozer

ARG KEYSTORE_FILE_PASSWORD
ARG APK_VERSION
ENV BUILDOZER_VERSION="1.5.0"

ENV USER="user"
ENV HOME_DIR="/home/${USER}"
ENV WORK_DIR="${HOME_DIR}/hostcwd" \
    SRC_DIR="${HOME_DIR}/src" \
    PATH="${HOME_DIR}/.local/bin:${PATH}"

# configures locale
RUN apt update -qq > /dev/null \
    && DEBIAN_FRONTEND=noninteractive apt install -qq --yes --no-install-recommends \
    locales && \
    locale-gen en_US.UTF-8
ENV LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8"

# system requirements to build most of the recipes
RUN apt update -qq > /dev/null \
    && DEBIAN_FRONTEND=noninteractive apt install -qq --yes --no-install-recommends \
    apksigner \
    autoconf \
    automake \
    build-essential \
    ccache \
    cmake \
    gettext \
    git \
    libffi-dev \
    libltdl-dev \
    libssl-dev \
    libtool \
    openjdk-17-jdk \
    patch \
    pkg-config \
    python3-distutils \
    python3-pip \
    python3-setuptools \
    sudo \
    unzip \
    zip \
    zlib1g-dev

# prepares non root env
RUN useradd --create-home --shell /bin/bash ${USER}
# with sudo access and no password
RUN usermod -append --groups sudo ${USER}
RUN echo "%sudo ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER ${USER}
WORKDIR ${WORK_DIR}

# Clone buildozer
RUN git clone --depth 1 --branch $BUILDOZER_VERSION https://github.com/kivy/buildozer.git
WORKDIR ${WORK_DIR}/buildozer

# installs buildozer and dependencies
RUN pip3 install --user --upgrade "Cython<3.0" wheel pip setuptools .

ENTRYPOINT ["buildozer"]


FROM buildozer

COPY buildozer.spec ./buildozer.spec
COPY sudoku_solver ./sudoku_solver

RUN buildozer android release
RUN mv ./bin/sudoku_solver-1.0.0-arm64-v8a_armeabi-v7a-release-unsigned.apk ./bin/sudoku_solver.apk

COPY keystore/sudoku_solver.keystore ./sudoku_solver.keystore
RUN apksigner sign --ks-key-alias apk --ks sudoku_solver.keystore --ks-pass pass:$KEYSTORE_FILE_PASSWORD ./bin/sudoku_solver.apk
RUN apksigner verify ./bin/sudoku_solver.apk

EXPOSE 8000

CMD ["serve"]
