import { stageRecord } from '../shared.js';

const REPOSITORY_SOURCES = {
  canonicality: 'CANONICALITY.json',
  phaseStatus: 'phase2/PHASE_STATUS.json',
  registryReadiness: 'generated/registry_views/registry_readiness.json',
  registries: 'registries/',
  machine: 'machine/',
  raw: 'raw/',
  tools: 'tools/',
  assembledSources: 'generated/assembled_sources/',
  generatedRegistryViews: 'generated/registry_views/',
  generatedRubrics: 'generated/rubrics/',
  generatedTests: 'generated/tests/',
};

export function optionalToolRagStage({ repositoryContext = null, toolResults = [] } = {}) {
  return stageRecord(12, 'optional-tool-rag', 'sourceborn', {
    enabled: true,
    execution: toolResults.length ? 'results-present' : 'available-not-invoked',
    repositorySources: REPOSITORY_SOURCES,
    repositoryContext,
    returnedToolResults: toolResults,
    excludedPaths: ['Grok-ASS'],
  });
}
