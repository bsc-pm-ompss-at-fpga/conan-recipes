from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class BinutilsConan(ConanFile):
    name = "binutils"
    version = "2.32"
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
    requires = "zlib/1.2.11"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://ftp.gnu.org/gnu/binutils/binutils-%s.tar.bz2" % self.version
        tools.get(source_url, sha256="de38b15c902eb2725eac6af21183a5f34ea4634cb0bcef19612b50e5ed31072d")
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        tools.mkdir(self._build_subfolder)
        condigure_dir = os.path.abspath(os.path.join(self.source_folder, self._source_subfolder))
        with tools.chdir(self._build_subfolder):
            # http://www.linuxfromscratch.org/lfs/view/stable/chapter06/binutils.html
            args = ["--enable-gold",
                    "--enable-ld=default",
                    "--enable-plugins",
                    "--disable-werrror",
                    "--enable-64-bit-bfd",
                    "--with-system-zlib",
                    "--enable-multilib"]
            if self.options.shared:
                args.extend(["--disable-static", "--enable-shared"])
            else:
                args.extend(["--disable-shared", "--enable-static"])
            env_build = AutoToolsBuildEnvironment(self)
            if self.settings.os == "Macos":
                env_build.cxx_flags.append("-std=c++11")  # TODO: cppstd?
            env_build.configure(args=args, configure_dir=condigure_dir, target=self.options.target)
            env_build.make()
            env_build.install()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)

    def _create_tool_var(self, name, value):
        cross_prefix = str(self.options.target) + "-" if self.options.target else ""
        path = os.path.join(self.package_folder, "bin", cross_prefix + value)
        self.output.info("Appending %s env var with : %s" % (name, path))
        return path

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH env var with : " + bindir)
        self.env_info.PATH.append(bindir)

        self.env_info.LD = self._create_tool_var('LD', 'ld')
        self.env_info.AS = self._create_tool_var('AS', 'as')
        self.env_info.ADDR2LINE = self._create_tool_var('ADDR2LINE', 'addr2line')
        self.env_info.AR = self._create_tool_var('AR', 'ar')
        self.env_info.NM = self._create_tool_var('NM', 'nm')
        self.env_info.OBJCOPY = self._create_tool_var('OBJCOPY', 'objcopy')
        self.env_info.OBJDUMP = self._create_tool_var('OBJDUMP', 'objdump')
        self.env_info.RANLIB = self._create_tool_var('RANLIB', 'ranlib')
        self.env_info.READELF = self._create_tool_var('READELF', 'readelf')
        self.env_info.SIZE = self._create_tool_var('SIZE', 'size')
        self.env_info.STRINGS = self._create_tool_var('STRINGS', 'strings')
        self.env_info.STRIP = self._create_tool_var('STRIP', 'strip')