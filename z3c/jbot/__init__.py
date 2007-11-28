import manager
from zope.pagetemplate.pagetemplatefile import PageTemplate

# add registration hook to ``zope.app.pagetemplate``
def jbot(pt_render):
    def render(self, *args, **kwargs): 
        manager.getGlobalTemplateManager().registerTemplate(self)
        return pt_render(self, *args, **kwargs)        
    return render

PageTemplate.pt_render = jbot(PageTemplate.pt_render)
