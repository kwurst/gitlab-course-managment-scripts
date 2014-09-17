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
#    directory is the path to the local directory where the projects should be cloned
#
# Requires pyapi-gitlab https://github.com/Itxaka/pyapi-gitlab version 6.2.3
#
# Reads your private GitLab API token from the file gitlabtoken.txt

import argparse
import csv
import sys
import os
import subprocess
import json
import gitlab   # Requires pyapi-gitlab https://github.com/Itxaka/pyapi-gitlab

with open('config.json') as json_data:
    config = json.load(json_data)
    json_data.close()

# Set up to parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('project', help='Path and namespace project was cloned from')
parser.add_argument('directory', help='Directory to clone the projects into')
args = parser.parse_args()

PIPE = subprocess.PIPE

# Create a GitLab object
git = gitlab.Gitlab(config['gitlab_url'], config['gitlab_token'], verify_ssl=config['verify_ssl'])

# Change to the directory for the assignment
os.chdir(args.directory)

# Get list of all directories
onlydirectories = [ f for f in os.listdir() \
                    if not os.path.isfile(os.path.join(os.curdir,f)) ]

# Get all projects of which I am a member
projects = []
# GitLab will only return projects in pages of max 100 projects
pageno = 1
pageprojects = git.getprojects(page=pageno, per_page=100)
while (len(pageprojects) > 0):
    projects = projects + pageprojects
    pageno = pageno + 1
    pageprojects = git.getprojects(page=pageno, per_page=100)
    
for project in projects:
    # Filter them to match the project path and name,
    # and filter out all the groups (weren't forked)
    # path_with_namespace includes group and project name e.g cs-101/lab1
    # so we only get correct course projects
    if 'forked_from_project' in project and \
        project['forked_from_project']['path_with_namespace']==args.project:
        
        # the list of all members (except me) with dashes in between
        # to be used as the directory to clone into
        members_dir = '-'.join([member['username']
                                for member in git.listprojectmembers(project['id'])
                                if member['username']!=config['gitlab_username'])

        # if the directory doesn't exist, clone the repository
        if members_dir not in onlydirectories:
            # the repo URL to clone
            repo_url = project['ssh_url_to_repo']

            # clone the student repository
            process = subprocess.Popen(["git", "clone", repo_url, members_dir], stdout=PIPE, stderr=PIPE)
            stdoutput, stderroutput = process.communicate()
        else:
            # the directory exists, so pull changes
            print("pulling to " + members_dir)
            os.chdir(members_dir)
            process = subprocess.Popen(["git", "pull", "origin", "master"], stdout=PIPE, stderr=PIPE)
            stdoutput, stderroutput = process.communicate()
            os.chdir("..")
