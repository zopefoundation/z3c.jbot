Overview
--------

The z3c.jbot (or "Just a bunch of templates") package allows drop-in
page template overrides.

It works by giving page templates a canonical filename which you can
use to provide a replacement in your own package. Simply register a
template overrides directory and give your new template the canonical
filename.

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

In python:

  >>> from z3c.jbot.manager import getGlobalTemplateManager
  >>> getGlobalTemplateManager().registerDirectory(directory)

In ZCML:

  <include package="z3c.jbot" file="meta.zcml" />
  <browser:templateOverrides directory="<directory>" />
  
