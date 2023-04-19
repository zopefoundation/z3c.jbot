import os
import sys

from zope.interface import implementer

from . import interfaces
from . import utility


IGNORE = object()
DELETE = object()


def normalize(filepath):
    return os.path.normcase(os.path.normpath(filepath))


def root_length(a, b):
    if b.startswith(a):
        return len(a)
    return 0


def sort_by_path(path, paths):
    return sorted(
        paths, key=lambda syspath: root_length(syspath, path), reverse=True
    )


def find_zope2_product(path):
    """Check the Zope 5 magic Products semi-namespace to see if the
    path is part of a Product."""
    _syspaths = sort_by_path(
        path,
        [normalize(path) for path in sys.modules["Products"].__path__],
    )
    syspath = _syspaths[0]

    if not path.startswith(syspath):
        return

    product = path[len(syspath) + 1:].split(os.path.sep, 2)[0]

    return normalize("Products." + product)


def find_package(syspaths, path):
    """Determine the Python-package where path is located.  If the path is
    not located within the Python sys-path, return ``None``.
    The returned path is already 'normcase'. """

    _syspaths = sort_by_path(path, syspaths)
    syspath = _syspaths[0]

    if not path.startswith(syspath):
        if not utility.ZOPE_3:
            return find_zope2_product(path)
        return None

    path = path[len(syspath):]

    # convert path to dotted filename
    if path.startswith(os.path.sep):
        path = path[1:]
    return path


class ResourceManagerFactory:
    def __init__(self, name):
        self.manager = TemplateManager(name)

    def __call__(self, layer):
        return self.manager


class TemplateManagerFactory:
    def __init__(self, name):
        self.manager = TemplateManager(name)

    def __call__(self, layer):
        return self.manager


@implementer(interfaces.ITemplateManager)
class TemplateManager:
    def __init__(self, name):
        self.syspaths = {normalize(p) for p in sys.path}
        self.resources = {}
        self.templates = {}
        self.paths = {}
        self.directories = set()
        self.name = name

    def registerDirectory(self, directory):
        directory = normalize(directory)
        self.directories.add(directory)

        for filename in os.listdir(directory):
            filename = os.path.normcase(filename)
            self.paths[filename] = normalize(
                "%s%s%s" %
                (directory, os.path.sep, filename))

        for template, filename in list(self.templates.items()):
            if filename is IGNORE:
                del self.templates[template]

    def unregisterDirectory(self, directory):
        directory = normalize(directory)
        self.directories.remove(directory)

        templates = []

        for template, filename in self.templates.items():
            if os.path.normcase(filename) in self.paths:
                templates.append(template)

        for filename in os.listdir(directory):
            if os.path.normcase(filename) in self.paths:
                del self.paths[filename]
        for template in templates:
            inst = template.__get__(self)
            self.registerTemplate(inst, template)
            del self.templates[template]
            inst.filename = inst._filename

    def unregisterAllDirectories(self):
        for directory in tuple(self.directories):
            self.unregisterDirectory(directory)

    def registerTemplate(self, template, token):
        # assert that the template is not already registered
        filename = self.templates.get(token)
        if filename is IGNORE:
            return

        # if the template filename matches an override, we're done
        if filename is not None:
            if self.paths.get(filename) == template.filename:
                return

        # verify that override has not been unregistered
        if filename is not None and filename not in self.paths:
            template.filename = template._filename
            del self.templates[token]

        # check if an override exists
        path = find_package(self.syspaths, normalize(template.filename))
        if path is None:
            # permanently ignore template
            self.templates[token] = IGNORE
            return

        filename = path.replace(os.path.sep, '.')
        if filename not in self.paths:
            self.templates[token] = IGNORE
            template._v_last_read = False
            return

        path = self.paths[filename]

        # save original filename
        template._filename = template.filename

        # save template and registry and assign path
        template.filename = path
        self.templates[token] = os.path.normcase(filename)

        return True

    def queryResourcePath(self, resource):
        path = self.resources.get(resource.path)
        if path is IGNORE:
            return

        if path is not None:
            return path

        path = find_package(self.syspaths, normalize(resource.path))
        if path is None:
            self.resources[resource.path] = IGNORE
            return

        filename = path.replace(os.path.sep, '.')
        resource_path = self.paths.get(filename)
        if resource_path is None:
            self.resources[resource.path] = IGNORE
            return

        return resource_path
