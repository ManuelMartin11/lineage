from datetime import datetime
from lineage.plumbing import get_active_branch, get_last_commit


class Release:
    def __init__(self, **params):
        self.experiment_name = params.get("experiment_name")
        self.experiment_description = params.get("experiment_description")
        self.model_version = params.get("model_version", None)
        self.code_commit = params.get("code_commit", None)

        if not self.code_commit:
            self.code_commit = get_last_commit()

        self.code_branch = params.get("code_branch", None)

        if not self.code_branch:
            self.code_branch = get_active_branch()

        self.data_version = params.get("data_version", None)
        self.hyperparameters: dict = params.get("hyperparameters", None)
        self.now = datetime.now().strftime("%D %H:%M")

        self.hyp_str = ""
        if self.hyperparameters:
            for key, value in self.hyperparameters.items():
                self.hyp_str += f"\n>{key} = {value}\n"

        self.release_note = self.draft_release_note()

    def draft_release_note(self):
        draft = f"""# Experiment Release Note\n{self.now}
        \n### Experiment Name\n>{self.experiment_name}
        \n### Experiment Description\n>{self.experiment_description}
        \n### Model Version\n>{self.model_version}
        \n### Code Commit\n>{self.code_commit}
        \n### Code Branch\n>{self.code_branch}
        \n### Data Version\n>{self.data_version}
        \n### Hyperparameters\n{self.hyp_str}
        """
        return draft
