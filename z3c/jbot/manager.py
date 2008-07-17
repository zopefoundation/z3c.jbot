from zope import interface

import os
import sys

import utility
import interfaces

IGNORE = object()

def root_length(a, b):
    if b.startswith(a):
        return len(a)
    else:
        return 0

def find_zope2_product(path):
    """Check the Zope2 magic Products semi-namespace to see if the
    path is part of a Product."""
    _syspaths = sorted(
                sys.modules["Products"].__path__,
                key=lambda syspath: root_length(syspath, path), reverse=True)
    syspath = _syspaths[0]

    if not path.startswith(syspath):
        return None

    product = path[len(syspath)+1:].split(os.path.sep, 2)[0]

    return "Products." + product


def find_package(syspaths, path):
    """Determine the Python-package where path is located.  If the path is
    not located within the Python sys-path, return ``None``."""

    _syspaths = sorted(
        syspaths, key=lambda syspath: root_length(syspath, path), reverse=True)

    syspath = _syspaths[0]
    
    path = os.path.normpath(path)
    if not path.startswith(syspath):
        if utility.ZOPE_2:
            return find_zope2_product(path)
        return None
    
    path = path[len(syspath):]
    
    # convert path to dotted filename
    if path.startswith(os.path.sep):
        path = path[1:]
        
    return path

class TemplateManagerFactory(object):
    def __init__(self):
        self.manager = TemplateManager()

    def __call__(self, layer):
        return self.manager
    
class TemplateManager(object):
    interface.implements(interfaces.ITemplateManager)
    
    def __init__(self):
        self.syspaths = tuple(sys.path)
        self.templates = {}
        self.paths = {}

    def registerDirectory(self, directory):
        for filename in os.listdir(directory):
            if filename.endswith('.pt'):
                self.paths[filename] = "%s/%s" % (directory, filename)

        for template, filename in self.templates.items():
            if filename is IGNORE:
                del self.templates[template]

    def unregisterDirectory(self, directory):
        templates = []
        
        for template, filename in self.templates.items():
            if filename in self.paths:
                templates.append(template)

        for filename in os.listdir(directory):
            if filename in self.paths:
                del self.paths[filename]

        for template in templates:
            self.registerTemplate(template)
            del self.templates[template]
            
    def registerTemplate(self, template):
        # only register templates that have a filename attribute
        if not hasattr(template, 'filename'):
            return
        
        # assert that the template is not already registered
        filename = self.templates.get(template)
        if filename is IGNORE:
            return

        # if the template filename matches an override, we're done
        paths = self.paths
        if paths.get(filename) == template.filename:
            return

        # verify that override has not been unregistered
        if filename is not None and filename not in paths:
            # restore original template
            template.filename = template._filename
            delattr(template, '_filename')
            del self.templates[template]
            
        # check if an override exists
        path = find_package(self.syspaths, template.filename)
        if path is None:
            # permanently ignore template
            self.templates[template] = IGNORE
            return
        
        filename = path.replace(os.path.sep, '.')
        if filename in paths:
            path = paths[filename]

            # save original filename
            template._filename = template.filename

            # save template and registry and assign path
            template.filename = path
            self.templates[template] = filename
        else:
            self.templates[template] = IGNORE

        # force cook
        template._v_last_read = False

        return True
