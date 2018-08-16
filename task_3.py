#!/usr/bin/env python3
from time import time


def count_points(A, B, C):
    def is_int(n):
        return True if n // 1 == n else False

    def norm_2(pt1, pt2):
        """
        Returns distance between two points
        """
        return ((pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2) ** 0.5

    class Vector:
        def __init__(self, pt1, pt2):
            self.coord = (pt2[0] - pt1[0], pt2[1] - pt1[1])
            self.len = norm_2(pt1, pt2)
            self.id = time()

    def is_perpendicular(a, b):
        ax, ay = a
        bx, by = b
        if ax * bx + ay * by == 0:
            return True
        else:
            return False

    def get_vectors(A, B, C):
        return Vector(A, B), Vector(B, C), Vector(C, A)

    def get_equal_sides(A, B, C):
        """
        If triangle, formed by given vertices equal sides return equal sides
        """
        sides = get_vectors(A, B, C)
        equal = [s1.len for s1 in sides for s2 in sides
                 if s1.len == s2.len and s1.id != s2.id]
        return equal

    def get_pts_on_line(pt1, pt2):
        pts_on_diag = 0
        x1, y1 = pt1
        x2, y2 = pt2
        x, y = abs(x2 - x1), abs(y2 - y1)
        if x1 == x2 or y1 == y2:
            return abs(max(x, y)) + 1
        step = max(x, y) / min(x, y)
        for i in range(min(x, y) + 1):
            if i * step % 1 == 0:
                pts_on_diag += 1
        return pts_on_diag

    def calc_pts_right_triangle(A, B, C):
        """
        Calculates number of points in right triangle
        """
        equal_sides = get_equal_sides(A, B, C)
        if equal_sides:
            if is_int(equal_sides[0]):
                # oriented like |__
                pts = 3
                for i in range(int(equal_sides[0]) - 1):
                    pts += 3 + i
                return pts
            else:
                # oriented like  .^.
                rec = Rectangle(A, B, C)
                h = min(rec.dimensions)
                pts = (h + 1) ** 2
                return pts
        else:
            # oriented like |__ with unequal sides
            rec = Rectangle(A, B, C)
            pt1, pt2 = rec.main_diag
            pts_on_diag = get_pts_on_line(pt1, pt2)
            pts = (rec.pts - pts_on_diag) // 2 + pts_on_diag
            return pts

    class Rectangle:
        def __init__(self, A, B, C):
            x_min, x, x_max = sorted([A[0], B[0], C[0]])
            y_min, y, y_max = sorted([A[1], B[1], C[1]])
            self.vertices = [(i, j) for i in [x_min, x_max] for j in
                             [y_min, y_max]]
            self.pts = (x_max - x_min + 1) * (y_max - y_min + 1)
            self.dimensions = (x_max - x_min, y_max - y_min)
            self.main_diag = ((x_min, y_min), (x_max, y_max))
            self.sides = {((x_min, y_min), (x_min, y_max)),
                          ((x_min, y_max), (x_max, y_max)),
                          ((x_max, y_max), (x_max, y_min)),
                          ((x_max, y_min), (x_min, y_min)),
                          }
            self.boundary_pts = sum(
                [get_pts_on_line(*s) for s in self.sides]) - 4
            self.external_triangles = []
            self.boundaries_overlap_line = None
            self.target_triangle_pts = self.pts
            self.overlapping_side_pts = None
            self.overlapping_vertices = None

        def find_external_triangles(self, triangle):
            """
            Creates a list of external triangles;
            Finds all possible overlaps such as:
            - Overlap of boundary lines
            - Overlap of rectangle and triangle by side
            - Overlap of same vertices, belonging to different triangles
            """
            paired_vertices = [s.coord for s in triangle.sides]
            # Overlaps added if one vertex of rectangle is used in
            # multiple triangles
            linking_vertices = {}
            for pair in paired_vertices:
                if pair in self.sides or pair[::-1] in self.sides:
                    # Don't create extra triangle if pair of vertices is
                    # already a side of rectangle
                    self.overlapping_side_pts = get_pts_on_line(*pair)
                else:
                    potential_vertices = set(self.vertices) - set(pair)
                    best_v = None
                    min_size = None

                    for v in potential_vertices:
                        rec = Rectangle(*pair, v)
                        if not min_size:
                            min_size = rec.pts
                            best_v = v
                        elif rec.pts < min_size:
                            min_size = rec.pts
                            best_v = v
                    new_triangle = Triangle(*pair, best_v)
                    if not set(new_triangle.vertices) < set(self.vertices):
                        # If at least one vertex of new triangle doesn't belong
                        # to rectangle this triangle might cause overlaps, when
                        # counting points
                        if not linking_vertices.get(best_v):
                            linking_vertices[best_v] = [new_triangle]
                        else:
                            linking_vertices[best_v].append(new_triangle)

                    self.external_triangles.append(new_triangle)

            for key in linking_vertices.keys():
                # Looking for overlapping sides of triangles
                if len(linking_vertices[key]) == 2:
                    pt1, pt2 = set(linking_vertices[key][0].vertices) & set(
                        linking_vertices[key][1].vertices)
                    self.boundaries_overlap_line = Side(pt1, pt2)

            self.overlapping_vertices = sum(
                [1 for t1 in self.external_triangles for t2 in
                 self.external_triangles if
                 set(t1.vertices) & set(t2.vertices) and t1 != t2]) // 2

    class Side:
        def __init__(self, pt1, pt2):
            self.coord = (pt1, pt2)
            self.len = norm_2(pt1, pt2)
            self.pts = get_pts_on_line(pt1, pt2)
            self.vector = Vector(pt1, pt2)

    class Triangle:
        def __init__(self, A, B, C):
            self.vertices = (A, B, C)
            self.sides = (Side(A, B), Side(B, C), Side(C, A))
            self.pts = 0
            self.boundary_pts = sum([s.pts for s in self.sides]) - 3

        def is_right(self):
            """Check if two sides of triangle are orthogonal"""
            AB, BC, CA = self.sides
            if is_perpendicular(AB.vector.coord, BC.vector.coord):
                return True
            elif is_perpendicular(BC.vector.coord, CA.vector.coord):
                return True
            elif is_perpendicular(CA.vector.coord, AB.vector.coord):
                return True
            else:
                return False

        def is_line(self):
            AB, BC, CA = [s.len for s in self.sides]
            if AB + BC == CA or BC + CA == AB or AB + CA == BC:
                return True
            else:
                return False

    def recursive_calc(triangle):
        """
        Recursively represent triangles as rectangle minus number of external
        triangles; if triangles are right, calculate points and subtract them
        from rectangle
        """
        if triangle.is_right():
            triangle.pts = calc_pts_right_triangle(*triangle.vertices)
            return triangle.pts
        else:
            rec = Rectangle(*triangle.vertices)
            rec.find_external_triangles(triangle)
            for ext_triangle in rec.external_triangles:
                ext_triangle.pts = recursive_calc(ext_triangle)
                rec.target_triangle_pts -= ext_triangle.pts

            if rec.boundaries_overlap_line:
                rec.target_triangle_pts += (rec.boundaries_overlap_line.pts - 1)

            rec.target_triangle_pts += rec.overlapping_vertices

            if rec.overlapping_side_pts:
                rec.target_triangle_pts -= (rec.overlapping_side_pts - 2)
            return rec.target_triangle_pts + triangle.boundary_pts

    if len({A, B, C}) == 1:
        return 1

    triangle = Triangle(A, B, C)

    if triangle.is_line():
        # if all vertices located on the same line
        start_pt, pt, end_pt = sorted(triangle.vertices,
                                      key=lambda x: x[0] + x[1])
        return get_pts_on_line(start_pt, end_pt)

    return recursive_calc(triangle)


assert count_points((0, 0), (0, 0), (0, 0)) == 1
assert count_points((0, 0), (1, 2), (3, 3)) == 5
assert count_points((0, 1), (1, 3), (-1, -4)) == 4
assert count_points((0, 0), (2, 2), (3, 3)) == 4
assert count_points((0, 0), (2, 2), (2, 2)) == 3
assert count_points((0, 0), (0, 2), (0, 3)) == 4
assert count_points((2, 3), (14, 6), (5, 9)) == 37
assert count_points((-2, -3), (-14, -6), (-5, -9)) == 37
assert count_points((4, -1), (0, -5), (6, -5)) == 19
assert count_points((4, -1), (6, 3), (6, -5)) == 15
assert count_points((0, 3), (6, 3), (0, -5)) == 33
assert count_points((4, -1), (6, 3), (0, -5)) == 9
assert count_points((-2, -5), (-1, 1), (5, 2)) == 23
assert count_points((-2, -5), (0, 0), (-2, 2)) == 13
assert count_points((-2, 2), (0, 0), (5, 2)) == 13
assert count_points((-2, -5), (5, -5), (5, 2)) == 36
assert count_points((-3, -7), (0, 0), (7, 3)) == 27
assert count_points((-2, -5), (0, 0), (5, 2)) == 16
assert count_points((5, 2), (0, 0), (-2, -5)) == 16
assert count_points((5, 2), (-2, -5), (0, 0)) == 16

# print(count_points((-2, -5), (0, 0), (5, 2)))
