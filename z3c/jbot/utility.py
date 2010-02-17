from zope import interface
from zope import component

try:
    from zope.site.hooks import getSite
except ImportError:
    from zope.app.component.hooks import getSite

from zope.publisher.interfaces import IRequest

import zope.security.management
import zope.security.interfaces

import interfaces

try:
    import Acquisition
    ZOPE_2 = True
except:
    ZOPE_2 = False

def getRequest():
    if ZOPE_2:
        # get request by acquisition
        site = getSite()
        if site is not None:
            try:
                return site.request
            except AttributeError:
                return site.REQUEST

    try:
        i = zope.security.management.getInteraction()
    except zope.security.interfaces.NoInteraction:
        return

    for p in i.participations:
        if IRequest.providedBy(p):
            return p

def getLayer():
    request = getRequest()

    if request is not None:
        return interface.providedBy(request)

    return interface.Interface

def getManagers():
    layer = getLayer()
    gsm = component.getGlobalSiteManager()

    for name, factory in reversed(
        gsm.adapters.lookupAll((layer,), interfaces.ITemplateManager)):
        yield factory(layer)
