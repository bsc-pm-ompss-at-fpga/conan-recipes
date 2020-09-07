from conans import ConanFile, tools, AutoToolsBuildEnvironment
import pathlib
import os
import multiprocessing
from shutil import copyfile

class Nanos6Conan(ConanFile):
    name = "binutils"
    version = "github"
    settings = "os", "compiler", "build_type", "arch"

    url = "git://sourceware.org/git/binutils-gdb.git"
    git_clone_name = "binutils_github"

    no_copy_source=True
    build_policy="missing"
    _autotools = None


    def source(self):
        pass#self.run("norm -rf "+self.git_clone_name+" && git clone %s "%self.url+self.git_clone_name)


    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
        
        self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
        args =[
                "--prefix={}".format(tools.unix_path(self.package_folder)),
                '--target=aarch64-linux',
                '--disable-multilib', 
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


if __name__ == "__main__":
    os.system('conan create . binutils/github@_/_')
    os.system('conan upload --all binutils/github -r ompss') 
