z3c.jbot
========

The z3c.jbot (or "Just a bunch of templates") package allows drop-in
page template and resource file overrides.

Templates
---------

It works with templates which are defined as an attribute on a view::

  >>> from zope.pagetemplate.pagetemplatefile import PageTemplateFile
  >>> class View(object):
  ...     template = PageTemplateFile("tests/templates/example.pt")
  >>> view = View()

To render the template, we instantiate the view and call the
``template`` attribute.

  >>> print(view.template())
  This is an example page template.

We use the global template manager to register and unregister new
template override directories.

If we register the directory where it's placed with the global template
manager, it will be used when rendering this template object instead
of the original filename::

  >>> import z3c.jbot.tests
  >>> directory = z3c.jbot.tests.__path__[0]

Register overrides directory (by default for any request); we confirm
that it's registered for the same template manager::

  >>> from z3c.jbot.metaconfigure import handler
  >>> manager = handler("%s/overrides/interface" % directory, interface.Interface)

We make sure that the presence of an additional, trivial manager, does
not affect the result. We register the system temporary directory::

  >>> import tempfile
  >>> handler(tempfile.tempdir, interface.Interface)
  <z3c.jbot.manager.TemplateManager object at ...>

We should now see that the new filename will be used for rendering::

  >>> print(view.template())
  Override from ./interface.

Before we proceed we'll clean up::

  >>> manager.unregisterAllDirectories()

The template does indeed render the original template::

  >>> print(view.template())
  This is an example page template.

Upon rendering, the global template manager will have reverted the
template filename to the original::

  >>> view.template.filename.replace("\\", "/")
  '.../z3c/jbot/tests/templates/example.pt'

Overrides can be registered for a specific layer. Let's register three
more overrides, one for the general-purpose ``IRequest`` layer, one
for the ``IHTTPRequest`` layer and one for a made-up ``IHTTPSRequest``
layer::

  >>> from zope.publisher.interfaces import IRequest
  >>> from zope.publisher.interfaces.http import IHTTPRequest
  >>> class IHTTPSRequest(IRequest):
  ...     """An HTTPS request."""

Next we register an overrides directory for the ``IRequest`` layer::

  >>> general = handler("%s/overrides/request" % directory, IRequest)

Let's set up an interaction with a trivial participation::

  >>> class Participation:
  ...     interaction = None

  >>> participation = Participation()
  >>> import zope.security.management
  >>> zope.security.management.newInteraction(participation)

This participation does not provide even the basic request interface::

  >>> IRequest.providedBy(participation)
  False

We don't expect the template to be overriden for this interaction::

  >>> print(view.template())
  This is an example page template.
  <BLANKLINE>

Let's upgrade it::

  >>> request = participation
  >>> interface.alsoProvides(request, IRequest)

  >>> print(view.template())
  Override from ./request.
  <BLANKLINE>

  >>> view.template._v_cooked
  1

Going back to a basic request::

  >>> interface.noLongerProvides(request, IRequest)
  >>> print(view.template())
  This is an example page template.
  <BLANKLINE>

Let's verify that we only cook once per template source::

  >>> output = view.template()
  >>> view.template._v_last_read and view.template._v_cooked
  1

  >>> interface.alsoProvides(request, IRequest)
  >>> output = view.template()
  >>> view.template._v_last_read and view.template._v_cooked
  1

  >>> print(view.template())
  Override from ./request.
  <BLANKLINE>

Now, if we switch to the HTTP-layer::

  >>> interface.noLongerProvides(request, IRequest)
  >>> interface.alsoProvides(request, IHTTPRequest)

  >>> print(view.template())
  Override from ./request.
  <BLANKLINE>

  >>> general.unregisterAllDirectories()

  >>> print(view.template())
  This is an example page template.
  <BLANKLINE>

  >>> http = handler("%s/overrides/http" % directory, IHTTPRequest)
  >>> https = handler("%s/overrides/https" % directory, IHTTPSRequest)

  >>> print(view.template())
  Override from ./http.
  <BLANKLINE>

Switching to HTTPS::

  >>> interface.noLongerProvides(request, IHTTPRequest)
  >>> interface.alsoProvides(request, IHTTPSRequest)

  >>> print(view.template())
  Override from ./https.
  <BLANKLINE>

  >>> interface.noLongerProvides(request, IHTTPSRequest)

Unregister all directories (cleanup)::

  >>> for manager, layer in ((http, IHTTPRequest), (https, IHTTPSRequest)):
  ...     interface.alsoProvides(request, layer)
  ...     _ = view.template()
  ...     manager.unregisterAllDirectories()
  ...     interface.noLongerProvides(request, layer)

The override is no longer in effect::

  >>> print(view.template())
  This is an example page template.
  <BLANKLINE>

Using ZCML
----------

First we load the metadirectives of the package. This will allow us
to register template overrides directories in configuration files.

  >>> from io import StringIO
  >>> from zope.configuration import xmlconfig
  >>> xmlconfig.XMLConfig('meta.zcml', z3c.jbot)()

Let's try registering the directory again::

  >>> xmlconfig.xmlconfig(StringIO("""
  ... <configure xmlns="http://namespaces.zope.org/browser">
  ... <jbot directory="%s/overrides/interface" />
  ... </configure>
  ... """ % directory))

Once again, the override will be in effect::

  >>> print(view.template())
  Override from ./interface.
  <BLANKLINE>

Providing the HTTP-request layer does not change this::

  >>> interface.alsoProvides(request, IHTTPRequest)

  >>> print(view.template())
  Override from ./interface.
  <BLANKLINE>

Unregister overrides::

  >>> for manager in z3c.jbot.utility.getManagers(IHTTPRequest):
  ...     manager.unregisterAllDirectories()

  >>> print(view.template())
  This is an example page template.
  <BLANKLINE>

Let's register overrides for the HTTP-request layer::

  >>> xmlconfig.xmlconfig(StringIO("""
  ... <configure xmlns="http://namespaces.zope.org/browser">
  ... <jbot
  ...      directory="%s/overrides/http"
  ...      layer="zope.publisher.interfaces.browser.IHTTPRequest" />
  ... </configure>
  ... """ % directory))

Since we now provide the HTTP-request layer, the override is used::

  >>> print(view.template())
  Override from ./http.
  <BLANKLINE>

Plone resources
---------------

We'll configure a plone static resource directory and set up
jbot-based resource overrides:

  >>> xmlconfig.xmlconfig(StringIO("""
  ... <configure package="z3c.jbot"
  ...     xmlns="http://namespaces.zope.org/browser" xmlns:plone="http://namespaces.plone.org/plone">
  ... <include package="plone.resource" file="meta.zcml" />
  ... <plone:static directory="tests/resources" type="plone"/>
  ... <jbot directory="tests/overrides/resources" />
  ... </configure>
  ... """))

Verify that we can query the test resource:

  >>> from plone.resource.utils import queryResourceDirectory
  >>> directory = queryResourceDirectory("plone", "z3c.jbot")
  >>> resource = directory['test.txt']
  >>> with open(resource.path) as f:
  ...     f.read()
  'Original\n'

If we try to publish this resource, we'll get the resource override instead:

  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.interfaces.browser import IBrowserPublisher
  >>> publisher = getMultiAdapter((resource, interface.Interface), IBrowserPublisher)
  >>> resource, _ = publisher.browserDefault(None)
  >>> with open(resource.path) as f:
  ...     f.read()
  'Override\n'
