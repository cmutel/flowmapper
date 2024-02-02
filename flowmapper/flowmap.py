from functools import cached_property
from .flow import Flow
from .match import match_rules, format_match_result
from .unit import Unit
from tqdm import tqdm
from typing import Callable, Optional
import pandas as pd
from pathlib import Path
import json
from collections import Counter

class Flowmap:
    """
    Crosswalk of flows from a source flow list to a target flow list.

    This class provides functionalities to map flows between different flow lists using a series of predefined match rules.

    Attributes
    ----------
    source_flows : list[Flow]
        The list of (unique) source flows to be mapped.
    source_flows_nomatch : list[Flow]
        The list of (unique) source flows that do not match any rule.
    target_flows : list[Flow]
        The list of target flows for mapping.
    target_flows_nomatch : list[Flow]
        The list of target flows that do not match any rule.

    """
    def __init__(
        self,
        source_flows: list[Flow],
        target_flows: list[Flow],
        rules: list[Callable[..., bool]] = None,
        nomatch_rules: list[Callable[..., bool]] = None,
        disable_progress: bool = False,
    ):
        """
        Initializes the Flowmap with source and target flows, along with optional matching rules.

        Duplicated flows are removed from both source and targets lists.

        Parameters
        ----------
        source_flows : list[Flow]
            The list of source flows to be mapped.
        target_flows : list[Flow]
            The list of target flows for mapping.
        rules : list[Callable[..., bool]], optional
            Custom rules for matching source flows to target flows. Default is the set of rules defined in `match_rules`.
        nomatch_rules : list[Callable[..., bool]], optional
            Rules to identify flows that should not be matched.
        disable_progress : bool, optional
            If True, progress bar display during the mapping process is disabled.

        """
        self.disable_progress = disable_progress
        self.rules = rules if rules else match_rules()
        if nomatch_rules:
            self.source_flows = []
            self.source_flows_nomatch = []
            
            for flow in source_flows:
                matched = False
                for rule in nomatch_rules:
                    if rule(flow):
                        self.source_flows_nomatch.append(flow)
                        matched = True
                        break
                if not matched:
                    self.source_flows.append(flow)
            self.source_flows = list(dict.fromkeys(self.source_flows))
            self.source_flows_nomatch = list(dict.fromkeys(self.source_flows_nomatch))

            self.target_flows = []
            self.target_flows_nomatch = []

            for flow in target_flows:
                matched = False
                for rule in nomatch_rules:
                    if rule(flow):
                        self.target_flows_nomatch.append(flow)
                        matched = True
                        break
                if not matched:
                    self.target_flows.append(flow)
            self.target_flows = list(dict.fromkeys(self.target_flows))
            self.target_flows_nomatch = list(dict.fromkeys(self.target_flows_nomatch))
        else:
            self.source_flows = list(dict.fromkeys(source_flows))
            self.source_flows_nomatch = []
            self.target_flows = list(dict.fromkeys(target_flows))
            self.target_flows_nomatch = []

    @cached_property
    def mappings(self):
        """
        Generates and returns a list of mappings from source flows to target flows based on the defined rules.

        Each mapping includes the source flow, target flow, conversion factor, the rule that determined the match, and additional information.

        A single match using the match rule with highest priority is returned for each source flow.

        Returns
        -------
        list[dict]
            A list of dictionaries containing the mapping details.

        """
        all_mappings = []
        for s in tqdm(self.source_flows, disable=self.disable_progress):
            for t in self.target_flows:
                for rule in self.rules:
                    is_match = rule(s, t)
                    if is_match:
                        all_mappings.append(
                            {'from': s,
                             'to': t,
                             'conversion_factor': s.conversion_factor if s.conversion_factor else s.unit.conversion_factor(t.unit),
                             'match_rule': rule.__name__,
                             'match_rule_priority': self.rules.index(rule),
                             'info': is_match}
                        )
                        break
        result = []
        seen_sources = set()
        sorted_mappings = sorted(all_mappings, key=lambda x: (x['from'], x['match_rule_priority']))
        for mapping in sorted_mappings:
            if mapping['from'] not in seen_sources:
                result.append(mapping)
                seen_sources.add(mapping['from'])
        
        return result

    @cached_property
    def _matched_source_flows_ids(self):
        return {map_entry['from'].id for map_entry in self.mappings}

    @cached_property
    def _matched_target_flows_ids(self):
        return {map_entry['to'].id for map_entry in self.mappings}

    @cached_property
    def matched_source(self):
        """
        Provides a list of source flows that have been successfully matched to target flows.

        Returns
        -------
        list[Flow]
            A list of matched source flow objects.

        """
        result = [
            flow
            for flow in self.source_flows 
            if flow.id in self._matched_source_flows_ids
        ]
        return result

    @cached_property
    def unmatched_source(self):
        """
        Provides a list of source flows that have not been matched to any target flows.

        Returns
        -------
        list[Flow]
            A list of unmatched source flow objects.

        """
        result = [
            flow 
            for flow in self.source_flows 
            if flow.id not in self._matched_source_flows_ids
        ]
        return result

    @cached_property
    def matched_source_statistics(self):
        """
        Calculates statistics for matched source flows, including the number of matches and the matching percentage for each context.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing matching statistics for source flows.

        """
        matched = Counter([flow.context.value for flow in self.matched_source])
        matched = pd.Series(matched).reset_index()
        matched.columns = ['context', 'matched']

        total = Counter([flow.context.value for flow in self.source_flows])
        total = pd.Series(total).reset_index()
        total.columns = ['context', 'total']

        df = pd.merge(matched, total, on='context', how='outer')
        df = df.fillna(0).astype({'matched': 'int', 'total': 'int'})

        df['percent'] = df.matched / df.total
        result = df.sort_values('percent')
        return result

    @cached_property
    def matched_target(self):
        """
        Provides a list of target flows that have been successfully matched to source flows.

        Returns
        -------
        list[Flow]
            A list of matched target flow objects.

        """
        result = [
            flow
            for flow in self.target_flows 
            if flow.id in self._matched_target_flows_ids
        ]
        return result

    @cached_property
    def unmatched_target(self):
        """
        Provides a list of target flows that have not been matched to any source flows.

        Returns
        -------
        list[Flow]
            A list of unmatched target flow objects.

        """
        result = [
            flow
            for flow in self.target_flows 
            if flow.id not in self._matched_target_flows_ids
        ]
        return result

    @cached_property
    def matched_target_statistics(self):
        """
        Calculates statistics for matched target flows, including the number of matches and the matching percentage for each context.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing matching statistics for target flows.

        """
        matched = Counter([flow.context.value for flow in self.matched_target])
        matched = pd.Series(matched).reset_index()
        matched.columns = ['context', 'matched']

        total = Counter([flow.context.value for flow in self.target_flows])
        total = pd.Series(total).reset_index()
        total.columns = ['context', 'total']

        df = pd.merge(matched, total, on='context', how='outer')
        df = df.fillna(0).astype({'matched': 'int', 'total': 'int'})

        df['percent'] = df.matched / df.total
        result = df.sort_values('percent')
        return result

    def statistics(self):
        """
        Prints out summary statistics for the flow mapping process.

        """
        source_msg = (
            f"{len(self.source_flows)} source flows ({len(self.source_flows_nomatch)} excluded)..."
            if self.source_flows_nomatch
            else f"{len(self.source_flows)} source flows..."
        )
        print(source_msg)
        target_msg = (
            f"{len(self.target_flows)} target flows ({len(self.target_flows_nomatch)} excluded)..."
            if self.target_flows_nomatch
            else f"{len(self.target_flows)} target flows..."
        )
        print(target_msg)
        print(
            f"{len(self.mappings)} mappings ({len(self.matched_source) / len(self.source_flows):.2%} of total)."
        )
        cardinalities = dict(Counter([x['cardinality'] for x in self._cardinalities]))
        print(f"Mappings cardinalities: {str(cardinalities)}")

    @cached_property
    def _cardinalities(self):
        """
        Calculates and returns the cardinalities of mappings between source and target flows.

        Returns
        -------
        list[dict]
            A sorted list of dictionaries, each indicating the cardinality relationship between a pair of source and target flows.

        """
        mappings = [(mapentry['from'].id, mapentry['to'].id) for mapentry in self.mappings]
        lhs_counts = Counter([pair[0] for pair in mappings])
        rhs_counts = Counter([pair[1] for pair in mappings])

        result = []

        for lhs, rhs in mappings:
            lhs_count = lhs_counts[lhs]
            rhs_count = rhs_counts[rhs]
            if lhs_count == 1 and rhs_count == 1:
                result.append({"from": lhs, "to": rhs, "cardinality": "1:1"})
            elif lhs_count == 1 and rhs_count > 1:
                result.append({"from": lhs, "to": rhs, "cardinality": "N:1"})
            elif lhs_count > 1 and rhs_count == 1:
                result.append({"from": lhs, "to": rhs, "cardinality": "1:N"})
            elif lhs_count > 1 and rhs_count > 1:
                result.append({"from": lhs, "to": rhs, "cardinality": "N:M"})

        return sorted(result, key = lambda x: x['from'])

    def to_randonneur(self, path: Optional[Path] = None):
        """
        Export mappings using randonneur data migration file format.

        Parameters
        ----------
        path : Path, optional
            If provided export the output file to disk.

        Returns
        -------
        list[dict]
            A list of dictionaries representing the formatted mapping results.

        """
        result = [
            format_match_result(map_entry['from'], 
                                map_entry['to'],
                                map_entry['conversion_factor'],
                                map_entry['info']) 
            for map_entry in self.mappings
        ]

        if not path:
            return result
        else:
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w') as fs: 
                json.dump(result, fs, indent=2)
        

    def to_glad(self, path: Optional[Path] = None, ensure_id: bool = False):
        """
        Export mappings using GLAD flow mapping format, optionally ensuring each flow has an identifier.

        Formats the mapping results according to Global LCA Data Access (GLAD) network initiative flow mapping format.

        Parameters
        ----------
        path : Path, optional
            If provided export the output file to disk.
        ensure_id : bool, optional
            If True, ensures each flow has an identifier, default is False.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the formatted mapping results in GLAD format.

        """
        data = []
        for map_entry in self.mappings:
            source_flow_id = map_entry['from'].uuid_raw_value if map_entry['from'].uuid_raw_value or not ensure_id else map_entry['from'].id
            row = {
                    'SourceFlowName': map_entry['from'].name_raw_value,
                    'SourceFlowUUID': source_flow_id,
                    'SourceFlowContext': '/'.join(map_entry['from'].context_raw_value),
                    'SourceUnit': map_entry['from'].unit_raw_value,
                    'MatchCondition': '',
                    'ConversionFactor': map_entry['conversion_factor'],
                    'TargetFlowName': map_entry['to'].name_raw_value,
                    'TargetFlowUUID': map_entry['to'].uuid_raw_value,
                    'TargetFlowContext': map_entry['to'].context.raw_value,
                    'TargetUnit': map_entry['to'].unit.raw_value,
                    'MemoMapper': map_entry['info'].get('comment')
                }
            data.append(row)

        result = pd.DataFrame(data)

        if not path:
            return result
        else:
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            result.to_excel(path, index = False)
