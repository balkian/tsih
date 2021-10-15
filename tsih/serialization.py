import os
import logging
import ast
import sys
import importlib
from itertools import product, chain


logger = logging.getLogger('soil')


builtins = importlib.import_module('builtins')

def name(value, known_modules=[]):
    '''Return a name that can be imported, to serialize/deserialize an object'''
    if value is None:
        return 'None'
    if not isinstance(value, type):  # Get the class name first
        value = type(value)
    tname = value.__name__
    if hasattr(builtins, tname):
        return tname
    modname = value.__module__
    if modname == '__main__':
        return tname
    if known_modules and modname in known_modules:
        return tname
    for kmod in known_modules:
        if not kmod:
            continue
        module = importlib.import_module(kmod)
        if hasattr(module, tname):
            return tname
    return '{}.{}'.format(modname, tname)


def serializer(type_):
    if type_ != 'str' and hasattr(builtins, type_):
        return repr
    return lambda x: x


def serialize(v, known_modules=[]):
    '''Get a text representation of an object.'''
    tname = name(v, known_modules=known_modules)
    func = serializer(tname)
    return func(v), tname

def deserializer(type_, known_modules=[]):
    if type(type_) != str:  # Already deserialized
        return type_
    if type_ == 'str':
        return lambda x='': x
    if type_ == 'None':
        return lambda x=None: None
    if hasattr(builtins, type_):  # Check if it's a builtin type
        cls = getattr(builtins, type_)
        return lambda x=None: ast.literal_eval(x) if x is not None else cls()
    # Otherwise, see if we can find the module and the class
    modules = known_modules or []
    options = []

    for mod in modules:
        if mod:
            options.append((mod, type_))

    if '.' in type_:  # Fully qualified module
        module, type_ = type_.rsplit(".", 1)
        options.append ((module, type_))

    errors = []
    for modname, tname in options:
        try:
            module = importlib.import_module(modname)
            cls = getattr(module, tname)
            return getattr(cls, 'deserialize', cls)
        except (ImportError, AttributeError) as ex:
            errors.append((modname, tname, ex))
    raise Exception('Could not find type {}. Tried: {}'.format(type_, errors))


def deserialize(type_, value=None, **kwargs):
    '''Get an object from a text representation'''
    if not isinstance(type_, str):
        return type_
    des = deserializer(type_, **kwargs)
    if value is None:
        return des
    return des(value)
