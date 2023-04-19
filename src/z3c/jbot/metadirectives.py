from zope.configuration import fields
from zope.configuration.fields import GlobalObject
from zope.interface import Interface


class ITemplateOverridesDirective(Interface):
    """Directive which registers a directory with template overrides."""

    directory = fields.Path(
        title="Path to directory",
        required=True,
    )

    layer = GlobalObject(
        title="The layer the overrides should be enabled for",
        description="By default overrides are used for all layers.",
        required=False,
    )
