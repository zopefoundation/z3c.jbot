import doctest
import unittest

import zope.component
import zope.interface

from .common import setUp
from .common import tearDown


OPTIONFLAGS = (
    doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
)


def test_suite():
    globs = dict(
        interface=zope.interface,
        component=zope.component)

    return unittest.TestSuite((
        doctest.DocFileSuite(
            'README.rst',
            optionflags=OPTIONFLAGS,
            setUp=setUp,
            tearDown=tearDown,
            globs=globs,
            package="z3c.jbot",
        ),
    ))
