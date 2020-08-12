import doctest
import re
import unittest

import six

import zope.component
import zope.interface

from .common import setUp
from .common import tearDown

OPTIONFLAGS = (
    doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
)


class Py23DocChecker(doctest.OutputChecker):

    def check_output(self, want, got, optionflags):
        # fix binary/unicode differences between python versions
        if six.PY2:
            want = re.sub("b'(.*?)'", "'\\1'", want)
        else:
            want = re.sub("u'(.*?)'", "'\\1'", want)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)


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
            checker=Py23DocChecker(),
        ),
    ))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
