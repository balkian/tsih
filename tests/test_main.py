from unittest import TestCase
import os
import shutil
import pathlib

from tsih import Dict


ROOT = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
DBROOT = ROOT / 'testdb'


class TestTsih(TestCase):
    def setUp(self):
        if not os.path.exists(DBROOT):
            os.makedirs(DBROOT)

    def tearDown(self):
        if os.path.exists(DBROOT):
            shutil.rmtree(DBROOT)

    def test_basic(self):
        '''The data stored in each version should be retrievable'''
        d = Dict()
        d['text'] = 'hello'
        d.version = 1
        d['text'] = 'world'
        assert d[(0, 'text')] == 'hello'
        assert d[(1, 'text')] == 'world'

    def test_auto_version(self):
        '''Changing a value when `auto_version` is on should produce a new version automatically'''
        d = Dict(version=0, auto_version=True)
        d['text'] = 'hello'
        d['text'] = 'world'
        assert d[(1, 'text')] == 'hello'
        assert d[(2, 'text')] == 'world'

    def test_serialized(self):
        '''
        Using the same database should enable retrieving the values of a previous
        dictionary.
        '''
        d = Dict(name='robot', db_path=DBROOT / 'basic.sqlite')
        d['text'] = 'hello'
        d.version = 25
        d['text'] = 'world'
        assert d[(0, 'text')] == 'hello'
        assert d[(24, 'text')] == 'hello'
        assert d[(25, 'text')] == 'world'
        del d

        recovered = Dict(name='robot', db_path=DBROOT / 'basic.sqlite')
        assert recovered[(0, 'text')] == 'hello'
        assert recovered[(24, 'text')] == 'hello'
        assert recovered[(25, 'text')] == 'world'

    def test_custom(self):
        '''
        Inheriting from the Dict class should not change the behavior.
        '''

        class CustomDict(Dict):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, db_path=DBROOT / 'custom.sqlite', **kwargs)

        d = CustomDict(name='robot')
        d['text'] = 'hello'
        d.version = 25
        d['text'] = 'world'
        assert d[(0, 'text')] == 'hello'
        assert d[(24, 'text')] == 'hello'
        assert d[(25, 'text')] == 'world'
        del d

        recovered = CustomDict(name='robot')
        assert recovered[(0, 'text')] == 'hello'
        assert recovered[(24, 'text')] == 'hello'
        assert recovered[(26, 'text')] == 'world'
