StringVal="libz libxml2bsc libxtasks papi binutils release2.4.0/ait release2.4.0/extrae release2.4.0/nanos5/_native release2.4.0/nanos5/nanos5 release2.4.0/mcxx release2.4.0/ompss"

# Iterate the string variable using for loop
for val in $StringVal; do
    cd recipes/$val && conan create . && cd -
done