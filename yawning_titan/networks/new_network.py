from __future__ import annotations

from logging import getLogger
from typing import Dict, List, Optional, Union

from numpy import ndarray

from yawning_titan.config.toolbox.core import ConfigGroup, ConfigGroupValidation
from yawning_titan.config.toolbox.groups.core import RestrictRangeGroup
from yawning_titan.config.toolbox.item_types.bool_item import BoolItem, BoolProperties
from yawning_titan.config.toolbox.item_types.float_item import (
    FloatItem,
    FloatProperties,
)
from yawning_titan.config.toolbox.item_types.int_item import IntItem, IntProperties
from yawning_titan.db.doc_metadata import DocMetadata
from yawning_titan.exceptions import ConfigGroupValidationError

_LOGGER = getLogger(__name__)

# --- Tier 0 groups


class NodePlacementGroup(ConfigGroup):
    """The pseudo random placement of the nodes in the network."""

    def __init__(
        self,
        doc: Optional[str] = None,
        use: Optional[bool] = False,
        count: Optional[int] = None,
        random: Optional[bool] = False,
    ):
        self.use = BoolItem(
            value=use,
            doc="Whether to place the node type randomly",
            properties=BoolProperties(allow_null=False, default=False),
        )
        self.count = IntItem(
            value=count,
            doc="The number of nodes to place within the network",
            properties=IntProperties(
                allow_null=True, min_val=0, inclusive_min=True, default=0
            ),
        )
        self.random = BoolItem(
            value=random,
            doc="Choose nodes completely randomly",
            properties=BoolProperties(allow_null=True, default=False),
        )
        super().__init__(doc)

    def validate(self) -> ConfigGroupValidation:
        """Extend the parent validation with additional rules specific to this :class: `~yawning_titan.config.toolbox.core.ConfigGroup`."""
        super().validate()
        if self.use.value:
            n = sum(
                1 if e.value else 0
                for k, e in self.get_config_elements().items()
                if k not in ["use", "count"]
            )
            try:
                if n == 0:
                    msg = "If the user does not set the placement of nodes then a method of setting them randomly must be chosen"
                    raise ConfigGroupValidationError(msg)
            except ConfigGroupValidationError as e:
                self.validation.add_validation(msg, e)

            try:
                if n > 1:
                    msg = f"{n} methods of choosing node placement have been selected but only 1 can be used"
                    raise ConfigGroupValidationError(msg)
            except ConfigGroupValidationError as e:
                self.validation.add_validation(msg, e)
        return self.validation


class NodeVulnerabilityGroup(RestrictRangeGroup):
    """Implementation of :class: `~yawning_titan.config.toolbox.groups.core.RestrictRangeGroup` using float values as min and max."""

    def __init__(
        self,
        doc: Optional[str] = None,
        restrict: Optional[bool] = False,
        min: Optional[Union[int, float]] = None,
        max: Optional[Union[int, float]] = None,
    ):
        self.restrict = BoolItem(
            value=restrict,
            doc="Whether to restrict this attribute.",
            properties=BoolProperties(allow_null=True, default=False),
        )
        self.min: FloatItem = FloatItem(
            value=min,
            doc="The minimum value of the attribute to restrict.",
            properties=FloatProperties(allow_null=True, min_val=0, inclusive_min=True),
        )
        self.max: FloatItem = FloatItem(
            value=max,
            doc="The maximum value of the attribute to restrict.",
            properties=FloatProperties(allow_null=True, min_val=0, inclusive_min=True),
        )
        self.doc: Optional[str] = doc
        self.validation = self.validate()


# --- Tier 1 groups


class EntryNodePlacementGroup(NodePlacementGroup):
    """The pseudo random placement of the nodes in the network."""

    def __init__(
        self,
        doc: Optional[str] = None,
        use: Optional[bool] = False,
        count: Optional[int] = None,
        random: Optional[bool] = False,
        place_close_to_edge: Optional[bool] = False,
        place_close_to_center: Optional[bool] = False,
    ):
        self.place_close_to_edge = BoolItem(
            value=place_close_to_edge,
            doc="Choose nodes closer to the edge of the network.",
            alias="prefer_edge_nodes_for_entry_nodes",
            properties=BoolProperties(allow_null=True, default=False),
        )
        self.place_close_to_center = BoolItem(
            value=place_close_to_center,
            doc="Choose nodes closer to the center of the network.",
            alias="prefer_central_nodes_for_entry_nodes",
            properties=BoolProperties(allow_null=True, default=False),
        )
        super().__init__(doc, use, count, random)


class HighValueNodePlacementGroup(NodePlacementGroup):
    """The pseudo random placement of the nodes in the network."""

    def __init__(
        self,
        doc: Optional[str] = None,
        use: Optional[bool] = False,
        count: Optional[int] = None,
        random: Optional[bool] = False,
        place_far_from_entry: Optional[bool] = False,
    ):
        self.place_far_from_entry = BoolItem(
            value=place_far_from_entry,
            doc="Choose nodes far away from entry nodes.",
            alias="choose_high_value_nodes_furthest_away_from_entry",
            properties=BoolProperties(allow_null=True, default=False),
        )
        super().__init__(doc, use, count, random)


# --- Tier 2 groups


class Network(ConfigGroup):
    """A set of optional restrictions that collectively constrain the types of network a game mode can be used upon."""

    def __init__(
        self,
        doc: Optional[str] = None,
        matrix: ndarray = None,
        positions: Dict[str, List[str]] = None,
        entry_nodes: Optional[List[str]] = None,
        vulnerabilities: Optional[Dict] = None,
        high_value_nodes: Optional[List[str]] = None,
        _doc_metadata: Optional[DocMetadata] = None,
        entry_node_random_placement: Optional[EntryNodePlacementGroup] = None,
        high_value_node_random_placement: Optional[HighValueNodePlacementGroup] = None,
        node_vulnerabilities: Optional[RestrictRangeGroup] = None,
    ):
        self._doc_metadata = _doc_metadata
        self.matrix = matrix
        self.positions = positions
        self.entry_nodes = entry_nodes
        self.vulnerabilities = vulnerabilities
        self.high_value_nodes = high_value_nodes

        if isinstance(entry_node_random_placement, EntryNodePlacementGroup):
            self.entry_node_random_placement = entry_node_random_placement
        elif isinstance(entry_node_random_placement, dict):
            self.entry_node_random_placement = EntryNodePlacementGroup(
                **entry_node_random_placement
            )
        else:
            self.entry_node_random_placement = EntryNodePlacementGroup(
                doc="The pseudo random placement of the entry nodes in the network."
            )

        if isinstance(high_value_node_random_placement, HighValueNodePlacementGroup):
            self.high_value_node_random_placement = high_value_node_random_placement
        elif isinstance(high_value_node_random_placement, dict):
            self.high_value_node_random_placement = HighValueNodePlacementGroup(
                **high_value_node_random_placement
            )
        else:
            self.high_value_node_random_placement = HighValueNodePlacementGroup(
                doc="The pseudo random placement of the high value nodes in the network."
            )

        if isinstance(node_vulnerabilities, RestrictRangeGroup):
            self.node_vulnerabilities = node_vulnerabilities
        elif isinstance(node_vulnerabilities, dict):
            self.node_vulnerabilities = RestrictRangeGroup(**node_vulnerabilities)
        else:
            self.node_vulnerabilities = RestrictRangeGroup(
                doc="The range of vulnerabilities for the nodes in the network used when vulnerability is set randomly."
            )

        self.entry_node_random_placement.count.alias = "number_of_entry_nodes"
        self.entry_node_random_placement.random.alias = "choose_entry_nodes_randomly"

        self.high_value_node_random_placement.count.alias = "number_of_high_value_nodes"
        self.high_value_node_random_placement.random.alias = (
            "choose_high_value_nodes_placement_at_random"
        )

        self.node_vulnerabilities.max.alias = "node_vulnerability_upper_bound"
        self.node_vulnerabilities.min.alias = "node_vulnerability_lower_bound"

        super().__init__(doc)

    @property
    def doc_metadata(self) -> DocMetadata:
        """The configs document metadata."""
        return self._doc_metadata

    @doc_metadata.setter
    def doc_metadata(self, doc_metadata: DocMetadata):
        if self._doc_metadata is None:
            self._doc_metadata = doc_metadata
        else:
            msg = "Cannot set doc_metadata as it has already been set."
            _LOGGER.error(msg)

    def to_dict(
        self,
        json_serializable: bool = False,
        include_none: bool = True,
        values_only: bool = False,
    ) -> Dict:
        """
        Serialize the :class:`~yawning_titan.networks.network.Network` as a :py:class:`dict`.

        :param json_serializable: If ``True``, the :attr:`~yawning_titan.networks.network.Network`
            "d numpy array is converted to a list."
        :param include_none: Determines whether to include empty fields in the dict. Has a default
            value of ``True``.
        :return: The :class:`~yawning_titan.networks.network.Network` as a :py:class:`dict`.
        """
        if json_serializable:
            values_only = True

        config_dict = super().to_dict(
            values_only=values_only
        )  # include_none=include_none,

        config_dict["matrix"] = self.matrix
        config_dict["positions"] = self.positions
        config_dict["entry_nodes"] = self.entry_nodes
        config_dict["vulnerabilities"] = self.vulnerabilities
        config_dict["high_value_nodes"] = self.high_value_nodes

        if json_serializable:
            config_dict["matrix"] = config_dict["matrix"].tolist()
        if self.doc_metadata is not None:
            config_dict["_doc_metadata"] = self.doc_metadata.to_dict()

        print("VHVH", config_dict)
        return config_dict
