z3c.jbot
========

The z3c.jbot (or "Just a bunch of templates") package allows drop-in
page template overrides.

Registration
------------

Let's instantiate a page template

  >>> from zope.pagetemplate.pagetemplatefile import PageTemplateFile
  >>> template = PageTemplateFile("tests/templates/example.pt")
  
A call to the template will render it.

  >>> template()
  u'This is an example page template.\n'

Providing a template override
-----------------------------

We use the global template manager to register and unregister new
template override directories.

If we register the directory where it's placed with the global template
manager, it will be used when rendering this template object instead
of the original filename.

  >>> import z3c.jbot.tests
  >>> directory = z3c.jbot.tests.__path__[0]

Register template manager factory. We'll register it for
``zope.interface.Interface`` which makes it available on all layers.
  
  >>> import z3c.jbot.manager
  >>> import z3c.jbot.interfaces
  >>> factory = z3c.jbot.manager.TemplateManagerFactory()
  >>> component.provideAdapter(
  ...     factory, (interface.Interface,), z3c.jbot.interfaces.ITemplateManager)

Register overrides directory.
  
  >>> manager = factory.manager
  >>> manager.registerDirectory("%s/templates" % directory)

Verify that we've registered the contents of the directory:

  >>> manager.paths
  {'z3c.jbot.tests.templates.example.pt': '.../z3c.jbot.tests.templates.example.pt',
   'example.pt': '.../example.pt'}
  
Notice that the file "z3c.jbot.tests.templates.example.pt" is the
dotted name for the original example page template file.

We should now see that the new filename will be used for rendering:

  >>> template()
  u'This template will override the example template.\n'

Before we proceed we'll clean up.

  >>> manager.unregisterDirectory("%s/templates" % directory)

The template does indeed render the original template.
  
  >>> template()
  u'This is an example page template.\n'

Upon rendering, the global template manager will have reverted the
template filename to the original.

  >>> template.filename
  '.../z3c.jbot/z3c/jbot/tests/templates/example.pt'

Overrides can be registered for a specific layer. Let's re-register an
override template factory for the HTTP-request layer.

  >>> from zope.publisher.interfaces.browser import IHTTPRequest
  >>> factory = z3c.jbot.manager.TemplateManagerFactory()
  >>> component.provideAdapter(
  ...     factory, (IHTTPRequest,), z3c.jbot.interfaces.ITemplateManager)

Register overrides directory.
  
  >>> manager = factory.manager
  >>> manager.registerDirectory("%s/templates" % directory)

Let's set up an interaction with a base request.

  >>> import zope.security.management
  >>> import zope.publisher.base
  >>> request = zope.publisher.base.BaseRequest("", {})
  >>> IHTTPRequest.providedBy(request)
  False
  >>> zope.security.management.newInteraction(request)  

Since this request is not an HTTP-request, we don't expect the
override to be enabled.

  >>> template()
  u'This is an example page template.\n'

Let's now engage in an interaction with an HTTP-request.
  
  >>> interface.alsoProvides(request, IHTTPRequest)
  >>> template()
  u'This template will override the example template.\n'

  >>> template._v_cooked
  1
  
Going back to a basic request.

  >>> interface.noLongerProvides(request, IHTTPRequest)
  >>> IHTTPRequest.providedBy(request)
  False
  
  >>> template()
  u'This is an example page template.\n'

Let's verify that we only cook once per template source.

  >>> import z3c.jbot.utility
  >>> z3c.jbot.utility.getManager().registerTemplate(template)
  >>> template._v_last_read and template._v_cooked
  1

  >>> interface.alsoProvides(request, IHTTPRequest)
  >>> z3c.jbot.utility.getManager().registerTemplate(template)
  >>> template._v_last_read and template._v_cooked
  1

  >>> template()
  u'This template will override the example template.\n'

  >>> z3c.jbot.utility.getManager().unregisterDirectory("%s/templates" % directory)
  >>> interface.noLongerProvides(request, IHTTPRequest)
  >>> z3c.jbot.utility.getManager().unregisterDirectory("%s/templates" % directory)
  
Configuring template override directories in ZCML
-------------------------------------------------

First we load the metadirectives of the package. This will allow us
to register template overrides directories in configuration files.

  >>> from cStringIO import StringIO
  >>> from zope.configuration import xmlconfig
  >>> xmlconfig.XMLConfig('meta.zcml', z3c.jbot)()

Let's try registering the directory again.

  >>> xmlconfig.xmlconfig(StringIO("""
  ... <configure xmlns="http://namespaces.zope.org/browser">
  ... <templateOverrides directory="%s/templates" />
  ... </configure>
  ... """ % directory))

Once again, the override will be in effect.
  
  >>> template()
  u'This template will override the example template.\n'

  >>> z3c.jbot.utility.getManager().unregisterDirectory("%s/templates" % directory)

Let's register overrides for the HTTP-request layer.

  >>> xmlconfig.xmlconfig(StringIO("""
  ... <configure xmlns="http://namespaces.zope.org/browser">
  ... <templateOverrides
  ...      directory="%s/templates"
  ...      layer="zope.publisher.interfaces.browser.IHTTPRequest" />
  ... </configure>
  ... """ % directory))

  >>> template()
  u'This is an example page template.\n'

If we now provide the HTTP-request layer, the override becomes active.
  
  >>> interface.alsoProvides(request, IHTTPRequest)
  >>> template()
  u'This template will override the example template.\n'
