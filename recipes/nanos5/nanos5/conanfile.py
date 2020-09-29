from conans import ConanFile, tools, AutoToolsBuildEnvironment
import pathlib
import os
import multiprocessing
from shutil import copyfile
import subprocess

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
        cmd = "cd {0} && ".format(self.package_folder)
        cmd = cmd + "conan install -s arch={0} ".format(rarch)
        cmd = cmd + " nanos5_internal/2.2.0@_/_"
        cmd = cmd + " --build=missing -g txt"
        return cmd


    def package(self):
        self.bashrun(self.Nanos5InstallCommand())
        command = "cd {} && cat conanbuildinfo.txt | grep rootpath_nanos5_internal -A1 | tail -n 1  | cat > nanos5_internal_path".format(self.package_folder)
        self.run(command)

    def package_info(self):
        self.env_info.path.append(self.package_folder)
