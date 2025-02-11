from zope import component
from zope import interface
from zope.publisher.interfaces.browser import IBrowserPublisher

from .manager import update_deprecated_templates_dict


try:
    from plone.resource.file import FilesystemFile
    HAS_PLONE_RESOURCE = True
except ModuleNotFoundError:
    HAS_PLONE_RESOURCE = False

from . import browser
from . import interfaces
from . import manager


def handler(directory, layer):
    lookup_all = component.getGlobalSiteManager().adapters.lookupAll

    # check if a template manager already exists
    factories = {
        factory
        for name, factory in lookup_all((layer,), interfaces.ITemplateManager)
    }

    # this might yield several factories (template managers); we check
    # if one is registered for exactly our layer
    base_factories = set()
    if layer is not interface.Interface:
        for base in layer.__bases__:
            for name, factory in lookup_all(
                (base,), interfaces.ITemplateManager
            ):
                base_factories.add(factory)

    try:
        factory = factories.difference(base_factories).pop()
    except KeyError:
        name = directory
        factory = manager.TemplateManagerFactory(directory)
        component.provideAdapter(
            factory, (layer,), interfaces.ITemplateManager, name=name
        )

        if HAS_PLONE_RESOURCE:
            component.provideAdapter(
                browser.FilesystemFileResourceBrowserPublisher,
                (FilesystemFile, layer), IBrowserPublisher
            )

    template_manager = factory(layer)
    template_manager.registerDirectory(directory)

    return template_manager


def templateOverridesDirective(_context, directory, layer=interface.Interface):
    # All template overrides must be loaded *after* the deprecations from
    # the deprecatedTemplatesDirective have been loaded, otherwise the
    # deprecations are not effective.  So set a higher order here.
    # zope.configuration uses the 'order' key for determining the
    # order in which it executes any registered actions.
    _context.action(
        discriminator=('jbot', directory, layer),
        callable=handler,
        args=(directory, layer),
        order=1000,
    )


def deprecatedTemplatesDirective(_context, dictionary):
    # Discriminators must be hashable.
    dict_discriminator = "-".join(sorted(dictionary.keys()))
    _context.action(
        discriminator=('jbot', dict_discriminator),
        callable=update_deprecated_templates_dict,
        args=(dictionary,),
        # Explicitly set the order just to be clear, although zero is the
        # default.
        order=0,
    )
