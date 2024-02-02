from flowmapper.utils import read_migration_files, read_flowlist
from flowmapper.flow import Flow
from flowmapper.flowmap import Flowmap

def test_transform_flow_with_conversion_factor(field_mapping, snapshot):
    
    source_flows_path = 'tests/data/sp.json'
    target_flows_path = 'tests/data/ei-3.7.json'
    
    transformations = read_migration_files('tests/data/transformations.json')
    
    source_flows = read_flowlist(source_flows_path)
    source_flows = [Flow(flow, field_mapping['source'], transformations) for flow in source_flows]
    target_flows = read_flowlist(target_flows_path)
    target_flows = [Flow(flow, field_mapping['target']) for flow in target_flows]

    flowmap = Flowmap(source_flows, target_flows)
    actual = flowmap.to_randonneur()
    assert actual == snapshot
