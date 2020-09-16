from conans import ConanFile, tools, AutoToolsBuildEnvironment, VisualStudioBuildEnvironment
from contextlib import contextmanager
import glob
import os


class LibzConan(ConanFile):
    name = "zlib"
    version = "bsc"
    url = "https://github.com/conan-io/conan-center-index"
    description = ("A Massively Spiffy Yet Delicately Unobtrusive Compression Library "
                   "(Also Free, Not to Mention Unencumbered by Patents)")
    topics = ("conan", "zlib", "compression")
    homepage = "https://zlib.net"
    license = "Zlib"
    settings = "os", "arch", "compiler", "build_type"
   
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    build_policy="missing"
    _autotools = None

    def source(self):
        source_url = "https://zlib.net/zlib-1.2.11.tar.gz"
        tools.get(source_url)
        extracted_dir = "zlib-1.2.11"
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
        
        self._autotools = True
        host = None
        if str(self.settings.arch) == "armv8":
            host = "aarch64-linux-gnu"
        else:
            host = str(self.settings.arch)+"-linux-gnu"

        self.run("CHOST={}  ./configure  {} ".format(host,
            "--prefix={}".format(tools.unix_path(self.package_folder)),
            ))
        return self._autotools
    


    def build(self):
        os.chdir(self._source_subfolder)
        self._configure_autotools()
        self.run("make -j all")

    def package(self): 
        os.chdir(self._source_subfolder)
        self._configure_autotools()
        self.run("make install  -j ")

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH env var with : " + bindir)
        self.env_info.PATH.append(bindir)
        self.env_info.LD_LIBRARY_PATH.append(self.package_folder+"/lib")
