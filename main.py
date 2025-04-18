from github import Github
import os
import yaml


def load_yaml(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def add_collaborators(data, org):
    internal_team = set()
    for role, users in data["internal_team"].items():
        internal_team.update(users)

    for project, details in data["projects"].items():
        for repo_name in details["repos"]:
            gh_repo = org.get_repo(repo_name)

            # get current collaborators
            current_collaborators = {
                collab.login for collab in gh_repo.get_collaborators()
            }

            # get maintainers list
            maintainers_list = details["team"] or []
            maintainers_set = set(maintainers_list)

            # see if there's anyone to add
            for maintainer in maintainers_set - current_collaborators - internal_team:
                print(f"Adding {maintainer} as a maintainer to {repo_name}")
                gh_repo.add_to_collaborators(maintainer, permission="write")

            # see if there's anyone to remove
            for collaborator in current_collaborators - maintainers_set - internal_team:
                print(f"{collaborator} needs to be removed from {repo_name}")
                # NOTE: This is a manual process, DO NOT MAKE THIS AUTOMATIC
                # gh_repo.remove_from_collaborators(collaborator)


def main():
    GITHUB_TOKEN = os.environ["X_GITHUB_TOKEN"]
    g = Github(GITHUB_TOKEN)
    org = g.get_organization("SDC-MUJ")
    data = load_yaml("projects.yaml")
    add_collaborators(data, org)


if __name__ == "__main__":
    main()
