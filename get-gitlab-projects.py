#!/usr/bin/env python3
# Copyright (C) 2014 Karl R. Wurst
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
# Gets (clones) all GitLab projects that were forked from a particular project.
#
# This script was written for the following use-case:
#
# The user is an instructor using GitLab for students to submit assignments.
# The instructor created a GitLab project from which the students fork their
#   own copy.
# The students have added the instructor to their project as at least a
#   "Reporter" for the instructor to be able to clone the project, or as at
#   at least a "Developer" for the instructor to push changes.
#
# Call as:
#   python get-gitlab-projects.py project-name directory
#
# where
#    project-name is the name of the GitLab namespace/projectname
#      e.g. kwurst/Lab1 or cs-100/Lab1
#      This is everything after the / after the server URL. In the examples:
#      http://gitlab.myschool.edu/kwurst/Lab1
#      http://gitlab.myschool.edu/cs-100/Lab1
#    directory is the path to the local directory
#      where the projects should be cloned
#
# Requires pyapi-gitlab https://github.com/Itxaka/pyapi-gitlab version 6.2.3
#
# Reads your private GitLab API token from the file gitlabtoken.txt

import argparse
import gitlabapiutilities as gitlab

parser = argparse.ArgumentParser()
parser.add_argument('groupName',
                    help='name for GitLab group e.g. cs-140-01-02-spring-2014')
parser.add_argument('projectName',
                    help='Path and namespace project was cloned from')
parser.add_argument('directory', help='Directory to clone the projects into')
args = parser.parse_args()

def main():
    groupId = gitlab.getGroupId(args.groupName)
    projectId = gitlab.getGroupProjectIdByName(groupId, args.projectName)
    gitlab.cloneForks(projectId, args.directory)

if __name__== "__main__":
  main()