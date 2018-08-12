#!/usr/bin/env python3
from time import time


def count_points(A, B, C):

    def is_int(n):
        return True if n//1==n else False

    def norm_2(pt1, pt2):
        """
        Returns distance between two points
        """
        return ((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)**0.5

    class Vector:
        def __init__(self, pt1, pt2):
            self.coord = (pt2[0]-pt1[0], pt2[1]-pt1[1])
            self.len = norm_2(pt1, pt2)
            self.id = time()

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

    def get_equal_sides(A, B, C):
        sides = get_vectors(A, B, C)
        equal = [s1.len for s1 in sides for s2 in sides if s1.len==s2.len and s1.id!=s2.id]
        return equal

    def calc_points(A, B, C):
        """
        Calculates number of points in right triangle
        """
        equal_sides = get_equal_sides(A,B,C)
        if equal_sides:
            if is_int(equal_sides[0]):
                # oriented like |__
                pts = 3
                for i in range(int(equal_sides[0])-1):
                    pts += 3+i
                return pts
            else:
                # oriented like  .^.
                rec = Rectangle(A, B, C)
                h = min(rec.dimensions)
                pts = (h+1)**2
                return pts
        else:
            # oriented like |__ with unequal sides
            rec = Rectangle(A, B, C)
            big_side = max(rec.dimensions)
            small_side = min(rec.dimensions)
            diag = rec.main_diag
            x_min, y_min = diag[0]
            x_max, y_max = diag[1]
            pts_on_diag = 0
            if small_side % 2 == 0 and big_side % 2 == 0:
                # y = k * x + b
                k = y_max/x_max
                for x in range(x_min, x_max):
                    if is_int(k*x):
                        pts_on_diag += 1
                pts_on_diag += 1
            else:
                pts_on_diag = 2
            pts = (rec.pts - pts_on_diag)//2 + pts_on_diag
            return pts

    def get_closest_point(point, *pts):
        min_dst = None
        closest = None
        for pt in pts[0]:
            dst = norm_2(point, pt)
            if not min_dst:
                min_dst = dst
                closest = pt
            elif min_dst <= dst:
                pass
            else:
                min_dst = dst
                closest = pt
        return closest

    def get_smallest_triangle(pt1, pt2, *pts):
        min_size = None
        best_pt = None
        pts = set(pts[0]) - {pt1} - {pt2}
        for pt in pts:
            rect = Rectangle(pt1, pt2, pt)
            size = rect.pts
            if not min_size:
                min_size = size
                best_pt = pt
            elif min_size <= size:
                pass
            else:
                min_size = size
                best_pt = pt
        return pt1, pt2, best_pt

    def pts_in_right_triangle(A, B, C):
        # CHECK THAT
        rect = Rectangle(A, B, C)
        print(rect.pts)
        return rect.pts//2 + 1

    class Rectangle:
        def __init__(self, A, B, C):
            x_min, x, x_max = sorted([A[0], B[0], C[0]])
            y_min, y, y_max = sorted([A[1], B[1], C[1]])
            self.vertices = [(i,j) for i in [x_min, x_max] for j in [y_min, y_max]]
            self.pts = (x_max-x_min+1)*(y_max-y_min+1)
            self.dimensions = (x_max-x_min, y_max-y_min)
            self.main_diag = ((x_min, y_min), (x_max, y_max))
            # insert triagle into smallest rectangle
        def find_external_triangles(self, A, B, C):
            lst = [A, B, C]
            paired = [(V1, V2) for V1 in lst for V2 in lst[::-1][:2] if V1!=V2][:3]
            ext = []
            for pair in paired:
                V1, V2 = pair

                ext.append(get_smallest_triangle(V1, V2, self.vertices))
            return ext

    rec = Rectangle(A,B,C)
    print('---',calc_points(A,B,C))
    print(pts_in_right_triangle(A,B,C))
    print(rec.find_external_triangles(A,B,C))
    #print('+++', get_diagonal(A,B,C))
    # print(get_smallest_triangle(A, B, [(1,2),(10,1)]))
    return is_right_triangle(A, B, C)


A = (0, 0)
B = (4, 0)
C = (0, 8)

print(count_points(A, B, C))