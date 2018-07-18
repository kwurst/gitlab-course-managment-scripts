#!/usr/bin/env python3
# Copyright (C) 2014, 2018 Karl R. Wurst
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA

####################################################################
# Removes the instructor from all GitLab projects forked from a specific group
#   - in this case a course/semester group.
#
# Call as:
#   python remove-from-gitlab-projects.py groupName
#
# where
#    groupName is the name of the GitLab group e.g. cs-140-01-02-spring-2014
#

import argparse
import gitlabapiutilities as gitlab

parser = argparse.ArgumentParser()
parser.add_argument('groupname',
                    help='name for GitLab group e.g. cs-140-01-02-spring-2014')
args = parser.parse_args()

def main():
    userId = gitlab.getUserId(gitlab.config['gitlabUsername'])
    removeUserFromGroupProjects(userId, args.groupName)

def removeUserFromGroupProjects(userId, groupName):
    groupProjects = gitlab.getGroupProjects(gitlab.getGroupId(groupName))
    for project in groupProjects:
        removeUserFromProjects(userId, gitlab.getForks(project['id']))

def removeUserFromProjects(userId, projects):
    for project in projects.json():
        gitlab.removeUserFromProject(userId, project['id'])

if __name__== "__main__":
  main()