from conans import ConanFile

class Nanos6Conan(ConanFile):
    name = "xtasks"
    version = "2.2.0-stub"
    git_clone_name = "xtasks"
    git_url = "https://pm.bsc.es/gitlab/ompss-at-fpga/xtasks"
    git_branch = "fix-missing-implementations"
    settings = "os", "compiler", "arch"
    options = {"target":"ANY"}
    default_options = {"target":"aarch64"}

    build_policy="missing"

    def source(self):
        self.run("git clone -b {} {} {}".format(self.git_branch, self.git_url, self.git_clone_name))

    def build(self):
        if str(self.options.target) == "aarch64":
            crosscompile = "aarch64-linux-gnu-"  
        self.run("cd {}/src  && CROSS_COMPILE={} PREFIX={} make install".format(self.source_folder+"/"+self.git_clone_name, crosscompile, self.package_folder))
        self.run("cd {}/lib  && cp libxtasks-stub.so libxtasks.so".format(self.package_folder))
