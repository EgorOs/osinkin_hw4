# **Task 3**
#### **Description:**
Given 3 vertices with integer coordinates for example (0,0), (1,2), (3, 3),
find the number of integer points inside triangle formed by vertices.
#### **Solution:**
##### Notes
1) We can easily calculate the number of points in rectangle as
 *n = (a + 1) * (b + 1)*, where *a* and *b* are sides of rectangle.
2) Calculation of pts in right triangle is pretty easy aswell, but there 
are three diffetent cases depending on orientation and equalty of sides,
further details about these cases can be found in body of
**calc_pts_right_triangle()** function.
3) When we present rectangle as a target triangle plus some external triangles 
[explained algorithm (2)], we should be aware of the fact that some triangles may use
same vertices of rectangle, in this case overlap happens and if we ignore it, we
will lose some points in the end. Variable **overlap** in function
**find_external_triangles()*** is a counter for such accidents, the function itself
returns the list of external triangles and the number of overlaps.
##### Algorithm
The idea is to calculate points in given triangle as algebraic sum of points in
several right triangles. So we sequentially wrapping triangles with rectangles.
1) If **target triangle** is right return the number of points
2) Else wrap **target triangle** with rectangle. Try to represent rectangle
as sum of **target triangle** and 1-3 **external triangles**. 
In this case:  
*T_tr = R - T_ext + O*, where  
*T_tr* - points in target triangle  
*R* - points in rectangle  
*T_ext* - points in external triangles (1-3)  
*O* - number of overlaps  
For triangle in **external triangles** go to step (1) 
if triangle is not right proceed to step (2).
