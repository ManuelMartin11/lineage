import re
import pickle
import joblib
from pathlib import Path


class SourcePathNotExists(Exception):
    pass


class LineageManager:

    """
    Example Usage:
    >>> from lineage.manager import LineageManager
    >>> rm = LineageManager()
    >>> rm.new_experiment()

    >>> model.fit()
    >>> ypred = model.predict()
    >>> results = metrics(ytrue, ypred)

    >>> rm.register_experiment_factors(
                model=model,
                data=data,
                results=results,
                exploration="eda.ipynb",
                releasenotes=release_info
            )
    """

    def __init__(self, source_path=""):
        self.__LINEAGEDIR__ = ".lineage"
        self.source_path = Path(source_path)
        self.project_path = Path.joinpath(Path(source_path),
                                          self.__LINEAGEDIR__)

        if not self.source_path.exists():
            raise SourcePathNotExists("""The provided path {}
                    does not exist""".format(self.source_path))
        if not self.project_path.exists():
            self.project_path.mkdir()

        self.experiment_set = "experiment_set_{}"
        self.experiment = "experiment_{}"
        self.experiment_factors = ["data", "exploration", "model",
                                   "results", "releasenotes"]

    def _create_factors(self, exp_path):
        """Create Experiment Factors"""
        for factor in self.experiment_factors:
            Path.joinpath(exp_path, factor).mkdir()

    def _create_experiment(self, set_id, exp_id):
        """Create Experiment"""
        exp_path = Path.joinpath(Path.joinpath(self.project_path,
                                               self.experiment_set.format(
                                                   set_id)),
                                 Path(self.experiment.format(exp_id)))
        exp_path.mkdir()

        # Create Experiment Factors
        self._create_factors(exp_path)

    def _create_set(self, set_id, exp_id):
        """Create new Experiment Set"""
        # Create Experiment Set
        set_path = Path.joinpath(self.project_path,
                                 Path(self.experiment_set.format(set_id)))
        set_path.mkdir()
        # Create Experiment
        self._create_experiment(set_id, exp_id)

    def new_set(self):
        """Create New Experiment Set"""
        last_set = self.get_latest_set()
        self._create_set(last_set + 1, 1)

    def new_experiment(self):
        """Create New Experiment"""
        latest_set = self.get_latest_set()
        if latest_set != -1:  # Create experiment only if there is a set
            latest_experiment = self.get_latest_experiment(latest_set)
            self._create_experiment(latest_set, latest_experiment + 1)

    def get_latest_set(self):
        """Get latest created Experiment Set"""
        current_sets = []
        for set_path in self.project_path.iterdir():
            match = re.search(r"\d+", set_path.name)  # Look for set_id
            if match:
                current_sets.append(int(match[0]))
        if not current_sets:
            return 0
        return max(current_sets)

    def get_latest_experiment(self, set_id):
        """Get latest created Experiment"""
        set_path = Path.joinpath(self.project_path,
                                 self.experiment_set.format(set_id))
        current_experiments = []
        for exp_path in set_path.iterdir():
            match = re.search(r"\d+", exp_path.name)  # Look for exp_id
            if match:
                current_experiments.append(int(match[0]))
        if not current_experiments:
            return 0
        return max(current_experiments)

    def get_factor(self, set_id, exp_id, factor_name):
        """Get path of specific experiment factor"""
        if factor_name not in self.experiment_factors:
            raise AttributeError("{} does not exist".format(factor_name))
        return Path.joinpath(
            self.project_path,
            Path(self.experiment_set.format(set_id)),
            Path(self.experiment.format(exp_id)),
            Path(factor_name)
        )

    @staticmethod
    def dump_factor_unit(obj, directory, filename, kind="joblib"):
        path = Path.joinpath(directory, filename)
        if kind == "joblib":
            with open(path, "wb") as f:
                joblib.dump(obj, f)
        elif kind == "pickle":
            with open(path, "wb") as f:
                pickle.dump(obj, f)
        else:
            with open(path, "w") as f:
                f.write(obj)

    def write_factor_unit(self, set_id, exp_id, factor, pythonobject):
        """Write an experiment factor unit"""
        factordirpath = self.get_factor(set_id, exp_id, factor)

        if factor == "data":
            self.dump_factor_unit(pythonobject, factordirpath,
                                  "data.joblib", kind="joblib")

        elif factor == "exploration":
            if type(pythonobject) != str:
                raise TypeError("Exploration pythonobject shoulde be a Path")
            with open(pythonobject, "r") as f:
                notebook = f.read()
            self.dump_factor_unit(notebook, factordirpath,
                                  "exploration.ipynb", kind="raw")

        elif factor == "model":
            self.dump_factor_unit(pythonobject, factordirpath,
                                  "model.joblib")

        elif factor == "results":
            self.dump_factor_unit(pythonobject, factordirpath,
                                  "results.pickle", kind="pickle")

        elif factor == "releasenotes":
            self.dump_factor_unit(pythonobject, factordirpath,
                                  "releasenotes.md", kind="raw")

    def register_experiment_factors(self, set_id=None, exp_id=None, **factors):
        """
        Register experiment factors in latest experiment or in desired one.
        """
        if not set_id:
            set_id = self.get_latest_set()
        if not exp_id:
            exp_id = self.get_latest_experiment(set_id)

        for factor in factors.keys():
            self.write_factor_unit(set_id, exp_id, factor, factors[factor])
