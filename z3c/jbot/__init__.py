import manager
from zope.pagetemplate.pagetemplatefile import PageTemplateFile

# add registration hook to ``zope.app.pagetemplate``
def jbot(func):
    def jbot_func(self, *args, **kwargs): 
        manager.getGlobalTemplateManager().registerTemplate(self)
        return func(self, *args, **kwargs)        
    return jbot_func

PageTemplateFile._cook_check = jbot(PageTemplateFile._cook_check)
try:
    from Products.PageTemplates.PageTemplateFile import PageTemplateFile as Z2PageTemplateFile
    Z2PageTemplateFile._cook_check = jbot(Z2PageTemplateFile._cook_check)
except ImportError:
    raise


