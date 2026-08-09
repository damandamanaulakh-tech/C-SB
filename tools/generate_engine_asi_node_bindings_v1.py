#!/usr/bin/env python3
from pathlib import Path
import json
from collections import defaultdict

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'generated/registry_views'
OUT.mkdir(parents=True,exist_ok=True)

def load(rel): return json.loads((ROOT/rel).read_text(encoding='utf-8'))

englib=load('registries/asi/ENGINE_LIBRARY_75_APPROVED_V1.json')
segmap=load('registries/asi/ENGINE_SEGMENT_BINDINGS_75_APPROVED_V1.json')
rels=load('generated/registry_views/brain_engine_relationships_compact_v1.json')
containers=load('registries/asi/OPERATIONAL_CONTAINERS_161_240_APPROVED_V1.json')
spine=load('machine/wiring/BRAIN_ENGINE_OPERATIONAL_SPINE_V1.json')

engine_meta={r[0]:{'name':r[1],'family':r[2],'engine_class':r[3]} for r in englib['records']}
engine_segments={r[0]:{'primary_segment_id':r[1],'secondary_segment_ids':[x.strip() for x in r[2].split(';') if x.strip()]} for r in segmap['records']}
container_meta={r[0]:{'segment_id':r[1],'element_code':r[2],'name':r[3],'weight_class':r[4]} for r in containers['records']}
element_map={e['element_code']:e for e in spine['elements']}

usage=defaultdict(list)
for c in rels['containers']:
    cid=c['container_id']
    for rank,eid in enumerate(c['engine_ids'],start=1):
        usage[eid].append({'container_id':cid,'rank':rank,'relationship_role':'Primary operator' if rank<=2 else 'Supporting operator'})

records=[]
for eid in [r[0] for r in englib['records']]:
    uses=usage.get(eid,[])
    elements=set(); ai_segments=set(); asi_segments=set(); nodes=set(); container_ids=[]; primary_count=0
    for u in uses:
        cid=u['container_id']; container_ids.append(cid)
        if u['rank']<=2: primary_count+=1
        ec=container_meta[cid]['element_code']; elements.add(ec)
        em=element_map[ec]
        ai_segments.update(em.get('primary_ai_segments',[]))
        asi_segments.update(em.get('primary_asi_segments',[]))
        nodes.update(em.get('asi_nodes',[]))
    meta=engine_meta[eid]
    sm=engine_segments.get(eid,{'primary_segment_id':None,'secondary_segment_ids':[]})
    records.append({
        'engine_id':eid,
        'engine_name':meta['name'],
        'family':meta['family'],
        'engine_class':meta['engine_class'],
        'source_primary_segment_id':sm['primary_segment_id'],
        'source_secondary_segment_ids':sm['secondary_segment_ids'],
        'source_operational_container_ids':sorted(container_ids,key=lambda x:int(x.split('-')[-1])),
        'source_operational_element_codes':sorted(elements),
        'source_usage_count':len(uses),
        'source_primary_operator_count':primary_count,
        'source_supporting_operator_count':len(uses)-primary_count,
        'phase2_ai_segments_from_elements':sorted(ai_segments),
        'phase2_asi_segments_from_elements':sorted(asi_segments),
        'phase2_asi_nodes_from_elements':sorted(nodes),
        'binding_status':'DERIVED_FROM_SOURCE_CONTAINER_RELATIONS' if uses else 'UNBOUND_IN_SOURCE_400_RELATION_MAP',
        'authority_note':'Engine identity and segment/container use are source records. AI/ASI segment and ASI-Node bindings are additive Phase-2 derivations through the approved E01..E08 operational spine; engines remain bounded operators, not autonomous authorities.'
    })

assert len(records)==75
payload={
    'registry_id':'ENGINE-75-PHASE2-ASI-NODE-BINDINGS-V1',
    'status':'GENERATED_ADDITIVE_MAPPING_NOT_SOURCE_REWRITE',
    'source_engine_registry':'registries/asi/ENGINE_LIBRARY_75_APPROVED_V1.json',
    'source_segment_bindings':'registries/asi/ENGINE_SEGMENT_BINDINGS_75_APPROVED_V1.json',
    'source_relationships':'generated/registry_views/brain_engine_relationships_compact_v1.json',
    'phase2_operational_spine':'machine/wiring/BRAIN_ENGINE_OPERATIONAL_SPINE_V1.json',
    'record_count':75,
    'rule':'Engine -> ASI Node is not guessed from engine name. It is derived from exact source Engine->Container relationships and the explicit Phase-2 mapping of each operational element E01..E08 to AI/ASI segments and ASI Nodes.',
    'records':records
}
(OUT/'engine_75_phase2_asi_node_bindings_v1.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
print('Generated Engine bindings:',len(records),'unbound source engines:',sum(r['binding_status'].startswith('UNBOUND') for r in records))
