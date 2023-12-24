"""
YASİN ATLI - 2020400246
ENES BAŞER - 2020400141
Group number: 49
"""
from mpi4py import MPI
import numpy as np
from machine import Machine
import sys

def main():
    # getting input file name 
    input_file_name = sys.argv[1]
    # getting output file name 
    output_file_name = sys.argv[2]
    #total machine number
    total_machine = 0
    # total clock cycle number
    clock_cycle = 0
    # list of operations cost 
    operation_costs = []
    # threshold value 
    threshhold = 0
    # list of machine objects
    machines = []    
    total_lines = 0
    # creating the terminal machine 
    mc_1 = Machine( product="",id=1,
                    parent_id=-1, isLeaf=False, 
                    operation="",child_machines=[],a_cost=0)
    # appengding the terminal machine into list of machines 
    machines.append(mc_1)
    with open(input_file_name, 'r') as input:
        lines = input.readlines()  # Read all lines into a list
        total_lines = len(lines)  # Get the total number of lines in the file
    with open(input_file_name, 'r') as input:
        counter = 0
        for row in input:
            row.strip()
            # first line that gives total machine number
            if(counter==0):
                total_machine=int(row)
            # second line that gives total clock cycle number    
            elif(counter == 1):
                clock_cycle=int(row)
            # third line that gives the opreation cost of the operations     
            elif(counter == 2):
                # adding all of them to the operation_cost list of integers
                operation_costs= [int(x) for x in row.split()]
            # fourth line that gives threshold value    
            elif(counter == 3):
                threshhold = int(row)
            else:
                    splitted_row=row.split()
                    """ if the line has 3 elements which means that it is a initilization of a
                        machine with machine id, parent id, and operation of the machine 
                    """
                    if(len(splitted_row)==3):
                        machine_id = int(splitted_row[0]) # first element of the row is machine id 
                        machine_parent_id = int(splitted_row[1]) # second element of the row is parent id 
                        is_Leaf = False #setting is leaf to false because we dont now if the machine is leaf or not yet
                        op = splitted_row[2] #third element of the row is operation of the machine 
                        mc = Machine( product="",id=machine_id,
                                            parent_id=machine_parent_id, isLeaf=is_Leaf, 
                                            operation=op,child_machines=[],a_cost=0) # creating machine object
                        parent_mc = machines[machine_parent_id-1] # getting parent machine 
                        parent_mc.add_child(mc.id) #adding the machine to its parents child_machines list
                        machines.append(mc) # adding the machine to machines list
                    else:          # else block is for leaf machines' product             
                        unread_lines = total_lines - counter  # getting the index of the leaf machine                
                        machines[len(machines)-unread_lines].product=splitted_row[0]  # getting the inserting product of the leaf machine 
                        machines[len(machines)-unread_lines].isLeaf=True  # settinf the isLeaf value of leaf machine True                                     
            counter+=1            
    empty_str_of_log=""
    f = open(output_file_name, "w") # opening the output file to write
    # spawning the paralel processses
    comm = MPI.COMM_SELF.Spawn(sys.executable, args=["worker.py"], maxprocs=len(machines))
    # for every clock cylcle     
    for _ in range(clock_cycle):     
        # for every clock_cycle we reach all the machines 
        for i,machine in  enumerate( machines):
            comm.send(empty_str_of_log,dest=i, tag = 99) # sending the log string
            comm.send(operation_costs,dest=i, tag = 52)  # sending operation cost list
            comm.send(clock_cycle,dest=i,tag=7) # sending clock cycle 
            comm.send(machines[i],dest=i,tag=41) # sending the machine
            comm.send(threshhold,dest=i, tag= 61)  # sending threshold value
        res = comm.recv(source=0,tag = 14) #receiving the final product of the cycle
        f.write(res+"\n") # writing the final product into output file 
    # for every clock cylcle
    for _ in range(clock_cycle):     
         # for every clock_cycle we reach all the machines 
        for i,machine in  enumerate( machines):
            # we receive the log of the machine 
            logg= comm.recv(source=i,tag=222)
            if(logg!=""): # if log exists
                f.write(logg+"\n") #writing the log into output file
        
    comm.Disconnect()   
if __name__ == "__main__":
    main()    
    
