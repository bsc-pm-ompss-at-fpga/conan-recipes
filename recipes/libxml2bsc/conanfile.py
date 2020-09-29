from conans import ConanFile, tools, AutoToolsBuildEnvironment, VisualStudioBuildEnvironment
from contextlib import contextmanager
import glob
import os


class Libxml2Conan(ConanFile):
    name = "libxml2"
    version = "bsc"
    url = "https://github.com/conan-io/conan-center-index"
    description = "libxml2 is a software library for parsing XML documents"
    topics = ("XML", "parser", "validation")
    homepage = "https://xmlsoft.org"
    license = "MIT"
    settings = "os", "arch", "compiler", "build_type"
   
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    build_policy="missing"
    requires = ["zlib/bsc", "lzma/5.2.4@bincrafters/stable"]
    _autotools = None

    def configure(self):
        self.options["lzma"].shared = True


    def source(self):
        source_url = "https://gitlab.gnome.org/GNOME/libxml2/-/archive/v2.9.8/libxml2-v2.9.8.tar.gz"
        tools.get(source_url)
        extracted_dir = "libxml2-v2.9.8"
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
        
        self._autotools = True

        if "PKGM4" in os.environ:
            self.run("mkdir m4 && autoreconf -fiv -I{}".format(os.environ["PKGM4"].rstrip())) 
        else:
            self.run("mkdir m4 && autoreconf -fiv") 
        host = None

        if str(self.settings.arch) == "armv8":
            host = "--host=aarch64-linux-gnu"
        else:
            host = "--host="+str(self.settings.arch)+"-linux-gnu"

        self.run("./configure {} {} {} {} {}".format(
            "--prefix={}".format(tools.unix_path(self.package_folder)),
            "--without-python",
             "--with-zlib={}".format(self.deps_cpp_info["zlib"].rootpath),
             "--with-lzma={}".format(self.deps_cpp_info["lzma"].rootpath),
            host))
        return self._autotools
    


    def build(self):
        os.chdir(self._source_subfolder)
        self._configure_autotools()
        self.run("make -j")

    def package(self): 
        os.chdir(self._source_subfolder)
        self._configure_autotools()
        self.run("make install -j")
        self.run("cd {} && rm -rf *.la".format(self.package_folder+"/lib"))


    def _create_tool_var(self, name, value):
        cross_prefix = str(self.options.target) + "-" if self.options.target else ""
        path = os.path.join(self.package_folder, "bin", cross_prefix + value)
        self.output.info("Appending %s env var with : %s" % (name, path))
        return path

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH env var with : " + bindir)
        self.env_info.PATH.append(bindir)
        self.env_info.LD_LIBRARY_PATH.append(self.package_folder+"/lib")
