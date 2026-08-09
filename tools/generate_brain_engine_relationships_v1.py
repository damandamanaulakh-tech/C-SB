#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated/registry_views"
OUT.mkdir(parents=True, exist_ok=True)

# Exact engine order per operational container, extracted from
# ASI_Brain_Engine_Combined_Corpus_v1.xlsx / 09 Engine-Container Map.
# Source invariant: first two are Primary operator; remaining three Supporting operator.
ENGINE_MAP = {
    161:['ENG-ARD-003','ENG-ARD-004','ENG-CORE-001','ENG-CORE-002','ENG-CORE-009'],
    162:['ENG-ARD-003','ENG-ARD-004','ENG-CORE-010','ENG-ORC-001','ENG-EXP-001'],
    163:['ENG-ARD-003','ENG-ARD-004','ENG-EXP-002','ENG-ARD-001','ENG-CORE-007'],
    164:['ENG-ARD-003','ENG-ARD-004','ENG-WLD-002','ENG-SB-008','ENG-WLD-001'],
    165:['ENG-ARD-003','ENG-ARD-004','ENG-OUT-001','ENG-RD-001','ENG-RGL-005'],
    166:['ENG-CORE-007','ENG-EVAL-001','ENG-URR-005','ENG-ARD-001','ENG-CORE-006'],
    167:['ENG-CORE-009','ENG-CORE-012','ENG-MEM-001','ENG-ARD-003','ENG-ARD-004'],
    168:['ENG-PAI-001','ENG-RD-003','ENG-ARD-003','ENG-ARD-004','ENG-URR-003'],
    169:['ENG-EXP-001','ENG-CORE-001','ENG-CORE-002','ENG-CORE-009','ENG-GRD-002'],
    170:['ENG-EXP-001','ENG-CORE-010','ENG-ORC-001','ENG-CORE-008','ENG-CORE-009'],
    171:['ENG-EXP-001','ENG-EXP-002','ENG-ARD-001','ENG-CORE-007','ENG-CORE-008'],
    172:['ENG-EXP-001','ENG-WLD-002','ENG-SB-008','ENG-ARD-001','ENG-CORE-003'],
    173:['ENG-EXP-001','ENG-OUT-001','ENG-RD-001','ENG-RGL-005','ENG-SB-005'],
    174:['ENG-CORE-007','ENG-EVAL-001','ENG-URR-005','ENG-EXP-001','ENG-ARD-001'],
    175:['ENG-CORE-009','ENG-CORE-012','ENG-MEM-001','ENG-EXP-001','ENG-ORC-001'],
    176:['ENG-EXP-001','ENG-PAI-001','ENG-RD-003','ENG-URR-003','ENG-URR-006'],
    177:['ENG-CORE-001','ENG-CORE-002','ENG-CORE-003','ENG-CORE-005','ENG-CORE-009'],
    178:['ENG-CORE-010','ENG-ORC-001','ENG-EXP-001','ENG-ARD-001','ENG-CORE-003'],
    179:['ENG-ARD-001','ENG-CORE-011','ENG-EXP-002','ENG-CORE-003','ENG-CORE-005'],
    180:['ENG-SB-008','ENG-ARD-001','ENG-CORE-003','ENG-CORE-005','ENG-RGL-005'],
    181:['ENG-OUT-001','ENG-RGL-005','ENG-SB-005','ENG-ARD-001','ENG-CORE-003'],
    182:['ENG-ARD-001','ENG-CORE-007','ENG-EVAL-001','ENG-URR-005','ENG-CORE-006'],
    183:['ENG-CORE-009','ENG-CORE-012','ENG-MEM-001','ENG-ORC-001','ENG-OUT-001'],
    184:['ENG-PAI-001','ENG-RD-003','ENG-OUT-001','ENG-URR-003','ENG-URR-006'],
    185:['ENG-CORE-002','ENG-CORE-003','ENG-CORE-010','ENG-PAI-001','ENG-SB-001'],
    186:['ENG-CORE-010','ENG-CORE-008','ENG-LOOP-001','ENG-SB-006','ENG-SB-007'],
    187:['ENG-CORE-008','ENG-LOOP-001','ENG-EXP-002','ENG-CORE-002','ENG-CORE-003'],
    188:['ENG-SB-008','ENG-CORE-003','ENG-CORE-002','ENG-CORE-008','ENG-CORE-010'],
    189:['ENG-SB-005','ENG-CORE-003','ENG-CORE-010','ENG-SB-001','ENG-SB-009'],
    190:['ENG-CORE-002','ENG-INF-001','ENG-CORE-007','ENG-EVAL-001','ENG-URR-005'],
    191:['ENG-CORE-010','ENG-OPS-001','ENG-WLD-003','ENG-CORE-009','ENG-CORE-012'],
    192:['ENG-PAI-001','ENG-INF-001','ENG-RD-003','ENG-CORE-008','ENG-LOOP-001'],
    193:['ENG-CORE-001','ENG-CORE-009','ENG-GRD-002','ENG-MEM-001','ENG-RD-002'],
    194:['ENG-ORC-001','ENG-CORE-009','ENG-GRD-001','ENG-PAT-001','ENG-CORE-010'],
    195:['ENG-CORE-007','ENG-GRD-002','ENG-CORE-001','ENG-CORE-009','ENG-CORE-012'],
    196:['ENG-CORE-012','ENG-ORC-001','ENG-CORE-001','ENG-CORE-007','ENG-CORE-009'],
    197:['ENG-GRD-002','ENG-ORC-001','ENG-RD-003','ENG-VER-001','ENG-EVAL-001'],
    198:['ENG-CORE-007','ENG-EVAL-001','ENG-GRD-002','ENG-ORC-001','ENG-RD-002'],
    199:['ENG-CORE-009','ENG-CORE-012','ENG-MEM-001','ENG-ORC-001','ENG-RD-003'],
    200:['ENG-RD-003','ENG-PAI-001','ENG-CORE-012','ENG-RD-002','ENG-VER-002'],
    201:['ENG-CORE-005','ENG-CORE-006','ENG-RD-001','ENG-RGL-001','ENG-URR-002'],
    202:['ENG-RD-001','ENG-URR-004','ENG-CORE-004','ENG-RGL-006','ENG-ARD-001'],
    203:['ENG-EXP-002','ENG-ARD-001','ENG-RGL-001','ENG-RGL-002','ENG-SUP-001'],
    204:['ENG-ARD-001','ENG-CORE-005','ENG-CORE-006','ENG-RGL-004','ENG-RGL-005'],
    205:['ENG-RD-001','ENG-RGL-005','ENG-URR-003','ENG-ARD-001','ENG-CORE-005'],
    206:['ENG-URR-005','ENG-ARD-001','ENG-CORE-006','ENG-URR-002','ENG-URR-004'],
    207:['ENG-CORE-004','ENG-CORE-012','ENG-MEM-001','ENG-RGL-003','ENG-SUP-003'],
    208:['ENG-URR-003','ENG-CORE-006','ENG-RGL-002','ENG-RGL-003','ENG-SUP-001'],
    209:['ENG-OUT-001','ENG-URR-006','ENG-SEQ-001','ENG-CORE-001','ENG-CORE-002'],
    210:['ENG-URR-006','ENG-SEQ-001','ENG-CORE-010','ENG-ORC-001','ENG-OUT-001'],
    211:['ENG-OUT-001','ENG-URR-006','ENG-SEQ-001','ENG-URR-004','ENG-EXP-002'],
    212:['ENG-OUT-001','ENG-URR-006','ENG-SEQ-001','ENG-ORC-001','ENG-WLD-002'],
    213:['ENG-OUT-001','ENG-SEQ-001','ENG-URR-006','ENG-CORE-010','ENG-ORC-001'],
    214:['ENG-EVAL-001','ENG-URR-005','ENG-CORE-007','ENG-URR-004','ENG-OUT-001'],
    215:['ENG-OUT-001','ENG-SEQ-001','ENG-CORE-009','ENG-CORE-012','ENG-MEM-001'],
    216:['ENG-URR-006','ENG-OUT-001','ENG-SEQ-001','ENG-PAI-001','ENG-RD-003'],
    217:['ENG-ARD-003','ENG-WLD-002','ENG-WLD-004','ENG-WLD-001','ENG-WLD-007'],
    218:['ENG-WLD-002','ENG-WLD-004','ENG-WLD-001','ENG-WLD-007','ENG-CORE-010'],
    219:['ENG-WLD-002','ENG-WLD-004','ENG-WLD-001','ENG-WLD-007','ENG-ARD-003'],
    220:['ENG-WLD-002','ENG-WLD-001','ENG-WLD-004','ENG-WLD-007','ENG-RGL-004'],
    221:['ENG-RD-001','ENG-WLD-002','ENG-WLD-004','ENG-WLD-001','ENG-WLD-007'],
    222:['ENG-CORE-007','ENG-EVAL-001','ENG-URR-005','ENG-ARD-001','ENG-CORE-006'],
    223:['ENG-WLD-001','ENG-CORE-009','ENG-CORE-012','ENG-MEM-001','ENG-WLD-002'],
    224:['ENG-PAI-001','ENG-RD-003','ENG-URR-006','ENG-WLD-002','ENG-WLD-004'],
    225:['ENG-RD-002','ENG-RD-003','ENG-WLD-005','ENG-CORE-001','ENG-CORE-002'],
    226:['ENG-EXP-001','ENG-WLD-005','ENG-CORE-010','ENG-ORC-001','ENG-SB-006'],
    227:['ENG-WLD-005','ENG-EXP-002','ENG-ARD-001','ENG-CORE-007','ENG-CORE-008'],
    228:['ENG-WLD-002','ENG-WLD-005','ENG-SB-008','ENG-ARD-001','ENG-CORE-003'],
    229:['ENG-WLD-005','ENG-OUT-001','ENG-RD-001','ENG-RD-003','ENG-RGL-005'],
    230:['ENG-CORE-007','ENG-EVAL-001','ENG-RGL-006','ENG-URR-005','ENG-ARD-001'],
    231:['ENG-CORE-009','ENG-CORE-012','ENG-MEM-001','ENG-RD-003','ENG-WLD-005'],
    232:['ENG-RD-003','ENG-PAI-001','ENG-WLD-005','ENG-RD-002','ENG-RGL-003'],
    233:['ENG-REV-001','ENG-CORE-001','ENG-CORE-002','ENG-CORE-009','ENG-GRD-001'],
    234:['ENG-EVO-001','ENG-META-001','ENG-META-002','ENG-SUP-002','ENG-SUP-004'],
    235:['ENG-EVO-001','ENG-META-001','ENG-META-002','ENG-SUP-002','ENG-SUP-004'],
    236:['ENG-META-001','ENG-SB-008','ENG-EVO-001','ENG-META-002','ENG-SUP-002'],
    237:['ENG-REV-001','ENG-SB-005','ENG-EVO-001','ENG-META-001','ENG-META-002'],
    238:['ENG-CORE-007','ENG-URR-005','ENG-ARD-001','ENG-CORE-006','ENG-URR-002'],
    239:['ENG-CORE-009','ENG-CORE-012','ENG-EVO-001','ENG-META-002','ENG-SUP-004'],
    240:['ENG-PAI-001','ENG-EVO-001','ENG-META-002','ENG-SUP-002','ENG-SUP-004'],
}

# Most parameter-source relations use COG-<ENGINE_ID>. These exact source exceptions
# are extracted from sheet 10; an engine has one stable source string across the sheet.
SOURCE_OVERRIDES = {
    'ENG-ARD-001':'COG-ENG-ARD-001; COG-CMP-CMP-006; COG-CMP-CMP-007',
    'ENG-CORE-001':'SRC-001; SRC-006; SRC-007',
    'ENG-CORE-002':'SRC-010; SRC-023; SRC-025',
    'ENG-CORE-004':'COG-ENG-CORE-004; COG-CMP-CMP-041; COG-CMP-CMP-076',
    'ENG-CORE-006':'COG-ENG-CORE-006; COG-CMP-CMP-013; COG-CMP-CMP-014',
    'ENG-CORE-007':'SRC-011; COG-ENG-CORE-007',
    'ENG-CORE-008':'COG-ENG-CORE-008; COG-CMP-CMP-021; COG-CMP-CMP-022',
    'ENG-CORE-009':'SRC-061; COG-ENG-CORE-009',
    'ENG-CORE-012':'COG-ENG-CORE-012; COG-CMP-CMP-097',
    'ENG-EVAL-001':'SRC-040; COG-ENG-EVAL-001; COG-CMP-CMP-059',
    'ENG-INF-001':'SRC-034; COG-ENG-INF-001; COG-CMP-CMP-034',
    'ENG-MEM-001':'COG-ENG-MEM-001; COG-CMP-CMP-031; COG-CMP-CMP-033',
    'ENG-OPS-001':'SRC-058; COG-ENG-OPS-001',
    'ENG-ORC-001':'SRC-062; COG-ENG-ORC-001',
    'ENG-OUT-001':'SRC-028; SRC-073; SRC-074',
    'ENG-PAI-001':'SRC-041; SRC-042; COG-ENG-PAI-001',
    'ENG-RD-001':'SRC-027; SRC-044; SRC-045',
    'ENG-RD-002':'SRC-009; SRC-060; SRC-065',
    'ENG-RD-003':'SRC-053; SRC-055; COG-ENG-RD-003',
    'ENG-RGL-001':'SRC-002; SRC-003; SRC-004',
    'ENG-URR-003':'SRC-071; SRC-072; COG-ENG-URR-003',
    'ENG-URR-004':'SRC-012; COG-ENG-URR-004',
    'ENG-URR-005':'SRC-066; COG-ENG-URR-005',
}

def source_for(engine_id):
    return SOURCE_OVERRIDES.get(engine_id, 'COG-' + engine_id)

engine_container = []
parameter_source = []
compact = []
for cnum in range(161, 241):
    cid = f'CON-{cnum:03d}'
    engines = ENGINE_MAP[cnum]
    for rank, eid in enumerate(engines, start=1):
        engine_container.append({
            'mapping_id': f'ECM-{cnum:03d}-{rank:02d}',
            'container_id': cid,
            'engine_id': eid,
            'relationship_role': 'Primary operator' if rank <= 2 else 'Supporting operator',
            'execution_rank': rank,
            'approval_status': 'APPROVED BY USER',
            'evidence_status': 'USER EVIDENT',
        })
    # Source sheet invariant: each of the six parameters in a container has the same
    # first-three engine/source bundle; relation 1 is Primary execution, 2/3 support.
    source_bundle=[]
    for idx, eid in enumerate(engines[:3], start=1):
        source_bundle.append([eid, source_for(eid), 'Primary execution' if idx == 1 else 'Cross-check / support'])
    start_pid = 2593 + (cnum - 161) * 6
    for local in range(6):
        pid = f'SB-ASI-P{start_pid + local:04d}'
        for idx, (eid, sources, role) in enumerate(source_bundle, start=1):
            parameter_source.append({
                'mapping_id': f'PES-{start_pid + local}-{idx}',
                'parameter_id': pid,
                'container_id': cid,
                'engine_id': eid,
                'cognitive_source_ids': sources,
                'role': role,
                'proof_debt_rule': 'Unresolved contradiction or missing external evidence remains labeled',
                'approval_status': 'APPROVED BY USER',
                'evidence_status': 'USER EVIDENT',
            })
    compact.append({'container_id':cid,'engine_ids':engines,'parameter_source_bundle':source_bundle})

assert len(engine_container) == 400
assert len(parameter_source) == 1440
assert len(compact) == 80

(OUT / 'brain_engine_relationships_compact_v1.json').write_text(json.dumps({
    'registry_id':'BRAIN-ENGINE-RELATIONSHIPS-COMPACT-V1',
    'status':'EXACT_SOURCE_DERIVED_APPROVED_USER_EVIDENT',
    'source':'ASI_Brain_Engine_Combined_Corpus_v1.xlsx#09 Engine-Container Map + #10 Parameter-Source Map',
    'compression_rule':'Lossless: 5 engine relations per operational container; six parameters per container share the same 3 engine/source bundle.',
    'engine_container_relationship_count':400,
    'parameter_engine_source_relationship_count':1440,
    'containers':compact,
}, indent=2), encoding='utf-8')

(OUT / 'engine_container_relationships_v1.json').write_text(json.dumps({
    'record_count':400,'records':engine_container}, indent=2), encoding='utf-8')
(OUT / 'parameter_engine_source_relationships_v1.json').write_text(json.dumps({
    'record_count':1440,'records':parameter_source}, indent=2), encoding='utf-8')
print('Generated exact source-derived relationships: 400 engine-container + 1440 parameter-engine/source')
