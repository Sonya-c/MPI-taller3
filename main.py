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
    res = []
    
    while len(res) < K:
        prank, pres = comm.recv(source=MPI.ANY_SOURCE)
        res = res + pres

        if (sended_packages < len(packages)):
            comm.send((True, packages[sended_packages]), dest=prank)
            print(f"Root send to process {prank} = {packages[sended_packages]}")
            sended_packages += 1
        else:
            print(f"Root send orden to finish to process {rank}")
            comm.send((False, None), dest=prank)

    print(*res,sep="\n")

else: 
    sw = True
    while sw:
        print(f"Process {rank} got package = {pkg}")
        res = []
        for number in pkg:
            res.append((number, prime_check(number)))
        
        comm.send((rank, res), dest=0)
        sw, pkg = comm.recv(source=0)

    print(f"Process {rank} ended")
