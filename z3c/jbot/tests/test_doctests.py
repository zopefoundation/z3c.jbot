import zope.interface
import zope.component
import zope.testing
import unittest

OPTIONFLAGS = (zope.testing.doctest.ELLIPSIS |
               zope.testing.doctest.NORMALIZE_WHITESPACE)

import zope.component.testing

def test_suite():
    globs = dict(
        interface=zope.interface,
        component=zope.component)

    return unittest.TestSuite((
        zope.testing.doctest.DocFileSuite(
            'README.txt',
            optionflags=OPTIONFLAGS,
            setUp=zope.component.testing.setUp,
            tearDown=zope.component.testing.tearDown,
            globs=globs,
            package="z3c.jbot"),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
