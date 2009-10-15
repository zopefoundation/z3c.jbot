Overview
========

The ``z3c.jbot`` (or "Just a bunch of templates") package allows
drop-in page template overrides. It works on Zope 2 and Zope 3. The
Chameleon rendering engine is supported [#]_.

Any template that is defined as a class-attribute can be overriden
using jbot, e.g. those used in views, viewlets and portlets. The
template overrides may be registered for any request layer or only a
specific layer.

To override a particular template, first determine its *canonical
filename*. It's defined as the path relative to the package within
which the template is located; directory separators are replaced with
dots.

Example:

  Suppose you want to override: /plone/app/layout/viewlets/logo.pt

  You would use the filename:   plone.app.layout.viewlets.logo.pt

Simply drop the file in a directory and register that directory for
use with jbot using a ZCML-directive::

  <include package="z3c.jbot" file="meta.zcml" />

  <browser:templateOverrides
      directory="<path>"
      layer="<layer>" />

Use of this package adds a small (2-3 ms per request on Plone) to the
total application response time.

.. [#] To enable Chameleon on Zope 2, use the ``five.pt`` package (CMF-apps like Plone should use ``cmf.pt`` which adds full support).

Author
------

Malthe Borch <mborch@gmail.com>
