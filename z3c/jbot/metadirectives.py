from zope.interface import Interface
from zope.configuration import fields

from Products.CMFPlone import PloneMessageFactory as _

class ITemplateOverridesDirective(Interface):
    """Directive which registers a directory with template overrides."""

    directory = fields.Path(title=_(u"Path to directory"),
                            required=True)

