from pysutils import multi_pop, NotGiven, is_iterable, NotGivenIter, \
    is_notgiven, find_path_package, import_split, posargs_limiter, grouper
from os import path
from nose.tools import eq_

def test_multi_pop():
    start = {'a':1, 'b':2, 'c':3}
    assert {'a':1, 'c':3} == multi_pop(start, 'a', 'c')
    assert start == {'b':2}
    
def test_notgiven():
    assert not None
    assert not NotGiven
    assert NotGiven != False
    assert None != False
    assert NotGiven is NotGiven
    assert NotGiven == NotGiven
    assert None is not NotGiven
    assert None == NotGiven
    assert not None != NotGiven
    assert NotGiven == None
    assert str(NotGiven) == 'None'
    assert unicode(NotGiven) == u'None'

def test_notgiveniter():
    assert not NotGivenIter
    assert NotGivenIter != False
    assert NotGivenIter is NotGivenIter
    assert NotGivenIter == NotGivenIter
    assert NotGivenIter == NotGiven
    assert NotGiven == NotGivenIter
    assert not [] != NotGivenIter
    assert NotGivenIter == []
    assert str(NotGivenIter) == '[]'
    assert unicode(NotGivenIter) == u'[]'
    assert is_iterable(NotGivenIter)
    assert len(NotGivenIter) == 0

    for v in NotGivenIter:
        self.fail('should emulate empty')
    else:
        assert True, 'should emulate empty'
    
def test_is_iterable():
    assert is_iterable([])
    assert is_iterable(tuple())
    assert is_iterable({})
    assert not is_iterable('asdf')
    
def test_is_notgiven():
    assert is_notgiven(NotGiven)
    assert is_notgiven(NotGivenIter)
    assert not is_notgiven(None)

def test_find_path_package():
    import email
    import email.mime
    import email.mime.base
    import test
    assert email is find_path_package(email.__file__)
    assert email is find_path_package(path.dirname(email.__file__))
    assert email is find_path_package(email.mime.__file__)
    assert email is find_path_package(email.mime.base.__file__)
    assert None is find_path_package(path.join(path.dirname(__file__), 'notthere.py'))
    assert None is find_path_package(path.dirname(__file__))
    assert test is find_path_package(path.join(path.dirname(test.__file__), 'output', 'test_cgi'))

    drive, casepath = path.splitdrive(path.dirname(email.__file__))
    if drive:
        assert email is find_path_package(drive.upper() + casepath)
        assert email is find_path_package(drive.lower() + casepath)

def test_import_split():
    assert import_split('path') == ('path', None, None)
    assert import_split('path.part.object') == ('path.part', 'object', None)
    assert import_split('path.part:object') == ('path.part', 'object', None )
    eq_(import_split('path.part:object.attribute'),
        ('path.part', 'object', 'attribute') )
    
def test_posargs_limiter():
    def take0():
        return 0
    def take1(first):
        return first
    def take2(first, second):
        return first + second
    def take3(first, second, third):
        return first + second + third
    assert posargs_limiter(take0, 1, 2, 3) == 0
    assert posargs_limiter(take1, 1, 2, 3) == 1
    assert posargs_limiter(take2, 1, 2, 3) == 3
    assert posargs_limiter(take3, 1, 2, 3) == 6
    
    class TheClass(object):
        def take0(self):
            return 0
        def take1(self, first):
            return first
        def take2(self, first, second):
            return first + second
        def take3(self, first, second, third):
            return first + second + third
    tc = TheClass()
    assert posargs_limiter(tc.take0, 1, 2, 3) == 0
    assert posargs_limiter(tc.take1, 1, 2, 3) == 1
    assert posargs_limiter(tc.take2, 1, 2, 3) == 3
    assert posargs_limiter(tc.take3, 1, 2, 3) == 6

def test_grouper():
    data = (
        {'color': 'red', 'number': 1, 'status':'active', 'link':'yes'},
        {'color': 'green', 'number': 2, 'status':'active', 'link':'yes'},
        {'color': 'blue', 'number': 3, 'status':'active', 'link':'no'},
        {'color': 'red', 'number': 4, 'status':'dead', 'link':'no'},
        {'color': 'green', 'number': 5, 'status':'dead', 'link':'yes'},
        {'color': 'blue', 'number': 6, 'status':'dead', 'link':'yes'},
    )
    assert grouper(data, 'status') == {
        'active' : [
            {'color': 'red', 'number': 1, 'status':'active', 'link':'yes'},
            {'color': 'green', 'number': 2, 'status':'active', 'link':'yes'},
            {'color': 'blue', 'number': 3, 'status':'active', 'link':'no'},
        ],
        'dead' : [
            {'color': 'red', 'number': 4, 'status':'dead', 'link':'no'},
            {'color': 'green', 'number': 5, 'status':'dead', 'link':'yes'},
            {'color': 'blue', 'number': 6, 'status':'dead', 'link':'yes'},
        ]
    }