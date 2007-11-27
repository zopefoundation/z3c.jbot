from zope import component
from z3c.jbot.manager import getGlobalTemplateManager

def templateOverridesDirective(_context, directory):
    getGlobalTemplateManager().registerDirectory(directory)
