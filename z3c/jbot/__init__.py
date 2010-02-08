from zope.pagetemplate.pagetemplatefile import PageTemplateFile

try:
    from Acquisition.interfaces import IAcquirer
except ImportError:
    IAcquirer = None

import utility
import logging

logger = logging.getLogger('jbot')

# Standard PageTemplateFile

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
            inst._v_last_read = False
            break

    if view is not None and IAcquirer is not None:
        if IAcquirer.providedBy(inst) and IAcquirer.providedBy(view):
            return inst.__of__(view)

    return inst

for pt_class in PT_CLASSES:
    pt_class.__get__ = get
    logger.info(repr(pt_class))

# Zope 2.12 ViewPageTemplateFile

try:
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile
    from Products.Five.browser.pagetemplatefile import BoundPageTemplate as FiveBoundPageTemplate
except ImportError:
    pass
else:
    pt_class = FiveViewPageTemplateFile
    bind = pt_class.__get__

    def five_get_and_bind(template, view=None, cls=None):
        inst = get(template, view, cls)
        if inst._v_last_read is False:
            inst.read()
        return bind(inst, view, cls)

    pt_class.__get__ = five_get_and_bind
    logger.info(repr(pt_class))

# five.pt / Chameleon

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

# CMF skin layer resources

try:
    import Products.CMFCore.FSObject
except ImportError:
    pass
else:
    fs_class = Products.CMFCore.FSObject.FSObject

    def get_skin_obj(obj, view=None, cls=None):
        layer = utility.getLayer()
        key = layer, obj
        inst = registry.get(key)
        if inst is None:
            cls = type(obj)
            inst = registry[key] = cls.__new__(cls)
            inst.__dict__ = obj.__dict__.copy()

        for manager in utility.getManagers():
            # register template; this call returns ``True`` if the
            # template was invalidated (changed filename)
            if manager.registerTemplate(inst, obj):
                inst._parsed = False
                inst.getObjectFSPath()

        return inst

    def get_filename(obj, *args):
        return obj._filepath

    def set_filename(obj, value, *args):
        obj._filepath = value

    fs_class.__get__ = get_skin_obj
    fs_class.filename = property(get_filename, set_filename)

    logger.info(repr(fs_class))
