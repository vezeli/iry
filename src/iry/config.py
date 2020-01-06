"""
Configuration file.
"""
from configparser import ConfigParser
from pathlib import Path
from types import MappingProxyType
from typing import Dict, Optional, Tuple

from appdirs import AppDirs
from dataclasses import dataclass, field

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


def app_location(appname: str, appauthor: str, purpose: str) -> Dict:
    """Find appropriate place for configuration and data files."""
    d = AppDirs(appname, appauthor)
    attr = "user_" + purpose + "_dir"
    dpaths = [Path().cwd(), Path(getattr(d, attr))]
    if purpose == "config":
        fname = DEFAULT_CONFIG_FILE
    if purpose == "data":
        fname = DEFAULT_DATA_FILE
    fpaths = {key: value / fname for key, value in enumerate(dpaths)}
    return fpaths


def determine_priority(paths: Dict[int, Path]) -> Optional[Path]:
    """Find configuration file that exists in the system."""
    for key in sorted(paths.keys()):
        if paths[key].exists():
            return paths[key]


@dataclass
class IryConfig:
    """Iry configuration."""
    config_file: str = DEFAULT_CONFIG_FILE
    data_file: str = DEFAULT_DATA_FILE
    fields: Tuple[str] = DEFAULT_FIELDS
    field_values: Tuple[Tuple[str, str]] = DEFAULT_FIELD_VALUES

    def __post_init__(self):
        """Change default values to mutable objects."""
        self.fields = list(self.fields)
        self.field_values = dict(self.field_values)

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


def load_config(path: Optional[Path]) -> IryConfig:
    # TODO: get required data from `path` file and create IryConfig object.
    # IryConfig has defaults so if there is no value given in `path` simply use
    # the defaults.
    if path is None:
        return IryConfig()
