from zope import interface
from zope import component

from zope.app.component.hooks import getSite
from zope.publisher.interfaces import IRequest

import zope.security.management
import zope.security.interfaces

import interfaces

try:
    import Products.PageTemplates
    ZOPE_2 = True
except ImportError:
    ZOPE_2 = False

def getRequest():
    try:
        i = zope.security.management.getInteraction()
        for p in i.participations:
            if IRequest.providedBy(p):
                return p
    except zope.security.interfaces.NoInteraction:
        pass
    
    if ZOPE_2:
        # get request by acquisition
        site = getSite()
        if site is not None:
            return site.REQUEST
    
def getLayer():
    request = getRequest()

    if request is not None:
        return interface.providedBy(request)

    return interface.Interface

def getManager():
    layer = getLayer()
    gsm = component.getGlobalSiteManager()
        
    factory = gsm.adapters.lookup((layer,), interfaces.ITemplateManager)
    if factory is not None:
        return factory.manager
