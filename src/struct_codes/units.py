from pint import Quantity, UnitRegistry

ureg = UnitRegistry(auto_reduce_dimensions=True)
meter = ureg.meter
millimeter = ureg.millimeter
inch = ureg.inch
kilogram = ureg.kilogram
giga_pascal = ureg.GPa
mega_pascal = ureg.MPa
