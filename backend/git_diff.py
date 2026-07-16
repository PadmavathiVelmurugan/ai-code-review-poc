from git import Repo
import os


def get_changed_files(repo_path):

    repo = Repo(repo_path)

    diff = repo.git.diff("HEAD~1", "HEAD", "--name-only")

    changed_files = []

    for file in diff.splitlines():

        if file.endswith(".java"):

            changed_files.append(
                os.path.normpath(file)
            )

    return changed_files