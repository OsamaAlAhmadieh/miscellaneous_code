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
    '''returns the line in the form: ax + y = b '''
    try:
        m = (y_coords[1] - y_coords[0])/(x_coords[1] - x_coords[0])
        b = y_coords[0] - m * x_coords[0]
        line = [-m, 1, b]
        return line
    except ZeroDivisionError:
        line = [1, 0, x_coords[0]]
        return line




def check_in_domain(sol, domain):
    ''''The function checks if the solution is in the domain. 
    Inputs:
        Sol: the intersectoin point with (x, y) coordinates 
        domain: tuple: ([x_min, x_max], [y_min, y_max])
    Outputs:
        in_domain: Boolean'''

    x = sol[0]
    y = sol[1]

    x_min = domain[0][0]
    x_max = domain[0][1]
    y_min = domain[1][0]
    y_max = domain[1][1]

    if x_min <= x <= x_max and y_min <= y <= y_max:
        in_domain = True 
    else: 
        in_domain = False

    return in_domain

if __name__ == '__main__':

    sol = (1, 2)
    domain = ([0 ,2], [0, 4])
    print(check_in_domain(sol, domain))

    line1 = [-0.5, 1, 0.5]
    line2 = [1, 1, 0]
    find_intersection(line1, line2)
