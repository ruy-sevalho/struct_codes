from pint import Quantity, UnitRegistry


def simplify_units(quantity: Quantity) -> float:
    return quantity.to_base_units().magnitude


ureg = UnitRegistry(auto_reduce_dimensions=True)
meter = ureg.meter
millimeter = ureg.millimeter
centemiter = ureg.centimeter
inch = ureg.inch
kilogram = ureg.kilogram
gigapascal = ureg.GPa
megapascal = ureg.MPa
newton = ureg.newton
kilonewton = 1000 * ureg.newton
