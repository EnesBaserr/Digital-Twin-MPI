"""
YASİN ATLI - 2020400246
ENES BAŞER - 2020400141
Group number: 49
"""
from mpi4py import MPI
import sys

def reverse(product):
    """
    Reverses the product string.
    """
    return product[::-1]
def trim(product):
    """
    Removes the first and the last letters from the product.
    """
    if len(product) > 2:
        return product[1:-1]
    return product
def chop(product):
    """
    Removes the last letter from the product.
    """
    if len(product) > 1:
        return product[:-1]
    return product
def enhance(product):
    """
    Duplicates the first and the last letter in the product.
    
    """
    if(len(product)>1):   
        return product[0] * 1 + product + product[-1] * 1
    else:
        return product[0] * 3

# Split Operation
def split(product):
    """
    Splits the product into two parts and discards the right part.
    """
    return product[:len(product)//2 + len(product) % 2]

def main():
    # Initialize MPI environment for the main proceses of the hw.py
    comm = MPI.Comm.Get_parent()
    size = comm.Get_size()
    rank = comm.Get_rank()
    #Initialize MPI environment for communation between machines
    comm2 = MPI.COMM_WORLD
    size2 = comm2.Get_size()
    rank2 = comm2.Get_rank()
    # receiving the clock cycle value from the main processes
    cycle = comm.recv(source=0, tag=7)   
    #receiving the data(that is stand for machine) from the main processses
    data = comm.recv(source=0, tag=41)   
    # receiving the string of the log from the main processes
    log_res = comm.recv(source=0,tag=99)
    #reveicing the list of integers of the cost of the operations from the main processes
    op_costs = comm.recv(source=0, tag =52)
    # receiving the threshold value from the main processes
    tHold = comm.recv(source=0,tag=61)
    #ploting clock cycle to all the machines
    for k in range (cycle) :
        """ chechking if the machine is leaf machine, if so we dont need to  
         receive a product from any other machine, because product of leaf machines 
         are given at the begining of the production cycle 
        """
        if(data.isLeaf):
            # getting the product of the leaf machine
            product2= data.product
            # getting the accumulated value of the machine
            accCost=data.a_cost
            # chechking if the operation is enhance
            if(data.operation=="enhance"):  
                # performing operation   
                product2=enhance(product2) 
                # adding the wear factor of the opreation to accumulated value
                data.a_cost=accCost+op_costs[0] 
                # checking whether accumulated cost exceed the threshold or not 
                if(data.a_cost>= tHold): 
                    # if so calculate the cost 
                    m_cost =(data.a_cost-tHold+1)* op_costs[0] 
                    #adding the log of the machine to the log string
                    log_res= log_res+f"{data.id}-{m_cost}-{k+1}"  
                    # setting accumulated value to 0 because it got maintanence
                    data.a_cost=0
                # chancing the operation    
                data.operation="split"
                # chechking if the operation is trim
            elif(data.operation=="trim"):     
                # performing operation       
                product2=trim(product2)
                # adding the wear factor of the opreation to accumulated value
                data.a_cost=accCost+op_costs[3]
                 # checking whether accumulated cost exceed the threshold or not
                if(data.a_cost>= tHold):
                    # if so calculate the cost 
                    m_cost =(data.a_cost-tHold+1)* op_costs[3]
                    #adding the log of the machine to the log string
                    log_res= log_res+f"{data.id}-{m_cost}-{k+1}"
                    # setting accumulated value to 0 because it got maintanence
                    data.a_cost=0
                # chancing the operation 
                data.operation="reverse"
            # chechking if the operation is chop
            elif(data.operation=="chop"): 
                # performing operation   
                product2=chop(product2)
                # adding the wear factor of the opreation to accumulated value
                data.a_cost=accCost+op_costs[2]
                # checking whether accumulated cost exceed the threshold or not
                if(data.a_cost>= tHold):
                    # if so calculate the cost 
                    m_cost =(data.a_cost-tHold+1)* op_costs[2]
                     #adding the log of the machine to the log string
                    log_res= log_res+f"{data.id}-{m_cost}-{k+1}"
                    # setting accumulated value to 0 because it got maintanence
                    data.a_cost=0
                # chancing the operation
                data.operation="enhance"
            # chechking if the operation is reverse
            elif(data.operation=="reverse"):
                # performing operation 
                product2=reverse(product2)
                # adding the wear factor of the opreation to accumulated value
                data.a_cost=accCost+op_costs[1]
                # checking whether accumulated cost exceed the threshold or not
                if(data.a_cost>= tHold):
                    # if so calculate the cost 
                    m_cost =(data.a_cost-tHold+1)* op_costs[1]
                    #adding the log of the machine to the log string
                    log_res= log_res+f"{data.id}-{m_cost}-{k+1}"
                    # setting accumulated value to 0 because it got maintanence
                    data.a_cost=0
                # chancing the operation    
                data.operation="trim"
             # chechking if the operation is split    
            elif(data.operation=="split"): 
                # performing operation 
                product2=split(product2)
                # adding the wear factor of the opreation to accumulated value
                data.a_cost=accCost+op_costs[4]
                # checking whether accumulated cost exceed the threshold or not
                if(data.a_cost>= tHold):
                    # if so calculate the cost 
                    m_cost =(data.a_cost-tHold+1)* op_costs[4]
                    #adding the log of the machine to the log string
                    log_res= log_res+f"{data.id}-{m_cost}-{k+1}"
                    # setting accumulated value to 0 because it got maintanence
                    data.a_cost=0
                # chancing the operation    
                data.operation="chop"
            # sending the product of the machine to its parent machine               
            comm2.send(product2
                    , dest = data.parent_id-1,tag =41)
        # if the machine is the terminal machine
        if(rank2==0):
            data3=""
            # getting all the prodcuts from its child machines by order of their ids
            for child in data.child_machines:
                data3+= comm2.recv(source = child-1, tag =41 )
                data.product=data3
            # sendign the final product to main processes
            comm.send(data3,dest=0,tag = 14)
        # if a machine is not leaf and not terminal    
        elif (rank2>0 and not(data.isLeaf)):
            data3=""
            # getting all the prodcuts from its child machines by order of their ids
            for child in data.child_machines:
                data3+= comm2.recv(source = child-1, tag =41 )
                data.product=data3
            accCost=data.a_cost
             # chechking if the operation is trim     
            if(data.operation=="trim"):
                # performing operation 
                data3=trim(data3)
                # adding the wear factor of the opreation to accumulated value
                data.a_cost=accCost+op_costs[3]
                # checking whether accumulated cost exceed the threshold or not
                if(data.a_cost>= tHold):
                     # if so calculate the cost 
                    m_cost =(data.a_cost-tHold+1)* op_costs[3]
                    #adding the log of the machine to the log string
                    log_res= log_res+f"{data.id}-{m_cost}-{k+1}"                
                    # setting accumulated value to 0 because it got maintanence
                    data.a_cost=0
                # chancing the operation  
                data.operation="reverse"
            # chechking if the operation is enhance
            elif(data.operation=="enhance"):
                # performing operation
                data3=enhance(data3)
                # adding the wear factor of the opreation to accumulated value
                data.a_cost=accCost+op_costs[0]
                # checking whether accumulated cost exceed the threshold or not
                if(data.a_cost>= tHold):
                    # if so calculate the cost 
                    m_cost =(data.a_cost-tHold+1)* op_costs[0]
                     #adding the log of the machine to the log string
                    log_res= log_res+f"{data.id}-{m_cost}-{k+1}"    
                    # setting accumulated value to 0 because it got maintanence   
                    data.a_cost=0
                # chancing the operation                    
                data.operation="split"
                # chechking if the operation is chop
            elif(data.operation=="chop"):
                # performing operation
                data3=chop(data3)
                # adding the wear factor of the opreation to accumulated value
                data.a_cost=accCost+op_costs[2]
                # checking whether accumulated cost exceed the threshold or not
                if(data.a_cost>= tHold):
                    # if so calculate the cost 
                    m_cost =(data.a_cost-tHold+1)* op_costs[2]
                     #adding the log of the machine to the log string
                    log_res= log_res+f"{data.id}-{m_cost}-{k+1}"
                    # setting accumulated value to 0 because it got maintanence
                    data.a_cost=0
                # chancing the operation  
                data.operation="enhance"
            # chechking if the operation is reverse
            elif(data.operation=="reverse"):
                # performing operation
                data3=reverse(data3)
                # adding the wear factor of the opreation to accumulated value
                data.a_cost=accCost+op_costs[1]
                # checking whether accumulated cost exceed the threshold or not
                if(data.a_cost>= tHold):
                    # if so calculate the cost 
                    m_cost =(data.a_cost-tHold+1)* op_costs[1]
                     #adding the log of the machine to the log string
                    log_res= log_res+f"{data.id}-{m_cost}-{k+1}"
                    # setting accumulated value to 0 because it got maintanence
                    data.a_cost=0
                # chancing the operation    
                data.operation="trim"
            # chechking if the operation is split
            elif(data.operation=="split"):
                # performing operation
                data3=split(data3)
                # adding the wear factor of the opreation to accumulated value
                data.a_cost=accCost+op_costs[4]
                # checking whether accumulated cost exceed the threshold or not
                if(data.a_cost>= tHold):
                    # if so calculate the cost 
                    m_cost =(data.a_cost-tHold+1)* op_costs[4]
                     #adding the log of the machine to the log string
                    log_res= log_res+f"{data.id}-{m_cost}-{k+1}"
                    # setting accumulated value to 0 because it got maintanence
                    data.a_cost=0
                # chancing the operation    
                data.operation="chop"
            # sending the product to machine's parent machine     
            comm2.send(data3,dest=data.parent_id-1,tag=41)      
        # sending the log string to main processes
        comm.send(log_res,dest=0,tag=222)
        # deleting the log string for other machines logs 
        log_res=""         
    comm.Disconnect()

if __name__ == "__main__":
    
    main()
    