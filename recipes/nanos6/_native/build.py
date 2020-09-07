from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(docker_run_options='--network bridge -v /root/.conan:/root/.conan', upload_dependencies="all")
    builder.add_common_builds()
    builder.run()