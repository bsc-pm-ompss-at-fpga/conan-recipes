from conans import ConanFile, AutoToolsBuildEnvironment, tools
import pathlib
import multiprocessing
import os
class NumactlConan(ConanFile):
    name = "numactl"
    version = "github"
    license = "GPL-2.0 license"
    author = "Author: Andi Kleen, SUSE Labs Cliff Wickman (cpw@sgi.com), Christoph Lameter (clameter@sgi.com) and Lee Schermerhorn (lee.schermerhorn@hp.com)."
    url = "https://github.com/numactl/numactl"
    description = "Simple NUMA policy support. It consists of a numactl program to run other programs with a specific NUMA policy and a libnuma shared library to set NUMA policy in applications."
    topics = ("hpc", "parallelism", "hardware")
    options = {"shared": [True, False]}
    default_options = {"shared": False}

    settings = "os", "compiler", "build_type", "arch"
    _autotools = None
    build_policy="missing"
    
    @property
    def _datarootdir(self):
        return os.path.join(self.package_folder, "bin", "share")

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
        
        self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
        args =[
        "--datarootdir={}".format(tools.unix_path(self._datarootdir)),
        "--prefix={}".format(tools.unix_path(self.package_folder)),
        ]
        host, build = None, None
        self._autotools.configure(args=args, configure_dir=self.source_folder, host=host, build=build)
        return self._autotools
        

    def source(self):
        self.run("git clone https://github.com/numactl/numactl tmp_src_numactl && mv tmp_src_numactl/* . && rm -rf tmp_src_numactl")
        self.run("./autogen.sh")


    def build(self):
        autotools = self._configure_autotools()
        autotools.make()

    def package(self): 
        self.copy("COPYING*", src=self.source_folder, dst="licenses")
        autotools = self._configure_autotools()
        autotools.install()
        self.run("cd {0}/lib && rm *.la ".format(self.package_folder))


    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self) 
        self.env_info.PKG_CONFIG_PATH.append(self.package_folder+"/lib/pkgconfig")
        self.env_info.LD_LIBRARY_PATH.append(self.package_folder+"/lib")


if __name__ == "__main__":
    os.system('conan create . numactl/github@_/_')
    os.system('conan upload --all numactl/github -r demo') 