import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..');

function readJson(relativePath) {
  try {
    return JSON.parse(fs.readFileSync(path.join(ROOT, relativePath), 'utf8'));
  } catch {
    return null;
  }
}

export function getRepositoryContext() {
  const canonicality = readJson('CANONICALITY.json');
  const phaseStatus = readJson('phase2/PHASE_STATUS.json');
  const readiness = readJson('generated/registry_views/registry_readiness.json');
  const humanWorkstream = phaseStatus?.phase2?.workstreams?.find((item) => item.id === 'P2-HUMAN') ?? null;

  return {
    canonicalityLoaded: Boolean(canonicality),
    phase1Status: phaseStatus?.phase1?.status ?? null,
    phase2Status: phaseStatus?.phase2?.status ?? null,
    human: {
      adoptionStatus: humanWorkstream?.status ?? null,
      generatedRelinkReady: readiness?.human?.ready_for_full_parameter_relink ?? null,
      lockedShape: readiness?.human?.locked_shape ?? null,
    },
    ai: {
      adoptionStatus: readiness?.ai?.adoption_status ?? null,
      sourceStatus: readiness?.ai?.source_status ?? null,
    },
    asi: {
      serviceNodeCount: readiness?.asi?.service_node_count ?? null,
      nodeBrainCount: readiness?.asi?.node_brain_v0_count ?? null,
      nodeBrainStatus: readiness?.asi?.node_brain_status ?? null,
    },
  };
}
