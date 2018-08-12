#!/usr/bin/env python3
from time import time


def count_points(A, B, C):

    def is_int(n):
        return True if n//1 == n else False

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

    def get_vectors(A, B, C):
        return Vector(A, B), Vector(B, C), Vector(C, A)

    def is_right_triangle(A, B, C):
        """Check if two sides of triangle are orthogonal"""
        AB, BC, CA = get_vectors(A, B, C)
        lst = (AB,BC,CA)
        paired_coords = [ (V1.coord, V2.coord) for V1 in lst for V2
                          in lst[::-1][:2] if V1.coord!=V2.coord][:3]
        is_right = [True for pair in paired_coords if is_perpendicular(*pair)]
        return True if is_right else False

    def get_equal_sides(A, B, C):
        """
        If triangle, formed by given vertices equal sides return equal sides
        """
        sides = get_vectors(A, B, C)
        equal = [s1.len for s1 in sides for s2 in sides
                 if s1.len==s2.len and s1.id!=s2.id]
        return equal

    def calc_pts_right_triangle(A, B, C):
        """
        Calculates number of points in right triangle
        """
        equal_sides = get_equal_sides(A,B,C)
        if equal_sides:
            if is_int(equal_sides[0]):
                # oriented like |__
                pts = 3
                pts_on_diag = 2
                for i in range(int(equal_sides[0])-1):
                    pts += 3+i
                    pts_on_diag += 1
                return pts, pts_on_diag
            else:
                # oriented like  .^.
                rec = Rectangle(A, B, C)
                h = min(rec.dimensions)
                pts = (h+1)**2
                pts_on_diag = h * 2 + 1
                return pts, pts_on_diag
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
            return pts, pts_on_diag

    def get_smaller_triangle(pt1, pt2, *pts):
        """
        Given 2 vertices of triangle and vertices of rectangle (*pts)
        returns the smallest triangle made from 2 input vertices and
        one vertex from *pts
        """
        min_size = None
        best_pt = None
        pts = set(pts[0]) - {pt1} - {pt2}
        for pt in pts:
            rect = Rectangle(pt1, pt2, pt)
            size = rect.pts
            d1, d2 = rect.dimensions
            if d1 * d2 == 0:
                return None
            if not min_size:
                min_size = size
                best_pt = pt
            elif min_size <= size:
                pass
            else:
                min_size = size
                best_pt = pt
        return pt1, pt2, best_pt

    class Rectangle:
        def __init__(self, A, B, C):
            x_min, x, x_max = sorted([A[0], B[0], C[0]])
            y_min, y, y_max = sorted([A[1], B[1], C[1]])
            self.vertices = [(i,j) for i in [x_min, x_max] for j in [y_min, y_max]]
            self.pts = (x_max-x_min+1)*(y_max-y_min+1)
            self.dimensions = (x_max-x_min, y_max-y_min)
            self.main_diag = ((x_min, y_min), (x_max, y_max))
            self.sides = {((x_min, y_min), (x_min, y_max)),
                         ((x_min, y_max), (x_max, y_max)),
                         ((x_max, y_max), (x_max, y_min)),
                         ((x_max, y_min), (x_min, y_min)),
                         }
            self.external_triangles = []

        def find_external_triangles(self, A, B, C):
            """
            Returns two elements:
            1) list of coordinates of triangles, which left if target triangle
            is cut out from rectangle
            2) integer number of overlaps (times, when one vertex of rectangle
            used in multiple external triangles)
            """
            lst = [A, B, C]
            paired = [(V1, V2) for V1 in lst for V2 in lst[::-1][:2] if V1!=V2][:3]
            # Overlaps added if one vertice of rectangle is used in
            # multiple triangles
            overlaps = 0
            extra_vertices = set()
            for pair in paired:
                V1, V2 = pair
                if (V1, V2) in self.sides or (V2, V1) in self.sides:
                    # Don't create extra triangle if pair of vertices is
                    # already a side of rectangle
                    pass
                else:
                    triangle = get_smaller_triangle(V1, V2, self.vertices)
                    # get_smaller_triangle returns None if it could not create
                    # new triangle with given set of vertices
                    if triangle:
                        new_vertice = triangle[2]
                        if new_vertice in extra_vertices:
                            overlaps += 1
                        else: 
                            extra_vertices.add(new_vertice)
                        self.external_triangles.append(triangle)
            return self.external_triangles, overlaps

    def recoursive_calc(A, B, C):
        """
        Recursively represent triangles as rectangle minus number of external
        triangles; if triangles are right, calculate points and subtract them
        from rectangle
        """
        if is_right_triangle(A, B, C):
            return calc_pts_right_triangle(A, B, C)
        else:
            rec = Rectangle(A, B, C)
            pts_in_target = rec.pts
            external, overlaps = rec.find_external_triangles(A, B, C)
            for triangle in rec.external_triangles:
                A, B, C = triangle
                pts, diag_pts = recoursive_calc(A, B, C)
                pts_in_target = pts_in_target - pts + diag_pts
            pts_in_target += overlaps
            return pts_in_target, 2

    return recoursive_calc(A, B, C)[0]

# A = (0, 0)
# B = (1, 2)
# C = (3, 3)
# print(count_points(A, B, C))
