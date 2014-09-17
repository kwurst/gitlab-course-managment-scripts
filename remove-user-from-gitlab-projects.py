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
# Removes the instructor from all GitLab projects forked from a specific group
#   - in this case a course/semester group.
#
#
# Call as:
#   python remove-from-gitlab-projects.py group user
#
# where
#    group is the name of the GitLab group e.g. cs-140-01-02-spring-2014
#    user is the GitLab username of the user to be removed
#
# Requires pyapi-gitlab https://github.com/Itxaka/pyapi-gitlab version 6.2.3
#
# Reads your private GitLab API token from the file gitlabtoken.txt

import argparse
import json
import gitlab   # Requires pyapi-gitlab https://github.com/Itxaka/pyapi-gitlab

with open('config.json') as json_data:
    config = json.load(json_data)
    json_data.close()

# Set up to parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('group', help='Name of the group')
parser.add_argument('user', help='User to remove')
args = parser.parse_args()

# Create a GitLab object
git = gitlab.Gitlab(config['gitlab_url'],
                    config['gitlab_token'],
                    verify_ssl=config['verify_ssl'])

# Get id of user
for user in git.getusers():
    if user['username'] == args.user:
        userid = user['id']

# Get all projects of which I am a member
# Since GitLab returns projects in "pages" you can't get them all at once
projects = []
pageno = 1
# let's get them in the largest batch allowed - 100 per page
pageprojects = git.getprojects(page=pageno, per_page=100)
# get pages as long as we haven't run out of projects
while (len(pageprojects) > 0):
    projects = projects + pageprojects
    pageno = pageno + 1
    pageprojects = git.getprojects(page=pageno, per_page=100)

for project in projects:
    # Filter them to get only projects which were forked from the group
    # and not owned by user
    # (path_with_namespace includes group and project name
    # e.g cs-140-01-02-spring-2014/lab1
    # so we only get correct semester projects)
    if ('forked_from_project' in project and  # must be forked from group
        project['forked_from_project']['path_with_namespace'].startswith(
            args.group) and
            project['owner']['id'] != userid):   # not owned by user to remove
        print('Removing from: ', project['name_with_namespace'])
        git.deleteprojectmember(project['id'], userid)
