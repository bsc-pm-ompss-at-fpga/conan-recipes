from conans import ConanFile, tools, AutoToolsBuildEnvironment
import pathlib
import os
import multiprocessing
from shutil import copyfile

class help2man(ConanFile):
    name = "help2man"
    version = "1.47.16"
    settings = "os", "compiler", "build_type", "arch"

    git_clone_name = "help2man"
    filename = "help2man-1.47.16"
    fileext = ".tar.xz"
    url = "https://ftp.gnu.org/gnu/help2man/{}{}".format(filename,fileext)
    
    no_copy_source=True
    build_policy="missing"
    _autotools = None


    def source(self):
        self.run("wget {0} && tar xf {1}{2} && mv {1} {3} && rm {1}{2} ".format(self.url, self.filename, self.fileext, self.git_clone_name))


    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
        
        self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
        args =[
                "--prefix={}".format(tools.unix_path(self.package_folder)),
        ]
        host, build = None, None
        env_build_vars = self._autotools.vars
        env_build_vars['CFLAGS'] = '-Wno-error'
        self._autotools.configure(args=args, configure_dir=self.source_folder+"/%s"%self.git_clone_name, host=host, build=build, vars=env_build_vars)
        return self._autotools
        

    def build(self):
        autotools = self._configure_autotools()
        autotools.make()
     
    def package(self): 
        self.copy("COPYING*", src=self.source_folder, dst="licenses")
        autotools = self._configure_autotools()
        autotools.install()


    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self) 
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))



