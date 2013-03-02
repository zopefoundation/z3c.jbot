Changes
=======

0.7.1 (2012-01-09)
------------------

- Fixed an issue where multiple registrations against the same layer
  would cause only one registration (decided randomly) to have effect.

  The lookup code now uses the specification resolution order to query
  for override registrations in order of specialization.
  [malthe]

0.7 (2012-01-05)
----------------

- Fixed issue where templates being patched by ``five.pt`` would not
  get properly jbotted.

- Use ``five.pt`` if available. [malthe]

- Fixed an issue where tests would fail on Zope 2.10. [malthe]

0.6.3 (2010-09-07)
------------------

- Fixed compatibility with Plone 3.x. [malthe]

0.6.2 (2010-02-17)
------------------

- Downgrade log messages to debug level. In normal operation they don't contain
  any valuable information. [hannosch]

- Prefer zope.site over zope.app.component if it is available. [hannosch]

0.6.1 (2010-02-09)
------------------

- Fix bungled release [optilude]

0.6.0 (2010-02-09)
------------------

- Zope 2.12 compatibility. [malthe]

- Added support for automatic configuration. [malthe]

- Fixed layer specialization ordering. [malthe]

0.5.3 (2009-10-31)
------------------

- ZCML-directive is now called ``jbot``. [malthe]

0.5.2 (2009-10-23)
------------------

- Fixed issue where an exception would be raised if a view was not an
  acquirer, while the context was. [gweis]

0.5.1 (2009-10-19)
------------------

- Acquisition-wrap template instance, if applicable. This fixes an
  issue on Zope 2.10 where legacy code would break.

0.5 (2009-10-16)
----------------

- Added support for CMF skin objects.

0.4 (2009-10-15)
----------------

- Added Chameleon-support.

- Reimplemented override logic; the total usage cost is now reduced to
  an insignificant amount. Meanwhile, only templates that are defined
  as class-attributes (e.g. on views, viewlets and portlets) can be
  overriden.

0.3 (2009-09-26)
----------------

- Improved test coverage.

- Refactored code, improving performance.

- Fixed issue with multiple layers.

0.2 (2008-07-14)
----------------

- Added layer support.

0.1 (2007-11-27)
----------------

- Initial public release.
