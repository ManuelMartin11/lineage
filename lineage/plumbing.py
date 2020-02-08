import git


def get_current_repo():
    return git.Repo()


def get_active_branch():
    repo = get_current_repo()
    return repo.active_branch.name


def get_last_commit():
    repo = get_current_repo()
    return repo.head.commit.hexsha


def do_commit(comment):
    repo = get_current_repo()
    repo.git.commit("-m", comment)
