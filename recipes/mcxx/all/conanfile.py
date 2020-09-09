from conans import ConanFile, tools, AutoToolsBuildEnvironment
from conans.errors import ConanInvalidConfiguration
from conans import tools

import pathlib
import os
import multiprocessing
from shutil import copyfile
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
import re

import subprocess

class McxxConan(ConanFile):
    git_clone_name = "mcxx_source"
    name = "mcxx"
    version = "2.2.0"
    settings = "compiler", "arch", "arch_build"
    
    git_url = "https://pm.bsc.es/gitlab/mercurium/mcxx"

    build_requires = ["sqlite3/3.30.1"]
    build_policy="missing"

    options = {"target":"ANY", "nanos6":"ANY", "nanos5":"ANY", "papi": [True, False], "cluster": [True, False]}
    default_options = {"nanos6":"2019.6", "target":"aarch64",  "nanos5":"latest", "papi": False, "cluster": False}

    _autotools = None

    def requirements(self):
        if self.options.nanos6 != "None":
            self.requires("nanos6/latest")


        print(self.options.nanos5)
        if self.options.nanos5 != "None":
            self.requires("nanos5/2.2.0")

    def configure(self):
        if self.options.target != "None":
            if self.options.target == "aarch64":
                self.options["nanos6"].target = "armv8"
                self.options["nanos5"].target = "armv8"
        else:
            self.options["nanos6"].target = self.settings.arch_build
            self.options["nanos5"].target = self.settings.arch_build

    def source(self):
        self.run("git clone {} {} ".format(self.git_url, self.git_clone_name))

    @property
    def _datarootdir(self):
        return os.path.join(self.package_folder, "share")

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
        
        self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
        env_build_vars = self._autotools.vars
        env_build_vars["LIBS"] = env_build_vars["LIBS"] + ' -lstdc++'
        args =[
        "--datarootdir={}".format(tools.unix_path(self._datarootdir)),
        "--prefix={}".format(tools.unix_path(self.package_folder)),
        'sqlite3_CFLAGS=-I%s'%self.deps_cpp_info["sqlite3"].rootpath+"/include",
        'sqlite3_LIBS=-L'+self.deps_cpp_info["sqlite3"].rootpath+"/lib",
        ]

        if self.options.nanos6 != "None":
            args.append("--enable-ompss-2")
            args.append("--with-nanos6={}".format(self.deps_cpp_info["nanos6"].rootpath))
        
        if self.options.nanos5 != "None":
            args.append("--enable-ompss")
            args.append("--enable-tl-openmp-nanox")
            args.append("--with-nanox={}".format(self.deps_cpp_info["nanos5"].rootpath))


        if self.options.target != "None":
            args.append("--target="+str(self.options.target)+"-linux-gnu")

        self._autotools.configure(args=args, configure_dir=self.source_folder+"/%s"%self.git_clone_name, vars=env_build_vars)
        return self._autotools
        

    def build(self):
        self.run("cd "+self.build_folder+ "/"+self.git_clone_name+" && autoreconf -fiv")
        autotools = self._configure_autotools()
        autotools.make()
     
    def package(self): 
        autotools = self._configure_autotools()
        autotools.install()
        self.run("echo {0} > {0}/first_package_path".format(self.package_folder))


    def package_info(self):
        self.cpp_info.libs = []#not propagate linking...
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
        if self.options.target != "None":
            self.env_info.MCC=self.package_folder+"/bin/{}mcc".format(str(self.options.target)+"-linux-gnu-")
            self.env_info.MCXX=self.package_folder+"/bin/{}mcxx".format(str(self.options.target)+"-linux-gnu-")
        else:
            self.env_info.MCC=self.package_folder+"/bin/mcc"
            self.env_info.MCXX=self.package_folder+"/bin/mcxx"

        #with open(self.deps_cpp_info["nanos6"].rootpath+'/first_package_path') as f: 
        #    first_line_nanos6 = f.readline() 
        file_to_edit = "{0}/share/mcxx/config.d/10.config.omp-base".format(self.package_folder)
        file_to_edit2 = "{0}/share/mcxx/config.d/50.config.omp.mercurium".format(self.package_folder)
        file_to_edit3 = "{0}/share/mcxx/config.d/40.config.cuda".format(self.package_folder)

        #self.run("sed -i 's+{0}+{1}+g' {2}".format(first_line_nanos6.rstrip(), self.deps_cpp_info["nanos6"].rootpath, file_to_edit))
        seek_home = "cat {} | grep 'preprocessor_options = -I' | head -1 | cut -d 'I' -f2- | cut -f1 -d'.' |  sed -e 's/^[[:space:]]*//'".format(file_to_edit)
        home_dir =  str(subprocess.check_output("conan config home", shell=True)).replace(".conan","").replace("b'","").replace("\\n'","").replace("/","\\/")
        home_to_replace  =  str(subprocess.check_output(seek_home, shell=True)).replace("b'","").replace("\\n'","").replace("/","\\/")

        self.run("bash -c \"sed -i 's/{}/{}/g'  {}  \"".format(home_to_replace, home_dir, file_to_edit))
        self.run("bash -c \"sed -i 's/{}/{}/g'  {}  \" ".format(home_to_replace, home_dir, file_to_edit2))
        self.run("bash -c \"sed -i 's/{}/{}/g'  {}  \" ".format(home_to_replace, home_dir, file_to_edit3))

        

if __name__ == "__main__":
    os.system('conan create . mcxx/latest@_/_')
    os.system('conan upload --all  mcxx/latest -r demo') 