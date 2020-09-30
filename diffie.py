# use Python 3 print function
# this allows this code to run on python 2.x and 3.x
from __future__ import print_function

sharedPrime = 23  # p
sharedBase = 5  # g

aSecret = 6  # a
bSecret = 15  # b

print("    Publicly Shared Prime: ", sharedPrime)
print("    Publicly Shared Base:  ", sharedBase)

# A = g^a mod p
A = (sharedBase ** aSecret) % sharedPrime
print("\nPublic Key1: ", A)

# B = g^b mod p
B = (sharedBase ** bSecret) % sharedPrime
print("Public Key2: ", B )

print("\nPrivately Calculated Shared Secret:")
# Shared Secret: s = B^a mod p
aSharedSecret = (B ** aSecret) % sharedPrime
print("A Shared Secret: ", aSharedSecret)

# Shared Secret: s = A^b mod p
bSharedSecret = (A ** bSecret) % sharedPrime
print("B Shared Secret: ", bSharedSecret)