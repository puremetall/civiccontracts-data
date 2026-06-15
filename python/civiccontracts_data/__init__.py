"""civiccontracts-data: an open client for public U.S. government contract data.

Maintained by CivicContracts (https://www.civiccontracts.com).
"""

from .client import CivicContractsClient, Award

__all__ = ["CivicContractsClient", "Award"]
__version__ = "0.1.0"
