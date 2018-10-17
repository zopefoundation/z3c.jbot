from zope import component
from zope import interface

from . import interfaces
from . import manager


def handler(directory, layer):
    lookup_all = component.getGlobalSiteManager().adapters.lookupAll

    # check if a template manager already exists
    factories = set(
        factory
        for name, factory in lookup_all((layer,), interfaces.ITemplateManager)
    )

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
        factory = manager.TemplateManagerFactory(name)
        component.provideAdapter(
            factory, (layer,), interfaces.ITemplateManager, name=name
        )

    factory(layer).registerDirectory(directory)

    return factory(layer)


def templateOverridesDirective(_context, directory, layer=interface.Interface):
    _context.action(
        discriminator=('jbot', directory, layer),
        callable=handler,
        args=(directory, layer),
    )
