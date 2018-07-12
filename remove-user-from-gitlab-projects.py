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
#
# Call as:
#   python remove-from-gitlab-projects.py group user
#
# where
#    group is the name of the GitLab group e.g. cs-140-01-02-spring-2014
#    user is the GitLab username of the user to be removed
#
# Requires requests
import requests

# need to fill in your GitLab access token here.
token = ''
# your GitLab user id (from User Settings> Profile)
userid = ''
# groupname can be a subgroup
groupname = ''

# get the group id
url = 'https://gitlab.com/api/v4/groups'
payload = {'private_token': token,
           'search': groupname}
groupinfo = requests.get(url, params=payload)
groupid = groupinfo.json()[0]['id']
print(groupid)

# get the group's projects
url = 'https://gitlab.com/api/v4/groups/' + str(groupid) + '/projects?per_page=100'
payload = {'private_token': token}
groupprojects = requests.get(url, params=payload)

for project in groupprojects.json():

    # get the forks of the project
    projectid = project['id']
    print(project['name'])
    url = 'https://gitlab.com/api/v4/projects/' + str(projectid) + '/forks?per_page=100'
    payload = {'private_token': token}
    forks = requests.get(url, params=payload)

    for fork in forks.json():
        print(fork['name_with_namespace'])
        forkid = fork['id']

        # remove the user from the members of the fork
        url = 'https://gitlab.com/api/v4/projects/' + str(forkid) + '/members/' + userid
        payload = {'private_token': token}
        requests.delete(url, params=payload)
