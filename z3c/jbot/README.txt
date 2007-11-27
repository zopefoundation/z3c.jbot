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

  >>> import z3c.jbot.manager
  >>> manager = z3c.jbot.manager.getGlobalTemplateManager()
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

  >>> manager.unregisterDirectory("%s/templates" % directory)
