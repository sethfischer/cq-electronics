"""Abstract base classes for CadQuery object containers."""

from __future__ import annotations

from abc import ABC, abstractmethod

import cadquery as cq


class CqWorkplaneContainer(ABC):
    """Abstract base class for CadQuery Workplane containers."""

    _cq_object: cq.Workplane

    @property
    def cq_object(self) -> cq.Workplane:
        """Get CadQuery object."""
        return self._cq_object

    @abstractmethod
    def _make(self) -> cq.Workplane:
        """Create CadQuery object."""
        ...


class CqAssemblyContainer(ABC):
    """Abstract base class for CadQuery Assembly containers."""

    _cq_object: cq.Assembly
    _name: str

    @property
    def cq_object(self) -> cq.Assembly:
        """Get CadQuery object."""
        return self._cq_object

    @property
    def name(self) -> str:
        """Assembly name."""
        return self._name

    def cq_part(self, name: str) -> cq.Shape | cq.Workplane:
        """Get part from CadQuery assembly."""
        result = self._cq_object.objects[name].obj

        if result is None:
            raise Exception(f"Invalid name: '{name}'.")

        return result

    def sub_assembly_name(self, name: str) -> str:
        """Sub assembly name."""
        return f"{self._name}__{name}"

    @abstractmethod
    def _make(self) -> cq.Assembly:
        """Create CadQuery object."""
        ...
