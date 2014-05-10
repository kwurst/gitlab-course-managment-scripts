gitlab-course-management-scripts
================================

Python scripts to manage students and projects in GitLab

* Requires pyapi-gitlab from https://github.com/Itxaka/pyapi-gitlab
* Reads your private GitLab API token from the file gitlabtoken.txt

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

*filename* is the path/name of the CSV file

## remove-user-from-gitlab-projects
**Remove the instructor from all GitLab projects forked from a specify group - in this case a course/semester group**

Call as:

python remove-user-from-gitlab-projects.py *group-name* *user*

where

*group-name* is the name of the GitLab group e.g. cs-140-01-02-spring-2014

*user* is the GitLab username of the user to be removed

