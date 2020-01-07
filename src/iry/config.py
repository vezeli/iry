"""
Configuration file.
"""
from configparser import ConfigParser
from pathlib import Path
from typing import Dict, Optional, Tuple

from appdirs import AppDirs
from dataclasses import dataclass

from iry import __appauthor__, __appname__

DEFAULT_CONFIG_FILE: str = "iry.cfg"
DEFAULT_DATA_FILE: str = "vault.pkl"
DEFAULT_FIELDS: Tuple[str] = (
    "Date",
    "Name",
    "Amount",
    "Origin",
    "Currency",
)
DEFAULT_FIELD_VALUES: Tuple[Tuple[str, str]] = (
    ("Origin", "Swish"),
    ("Currency", "SEK"),
)


def select(purpose: str, priority_path: Optional[str] = None, **kwargs) -> Optional[Path]:
    """Selects a file with the highest priority.

    ``purpose`` is either "config" or "data". In case configuration or data
    files don't exist the function returns ``None``.
    """
    priority_path = Path(priority_path)
    appauthor = kwargs.get("appauthor", __appauthor__)
    appname = kwargs.get("appname", __appname__)
    appfiles = default_app_dirs(appname, appauthor, purpose)
    if priority_path:
        appfiles = insert_high_priority(priority_path, appfiles)
    thefile = prioritize(appfiles, purpose)
    return thefile


def insert_high_priority(value: Path, fpaths: Dict[int, Path]) -> Dict[int, Path]:
    """Adds a high-priority file path to ``fpaths``."""
    max_priority = max(fpaths.keys())
    max_priority += 1
    fpaths[max_priority] = value
    return fpaths


def default_app_dirs(appname: str, appauthor: str, purpose: str) -> Dict[int, Path]:
    """Returns default application configuration or data paths.

    Returns a dictionary with keys of type ``int`` where values store paths to
    application's configuration or data file (depending on ``purpose``). The
    keys with higher values store paths with higher priority. Priority
    determines order in which the files are going to be used.
    """
    d = AppDirs(appname, appauthor)
    attr = "user_" + purpose + "_dir"
    dpaths = [Path(getattr(d, attr)), Path().cwd()]
    if purpose == "config":
        fname = DEFAULT_CONFIG_FILE
    if purpose == "data":
        fname = DEFAULT_DATA_FILE
    fpaths = {key: value / fname for key, value in enumerate(dpaths)}
    return fpaths


def prioritize(paths: Dict[int, Path], purpose: str) -> Optional[Path]:
    """Returns highest-priority and existing filepath from ``paths``.

    Finds existing configuration or data file in ``paths`` with highest
    priority and returns it, otherwise returns ``None``.
    """
    for key in sorted(paths.keys(), reverse=True):
        if purpose == "config":
            if paths[key].exists():
                return paths[key]
        if purpose == "data":
            return paths[key]


@dataclass
class IryConfig:
    """Main configuration class."""
    config_file: str = DEFAULT_CONFIG_FILE
    data_file: str = DEFAULT_DATA_FILE
    fields: Tuple[str] = DEFAULT_FIELDS
    defaults_for_fields: Tuple[Tuple[str, str]] = DEFAULT_FIELD_VALUES

    def __post_init__(self):
        """Change default values to mutable objects."""
        self.fields = list(self.fields)
        self.defaults_for_fields = dict(self.defaults_for_fields)

    @staticmethod
    def field_to_attr(field_name: str):
        """Convention for changing field name to attribute name.

        Field names can sometimes contain whitespace characters while class
        attributes cannot. Field names are therefore mapped to attribute names
        by changing upper case letters to lower cases letters and substituting
        whitespace characters with underscore separators. This procedure
        follows PEP8."""
        sep = "_"
        attr = sep.join(field_name.lower().split())
        return attr

    @classmethod
    def from_cfg_path(cls, path):
        pass

    @property
    def attrs(self):
        return [self.field_to_attr(field) for field in self.fields]

    def add_field_value(self, field, value):
        if field not in self.fields:
            msg = "Cannot assign value for field that doesn't exist in fields"
            raise ValueError(msg)
        else:
            self.defaults_for_fields[field] = value


def load_config(path: Optional[Path]) -> IryConfig:
    # TODO: get required data from `path` file and create IryConfig object.
    # IryConfig has defaults so if there is no value given in `path` simply use
    # the defaults.
    if path is None:
        return IryConfig()
