import numpy as np
from numpy.linalg import LinAlgError
    
def find_intersection(line1, line2):
    '''line1 is represented by its x and y coefficients
    example: ax + by = c -> line1 = [a,b,c]'''
    A = np.array([line1[0:2], line2[0:2]])
    b = np.array([[line1[2]], [line2[2]]])
    try:
        x = np.linalg.inv(A) @ b
        intersection = True
        return (intersection, x)
    except LinAlgError:
        intersection = False
        return (intersection, None)

    


def get_line_eq(x_coords, y_coords):
    '''returns the line in the form '''
    try:
        m = (y_coords[1] - y_coords[0])/(x_coords[1] - x_coords[0])
        b = y_coords[0] - m * x_coords[0]
        line = [-m, 1, b]
        return line
    except ZeroDivisionError:
        line = [1, 0, x_coords[0]]
        return line

line1 = [-0.5, 1, 0.5]
line2 = [1, 1, 0]

find_intersection(line1, line2)