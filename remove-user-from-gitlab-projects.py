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
# Removes the instructor from all GitLab projects forked from a specific group -
#   in this case a course/semester group.
#
#
# Call as:
#   python remove-from-gitlab-projects.py group user
#
# where
#    group is the name of the GitLab group e.g. cs-140-01-02-spring-2014
#    user is the GitLab username of the user to be removed
#
# Requires pyapi-gitlab https://github.com/Itxaka/pyapi-gitlab version 6.2
#   Version 6.2 (as installed by pip) has some errors - not updated for Python 3
#      /Library/Frameworks/Python.framework/Versions/3.3/lib/python3.3/site-packages/gitlab/__init__.py
#         Lines 994, 995 are missing parentheses for print
#         Line 518 needs 'verify=self.verify_ssl' in request
#      /Library/Frameworks/Python.framework/Versions/3.3/lib/python3.3/site-packages/tests/pyapi-gitlab_test.py
#         Line 162 is missing parentheses for print
# 
# Reads your private GitLab API token from the file gitlabtoken.txt

import argparse
import gitlab   # Requires pyapi-gitlab https://github.com/Itxaka/pyapi-gitlab

GITLAB_URL = 'https://git.cs.worcester.edu'     # replace with yours

# Set up to parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('group', help='Name of the group')
parser.add_argument('user', help='User to remove')
parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
args = parser.parse_args()

# Get my private GitLab token
# stored in a file so that I can .gitignore the file
token = open('gitlabtoken.txt').readline().strip()

# Create a GitLab object
# For our server, verify_ssl has to be False, since we have a self-signed certificate
git = gitlab.Gitlab(GITLAB_URL, token, verify_ssl=False)

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
    # Filter them to get only projects which were forked from the group and not owned by user
    # (path_with_namespace includes group and project name e.g cs-140-01-02-spring-2014/lab1
    # so we only get correct semester projects)
    if ('forked_from_project' in project and    # needs to have been forked from group
       project['forked_from_project']['path_with_namespace'].startswith(args.group) and 
       project['owner']['id'] != userid):        # not owned by user to be removed
        print('Removing from: ', project['name_with_namespace'])
        git.deleteprojectmember(project['id'], userid)



        
