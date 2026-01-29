import numpy as np

'''
    r : float # Distance between particles
    h : float # Its height of cell
'''

def Viscosity_Lapaclian(r,h):
    if r <= 0 or r > h:
        return 0.0

    term = 40 / (np.pi * h ** 5)
    return term * (h - r)