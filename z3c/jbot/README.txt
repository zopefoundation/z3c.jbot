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

Register overrides directory (by default for any request); we confirm
that it's registered for the same template manager.

  >>> from z3c.jbot.metaconfigure import handler
  >>> manager = handler("%s/overrides/interface" % directory, interface.Interface)

We should now see that the new filename will be used for rendering:

  >>> template()
  u'Override from ./interface.\n'

Before we proceed we'll clean up.

  >>> manager.unregisterAllDirectories()

The template does indeed render the original template.

  >>> template()
  u'This is an example page template.\n'

Upon rendering, the global template manager will have reverted the
template filename to the original.

  >>> template.filename
  '.../z3c.jbot/z3c/jbot/tests/templates/example.pt'

Overrides can be registered for a specific layer. Let's register three
more overrides, one for the general-purpose ``IRequest`` layer, one
for the ``IHTTPRequest`` layer and one for a made-up ``IHTTPSRequest``
layer.

  >>> from zope.publisher.interfaces import IRequest
  >>> from zope.publisher.interfaces.http import IHTTPRequest
  >>> class IHTTPSRequest(IRequest):
  ...     """An HTTPS request."""

Next we register an overrides directory for the ``IRequest`` layer.

  >>> general = handler("%s/overrides/request" % directory, IRequest)

Let's set up an interaction with a trivial participation.

  >>> class Participation:
  ...     interaction = None

  >>> participation = Participation()
  >>> import zope.security.management
  >>> zope.security.management.newInteraction(participation)

This participation does not provide even the basic request interface.

  >>> IRequest.providedBy(participation)
  False

We don't expect the template to be overriden for this interaction.

  >>> template()
  u'This is an example page template.\n'

Let's upgrade it.

  >>> request = participation
  >>> interface.alsoProvides(request, IRequest)

  >>> template()
  u'Override from ./request.\n'

  >>> template._v_cooked
  1

Going back to a basic request.

  >>> interface.noLongerProvides(request, IRequest)
  >>> template()
  u'This is an example page template.\n'

Let's verify that we only cook once per template source.

  >>> output = template()
  >>> template._v_last_read and template._v_cooked
  1

  >>> interface.alsoProvides(request, IRequest)
  >>> output = template()
  >>> template._v_last_read and template._v_cooked
  1

  >>> template()
  u'Override from ./request.\n'

Now, if we switch to the HTTP-layer.

  >>> interface.noLongerProvides(request, IRequest)
  >>> interface.alsoProvides(request, IHTTPRequest)

  >>> template()
  u'Override from ./request.\n'

  >>> general.unregisterAllDirectories()

  >>> template()
  u'This is an example page template.\n'

  >>> http = handler("%s/overrides/http" % directory, IHTTPRequest)
  >>> https = handler("%s/overrides/https" % directory, IHTTPSRequest)

  >>> template()
  u'Override from ./http.\n'

Switching to HTTPS.

  >>> interface.noLongerProvides(request, IHTTPRequest)
  >>> interface.alsoProvides(request, IHTTPSRequest)

  >>> template()
  u'Override from ./https.\n'

  >>> interface.noLongerProvides(request, IHTTPSRequest)

Unregister all directories (cleanup).

  >>> for manager, layer in ((http, IHTTPRequest), (https, IHTTPSRequest)):
  ...     interface.alsoProvides(request, layer)
  ...     _ = template()
  ...     manager.unregisterAllDirectories()
  ...     interface.noLongerProvides(request, layer)

The override is no longer in effect.

  >>> template()
  u'This is an example page template.\n'

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
  ... <templateOverrides directory="%s/overrides/interface" />
  ... </configure>
  ... """ % directory))

Once again, the override will be in effect.

  >>> template()
  u'Override from ./interface.\n'

Providing the HTTP-request layer does not change this.

  >>> interface.alsoProvides(request, IHTTPRequest)

  >>> template()
  u'Override from ./interface.\n'

Unregister overrides.

  >>> for manager in z3c.jbot.utility.getManagers():
  ...     manager.unregisterAllDirectories()

  >>> template()
  u'This is an example page template.\n'

Let's register overrides for the HTTP-request layer.

  >>> xmlconfig.xmlconfig(StringIO("""
  ... <configure xmlns="http://namespaces.zope.org/browser">
  ... <templateOverrides
  ...      directory="%s/overrides/http"
  ...      layer="zope.publisher.interfaces.browser.IHTTPRequest" />
  ... </configure>
  ... """ % directory))

Since we now provide the HTTP-request layer, the override is used.

  >>> template()
  u'Override from ./http.\n'

