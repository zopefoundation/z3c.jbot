from zope.interface import Interface
from zope.interface import providedBy
from zope.component import getGlobalSiteManager

try:
    from zope.site.hooks import getSite
except ImportError:
    from zope.app.component.hooks import getSite

from zope.publisher.interfaces import IRequest

import zope.security.management
import zope.security.interfaces

from z3c.jbot.interfaces import ITemplateManager


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


def getLayer(request):

    if request is not None:
        return providedBy(request)

    return Interface


MANAGER_CACHE_KEY = 'z3c.jbot.cached_managers'


def getManagers(layer, request):
    if not request:
        return []
    try:
        adapters = getGlobalSiteManager().adapters._adapters[1]
    except IndexError:
        return []

    if MANAGER_CACHE_KEY in request.environ:
        return request.environ[MANAGER_CACHE_KEY]

    all_managers = []
    for iface in layer.__sro__:
        by_interface = adapters.get(iface)

        if by_interface is not None:
            managers = by_interface.get(ITemplateManager)

            if managers is not None:
                items = managers.items()
                if len(items) > 1:
                    items = sorted(items)

                for name, factory in items:
                    all_managers.append(factory(layer))
    all_managers.sort(key=lambda m: m.order)
    request.environ[MANAGER_CACHE_KEY] = all_managers
    return all_managers
