Overview
--------

The z3c.jbot (or "Just a bunch of templates") package allows drop-in
page template overrides.

It works by giving page templates a canonical filename which you can
use to provide a replacement in your own package. Simply register a
template overrides directory and give your new template the canonical
filename.

Overrides may be registered for a specific layer or any layer.


Canonical filename
------------------

The canonical filename is defined as the path relative to the package
within which the template is located with directory separators
replaced with dots.

Example:

  Suppose you want to override: /plone/app/layout/viewlets/logo.pt
  You would use the filename:   plone.app.layout.viewlets.logo.pt


Registering a on overrides directory
------------------------------------

A Zope component configuration directive is available to configure
overrides.

  <include package="z3c.jbot" file="meta.zcml" />
  
  <browser:templateOverrides
      directory="<directory>"
      layer="<layer>" />
  

Performance considerations
--------------------------

The use of jbot adds to the general page load time. On a site with
many templates this may be as much as 25 ms per request (a 9% increase
on my machine).

      
Author
------

Malthe Borch <mborch@gmail.com>
