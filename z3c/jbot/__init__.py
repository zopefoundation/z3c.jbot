from zope.pagetemplate.pagetemplatefile import PageTemplateFile

import utility
import logging
import threading

logger = logging.getLogger('jbot')

PT_CLASSES = [PageTemplateFile]

try:
    import Products.PageTemplates.PageTemplateFile
    PT_CLASSES.append(Products.PageTemplates.PageTemplateFile.PageTemplateFile)
except:
    pass

_v_cache = threading.local()

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
        __dict__ = template.__dict__

        # note: exceptions should not arise during normal service
        try:
            layer = _v_cache.layer
        except AttributeError:
            layer = None

        try:
            # any of these could raise a key-error
            attrs = __dict__['_v_attrs']
            return attrs[layer, key]
        except KeyError:
            return __dict__.get(key) or self.default

    def _set(self, template, value):
        key = self.name
        __dict__ = template.__dict__

        # note: exceptions should not arise during normal service
        try:
            layer = _v_cache.layer
        except AttributeError:
            layer = None

        try:
            attrs = __dict__['_v_attrs']
        except KeyError:
            attrs = __dict__['_v_attrs'] = {}

        attrs[layer, key] = value
        __dict__.setdefault(key, value)

# registration hook to template manager
def jbot(func):
    def patch(self, *args, **kwargs):
        _v_cache.layer = utility.getLayer()

        for manager in utility.getManagers():
            # register template; this call returns ``True`` if
            # template was invalidated
            if manager.registerTemplate(self):
                break

        return func(self, *args, **kwargs)
    return patch

logger.info("Patching page template classes for use with z3c.jbot...")

# patch ``_cook_check``-method to insert jbot-logic
for pt_class in PT_CLASSES:
    pt_class._cook_check = jbot(pt_class._cook_check)

# munge per-layer attribute descriptors on class
for pt_class in PT_CLASSES:
    for name in ('_v_macros', '_v_program', '_v_cooked', '_v_errors',
                 '_v_last_read', '_v_warning', '_text_',
                 'filename', '_filename', 'content_type', 'is_html'):
        setattr(pt_class, name, LayerProperty(pt_class, name))
