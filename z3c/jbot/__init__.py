from zope.pagetemplate.pagetemplatefile import PageTemplateFile

import utility
import logging

logger = logging.getLogger('jbot')

PT_CLASSES = [PageTemplateFile]

try:
    import Products.PageTemplates.PageTemplateFile
    PT_CLASSES.append(Products.PageTemplates.PageTemplateFile.PageTemplateFile)
except:
    pass

registry = {}

def get(template, view=None, cls=None):
    layer = utility.getLayer()
    key = layer, template
    inst = registry.get(key)
    if inst is None:
        cls = type(template)
        inst = registry[key] = cls.__new__(cls)
        inst.__dict__ = template.__dict__.copy()

    for manager in utility.getManagers():
        # register template; this call returns ``True`` if the
        # template was invalidated (changed filename)
        if manager.registerTemplate(inst, template):
            break

    return inst

try:
    import five.pt.pagetemplate
except ImportError:
    pass
else:
    pt_class = five.pt.pagetemplate.ViewPageTemplateFile
    bind = pt_class.__get__

    def get_and_bind(template, view=None, cls=None):
        inst = get(template, view, cls)
        if inst._v_last_read is False:
            inst.registry.purge()
            inst.read()
        return bind(inst, view, cls)

    pt_class.__get__ = get_and_bind
    logger.info(repr(pt_class))

for pt_class in PT_CLASSES:
    pt_class.__get__ = get
    logger.info(repr(pt_class))
