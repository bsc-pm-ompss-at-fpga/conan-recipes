from conans import ConanFile

class Nanos6Conan(ConanFile):
    name = "xtasks"
    version = "2.2.0-stub"
    git_clone_name = "xtasks"
    git_url = "https://pm.bsc.es/gitlab/ompss-at-fpga/xtasks"
    settings = "os", "compiler", "arch"
 
    build_policy="missing"

    def source(self):
        self.run("git clone {} {}".format(self.git_url, self.git_clone_name))

    def build(self):
        if str(self.settings.arch) == "armv8":
            crosscompile = "aarch64-linux-gnu-" 
        else:
            crosscompile = str(self.settings.arch)+"-linux-gnu-"

        self.run("cd {}/src  && CROSS_COMPILE={} PREFIX={} make install".format(self.source_folder+"/"+self.git_clone_name, crosscompile, self.package_folder))
        self.run("cd {}/lib  && cp libxtasks-stub.so libxtasks.so".format(self.package_folder))

    def package_info(self):
        self.env_info.LD_LIBRARY_PATH.append(self.package_folder+"/lib")
