# Gaia
Virtual Assistant to help with your environmental needs.

-------------------------------------------------------------
# Activate Virtual Environment

## CREATE NEW VENV FOR EACH SESSION. UPDATE requirements.txt IF YOU ADD NEW PACKAGES
## venv is in .gitignore so it should not be in the repository. we keep an updated list of dependencies in requirements.txt.

## mac 
> python3 -m venv venv
## windows
> python -m venv venv

## mac
source venv/bin/activate
## windows
.\venv\Scripts\Activate

# Install requirments.txt
pip install -r requirements.txt

# UPDATE requirements.txt
pip freeze > requirements.txt 


# YOU MUST BE IN VIRTUAL ENVIRONMENT WHENVER DEVELOPING/RUNNING LOCALLY

# run server
flask --debug --app app.views run
-------------------------------------------------------------
# ChatGPT tutorial for github

# Fetch Latest Changes:
git fetch

# Create Feature Branch:
git checkout -b feature-branch-name main
Replace feature-branch-name with the name of your feature branch.

# Work on Your Feature:
Make your changes, add new features, fix bugs, etc., in this branch.

# Add, Commit, and Push:
After finishing your changes, add them to the staging area, commit them with a descriptive message, and push the branch to the remote repository.
git add .
git commit -m "Your commit message"
git push origin feature-branch-name

# Create a Pull Request (Optional):
If you're working in a team, create a pull request from your feature branch to the main branch on your Git hosting service (e.g., GitHub, GitLab, Bitbucket). This allows your team to review your changes before merging them into the main branch.

# Merge Changes into Main:
Once your changes are approved, you can merge them into the main branch either through your Git hosting service's interface or locally if you have the necessary permissions.
git checkout main
git merge --no-ff feature-branch-name
git push origin main

# Clean Up:
After merging, you can delete your feature branch both locally and remotely (if you created a pull request).
git branch -d feature-branch-name
git push origin --delete feature-branch-name

# HOW TO PULL FROM SPECIFIC BRANCH
git pull origin <branchname>

# REMEMBER
Remember to replace feature-branch-name with your actual feature branch name. This workflow helps keep your main branch clean and allows for better collaboration in a team environment.

# USEFUL LINKS
https://github.com/humiaozuzu/awesome-flask?tab=readme-ov-file#admin-interface
This is a bumch of useful flask intergrations`