from conans import ConanFile, AutoToolsBuildEnvironment, tools
import pathlib, os, multiprocessing

class HwlocConan(ConanFile):
    name = "gcc9"
    version = "aarch64"
    license = "https://raw.githubusercontent.com/crosstool-ng/crosstool-ng/master/COPYING"
    author = "crosstool-ng"
    url = "https://github.com/crosstool-ng/crosstool-ng"
    description = "Build toolchains"
    topics = ("hpc", "parallelism", "hardware")
    settings = "os", "compiler", "build_type", "arch"
    _autotools = None
    build_policy="missing"
    build_requires= ["crosstool/github"]



    def source(self):
        self.run("wget https://raw.githubusercontent.com/Rucadi/ompssdevfpga/master/arm64.config")
        self.run("mv arm64.config .config")

    def package(self): 
        os.environ["CT_EXPERIMENTAL"] = "y"
        os.environ["CT_ALLOW_BUILD_AS_ROOT"] = "y"
        os.environ["CT_ALLOW_BUILD_AS_ROOT_SURE"] = "y"
        os.environ["CT_TOP_DIR"] = self.build_folder
        os.environ["CT_PREFIX_DIR"] = self.package_folder
        os.environ["CT_TARGET"] = self.package_folder
        self.run("echo $CT_PREFIX_DIR")
        self.run("ct-ng build")

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "aarch64-unknown-linux-gnu/bin"))
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
 

if __name__ == "__main__":
    os.system('conan create . hwloc/github@_/_')
    os.system('conan upload --all hwloc/github -r ompss') 
