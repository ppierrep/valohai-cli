import os

import valohai_yaml

from valohai_cli.exceptions import NoProject
from valohai_cli.settings import settings
from valohai_cli.utils import get_project_directory, walk_directory_parents


class Project:
    def __init__(self, data, directory=None):
        self.data = data
        self.directory = directory

    id = property(lambda p: p.data['id'])
    name = property(lambda p: p.data['name'])

    def get_config(self):
        filename = os.path.join(self.directory, 'valohai.yaml')
        with open(filename) as infp:
            config = valohai_yaml.parse(infp)
            config.project = self
            return config


def get_project(dir=None, require=False):
    """
    Get the Valohai project object for a directory context.

    The object is augmented with the `dir` key.

    :param dir: Directory (defaults to cwd)
    :param require: Raise an exception if no project is found
    :return: Project object, or None.
    :rtype: Project|None
    """
    links = settings.get('links') or {}
    if not links:
        if require:
            raise NoProject('No projects are configured')
        return None
    orig_dir = dir or get_project_directory()
    for dir in walk_directory_parents(orig_dir):
        project_obj = links.get(dir)
        if project_obj:
            return Project(data=project_obj, directory=dir)
    if require:
        raise NoProject('No project is linked to %s' % orig_dir)
    return None
