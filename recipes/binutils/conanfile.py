from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class BinutilsConan(ConanFile):
    name = "binutils"
    version = "2.31"
    description = "The GNU Binutils are a collection of binary tools"
    topics = ("conan", "bintuils", "utilities", "toolchain")
    url = "https://github.com/bincrafters/conan-binutils"
    homepage = "https://www.gnu.org/software/binutils/"
    license = "GPL-3.0-or-later"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "target": "ANY"}
    default_options = {"shared": False, "fPIC": True, "target": None}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    build_policy="missing"
    requires = "zlib/bsc"
    _autotools = None


    def source(self):
        source_url = "https://ftp.gnu.org/gnu/binutils/binutils-%s.tar.bz2" % self.version
        tools.get(source_url)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
        
        self._autotools = True

        host = None
        if str(self.settings.arch) == "armv8":
            host = "--host=aarch64-linux-gnu"
        else:
            host = "--host="+str(self.settings.arch)+"-linux-gnu"

        self.run("./configure {} {} {} {}".format(
            "--prefix={}".format(tools.unix_path(self.package_folder)),
            "--enable-shared",
            host,
            "--enable-install-libiberty"))
        return self._autotools
    


    def build(self):
        os.chdir(self._source_subfolder)
        self._configure_autotools()
        self.run("make -j")

    def package(self): 
        os.chdir(self._source_subfolder)
        self._configure_autotools()
        self.run("make install -j")


    def _create_tool_var(self, name, value):
        cross_prefix = str(self.options.target) + "-" if self.options.target else ""
        path = os.path.join(self.package_folder, "bin", cross_prefix + value)
        self.output.info("Appending %s env var with : %s" % (name, path))
        return path
