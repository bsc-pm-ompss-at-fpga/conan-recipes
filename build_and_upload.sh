StringVal="libz libxml2bsc libxtasks papi ait binutils extrae nanos5/_native nanos5/nanos5 mcxx ompss "

# Iterate the string variable using for loop
for val in $StringVal; do
    cd recipes/$val && conan create . && cd -
done