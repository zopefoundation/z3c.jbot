Overview
========

The ``z3c.jbot`` (or "Just a bunch of templates") package allows easy
customization of existing templates and images. It works on Zope 2 and
Zope 3.

The Chameleon rendering engine is supported [#]_.

Use of this package adds a small (2-3 ms per request on Plone) to the
total application response time.

.. [#] To enable Chameleon on Zope 2, use the ``five.pt`` package (CMF-apps like Plone should use ``cmf.pt`` which adds full support).

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

Author
------

Malthe Borch <mborch@gmail.com>
