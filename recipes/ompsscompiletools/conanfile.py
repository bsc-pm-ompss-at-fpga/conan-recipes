
from conans import ConanFile
import os

class ompsscompiletools(ConanFile):
    name = "compiletools"
    version = "bsc"
    settings = "compiler", "arch", "arch_build"
    requires = ["autoconf/2.69", "automake/1.16.2", "libtool/2.4.6", "pkg-config_installer/0.29.2@bincrafters/stable", "make/4.2.1", "flex/2.6.4", "bison/3.5.3", "gperf/3.1"]

    def package_info(self):
        self.env_info.PKGM4=self.deps_cpp_info["pkg-config_installer"].rootpath+"/share/aclocal"
 
