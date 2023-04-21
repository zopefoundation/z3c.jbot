from zope.interface import implementer
from zope.interface import providedBy
from zope.publisher.interfaces.browser import IBrowserPublisher


try:
    from plone.resource.file import FilesystemFile
    HAS_PLONE_RESOURCE = True
except ImportError:
    HAS_PLONE_RESOURCE = False

from .utility import getManagers


@implementer(IBrowserPublisher)
class FilesystemFileResourceBrowserPublisher:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def browserDefault(self, request):
        assert HAS_PLONE_RESOURCE
        layer = providedBy(request)
        for manager in getManagers(layer):
            path = manager.queryResourcePath(self.context)
            if path is not None:
                resource = FilesystemFile(
                    self.context.__parent__,
                    request,
                    path,
                    self.context.__name__,
                )
                break
        else:
            resource = self.context

        return resource, ()
