from conans import ConanFile, tools, AutoToolsBuildEnvironment
import pathlib
import os
import multiprocessing
from shutil import copyfile

class nanos5Proxy(ConanFile):
    
    name = "nanos5"
    version = "latest"
    settings = "compiler", "arch"
    build_policy="always"
    options = {"target":"ANY"}
    default_options = {"target":"armv8"} 

    def bashrun(self, command):
        self.run("bash -c \"{0}\"".format(command))

    def joincmd(self, command1, command2):
        return command1+" && "+command2

    def Nanos6InstallCommand(self):
        cmd = "cd {0} && ".format(self.build_folder)
        cmd = cmd + "conan install -s arch={0} ".format(str(self.options.target))
        cmd = cmd + " nanos5_internal/fpga@_/_"
        cmd = cmd + " --build=missing -g deploy "
        return cmd

    def package(self):
        self.bashrun(self.Nanos6InstallCommand())
        self.bashrun("cd {} && cp -r nanos5_internal/* xtasks/* ait/* {}".format(self.build_folder, self.package_folder))
        self.bashrun("echo {0} > {0}/first_package_path".format(self.package_folder))

    def package_info(self):
        self.env_info.LD_LIBRARY_PATH.append(self.package_folder+"/lib")
        self.env_info.path.append(self.package_folder)

if __name__ == "__main__":
    os.system('conan create . nanos5/latest@_/_ ')
    os.system('conan upload  nanos5/latest@_/_ -r demo') 
