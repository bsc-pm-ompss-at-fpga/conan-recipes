# Conan Repo

CONAN_BUILD_POLICY=missing CONAN_DOCKER_IMAGE_SKIP_PULL=1 CONAN_GCC_VERSIONS=9 CONAN_ARCHS=ppc64le  CONAN_PIP_COMMAND=pip3 CONAN_USE_DOCKER=1  python3 build.py 

Requirements
------------

patchelf

   $ sudo apt-get install patchelf

git-lfs

   https://git-lfs.github.com
   $ sudo apt-get install git-lfs

Conan

   https://conan.io/downloads.html
   sudo apt install conan-ubuntu-64_1_30_2.deb
