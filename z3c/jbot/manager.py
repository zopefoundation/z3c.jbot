import sys
import os.path

IGNORE = object()

def root_length(a, b):
    if b.startswith(a):
        return len(a)
    else:
        return 0

def find_package(syspaths, path):
    """Determine the Python-package where path is located.  If the path is
    not located within the Python sys-path, return ``None``."""

    _syspaths = sorted(
        syspaths, key=lambda syspath: root_length(syspath, path), reverse=True)

    syspath = _syspaths[0]
    
    path = os.path.normpath(path)
    if not path.startswith(syspath):
        return None
    
    path = path[len(syspath):]
    
    # convert path to dotted filename
    if path.startswith(os.path.sep):
        path = path[1:]
        
    return path
    
class GlobalTemplateManager(object):
    def __init__(self):
        self.syspaths = tuple(sys.path)
        self.templates = {}
        self.paths = {}
        
    def registerDirectory(self, directory):
        for filename in os.listdir(directory):
            if filename.endswith('.pt'):
                self.paths[filename] = "%s/%s" % (directory, filename)

    def unregisterDirectory(self, directory):
        for filename in os.listdir(directory):
            if filename in self.paths:
                del self.paths[filename]
        
    def registerTemplate(self, template):
        # only register templates that have a filename attribute
        if not hasattr(template, 'filename'):
            return
        
        # assert that template is not already registered
        filename = self.templates.get(template)
        if filename is IGNORE:
            return

        if self.paths.get(filename) == template.filename:
            return

        if filename is not None and filename not in self.paths:
            # template file has been unregistered; restore
            # original template
            template.filename = template._filename
            delattr(template, '_filename')

        path = find_package(self.syspaths, template.filename)
        if path is None:
            self.templates[template] = IGNORE
            return
        
        filename = path.replace(os.path.sep, '.')

        if filename in self.paths:
            path = self.paths[filename]
            
            # save original filename
            template._filename = template.filename

            # save template and registry and assign path
            template.filename = path
            self.templates[template] = filename

        template._v_last_read = False
        
GlobalTemplateManager = GlobalTemplateManager()

def getGlobalTemplateManager():
    return GlobalTemplateManager
