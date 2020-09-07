
from conans import ConanFile
import os

class compile_tools(ConanFile):
    name = "compiletools"
    version = "1.0"
    settings = "compiler", "arch", "arch_build"
    requires = ["autoconf/2.69", "automake/1.16.2", "libtool/2.4.6", "pkg-config_installer/0.29.2@bincrafters/stable", "make/4.2.1", "flex/2.6.4", "bison/3.7.1", "gperf/3.1"]

    def package_info(self):
        self.env_info.PKGM4=self.deps_cpp_info["pkg-config_installer"].rootpath+"/share/aclocal"

if __name__ == "__main__":
    os.system('conan create . compiletools/1.0@_/_')
    os.system('conan upload --all compiletools/1.0@_/_ -r demo') 
