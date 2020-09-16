from conans import ConanFile, tools, AutoToolsBuildEnvironment
import pathlib
import os
import multiprocessing
from shutil import copyfile
import tempfile
import platform

class Ait(ConanFile):
    
    name = "ait"
    version = "2.2.0"

    git_url = "https://pm.bsc.es/gitlab/ompss-at-fpga/ait"
    git_clone_name = "ait_source"

    git_branch =  "ompss-at-fpga-release/2.2.0"

    options = {"python3":"ANY", "mode":"ANY", "backend":"ANY"}
    default_options = {"mode":"public", "backend":"all"}

    build_policy="missing"
    no_copy_source=True

    def configure(self):
        self.options.python3 = platform.python_version()

    def source(self):
        self.run("git clone -b {0} {1} {2} && cd {2} && git lfs install && git lfs fetch && git lfs pull".format(self.git_branch, self.git_url, self.git_clone_name))

    def build(self):
        pass

    def package(self):
        tempdir = tempfile.mkdtemp()
        tempdir2 = tempfile.mkdtemp()
        self.run("cp -r {4}/* {0} && cd {0}/ait_source && ./install.sh {1} {2} {3}".format(tempdir,tempdir2, str(self.options.mode), str(self.options.backend), self.source_folder))
        self.copy("*", src=tempdir2)
        self.run("cd {} && tar cf scripts.tar.gz scripts".format(self.package_folder))

    def package_info(self):
        self.env_info.path.append(self.package_folder)
        self.run("cd {} && tar xf scripts.tar.gz".format(self.package_folder))
