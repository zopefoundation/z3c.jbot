import sys
import os.path

import threading

def root_length(a, b):
    if b.startswith(a):
        return len(a)
    else:
        return 0

def find_package(path):
    # find out in which package this file is located
    syspaths = sys.path
    syspaths.sort(key=lambda syspath: root_length(syspath, path),
                  reverse=True)
        
    path = path[len(syspaths[0]):]

    # convert path to dotted filename
    if path.startswith(os.path.sep):
        path = path[1:]

    return path
    
class GlobalTemplateManager(threading.local):
    def __init__(self):
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
        if self.paths.get(filename) == template.filename:
            return

        if filename and filename not in self.paths:
            # template file has been unregistered; restore
            # original template
            template.filename = template._filename
            delattr(template, '_filename')
                        
        path = find_package(template.filename)
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
