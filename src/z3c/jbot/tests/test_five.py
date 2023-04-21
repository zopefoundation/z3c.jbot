import unittest

from Testing.ZopeTestCase import ZopeTestCase

from . import common


class FiveTests(ZopeTestCase):
    def setUp(self):
        common.setUp(self)
        super().setUp()

        from Products.Five.browser import BrowserView
        from Products.Five.browser.pagetemplatefile import \
            ZopeTwoPageTemplateFile as Template

        class MockView(BrowserView):
            template = Template("templates/example.pt")
            interface_override = Template(
                "overrides/interface/z3c.jbot.tests.templates.example.pt"
            )
            http_override = Template(
                "overrides/http/z3c.jbot.tests.templates.example.pt"
            )
            https_override = Template(
                "overrides/https/z3c.jbot.tests.templates.example.pt"
            )

        # set up mock site and request
        from zope import component
        from zope.publisher.browser import TestRequest

        class MockSite:
            REQUEST = TestRequest("en")
            getSiteManager = component.getSiteManager

        from zope.component.hooks import setHooks
        from zope.component.hooks import setSite

        setHooks()
        setSite(MockSite())
        self._request = MockSite.REQUEST

        # render templates for later comparison
        view = self._view = MockView(self.folder, MockSite.REQUEST)
        self._original = view.template()
        self._interface_override = view.interface_override()
        self._http_override = view.http_override()
        self._https_override = view.https_override()

        import z3c.jbot.tests

        self._tests = z3c.jbot.tests.__path__[0]

    def tearDown(self):
        import zope.component.testing

        zope.component.testing.tearDown(self)

    def test_override_for_interface(self):
        from zope import interface

        from z3c.jbot.metaconfigure import handler

        handler("%s/overrides/interface" % self._tests, interface.Interface)
        self.assertEqual(self._view.template(), self._interface_override)

    def test_override_for_httprequest(self):
        from zope import interface
        from zope.publisher.interfaces.browser import IHTTPRequest

        from z3c.jbot.metaconfigure import handler

        class IHTTPSRequest(IHTTPRequest):
            pass

        # register handlers
        handler("%s/overrides/interface" % self._tests, interface.Interface)
        handler("%s/overrides/https" % self._tests, IHTTPSRequest)

        # we get the general override
        self.assertEqual(self._view.template(), self._interface_override)

        # provide the http layer
        from zope.interface import alsoProvides

        alsoProvides(self._request, IHTTPSRequest)
        self.assertEqual(self._view.template(), self._https_override)

        # revert to general override
        from zope.interface import noLongerProvides

        noLongerProvides(self._request, IHTTPSRequest)
        self.assertEqual(self._view.template(), self._interface_override)


def test_suite():
    return unittest.TestSuite(
        (unittest.defaultTestLoader.loadTestsFromTestCase(FiveTests),))
