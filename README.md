gitlab-course-management-scripts
================================

Python scripts to manage students and projects in GitLab

* Requires pyapi-gitlab from https://github.com/Itxaka/pyapi-gitlab version 6.2.3
* Reads your private GitLab API token from the file gitlabtoken.txt

##get-gitlab-projects
**Gets (clones) all GitLab projects that were forked from a particular project.**

This script was written for the following use-case:
* The user is an instructor using GitLab for students to submit assignments.
* The instructor created a GitLab project from which the students fork their own copy.
* The students have added the instructor to their project as at least a "Reporter" for the instructor to be able to clone the project, or as at at least a "Developer" for the instructor to push changes.

Call as:

python get-gitlab-projects.py *project-name* *directory*

where
* *project-name* is the name of the GitLab namespace/projectname e.g. kwurst/Lab1 or cs-100/Lab1
This is everything after the / after the server URL. In the examples:
http://gitlab.myschool.edu/kwurst/Lab1
http://gitlab.myschool.edu/cs-100/Lab1
* *directory* is the path to the local directory where the projects should be cloned

You must edit the script to include:

* the URL to your GitLab server

## create-gitlab-users
**Create GitLab user accounts from a Blackboard class list**

You must edit the script to include:

* the URL to your GitLab server
* your email domain
* the GitLab id for the group created for the class
* the access level for the students (if you want to change it to something other than ‘reporter’)

To create the class list:

1. From within Blackboard, go to Grade Center:Full Grade Center
2. From Work Offline, choose Download
3. Choose "Delimiter Type: Comma" and "Include Hidden Information: Yes", and click Submit
4. Download the file.

Call as:

python create-gitlab-users.py *filename*

where 

* *filename* is the path/name of the CSV file

## remove-user-from-gitlab-projects
**Remove the instructor from all GitLab projects forked from a specify group - in this case a course/semester group**

Call as:

python remove-user-from-gitlab-projects.py *group-name* *user*

where

* *group-name* is the name of the GitLab group e.g. cs-140-01-02-spring-2014

* *user* is the GitLab username of the user to be removed

