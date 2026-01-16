# project/utils/helpers.py
import math

def calculate_distance(x1, y1, x2, y2):
    """Tính khoảng cách giữa 2 điểm."""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def is_point_in_circle(x, y, circle_x, circle_y, radius):
    """Kiểm tra xem điểm (x,y) có nằm trong hình tròn không."""
    return calculate_distance(x, y, circle_x, circle_y) <= radius
