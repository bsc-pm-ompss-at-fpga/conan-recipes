from conans import ConanFile, AutoToolsBuildEnvironment, tools
import pathlib, os, multiprocessing

class HwlocConan(ConanFile):
    name = "crosstool"
    version = "github"
    license = "https://raw.githubusercontent.com/crosstool-ng/crosstool-ng/master/COPYING"
    author = "crosstool-ng"
    url = "https://github.com/crosstool-ng/crosstool-ng"
    description = "Build toolchains"
    topics = ("hpc", "parallelism", "hardware")
    settings = "os", "compiler", "build_type", "arch"
    _autotools = None
    build_policy="missing"
    def source(self):
        self.run("git clone https://github.com/crosstool-ng/crosstool-ng ct-ng && mv ct-ng/* . && rm -rf ct-ng")
        self.run("./bootstrap")


    @property
    def _datarootdir(self):
        return os.path.join(self.package_folder, "bin", "share")

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
        
        self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
        args =[
        "--datarootdir={}".format(tools.unix_path(self._datarootdir)),
        "--prefix={}".format(tools.unix_path(self.package_folder)),
        ]
        host, build = None, None
        self._autotools.configure(args=args, configure_dir=self.source_folder, host=host, build=build)
        return self._autotools
        
    def build(self):
        autotools = self._configure_autotools()
        autotools.make()

    def package(self): 
        autotools = self._configure_autotools()
        autotools.install()


    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
 

if __name__ == "__main__":
    os.system('conan create . hwloc/github@_/_')
    os.system('conan upload --all hwloc/github -r ompss') 
