# TSIH - A dict with a HISTory

`tsih.Dict` is a type of `UserDict` that allows versioning, backed up by a `sqlite3` database.

* Transparent operation
* Only changes (deltas) are stored.
* Forward-filling of values. A value is reused in future versions, unless it changes.
* Auto-versioning option (off by default), to produce a new version every time a value change happens.
* Ability to store related entries as separate dictionaries. Each `tsih.Dict` has a `dict_name` that is used in the database to identify the dictionary.
* Tuple-based indexing. Get and set values by `dict_name`, `version` and `key`.

## Usage and examples

`tsih.Dict` objects can be used just like regular dictionaries:

```python
>>> from tsih import Dict
>>> a = Dict()
>>> a['test'] = True
>>> a
{'test': True}
>>> a.get('missing', 5)
5
>>> a['missing']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'missing'
```

But at any point, new versions can be produced:

```python
>>> a.version
0
>>> a['start'] = 'now'
>>> a
{'test': True, 'start': 'now'}
>>> a.version = 1
>>> a['start'] = 'one version ago'
>>> a
{'test': True, 'start': 'one version ago'}
```

Previous values can be accessed using tuple keys, i.e., (version, key):

```python
>>> a[(0, 'start')]
'now'
>>> a[(1, 'start')]
'one version ago'
```

Each version only "records" changes, but later versions (even if they don't exist yet) inherit unchanged values from the previous ones:

```python
>>> a[(5, 'start')]  
'one version ago'
>>> a.version = 5
>>> # Until the value is changed
>>> a['start'] = '4 versions ago' 
>>> a[(5, 'start')]
'4 versions ago'
```

You can access *every* state of the Dict using `None` in place of the version and/or the key.
In that case, we will get an iterator, which we can turn into a list explicitly or with the `.value` method.

For example, here we get all the changes to the `start` key:

```python
>>> a[(None, 'start')].value() # 
[(0.0, 'now'), (1.0, 'one version ago'), (5.0, '4 versions ago')]
```

Similarly, to get the keys and values at a specific version:

```python
>>> list(a[(0, None)])
[('start', 'now'), ('test', True)]
```

Or, we can combine both to get the keys and values at every version:

```python
>>> a[(None, None)].value()
[(0.0, 'start', 'now'), (1.0, 'start', 'one version ago'), (5.0, 'start', '4 versions ago'), (0.0, 'test', True), (1.0, 'test', True), (5.0, 'test', True)]
```

## Use cases

Tsih was originally part of the [Soil](https://github.com/gsi-upm/soil) Agent-Based Social Simulation framework, where both the environment and the agents need to keep track of state (i.e., attribute) changes.
