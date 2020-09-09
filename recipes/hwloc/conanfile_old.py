from conans import ConanFile, AutoToolsBuildEnvironment, tools
import pathlib, os, multiprocessing

class HwlocConan(ConanFile):
    name = "hwloc"
    version = "github"
    license = "BSD license"
    author = "Open-MPI  www.open-mpi.org"
    url = "https://github.com/open-mpi/hwloc"
    description = "The Hardware Locality (hwloc) software project aims at easing the process of discovering hardware resources in parallel architectures"
    topics = ("hpc", "parallelism", "hardware")
    generators = "pkg_config"
    settings = "os", "compiler", "build_type", "arch"
    _autotools = None
    build_policy="missing"
    def source(self):
        self.run("git clone https://github.com/open-mpi/hwloc tmp_src_hwloc && mv tmp_src_hwloc/* . && rm -rf tmp_src_hwloc")
        self.run("./autogen.sh")


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
        self._autotools.configure(args=args, configure_dir=self.source_folder)
        return self._autotools
        
    def build(self):
        autotools = self._configure_autotools()
        autotools.make()

    def package(self): 
        autotools = self._configure_autotools()
        autotools.install()
        self.run("cd {0}/lib && rm *.la ".format(self.package_folder))



    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.env_info.LD_LIBRARY_PATH.append(self.package_folder+"/lib")
        self.env_info.PKG_CONFIG_PATH.append(self.package_folder+"/lib/pkgconfig") 
 

if __name__ == "__main__":
    os.system('conan create . hwloc/github@_/_')
    os.system('conan upload --all hwloc/github -r demo') 
