from zope.pagetemplate.pagetemplatefile import PageTemplateFile

import manager
import utility

PT_CLASSES = [PageTemplateFile]

if utility.ZOPE_2:
    import Products.PageTemplates.PageTemplateFile
    PT_CLASSES.append(Products.PageTemplates.PageTemplateFile.PageTemplateFile)

class LayerProperty(property):
    """Layer-specific property class.

    Instance attributes are instance *and* layer-specific when defined
    using this property class.

    Lookup order:

      1. By layer
      2. By instance
      3. By class

    This pattern takes into account that attributes may be set before
    the property is defined on the class.
    """
    
    def __init__(self, cls, name):
        self.name = name
        self.default = getattr(cls, name, None)
        property.__init__(self, self._get, self._set)
        
    def _get(self, template):
        key = self.name
        layer = utility.getLayer()
        attrs = getattr(template, '_v_attrs', template.__dict__)
        if (layer, key) in attrs:
            return attrs[layer, key]
        return attrs.get(key) or template.__dict__.get(key) or self.default
    
    def _set(self, template, value):
        key = self.name
        layer = utility.getLayer()
        attrs = template.__dict__.get('_v_attrs')
        if attrs is None:
            attrs = template._v_attrs = {}

        # set value
        attrs[layer, key] = value
            
        # set default value
        attrs.setdefault(key, value)
            
# registration hook to template manager
def jbot(func):
    def patch(self, *args, **kwargs):
        manager = utility.getManager()
        if manager is not None:
            manager.registerTemplate(self)
        
        return func(self, *args, **kwargs)        
    return patch

for pt_class in PT_CLASSES:
    # patch ``_cook_check``-method to insert jbot-logic
    pt_class._cook_check = jbot(pt_class._cook_check)

    # munge per-layer attribute descriptors on class
    for name in ('_v_macros', '_v_program', '_v_cooked', '_v_errors',
                 '_v_last_read', '_v_warning', '_text_',
                 'filename', 'content_type', 'is_html'):
        setattr(pt_class, name, LayerProperty(pt_class, name))
