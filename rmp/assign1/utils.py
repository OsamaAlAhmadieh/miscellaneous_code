import numpy as np
from numpy.linalg import LinAlgError
    
def find_intersection(line1, line2):
    '''line1 is represented by its x and y coefficients
    example: ax + by = c -> line1 = [a,b,c]'''
    A = np.array([line1[0:1], line2[0:1]])
    b = np.array([line1[2], line2[2]])
    try:
        x = np.linalg.inv(A) @ b
        intersection = True
    except LinAlgError:
        intersection = False

    return (intersection, x)


    