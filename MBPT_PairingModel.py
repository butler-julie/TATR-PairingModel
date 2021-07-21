#################################################
# Many-Body Pertubation Theory (MBPT) Pairing Model
# Julie Butler Hartley
# Version 1.0.0
# Date Created: July 21, 2021
# Last Modified: July 21, 2021
# Modified from code provided by LNP936 by Morten Hjorth-Jensen
#
# Performs MBPT energy calculations on the pairing model of any size with the 
# restriction that there are the same number of holes and particle states.
#
# July 21, 2021: Currently only MBPT2 is implemented but hope to have MBPT3 in the near future.
#################################################

#############################
# IMPORTS
#############################
# Third Party Imports
import matplotlib.pyplot as plt
import numpy as np

#############################
# MAKE GENERAL BASIS
#############################
def make_general_basis (size):
    """
        Inputs:
            size (an int): The total number of particles and holes.  Must be
                an even number with half of the number also being even.
        Returns:
            below_fermi (a tuple): the indices of the states below the Fermi
                level
            above_fermi (a tuple): the indices of the states above the Fermi
                level
            states (a list): a list of all states in the pairing model
        This function makes a pairing model basis of a given size with the
        same number of particles and holes.  The argument size must be an 
        even number with half of size also being even (i.e. 4, 8, 12, ...)
    """
    # There needs to be an even number of states
    assert size%2 == 0
    half = int(size/2)
    # There needs to be an even number of particles/holes
    assert half%2 == 0
    
    # The indices of the states below the Fermi level
    below_fermi = np.arange(half)
    below_fermi = tuple(below_fermi)
    
    # The indices of the states above the Fermi level
    above_fermi = np.arange(half, size)
    above_fermi = tuple(above_fermi)
    
    # Create the states with two single particle states per energy level
    states = []
    for i in range (1, half+1):
        states.append((i, 1))
        states.append((i, -1))
        
    return below_fermi, above_fermi, states

def h0(p,q, states):
    if p == q:
        p1, s1 = states[p]
        return (p1 - 1)
    else:
        return 0

def f(p,q, states):
    if p == q:
        return 0
    s = h0(p,q)
    for i in below_fermi:
        s += assym(p,i,q,i)
        return s


def assym(p,q,r,s, states, g):
    p1, s1 = states[p]
    p2, s2 = states[q]
    p3, s3 = states[r]
    p4, s4 = states[s]

    if p1 != p2 or p3 != p4:
        return 0
    if s1 == s2 or s3 == s4:
        return 0
    if s1 == s3 and s2 == s4:
        return -g/2.
    if s1 == s4 and s2 == s3:
        return g/2.

def eps(holes, particles, states):
    E = 0
    for h in holes:
        p, s = states[h]
        E += (p-1)
    for p in particles:
        p, s = states[p]
        E -= (p-1)
    return E


# This is the LNP936 MBPT code with only a few changes.  Note that I did
# change the number of points generated from 20 to 50 to provide more data
def mbpt2_pairingmodel (size, g):
    # Make the basis (definite the single particle states below the fermi
    # level, above the fermi level, and the labels for all the states)
    below_fermi, above_fermi, states = make_general_basis(size)

    temp_amps = []
    # Diagram 1
    # MBPT2 Diagram
    s1 = 0
    for a in above_fermi:
        for b in above_fermi:
            for i in below_fermi:
                for j in below_fermi:
                    s1 += 0.25*assym(a,b,i,j, states, g)*assym(i,j,a,b, states, g)/eps((i,j),(a,b), states)
                    # For each iteration append the amplitude to the list temp_amps
                    temp_amps.append(assym(a,b,i,j, states, g)*assym(i, j, a, b, states, g)/eps((i,j),(a,b), states))

    corr2 = s1
    return corr2, temp_amps               