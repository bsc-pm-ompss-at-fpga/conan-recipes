from conans import ConanFile, tools, AutoToolsBuildEnvironment
import pathlib
import os
import multiprocessing
from shutil import copyfile
import tempfile
class Ait(ConanFile):
    
    name = "ait"
    version = "2.2.0"

    git_url = "https://pm.bsc.es/gitlab/ompss-at-fpga/ait"
    git_clone_name = "ait_source"

    git_branch =  "ompss-at-fpga-release/2.2.0"

    options = {"mode":"ANY", "backend":"ANY"}
    default_options = {"mode":"public", "backend":"all"}

    build_policy="missing"

    def source(self):
        self.run("git clone -b {0} {1} {2} && cd {2} && git lfs install && git lfs fetch && git lfs pull".format(self.git_branch, self.git_url, self.git_clone_name))

    def build(self):
        tempdir = tempfile.mkdtemp()
        self.run("cp -r * {0} && cd {0}/ait_source && ./install.sh {1} {2} {3}".format(tempdir,self.package_folder, str(self.options.mode), str(self.options.backend)))

    def package(self):
        pass

    def package_info(self):
        self.env_info.path.append(self.package_folder)
