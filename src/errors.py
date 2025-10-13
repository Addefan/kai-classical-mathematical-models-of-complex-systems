from enum import Enum


class ParsingError(str, Enum):
    not_found = "not_found"
    not_exist = "not_exist"
