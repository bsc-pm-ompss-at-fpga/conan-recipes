from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
import os


class Libhwloc(ConanFile):
    name = "hwloc"
    version = "2.1.0"
    description = "The Hardware Locality (hwloc) software project aims at easing the process of discovering hardware resources in parallel architectures"
    topics = ("conan", "libname", "logging")
    url = "https://github.com/open-mpi/hwloc"
    author = "Open-MPI  www.open-mpi.org"
    
    homepage = "https://www.open-mpi.org/projects/hwloc/"
    license = "BSD license"

    settings = "os", "compiler", "build_type", "arch"

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    _autotools = None

    build_policy="missing"


    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" +self.name + "-"+ self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _autogen(self):
        self.run("ls -lah")
        self.run("cd {}".format(self._source_subfolder)+" && ./autogen.sh")

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
        
        self.run("pwd")
        self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
        args =[
        "--prefix={}".format(tools.unix_path(self.package_folder)),
        ]
        self._autotools.configure(args=args, configure_dir=self.build_folder+"/"+self._source_subfolder)
        return self._autotools

    def build(self):
        self._autogen()
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