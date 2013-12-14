import gitlab

# Get my private GitLab token
# stored in a file so that I can .gitignore the file
token = open('gitlabtoken.txt').readline().strip()

# Create a gitlab object
# For our server, verify_ssl has to be False, since we have a self-signed certificate
git = gitlab.Gitlab("https://git.cs.worcester.edu", token, verify_ssl=False)

# Example - get all the users, then get first user's username
users = git.getusers()
print(users[0]['username'])
