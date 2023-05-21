"""
Taller 3
"""

import sys
from mpi4py import MPI

comm = MPI.COMM_WORLD

def prime_check(num: int) -> bool:
    """
    Cheks is a number is primer
    """
    if num == 1: return False 
    divisores = 0

    for i in range(2, num):
        if num % i == 0:
            divisores += 1
            break
    if divisores == 0:
        return True
    else:
        return False

K: int = int(sys.argv[1]) # Number of number to checj
Q: int = int(sys.argv[2]) # I guess this is the start

n = comm.Get_size() # Number of process
rank = comm.Get_rank()

# SEND THE INITIAL DATA 
if rank == 0: # the root
    packages = [list(range(Q, Q + K))[i:i + 10] for i in range(0, K, 10)]
    pkg = [None] + packages[:n - 1]
else:
    pkg = None

pkg = comm.scatter(pkg, root=0)

if rank == 0:
    sended_packages = n - 1
    recived_packages = 0 
    res = 0
    
    while recived_packages < len(packages):
        prank, pres = comm.recv(source=MPI.ANY_SOURCE)
        recived_packages = recived_packages + 1
        res += pres

        if (sended_packages < len(packages)):
            comm.send((True, packages[sended_packages]), dest=prank)
            print(f"Root send to process {prank} = {packages[sended_packages]}")
            sended_packages += 1
        else:
            print(f"Root send orden to finish to process {rank}")
            comm.send((False, None), dest=prank)

    print("RES = ", res)
    res = 0
    for number in range(Q, K + 1):
        if prime_check(number):
            res += 1
    print("RES (linear) = ", res)
else: 
    sw = True
    while sw:
        print(f"Process {rank} got package = {pkg}")
        res = 0
        for number in pkg:
            if prime_check(number): res += 1
        
        comm.send((rank, res), dest=0)
        sw, pkg = comm.recv(source=0)

    print(f"Process {rank} ended")
