from lineage.manager import LineageManager
from lineage.bulletin import Release


class Experiment(Release):

    def __init__(self, new_set=False, **args):
        self.__MUSTHAVE__ = ["experiment_name", "data_version"]
        self.args = args
        self.__mandatory_args()
        super().__init__(**args)

        self.lm = LineageManager()

        if self.lm.get_latest_set() < 1 or new_set:
            self.lm.new_set()  # New set + new experiment
            self.current_set_id = self.lm.get_latest_set()
            self.current_exp_id = self.lm.get_latest_experiment(
                self.current_set_id)
        else:
            self.current_set_id = self.lm.get_latest_set()
            self.lm.new_experiment()
            self.current_exp_id = self.lm.get_latest_experiment(
                self.current_set_id)

    def __mandatory_args(self):
        if not all([True for must in self.__MUSTHAVE__
                    if must in self.args.keys()]):

            raise AttributeError(f"""You must provide
                        {self.__MUSTHAVE__} arguments""")

    def export_release_note(self, **args):
        rl = Release(**args)
        return rl.draft_release_note()

    def register(self, **factors):
        self.lm.register_experiment_factors(self.current_set_id,
                                            self.current_exp_id,
                                            **factors)
