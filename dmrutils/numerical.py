import math

import numpy as np


def nanpercentile_mask(x, ptiles=(5, 95)):
    """ Return a logical mask for x based on percentile range.

    x     -- Numpy array
    ptiles -- Tuple of (min, max) percentile values to keep, inclusive
    """
    return np.logical_and(x >= np.nanpercentile(x, ptiles[0]), x <= np.nanpercentile(x, ptiles[1]))


def median_polish(array, iterations=25):
    """
    Implementation of Tukey's median polish algorithm.
    
    array       -- 2-dimensional numpy array
    iterations  -- number of iterations for effect measurement
    """
    array = array.copy()
    grand_effect = 0
    median_row_effects = 0
    median_col_effects = 0
    row_effects = np.zeros(array.shape[0])
    col_effects = np.zeros(array.shape[1])

    for i in range(iterations):
        row_medians = np.nanmedian(array, 1) 
        row_effects += row_medians
        median_row_effects = np.nanmedian(row_effects)
        grand_effect += median_row_effects
        row_effects -= median_row_effects
        array -= row_medians[:,np.newaxis]
            
        col_medians = np.nanmedian(array, 0) 
        col_effects += col_medians
        median_col_effects = np.nanmedian(col_effects)
        array -= col_medians 
        grand_effect += median_col_effects

    return (grand_effect, col_effects, row_effects, array)  


def rdp(points, epsilon):
    """
    Implementation of the Ramer-Douglas-Peucker algorithm for reducing
    the number of points used to define a curve.

    points   -- List of (x, y) tuples
    epsilon  -- Threshold of perpindicular distance to determine need for endpoint.
                Will have to vary this based on the application/interpretation of 
                euclidean distance.
    """
    dmax = 0
    index = 0
    end = len(points)

    def orthogonal_distance(point, line):
        """ 
        Distance from point to line. 
        """
        a, b = line
        numerator = abs((b[1] - a[1]) * point[0] - (b[0] - a[0]) * point[1] + (b[0] * a[1]) - (b[1] * a[0]))
        denominator = math.sqrt((b[1] - a[1]) ** 2 + (b[0] - a[0]) ** 2)
        return float(numerator) / denominator

    for i in range(1, end):
        d = orthogonal_distance(points[i], (points[0], points[-1]))
        if d > dmax:
            index = i
            dmax = d

    if dmax > epsilon:
        results_a = rdp(points[:index], epsilon)
        results_b = rdp(points[index:], epsilon)
        results = results_a[:-1] + results_b        
    else:
        results = [points[0], points[-1]]
    
    return results

