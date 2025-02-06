from dataclasses import asdict

from pint import Quantity


def simplify_units(quantity: Quantity) -> float:
    """Reduce quantity to base units and get magnitude"""
    return quantity.to_base_units().magnitude


def simplify_dataclass(data_objetct):
    """
    Converts dataclass to dictionary and simplify quantites to magnitude of base unit.
    """
    d = asdict(data_objetct)
    for key, value in d.items():
        if isinstance(value, Quantity):
            d[key] = simplify_units(value)
    return d
