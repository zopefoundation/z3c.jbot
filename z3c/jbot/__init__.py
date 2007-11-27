import manager
from zope.pagetemplate.pagetemplatefile import PageTemplate

# add registration hook to ``zope.app.pagetemplate``
pt_render = PageTemplate.pt_render
def patched_pt_render(self, *args, **kwargs):
    manager.getGlobalTemplateManager().registerTemplate(self)
    return pt_render(self, *args, **kwargs)

PageTemplate.pt_render = patched_pt_render
