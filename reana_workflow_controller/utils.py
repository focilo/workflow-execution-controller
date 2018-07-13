# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2017, 2018 CERN.
#
# REANA is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# REANA is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# REANA; if not, write to the Free Software Foundation, Inc., 59 Temple Place,
# Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization or
# submit itself to any jurisdiction.
"""Workflow persistence management."""

import fs
import fs.path as fs_path
from flask import current_app as app
from reana_commons.utils import get_user_workflows_dir


def create_workflow_workspace(path):
    """Create workflow workspace.

    :param path: Relative path to workspace directory.
    :return: Absolute workspace path.
    """
    reana_fs = fs.open_fs(app.config['SHARED_VOLUME_PATH'])
    if not reana_fs.exists(path):
        reana_fs.makedirs(path)


def get_workflow_files_dir(workflow, file_type, action='list'):
    """Given a workflow and a file type, returns path to the file type dir."""
    workspace = get_workflow_dir(workflow)
    if action == 'list':
        return fs_path.join(workspace,
                            app.config['ALLOWED_LIST_DIRECTORIES'][file_type])
    elif action == 'seed':
        return fs_path.join(workspace,
                            app.config['ALLOWED_SEED_DIRECTORIES'][file_type])


def list_directory_files(directory):
    """Return a list of files inside a given directory."""
    fs_ = fs.open_fs(directory)
    file_list = []
    for file_name in fs_.walk.files():
        file_details = fs_.getinfo(file_name, namespaces=['details'])
        file_list.append({'name': file_name.lstrip('/'),
                          'last-modified': file_details.modified.isoformat(),
                          'size': file_details.size})
    return file_list
