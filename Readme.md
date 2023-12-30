# Contributors
  [***Yasin ATLI - 2020400246***](https://github.com/TheRealLowyer) \
  [***Enes BAŞER - 2020400141***](https://github.com/EnesBaserr)

# Description
This project is designed to enhance our understanding of the core concepts in paralel programming. We will be given the input file of a factory production cycle that includes machines and first products of the leaf machines and our task is to thoroughly analyze it and creating paralel production processes for every cycle.

A factory runs many processes parallel to each other. To simulate the factory better, and to increase
effciency of the simulation, we must implement a parallel algorithm using MPI. The factory
consists of various machines connected to each other, and each machine needs to be implemented
as a worker/slave process. These processes must communicate with each other.

Products are the things machines are processing. A machine receives some products, performs
some operations on them, and passes its output product to another machine. Eventually, our
factory produces a final product.

The layout of your factory is a tree structure. A machine may receive multiple products from
other machines, but it passes its output product to a single machine. Finally, products arrive at a
terminal machine (root node of the tree).

The machines perform various operations. These operations are add, enhance, reverse, chop, trim
and split.All machines perform add operation when they receive a product. Then any of the other
operation is applied according to rules specified below. The terminal machine performs only the
add operation and performs no other operations. As mentioned previously, each machine has a
unique id assigned to it. If a machine id is an odd number, then this machine performs only
reverse or trim operations in a production cycle and alternates between them for each cycle. This
means that if a machine performs reverse, then it performs trim for the next received products,
and then reverse and so on. Please note that regardless of the machine id and previous operations,
all machines perform add operation initially. For machines with even number id's, they alternate
between enhance, split, and chop in this order.

Machines wear out as they perform their operations. After a certain threshold, they must notify
the control room that they need maintenance. You may assume that maintenance happens instantaneously and machines perform their operations as usual. The simulation is not intended to
simulate breakdown times. It aims to predict costs of maintenances, which depends on various
factors. Cost = (Accumulated_value + Threshold_value -1) * Wear_factor_of_the_operation
# Dependencies
The liblaries need to be installed :
-mpi4py \
-numpy \
-sys \
through pip instal <...>
# Run and Test
This is how you can run the implemented algorithm code in Python

cd where_the_unzipped_file_is

mpiexec -n 1 python hw.py <input_file_name> <output_file_name>

And the products of the clock cycles and the logs of the machines will be written in the output file . 
