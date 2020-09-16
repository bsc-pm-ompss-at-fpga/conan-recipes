from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

class PapiConan(ConanFile):
    name = "papi"
    version = "6.0.0"
    license = "MIT"
    url = "https://bitbucket.org/icl/papi.git"
    description = "The Performance Application Programming Interface (PAPI) provides tool designers and application engineers with a consistent interface and methodology for the use of low-level performance counter hardware"
    settings = "os", "compiler", "build_type", "arch"
    _autotools = None
    build_policy="missing"

    def source(self):
        self.run("git clone -b papi-6-0-0-t https://bitbucket.org/icl/papi.git")


    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
        
        self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
        args=[
            "--prefix={}".format(tools.unix_path(self.package_folder)),
            "--with-walltimer=cycle",
            "--with-tls=__thread",
            "--with-virtualtimer=perfctr ",
            "--with-perf-events",
            "--with-tests="
             ]

        env_build_vars =  self._autotools.vars
        env_build_vars['CFLAGS'] = '-Wno-error'
        env_build_vars['CPPFLAGS'] = '-Wno-error'

        if str(self.settings.arch)=='armv8':
            args.append("--with-arch=aarch64")
            args.append("--with-CPU=arm")
        elif str(self.settings.arch)=='x86_64':
            args.append("--with-arch=x86_64")

        args.append("--with-ffsll")

        self._autotools.configure(args=args, vars=env_build_vars)

        return self._autotools
        

    def build(self):
        os.chdir("papi/src")
        autotools = self._configure_autotools()
        autotools.make()

    def package(self): 
        os.chdir("papi/src")
        autotools = self._configure_autotools()
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = ["papi"]
        self.env_info.LD_LIBRARY_PATH.append(self.package_folder+"/lib")
