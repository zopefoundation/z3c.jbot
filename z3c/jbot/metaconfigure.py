from zope import interface
from zope import component

import manager
import interfaces

def handler(directory, layer):
    gsm = component.getGlobalSiteManager()

    # check if a template manager already exists
    factories = set(factory for name, factory in gsm.adapters.lookupAll(
        (layer,), interfaces.ITemplateManager))

    # if factory is available on the interface bases of the layer we
    # discard it and register a new manager specialized to the layer
    if layer is interface.Interface:
        base_factories = set()
    else:
        base_factories = set(factory for name, factory in gsm.adapters.lookupAll(
            (interface.implementedBy(layer.__bases__),), interfaces.ITemplateManager))

    try:
        factory = factories.difference(base_factories).pop()
    except KeyError:
        factory = manager.TemplateManagerFactory()
        component.provideAdapter(
            factory, (layer,), interfaces.ITemplateManager, name=directory)

    factory(layer).registerDirectory(directory)
    
def templateOverridesDirective(_context, directory, layer=interface.Interface):
    _context.action(
        discriminator = ('override', directory, layer),
        callable = handler,
        args = (directory, layer),
        )
