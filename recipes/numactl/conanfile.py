from conans import ConanFile, AutoToolsBuildEnvironment, tools
import pathlib
import multiprocessing
import os
class NumactlConan(ConanFile):
    name = "numactl"
    version = "2.0.13"
    description = "Simple NUMA policy support. It consists of a numactl program to run other programs with a specific NUMA policy and a libnuma shared library to set NUMA policy in applications."
    topics = ("hpc", "parallelism", "hardware")
    url = "https://github.com/numactl/numactl"

    license = "GPL-2.0 license"
    author = "Author: Andi Kleen, SUSE Labs Cliff Wickman (cpw@sgi.com), Christoph Lameter (clameter@sgi.com) and Lee Schermerhorn (lee.schermerhorn@hp.com)."
   

    settings = "os", "compiler", "build_type", "arch"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    _autotools = None
    build_policy="missing"
    
    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-"+ self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
        
        self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
        args =[
        "--prefix={}".format(tools.unix_path(self.package_folder)),
        ]
        self._autotools.configure(args=args, configure_dir=self.build_folder+"/"+self._source_subfolder)
        return self._autotools
        
    def _autogen(self):
        self.run("cd {}".format(self._source_subfolder)+" && ./autogen.sh")

    def build(self):
        self._autogen()
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

