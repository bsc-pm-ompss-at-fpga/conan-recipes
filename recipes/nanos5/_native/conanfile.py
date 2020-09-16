
from conans import ConanFile, tools, AutoToolsBuildEnvironment
import pathlib
import os
import multiprocessing
from shutil import copyfile
import platform

class Nanos5Conan(ConanFile):
    name = "nanos5_internal"
    version = "2.2.0"
    git_clone_name = "nanos5_source"
    git_url = "https://pm.bsc.es/gitlab/ompss-at-fpga/nanox"

    settings = "os", "compiler", "build_type", "arch"

    requires = ["xtasks/2.2.0-stub", "extrae/2.2.0"]
    build_policy="missing"
    _autotools = None


    def source(self):
        self.run("git clone -b ompss-at-fpga-release/2.2.0 {0} {1}".format(self.git_url, self.git_clone_name))


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
        '--with-xtasks=%s' % self.deps_cpp_info["xtasks"].rootpath,
        '--with-extrae={}'.format(self.deps_cpp_info["extrae"].rootpath)
        ]
        self._autotools.cxx_flags.append("-Wno-unused-variable")
        
        if(str(self.settings.arch) == platform.machine()):
            self._autotools.configure(args=args, configure_dir=self.source_folder+"/%s"%self.git_clone_name, host=False, build=False, target=False)
        else:
            self._autotools.configure(args=args, configure_dir=self.source_folder+"/%s"%self.git_clone_name)

        return self._autotools
        

    def build(self):
        if "PKGM4" in os.environ:
            self.run("cd {0}/{1} &&  autoreconf -fiv -I{2}".format(self.build_folder, self.git_clone_name, os.environ["PKGM4"])) 
        else:
            self.run("cd {0}/{1} &&  autoreconf -fiv".format(self.build_folder, self.git_clone_name)) 
        autotools = self._configure_autotools()
        autotools.make()
     
    def package(self): 
        autotools = self._configure_autotools()
        autotools.install()
        self.run("echo {0} > {0}/first_package_path".format(self.package_folder))


    def package_info(self):
        self.cpp_info.libs = []  # not propagate linking...
        self.cpp_info.system_libs = []  # System libs to link again
        self.cpp_info.sharedlinkflags = [] 
        self.cpp_info.exelinkflags = [] 
        self.env_info.NANOS6_INCLUDE=self.package_folder+"/include"
        self.env_info.NANOS6_HOME= self.package_folder
        self.env_info.NANOS6_LIBS=self.package_folder+"/lib"
        self.env_info.LD_LIBRARY_PATH.append(self.package_folder+"/lib")


