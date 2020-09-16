from conans import ConanFile, tools, AutoToolsBuildEnvironment
import pathlib
import os
import multiprocessing
from shutil import copyfile

class nanos5Proxy(ConanFile):
    
    name = "nanos5"
    version = "2.2.0"
    settings = "compiler", "arch"
    build_policy="always"
    options = {"target":"ANY"}
    default_options = {"target":"aarch64"} 

    def bashrun(self, command):
        self.run("bash -c \"{0}\"".format(command))

    def joincmd(self, command1, command2):
        return command1+" && "+command2

    def Nanos5InstallCommand(self):
        rarch = str(self.options.target)
        if rarch == "aarch64":
            rarch = "armv8"
        cmd = "cd {0} && ".format(self.build_folder)
        cmd = cmd + "conan install -s arch={0} ".format(rarch)
        cmd = cmd + " nanos5_internal/2.2.0@_/_"
        cmd = cmd + " --build=missing -g deploy "
        return cmd

    def package(self):
        self.bashrun(self.Nanos5InstallCommand())
        self.bashrun("rm {0}/papi/bin".format(self.build_folder))
        self.bashrun("cd {0} &&  cp -r nanos5_internal/* xtasks/* papi/* extrae/* {1} && cp {1}/lib/libxtasks.so* {1}/lib/performance/ && cp {1}/lib/libxtasks.so* {1}/lib/debug/ && cp {1}/lib/libxtasks.so* {1}/lib/instrumentation".format(self.build_folder, self.package_folder))
        self.bashrun("cd {0} &&  cp {1}/lib/libpapi.so* {1}/lib/performance/  && cp {1}/lib/libpapi.so* {1}/lib/debug && cp {1}/lib/libpapi.so* {1}/lib/instrumentation".format(self.build_folder, self.package_folder))

    def package_info(self):
        self.env_info.LD_LIBRARY_PATH.append(self.package_folder+"/lib")
        self.env_info.path.append(self.package_folder)