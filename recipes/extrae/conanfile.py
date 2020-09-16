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
    requires = ["papi/6.0.0"]
    build_requires = ["boost/1.73.0", "binutils/2.31", "libxml2/bsc", "zlib/bsc"]
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
        

        print(self.deps_cpp_info["papi"].rootpath)
        self._autotools = True
        args =[
        "--without-mpi",
        "--without-unwind",
        "--without-dyninst",
        "--datarootdir={}".format(tools.unix_path(self._datarootdir)),
        "--prefix={}".format(tools.unix_path(self.package_folder)),
        '--with-papi={} '.format(self.deps_cpp_info["papi"].rootpath),
        '--with-libz={}'.format(self.deps_cpp_info["zlib"].rootpath),
        '--with-binutils={}'.format(self.deps_cpp_info["binutils"].rootpath),
        ]
        
        if str(self.settings.arch) == "armv8":
            args.append("--enable-arm64")
            args.append("--host=aarch64-linux-gnu")
        else:
            args.append("--host="+str(self.settings.arch)+"-linux-gnu")

        print(' '.join(map(str, args)) )
        self.run("LD_LIBRARY_PATH={} ./configure {}".format(self.deps_cpp_info["zlib"].rootpath+"/lib",' '.join(map(str, args)) ), run_environment=True)
        return self._autotools
        

    def build(self):
        os.chdir(self.build_folder+"/"+self.git_clone_name)
        if "PKGM4" in os.environ:
            self.run("cd {0}/{1} &&  autoreconf -fiv -I{2}".format(self.build_folder, self.git_clone_name, os.environ["PKGM4"])) 
        else:
            self.run("cd {0}/{1} &&  autoreconf -fiv".format(self.build_folder, self.git_clone_name)) 
        self._configure_autotools()
        self.run("cd {}  && make -j".format(self.build_folder+"/"+self.git_clone_name))
     
    def package(self):
        os.chdir(self.build_folder+"/"+self.git_clone_name)
        autotools = self._configure_autotools()
        self.run("cd {}  && make install".format(self.build_folder+"/"+self.git_clone_name))


    def package_info(self):
        self.env_info.LD_LIBRARY_PATH.append(self.package_folder+"/lib")
