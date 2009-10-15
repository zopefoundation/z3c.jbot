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

logger.info("Patching page template classes for use with z3c.jbot...")

registry = {}

for pt_class in PT_CLASSES:
    def get(template, view=None, cls=None):
        layer = utility.getLayer()
        key = layer, template
        inst = registry.get(key)
        if inst is None:
            cls = type(template)
            inst = registry[key] = cls.__new__(cls)
            inst.__dict__ = template.__dict__.copy()

        for manager in utility.getManagers():
            # register template; this call returns ``True`` if
            # template was invalidated
            if manager.registerTemplate(inst, template):
                break

        return inst

    pt_class.__get__ = get
