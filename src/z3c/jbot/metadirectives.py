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


class IDeprecatedTemplatesDirective(Interface):
    """Directive which registers a dictionary with deprecated templates.

    This can be used when you move templates and want an existing jbot
    override for the old template path to still work.

    Example:

    * You move old_package/test.pt to new_package/test.pt.
    * You register a dictionary with:
      {"old_package.test.pt": "new_package.test.pt"}
    * If a third party package has a template override old_package.test.pt,
      we display a warning that the package should use new_package.test.pt.
    * The override with the old name still works:
      instead of new_package/test.pt, the override is used.
    * Of course an override with the new name works as well.
    """

    dictionary = GlobalObject(
        title="Python path to dictionary",
        required=True,
    )
