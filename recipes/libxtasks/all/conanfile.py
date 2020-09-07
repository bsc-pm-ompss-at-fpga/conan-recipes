from conans import ConanFile, tools, AutoToolsBuildEnvironment
import pathlib
import os
import multiprocessing
from shutil import copyfile

class Nanos6Conan(ConanFile):
    name = "xtasks"
    version = "2.2.0"
    git_clone_name = "xtasks"
    git_url = "https://pm.bsc.es/gitlab/ompss-at-fpga/xtasks"

    settings = "os", "compiler", "arch"
    options = {"target":"ANY"}
    default_options = {"target":"armv8"}


    def source(self):
        self.run("git clone  {0} {1}".format(self.git_url, self.git_clone_name))

    def build(self):
        if str(self.options.target) == "armv8":
            crosscompile = "aarch64-linux-gnu-"  
        self.run("cd {}/src  && CROSS_COMPILE={} PREFIX={} make install".format(self.source_folder+"/"+self.git_clone_name, crosscompile, self.package_folder))
        self.run("cd {}/lib  && cp libxtasks-stub.so libxtasks.so".format(self.package_folder))


if __name__ == "__main__":
    os.system('conan create . xtasks/2.2.0@_/_ -s arch=armv8')
    os.system('conan upload --all xtasks/2.2.0@_/_ -r demo') 
