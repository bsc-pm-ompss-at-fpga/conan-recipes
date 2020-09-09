from conans import ConanFile, tools, AutoToolsBuildEnvironment
import pathlib
import os
import multiprocessing
from shutil import copyfile

class Extrae(ConanFile):
    name = "extrae"
    version = "2.2.0"

    git_clone_name = "extrae"
    git_url = "https://pm.bsc.es/gitlab/ompss-at-fpga/extrae"
    git_branch =  "ompss-at-fpga-release/2.2.0"
    settings = "os", "compiler", "build_type", "arch"
    build_policy="missing"
    requires = ["papi/5.7.0"]
    build_requires = ["boost/1.73.0", "binutils/2.32", "libxml2/2.9.10"]
    build_policy="missing"

    _autotools = None


    def requirements(self):
        self.options["boost"].header_only = True

    def source(self):
        self.run("git clone -b {0} {1} {2}".format(self.git_branch, self.git_url, self.git_clone_name))


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
        '--enable-arm64'
        '--with-papi={}'.format(self.deps_cpp_info["papi"].rootpath),
        '--with-binutils={}'.format(self.deps_cpp_info["binutils"].rootpath),
        '--without-mpi',
        '--without-unwind',
        '--without-dyninst'
        ]

                
        self._autotools.configure(args=args, configure_dir=self.source_folder+"/%s"%self.git_clone_name)
        return self._autotools
        

    def build(self):
        if "PKGM4" in os.environ:
            self.run("cd {0}/{1} &&  autoreconf -fiv -I{2}".format(self.source_folder, self.git_clone_name, os.environ["PKGM4"])) 
        else:
            self.run("cd {0}/{1} &&  autoreconf -fiv".format(self.source_folder, self.git_clone_name)) 
        autotools = self._configure_autotools()
        autotools.make()
     
    def package(self): 
        autotools = self._configure_autotools()
        autotools.install()
        self.run("echo {0} > {0}/first_package_path".format(self.package_folder))


    def package_info(self):
        self.env_info.NANOS6_INCLUDE=self.package_folder+"/include"
        self.env_info.NANOS6_HOME= self.package_folder
        self.env_info.NANOS6_LIBS=self.package_folder+"/lib"

