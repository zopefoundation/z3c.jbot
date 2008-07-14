import zope.interface
import zope.component
import zope.testing
import unittest

OPTIONFLAGS = (zope.testing.doctest.ELLIPSIS |
               zope.testing.doctest.NORMALIZE_WHITESPACE)

import zope.component.testing

def test_suite():
    doctests = ['README.txt']
    globs = dict(
        interface=zope.interface,
        component=zope.component)
    
    try:
        import Products.Five
        doctests.append('Five.txt')
    except:
        pass
    
    return unittest.TestSuite((
        zope.testing.doctest.DocFileSuite(doctest,
                                          optionflags=OPTIONFLAGS,
                                          setUp=zope.component.testing.setUp,
                                          tearDown=zope.component.testing.tearDown,
                                          globs=globs,
                                          package="z3c.jbot") for doctest in doctests
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
