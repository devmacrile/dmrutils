"""
Functions and decorators for caching results locally.


Example usage:  

@money(key_func, cache_directory)
def f(x):
    return y


Similar to https://docs.python.org/3/library/functools.html#functools.lru_cache
Use numpy_key where x is a numpy array.
Using json instead of pickle appears to be faster, but requires custom encoder and decoder.

Credit/author: michael.james.asher@gmail.com, https://github.com/mjasher
"""

import datetime
import multiprocessing
import os
import simplejson as json

from functools import wraps
import numpy
import pandas

mutex = multiprocessing.Lock()



"""
Custom json encoder allows sevearal data types to be saved as json
"""
class DateNumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return {'type': 'numpy.ndarray', 'data_type': str(obj.dtype), 'data': obj.tolist()}
        elif isinstance(obj, datetime.datetime):
            return {'type': 'datetime.datetime', 'data': obj.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}
        elif isinstance(obj, datetime.date):
            return {'type': 'datetime.date', 'data': obj.strftime("%Y-%m-%d")}
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).date().isoformat()
        elif isinstance(obj, pandas.DataFrame):
            try:
                return obj.to_json()
            except:
                return obj.as_matrix().tolist()
        else:
            return super(DateNumpyEncoder, self).default(obj)


def DateNumpyDecoder(dct):
    if isinstance(dct, dict) and 'type' in dct and dct['type'] == 'numpy.ndarray':
        return numpy.array(dct['data']).astype(getattr(numpy, dct['data_type']))
    elif isinstance(dct, dict) and 'type' in dct and dct['type'] == 'datetime.datetime':
        return datetime.datetime.strptime(dct['data'], "%Y-%m-%dT%H:%M:%S.%fZ")
    elif isinstance(dct, dict) and 'type' in dct and dct['type'] == 'datetime.date':
        return datetime.datetime.strptime(dct['data'], "%Y-%m-%d").date()
    return dct


"""
Some useful key functions
"""
def numpy_key(original_x, *args, **kwargs):
    x = original_x.copy()
    x.flags.writeable = False
    key = str(hash(x.data))
    return key

def join_key(*args, **kwargs):
    return str(hash(''.join([json.dumps(a, cls=DateNumpyEncoder, ignore_nan=True) for a in args + tuple(kwargs.values())])))

def concat_key(*args, **kwargs):
    return '_'.join(str(a) for a in args + tuple(kwargs.values()))

def date_place_key(geom, years):
    return str(hash(''.join([str(y) for y in years]) + json.dumps(geom)))

def one_key(*args, **kwargs):
    return "one_key"


def money(key_func=join_key, cache_directory=None):
    """
    A decorator to cache a given function for a set of arguments.
    Return values persisted to <cache_directory>/some_function/<key_func(args)>
    
    Note: does not manage the cached data, so need to perform manual clean-up.
    """
    
    def decorator(func):
        if cache_directory is None:
            local_cache_directory = os.path.join(os.environ.get('CACHE_DIR', '/tmp'),  func.__module__ + '.' + func.__name__)
        else:
            local_cache_directory = cache_directory

        @wraps(func)
        def f_with_cache(*args, **kwargs):
            key = key_func(*args, **kwargs)
            mutex.acquire()
            if not os.path.exists(local_cache_directory):
                os.makedirs(local_cache_directory)
            mutex.release()
            cache_file = os.path.join(local_cache_directory, key)

            if os.path.exists(cache_file):
                # deals with broken cached files
                try:
                    with open(cache_file, "rb") as file:
                        y = json.load(file, object_hook=DateNumpyDecoder)
                    return y
                except:
                    pass
            
            y = func(*args, **kwargs) 
            with open(cache_file, "wb") as file:
                json.dump(y, file, cls=DateNumpyEncoder, ignore_nan=True)
            return y

        return f_with_cache

    return decorator
