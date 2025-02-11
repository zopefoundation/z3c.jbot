Overview
========

The ``z3c.jbot`` (or "Just a bunch of templates") package allows easy
customization of existing templates and images. It works on Zope 2 and
Zope 3.

The Chameleon rendering engine is supported.

Use of this package adds a small (2-3 ms per request on Plone) to the
total application response time.

Usage
-----

To override a particular file, first determine its *canonical
filename*. It's defined as the path relative to the package within
which the file is located; directory separators are replaced with
dots.

Example:

  Suppose you want to override: /plone/app/layout/viewlets/logo.pt

  You would use the filename:   plone.app.layout.viewlets.logo.pt

Simply drop the file in a directory and register that directory for
use with jbot using a ZCML-directive::

  <include package="z3c.jbot" file="meta.zcml" />

  <browser:jbot
      directory="<path>"
      layer="<layer>" />

Templates in views, viewlets and portlets
-----------------------------------------

Any template that is defined as a class-attribute can be overriden
using jbot, e.g. those used in views, viewlets and portlets. The
template overrides may be registered for any request layer or only a
specific layer.

CMF objects
-----------

Any skin-object (e.g. images, templates) on the file system (directory
views) can be overridden.

Plone resources
---------------

If `plone.resource` is installed, it's possible to use jbot to
override filesystem resources.

Deprecation warnings
--------------------

Imagine this situation:

* You have a ``base`` package with a page template ``original.pt``.
* Someone else overrides this in a project specific package by creating a file ``base.original.pt``.
* Now for some reason you rename the template to ``new.pt``.
* The template override in the project no longer works and the other person starts asking questions or complaining.

To solve this problem, you can register that a template path is deprecated.
First add a dictionary to the ``base`` package, let's say in a file ``utils.py``::

  deprecated_templates = {
      "base.original.pt": "base.new.pt",
  }

In your ``configure.zcml`` you add::

  <configure
      xmlns="http://namespaces.zope.org/zope"
      xmlns:zcml="http://namespaces.zope.org/zcml"
      >
  ...
    <configure zcml:condition="have jbot-deprecations">
      <include package="z3c.jbot" file="meta.zcml" />
      <jbot:jbotDeprecated dictionary=".utils.deprecated_templates">
    </configure>
  </configure>

TODO: check if I have this correct.  I think we need to define xmlns:jbot.

The result is:

1. The old override ``base.original.pt`` works for the new location as well.
2. The user gets a warning that they should use ``base.new.pt`` instead.

Author
------

Malthe Borch <mborch@gmail.com>
