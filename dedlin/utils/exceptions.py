"""
Custom exceptions so we don't have to raise Exception or some other
inappropriate exception
"""


class DedlinException(Exception):
    """
    Any Exception from dedlin and not some other random module
    """
