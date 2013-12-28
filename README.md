create-gitlab-users
===================

Create GitLab users from a Blackboard class list

1. From within Blackboard, go to Grade Center:Full Grade Center
2. From Work Offline, choose Download
3. Choose Comma delimiter, and click Submit
4. Download the file.

Call as:
python create-gitlab-users.py filename

where filename is the path/name of the CSV file

Requires pyapi-gitlab https://github.com/Itxaka/pyapi-gitlab
Reads your private GitLab API token from the file gitlabtoken.txt
