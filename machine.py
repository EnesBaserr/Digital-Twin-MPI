"""
YASİN ATLI - 2020400246
ENES BAŞER - 2020400141
Group number: 49
"""
class Machine:
    def __init__(self, product : str , id: int,
                  parent_id: int, isLeaf: bool , 
                  operation : str,child_machines:[],a_cost:int):
        """
        Initialize the Machine object.

        Args:
        - prdouct (str): The string product of the machine.
        - id (int): The unique identifier for the machine.
        - parent_id (int): The identifier of the parent machine.
        - isLeaf (bool): A boolean indicating if the machine is a leaf node.
        - child_machines(list): A list of child machines' ids.
        - operation(str): The current operation of the machine
        -a_cost(int): Accumulated value of the machine that caused by the wear factor of the operations 
        """
        self.product = product
        self.id = id
        self.parent_id = parent_id
        self.isLeaf = isLeaf
        self.child_machines = []
        self.operation=operation
        self.a_cost=a_cost
    def add_child(self, child_machine):
        """
        Add a child machine to the current machine.
        Args:
        - child_machine (Machine): The child machine to be added.
        """
        self.child_machines.append(child_machine)
        self.child_machines = sorted(self.child_machines)
    def __repr__(self):
        return f"""Machine(id={self.id}, parent_id={self.parent_id},
                  isLeaf={self.isLeaf}, operation={self.operation},
                  product = {self.product} ,
                  childs={self.child_machines} , a_cost ={self.a_cost} )\n"""
