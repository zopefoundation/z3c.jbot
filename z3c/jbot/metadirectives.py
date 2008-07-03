from zope.interface import Interface
from zope.configuration import fields

class ITemplateOverridesDirective(Interface):
    """Directive which registers a directory with template overrides."""

    directory = fields.Path(
        title=u"Path to directory",
        required=True)

