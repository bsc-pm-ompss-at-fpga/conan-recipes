from conans import ConanFile, tools, AutoToolsBuildEnvironment
import pathlib
import os
import multiprocessing
from shutil import copyfile
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

class OmpSs2Conan(ConanFile):
    name = "ompss2"
    version = "2019.6"
    settings = "compiler", "arch", "arch_target"
    options = {"version": "ANY"}
    default_options = {"version": "2019.6"}

    def requirements(self):
        self.requires("mcxx/latest")

    def configure(self):
        self.options["mcxx"].nanos6 = self.options.version

if __name__ == "__main__":
    os.system('conan create . ompss2/2019.6@_/_')
    os.system('conan upload --all ompss2/2019.6 -r demo') 
