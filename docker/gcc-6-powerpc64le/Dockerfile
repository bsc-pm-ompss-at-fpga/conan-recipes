FROM conanio/gcc6

LABEL maintainer="Luis Martinez de Bartolome <luism@jfrog.com>"

ENV CC=powerpc64le-linux-gnu-gcc-6 \
    CXX=powerpc64le-linux-gnu-g++-6 \
    CMAKE_C_COMPILER=powerpc64le-linux-gnu-gcc-6 \
    CMAKE_CXX_COMPILER=powerpc64le-linux-gnu-g++-6 \
    STRIP=powerpc64le-linux-gnu-strip \
    RANLIB=powerpc64le-linux-gnu-ranlib \
    AS=powerpc64le-linux-gnu-as \
    AR=powerpc64le-linux-gnu-ar \
    LD=powerpc64le-linux-gnu-ld \
    FC=powerpc64le-linux-gnu-gfortran-6

COPY sources.list /etc/apt/sources.list
COPY ppc64le.list /etc/apt/sources.list.d/ppc64le.list

RUN sudo dpkg --add-architecture ppc64le \
    && sudo apt-get -qq update \
    && sudo apt-get install -y --no-install-recommends \
       ".*6.*powerpc64le-linux-gnu.*" \
    && sudo update-alternatives --install /usr/bin/powerpc64le-linux-gnu-gcc powerpc64le-linux-gnu-gcc /usr/bin/powerpc64le-linux-gnu-gcc-6 100 \
    && sudo update-alternatives --install /usr/bin/powerpc64le-linux-gnu-g++ powerpc64le-linux-gnu-g++ /usr/bin/powerpc64le-linux-gnu-g++-6 100 \
    && sudo update-alternatives --install /usr/bin/powerpc64le-linux-gnu-gcov powerpc64le-linux-gnu-gcov /usr/bin/powerpc64le-linux-gnu-gcov-6 100 \
    && sudo update-alternatives --install /usr/bin/powerpc64le-linux-gnu-gcov-dump powerpc64le-linux-gnu-gcov-dump /usr/bin/powerpc64le-linux-gnu-gcov-dump-6 100 \
    && sudo update-alternatives --install /usr/bin/powerpc64le-linux-gnu-gcov-tool powerpc64le-linux-gnu-gcov-tool /usr/bin/powerpc64le-linux-gnu-gcov-tool-6 100 \
    && sudo rm -rf /var/lib/apt/lists/* \
    && pip install -q --no-cache-dir conan conan-package-tools --upgrade \
    && conan profile new default --detect \
    && conan profile update settings.arch=armv8 default
