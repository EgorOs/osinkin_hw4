#!/usr/bin/env python3

def count_points(a, b, c):


    pass

A = (0, 0)
B = (0, 9)
C = (2, 0)

# def vector(pt1, pt2):
    # return (pt2[0]-pt1[0], pt2[1]-pt1[1])

def norm_2(pt1, pt2):
    """
    Returns distance between two points
    """
    return ((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)**0.5

class Vector:
    def __init__(self, pt1, pt2):
        self.coord = (pt2[0]-pt1[0], pt2[1]-pt1[1])
        self.len = norm_2(pt1, pt2)

def is_perpendicular(a,b):
    ax, ay = a
    bx, by = b
    if ax*bx+ay*by == 0:
        return True
    else:
        return False

def get_vectors(A,B,C):
    return Vector(A, B), Vector(B, C), Vector(C, A)

def is_right_triangle(A, B, C):
    AB, BC, CA = get_vectors(A, B, C)
    lst = (AB,BC,CA)
    paired_coords = [ (V1.coord, V2.coord) for V1 in lst for V2 in lst[::-1][:2] if V1.coord!=V2.coord][:3]
    is_right = [True for pair in paired_coords if is_perpendicular(*pair)]
    return True if is_right else False

def is_simple_triangle(A, B, C):
    """
    The triangle is considered simple
    if one of its sides has length of 1
    """
    AB, BC, CA = get_vectors(A, B, C)
    lst = (AB,BC,CA)
    is_simple = [True for V in lst if V.len == 1]
    return True if is_simple else False


# print(is_perpendicular(AB,AC))
print(is_right_triangle(A,B,C))
print(is_simple_triangle(A,B,C))