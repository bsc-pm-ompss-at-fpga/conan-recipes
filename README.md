# Installing conan

[Conan](conan.io)  is a package manager that will install packages on your home (directory .conan).  Conan will check for your gcc/architecture configuration and download a binary package that matches it. If there is no binary package that matches your compiler version or architecture, it will compile it from source.


In order to achieve that, Conan uses a file called "Recipe", which contains the dependencies between libraries and how to generate the package (aka compile it). 

Once you create a package from a recipe, it's possible to upload it to a public repository, where other people can download it. Also, you can host your own repository, using the **server** folder in this repo.

to install conan, you only have to make the following command:
* `pip3 install conan` 

After a successful conan installation, you have to add the ompss_at_fpga remote in order to make conan see our packages:
* `conan remote add ompssfpga https://api.bintray.com/conan/bsc-pm/ompss_at_fpga` 
  

# Creating packages from recipes

In the recipe folder, we can see that there is a bunch of folders with the name of libraries, each folder contains a conanfile that creates the package for that library.

For example, if we want to generate ***papi*** package, we go to
``recipes/papi`` and we use the command ``conan create .``

This, will create the papi package, using the host architecture as a target, and the current compiler toolchain in our PATH. 

We can change this behaviour using [settings](https://docs.conan.io/en/latest/creating_packages/getting_started.html#creating-and-testing-packages). For example, we could compile papi for arm64 with the following command:

 ``conan create . -s arch=armv8``. 


Once this package is generated, we can upload it to our repo.

# Uploading conan packages

When uploading, we can decide if we want to upload a binary package or only the recipe.

If we decide to upload a binary package, if someone tries to request for that library/tool with the same compiler and architecture than the ones that generated it, instead of compiling it again, they will use the binary package. 

However, if the compiler or architecture differs or there is no binary package, conan will use the recipe in order to build the library/tool.

Keep in mind that, while most of the libraries and tools can be supplied by conan, things like the compiler, or some tools may need to be installed in the machine in order to use a recipe. 

To upload a recipe to a conan repository, we can do:

``conan upload papi/6.0.0 -r ompssfpga``

This will upload our local papi version 6.0.0 to that repository.

If we want to upload it with the binary package we canadd the --all directive to it.

``conan upload papi/6.0.0 -r ompssfpga --all``


# Using Docker to create packages

Since it's a good practice to upload as much packages as possible with the binary included, in order to improve the experience of the users, we created some docker images with a powerpc environment, which was missing from [conan-docker-tools](https://github.com/conan-io/conan-docker-tools) 
#  Using Conan to install OmpSS@FPGA Release.

This page should help you install the OmpSs@FPGA toolchain using conan package manager.

# Prerequisites
 - [Python 3.5 or later](https://www.python.org/)
 - GCC/Gfortran
-- Optionally crosscompile variants
 - Vendor backends:
   - [Xilinx Vivado 2017.3 or later](https://www.xilinx.com/products/design-tools/vivado.html)



# Prerequisites for building from source
 - [Git Large File Storage](https://git-lfs.github.com/)
 - [Python 2](https://www.python.org/)
 - rsync
 - [patchelf](https://github.com/NixOS/patchelf)

# Optional prerequisites when building from source
- Autoconf
- Automake
- libtool
- pkg-config
- make
- flex
- bison
- gperf




# Installing ompss@fpga release


Now that we have conan configurated, we will use it to install ompss@fpga toolchain.

The base command in order to install the release 2.2.0 (the only one supported by this method of installation) is the following one:

* `conan install ompss_fpga/2.4.0@ -g virtualenv` 

This, will install the ompss@fpga 2.2.0 release targeting **[ARM64]** by default , and will generate some scripts in the same directory where you executed this command.
The two most important scripts are:
* `activate.sh` 
* `deactivate.sh` 

In order to be able to use the recently-installed toolchain, you must source the `activate.sh` file, using the following command:
* `source activate.sh` 

In order to remove the modifications to your environment variables, you should deactivate sourcing the other file:
-   `source dactivate.sh`


## x86_64 and others
Conan will install arm64 toolchain by default, in order to change this default behavior, you must set the target option to the installation by the following command:

* `conan install ompss_fpga/2.4.0@ -o *:target=x86_64 -g virtualenv` 

This will generate the toolchain for target  x86_64, using the prefix   x86_64-linux-gnu 

# Building ompss@fpga release

If there was no binary package available por your architecture/compiler, you will be prompted to compile the release from source. 

At the beginning of the guide, there is a list of optional packages that you must have installed in your machine in order to compile this release, however, we facilitate the process offering a conan package that already contains the tools.

If you decide to install the tools using conan, you must install the following package and activate its environment
```
conan install compiletools/bsc@ -g virtualenv --build=missing
source activate.sh
```

after that, you can install the release, which will trigger the building-from-source.

```
conan install ompss_fpga/2.4.0@ -g virtualenv --build=missing
source activate.sh
```

## Known problems

Since vivado uses it's own GCC, and it's set to path when sourcing vivado, the cross-compiler you use must be compatible with the GCC version that vivado uses. 
You can overcome this limitation by avoiding sourcing all the vivado settings or removing the vivado gcc compiler of the PATH env variable. 