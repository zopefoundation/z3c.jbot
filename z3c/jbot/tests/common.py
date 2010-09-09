import zope.component.testing
import zope.configuration.xmlconfig


def setUp(test):
    zope.component.testing.setUp(test)

    import z3c.jbot
    zope.configuration.xmlconfig.XMLConfig('configure.zcml', z3c.jbot)()

    # enable five.pt if present
    try:
        import five.pt
    except ImportError:
        pass
    else:
        zope.configuration.xmlconfig.XMLConfig('configure.zcml', five.pt)()
