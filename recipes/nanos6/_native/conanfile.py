from conans import ConanFile, tools, AutoToolsBuildEnvironment
import pathlib
import os
import multiprocessing
from shutil import copyfile

class Nanos6Conan(ConanFile):
    name = "nanos6_internal"
    version = "2019.6"

    git_clone_name = "nanos6_source"
    git_url = "https://github.com/bsc-pm/nanos6"
    git_branch =  "github-release-2019.06-fixes"
    settings = "os", "compiler", "build_type", "arch"

    requires = ["hwloc/github", "numactl/github"] 
    build_requires = ["boost/1.73.0"]
    build_policy="missing"

    options = {"papi": [True, False], "cluster": [True, False]}
    default_options = {"papi": False, "cluster": False}

    _autotools = None

    def requirements(self):
        self.options["boost"].header_only = True
        if self.options.papi:
            self.requires("papi/5.7.0")

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
        '--with-libnuma=%s' % self.deps_cpp_info["numactl"].rootpath,
        '--with-boost=%s' % self.deps_cpp_info["boost"].rootpath,
        'hwloc_CFLAGS=-I%s'%self.deps_cpp_info["hwloc"].rootpath+"/include",
        'hwloc_LIBS=-L'+self.deps_cpp_info["hwloc"].rootpath+"/lib",
        '--with-symbol-resolution=ifunc'
        ]

        if(self.options.papi):
            args.append("--with-papi={0}".format(self.deps_cpp_info["papi"].rootpath))
        if(self.options.cluster):
            args.append("--enable-execution-workflow")
            args.append("--enable-cluster")
            
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
        self.cpp_info.libs = []  # not propagate linking...
        self.cpp_info.system_libs = []  # System libs to link again
        self.cpp_info.sharedlinkflags = [] 
        self.cpp_info.exelinkflags = [] 
        self.env_info.NANOS6_INCLUDE=self.package_folder+"/include"
        self.env_info.NANOS6_HOME= self.package_folder
        self.env_info.NANOS6_LIBS=self.package_folder+"/lib"


if __name__ == "__main__":
    os.system('conan create . nanos6_internal/2019.6@_/_')
    os.system('conan upload --all nanos6_internal/2019.6@_/_ -r demo') 
