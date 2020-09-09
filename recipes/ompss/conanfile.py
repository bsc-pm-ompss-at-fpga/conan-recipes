from conans import ConanFile, tools, AutoToolsBuildEnvironment
import pathlib
import os
import multiprocessing
from shutil import copyfile

class OmpSs(ConanFile):
    
    name = "ompss_fpga"
    version = "2.2.0"
    settings = "compiler", "arch"
    build_policy="always"
    requires = ["ait/2.2.0", "mcxx/latest"]
    
    options = {"target":"ANY"}
    default_options = {"target":"aarch64"} 

    def requirements(self):
        self.options["mcxx"].nanos6=None
        self.options["mcxx"].target=self.options.target

