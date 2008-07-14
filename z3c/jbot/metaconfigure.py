from zope import interface
from zope import component

import manager
import interfaces

def handler(directory, layer):
    gsm = component.getGlobalSiteManager()

    # check if a template manager already exists
    factory = gsm.adapters.lookup((layer,), interfaces.ITemplateManager)

    if factory is None:
        factory = TemplateManagerFactory()
        component.provideAdapter(factory, (layer,), interfaces.ITemplateManager)

    factory.manager.registerDirectory(directory)

def templateOverridesDirective(_context, directory, layer=interface.Interface):
    _context.action(
        discriminator = ('override', directory, layer),
        callable = handler,
        args = (directory, layer),
        )
