from conans import ConanFile, tools, AutoToolsBuildEnvironment, RunEnvironment
import pathlib
import os
import multiprocessing
from shutil import copyfile
import requests

class GitConan(ConanFile):
    name = "git"
    settings = "os", "compiler", "build_type", "arch", "arch_build"
    version = "2.28.0"
    git_foldername = "git-{0}".format(version)
    build_requires = ["libtool/2.4.6", "openssl/1.1.1g","expat/2.2.9"]

    no_copy_source=True
    build_policy="missing"
    
    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def build_requirements(self):
        if self.settings.arch_build == self.settings.arch:
            self.build_requires("autoconf/2.69")
            self.build_requires("automake/1.16.2")
            self.build_requires("pkg-config_installer/0.29.2@bincrafters/stable")
            self.build_requires("make/4.2.1")

    def _commonCommandCompileGit(self, install):
        self.build_requires
        ldflags = "-L{0} -L{1} -L{2} -Wl,--no-as-needed -ldl".format(self.deps_cpp_info["libtool"].rootpath+"/lib",self.deps_cpp_info["openssl"].rootpath+"/lib",self.deps_cpp_info["expat"].rootpath+"/lib" )
        return "cd {0}/{1} && make  -j$(nproc)  {2} prefix={3} LDFLAGS=\"{4}\" OPENSSLDIR={5} EXPATDIR={6}  NO_CURL=1".format(
            self.source_folder,
            self._source_subfolder,
            install,
            tools.unix_path(self.package_folder),
            ldflags,
            self.deps_cpp_info["openssl"].rootpath,
            self.deps_cpp_info["expat"].rootpath)


    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "git-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        self.run(self._commonCommandCompileGit(""))

     
    def package(self): 
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        self.run(self._commonCommandCompileGit("install"))
  
        if str(self.settings.arch) == "armv8":
            filename = "git-lfs-linux-arm64-v2.12.0"
        elif str(self.settings.arch) == "x86_64":
            filename = "git-lfs-linux-amd64-v2.12.0"

        urldown = "https://github.com/git-lfs/git-lfs/releases/download/v2.12.0/{}.tar.gz".format(filename)
        self.run("mkdir down && wget {0} && tar xf {1}.tar.gz && PREFIX={2} ./install.sh && cd .. && rm -rf down".format(urldown,filename,str(self.package_folder)))

    def package_info(self):
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))


if __name__ == "__main__":
    os.system('conan create .')
    os.system('conan upload --all {0}/{1} -r ompss'.format(GitConan.name, GitConan.version)) 