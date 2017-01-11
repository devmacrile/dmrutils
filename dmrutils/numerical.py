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
