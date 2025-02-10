import unittest

from Testing.ZopeTestCase import ZopeTestCase

from . import common


deprecations = {
    "z3c.jbot.tests.templates.example_deprecated.pt": "z3c.jbot.tests.templates.example.pt"  # noqa: E501
}


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
            interface_deprecated_override = Template(
                "overrides/interface_deprecated/z3c.jbot.tests.templates.example_deprecated.pt"  # noqa: E501
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
        self._interface_deprecated_override = view.interface_deprecated_override()  # noqa: E501
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

    def test_zcml_features(self):
        from zope.configuration import xmlconfig
        from zope.configuration.config import ConfigurationMachine

        context = ConfigurationMachine()
        xmlconfig.registerCommonDirectives(context)

        xmlconfig.string(
            """
            <configure
                xmlns="http://namespaces.zope.org/zope"
            >
                <include package="z3c.jbot" file="meta.zcml" />
            </configure>
            """, context=context
        )

        self.assertTrue(context.hasFeature("jbot-deprecations"))

    def test_deprecated_override(self):
        from unittest.mock import patch

        from zope import interface

        from z3c.jbot.metaconfigure import handler

        overrides_folder = f"{self._tests}/overrides/interface_deprecated"

        # Without the deprecation in place we do not get any warnings
        with patch("warnings.warn") as mock_warn:
            handler(overrides_folder, interface.Interface)
            self.assertEqual(mock_warn.call_count, 0)

        # and the view still uses the original template because the override
        # is referring to a not existent template
        self.assertEqual(self._view.template(), self._original)

        # We now set up the deprecation
        from zope.configuration import xmlconfig
        xmlconfig.string(
            """
            <configure
                xmlns="http://namespaces.zope.org/zope"
                xmlns:browser="http://namespaces.zope.org/browser"
            >
                <include package="z3c.jbot" file="meta.zcml" />
                <browser:jbotDeprecated dictionary="z3c.jbot.tests.test_five.deprecations" />
            </configure>
            """  # noqa: E501
        )

        # And rerun the handler
        with patch("warnings.warn") as mock_warn:
            handler(
                overrides_folder, interface.Interface
            )
            self.assertEqual(mock_warn.call_count, 1)
            self.assertTupleEqual(
                mock_warn.call_args.args,
                (
                    f'Template {self._tests}/overrides/interface_deprecated/z3c.jbot.tests.templates.example_deprecated.pt '  # noqa: E501
                    f'deprecated, use z3c.jbot.tests.templates.example.pt instead.',  # noqa: E501
                )
            )

        # The view now is able to resolve the renamed template
        self.assertEqual(
            self._view.template(),
            self._interface_deprecated_override,
        )


def test_suite():
    return unittest.TestSuite(
        (unittest.defaultTestLoader.loadTestsFromTestCase(FiveTests),))
