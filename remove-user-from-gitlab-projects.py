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
# Requires requests
import requests
import argparse
import json

with open('config.json') as json_data:
    config = json.load(json_data)
    json_data.close()

parser = argparse.ArgumentParser()
parser.add_argument('groupname',
                    help='name for GitLab group e.g. cs-140-01-02-spring-2014')
args = parser.parse_args()

baseURL = config['gitlabURL'] + 'api/v4/'
basePayload = {'private_token': config['gitlabToken']}

def main():
    userId = getGitlabID(config['gitlabUsername'])
    removeUserFromGroupProjects(userId, args.groupName)

def removeUserFromGroupProjects(userId, groupName):
    groupProjects = getGroupProjects(getGroupId(groupName))
    for project in groupProjects:
        removeUserFromProjects(userId, getForks(project))

def removeUserFromProjects(userId, projects):
    for project in projects.json():
        removeUserFromProject(userId, project['id'])

def removeUserFromProject(userId, projectId):
    url = baseUrl + 'projects/' + str(projectId) + '/members/' + userId
    requests.delete(url, params=basePayload)

def getGroupProjects(groupId):
    url = baseUrl + 'groups/' + str(groupId) + '/projects?per_page=100'
    return requests.get(url, params=basePayload)

def getForks(project):
    url = baseUrl + 'projects/' + str(project['id']) + '/forks?per_page=100'
    return requests.get(url, params=basePayload)

def getGitlabID(gitlabUsername):
    url = baseURL + 'users'
    userInfo = requests.get(url, params=addToBasePayload('username', gitlabUsername))
    return userInfo.json()[0]['id']

def getGroupId(groupName):
    url = baseUrl + 'groups'
    groupInfo = requests.get(url, params=addToBasePayload('search', groupName))
    return groupInfo.json()[0]['id']

def addToBasePayload(key, value):
    payload = basePayload.copy()
    payload[key] = value
    return payload

if __name__== "__main__":
  main()