import numpy as np


def nanpercentile_mask(x, range=(5, 95)):
    """ Return a logical mask for x based on percentile range.

    x     -- Numpy array
    range -- Tuple of (min, max) percentile values to keep, inclusive
    """
    return np.logical_and(x >= np.nanpercentile(x, 25), x <= np.nanpercentile(x, 75))  
