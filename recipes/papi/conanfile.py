from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

class PapiConan(ConanFile):
    name = "papi"
    version = "6.0.0"
    license = "MIT"
    url = "https://bitbucket.org/icl/papi.git"
    description = "The Performance Application Programming Interface (PAPI) provides tool designers and application engineers with a consistent interface and methodology for the use of low-level performance counter hardware"
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        self.run("git clone -b papi-6-0-0-t https://bitbucket.org/icl/papi.git")

    def build(self):
        os.chdir("papi/src")
        autotools = AutoToolsBuildEnvironment(self)
        autotools.fpic = True
        vars = autotools.vars
        vars["LIBS"] = "-ldl"
        env_build_vars = autotools.vars
        env_build_vars['CFLAGS'] = '-Wno-error'
        env_build_vars['CPPFLAGS'] = '-Wno-error'

        args=[
            "--prefix={}".format(tools.unix_path(self.package_folder)),
            "--with-ffsll",
            "--host=aarch64-linux-gnu",
            "--with-arch=aarch64",
            "--with-CPU=arm",
            "--with-walltimer=cycle",
            "-with-tls=__thread",
            "--with-virtualtimer=perfctr",
            "--with-perf-events"
             ]
        autotools.configure(args=args, vars=env_build_vars)
        autotools.make(vars=vars)

    def package(self):
        self.copy("*.h", dst="include", src="papi/src")
        self.copy("*.a", dst="lib", src="papi/src", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["papi"]