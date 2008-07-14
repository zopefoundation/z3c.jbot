from zope.pagetemplate.pagetemplatefile import PageTemplateFile

import manager
import utility

NO_DEFAULT = object()

class LayerProperty(property):
    """Layer-specific property class.

    Instance attributes are instance *and* layer-specific when defined
    using this property class.
    """
    
    def __init__(self, name):
        self.name = name
        self.default = getattr(PageTemplateFile, name, NO_DEFAULT)
        property.__init__(self, self._get, self._set)
        
    def _get(self, template):
        layer = utility.getLayer()
        attributes = getattr(template, '_v_attrs', template.__dict__)
        key = self.name
        if (layer, key) in attributes:
            return attributes[layer, key]

        return self.default
    
    def _set(self, template, value):
        layer = utility.getLayer()
        template.__dict__.setdefault('_v_attrs', {})[layer, self.name] = value
        if self.default is NO_DEFAULT:
            self.default = value
            
# registration hook to template manager
def jbot(func):
    def patch(self, *args, **kwargs):
        manager = utility.getManager()
        if manager is not None:
            manager.registerTemplate(self)
        
        return func(self, *args, **kwargs)        
    return patch

# patch ``_cook_check``-method to insert jbot-logic
PageTemplateFile._cook_check = jbot(PageTemplateFile._cook_check)
try:
    from Products.PageTemplates.PageTemplateFile import PageTemplateFile as Z2PageTemplateFile
    Z2PageTemplateFile._cook_check = jbot(Z2PageTemplateFile._cook_check)
except ImportError:
    pass

# munge per-layer attribute descriptors on class
for name in ('_v_macros', '_v_program', '_v_cooked', '_v_errors',
             '_v_last_read', '_v_warning', '_text_', 'filename'):
    setattr(PageTemplateFile, name, LayerProperty(name))
