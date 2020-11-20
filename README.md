
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

# Installing conan

Conan is a package manager that will install packages on your home (directory .conan).  Conan will check for your gcc/architecture configuration and download a binary package that matches it. If there is no binary package that matches your compiler version or architecture, it will compile it from source.

to install conan, you only have to make the following command:
* `pip3 install conan` 

After a successful conan installation, you have to add the ompss_at_fpga remote in order to make conan see our packages:
* `conan remote add ompssfpga https://api.bintray.com/conan/bsc-pm/ompss_at_fpga` 


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