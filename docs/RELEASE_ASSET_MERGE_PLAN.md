# Backend Docs Release Merge Plan

This is the conservative policy decision layer built from the 383-asset release manifest plus structural content profiling.

- Release records: **383**
- Canonical reconciliation candidates: **180**
- Exact byte matches already in the repo are skipped.
- Release digest duplicates are skipped for import while all alias records remain in provenance.
- Grok-specific filenames are quarantined; a mixed file is **not** quarantined merely because it mentions Grok.

## Actions

| Action | Assets |
|---|---:|
| `semantic-reconcile-candidate` | 180 |
| `preserve-pointer-and-review` | 159 |
| `quarantine-pointer-only` | 18 |
| `skip-release-duplicate` | 13 |
| `keep-out-of-c-sb-core` | 7 |
| `skip-exact-existing` | 6 |

## Final routes

| Route | Assets |
|---|---:|
| `sourceborn-core` | 93 |
| `reference` | 60 |
| `research` | 56 |
| `model-evidence` | 37 |
| `engines` | 24 |
| `tests-audits` | 24 |
| `parameters` | 20 |
| `quarantine` | 18 |
| `archives-transcripts` | 14 |
| `sequence` | 10 |
| `asi` | 9 |
| `off-project` | 7 |
| `operations` | 6 |
| `wisdom` | 3 |
| `visuals` | 2 |

## Canonical reconciliation queue

These assets are **candidates**, not automatic replacements. The first landing zone is provenance/raw custody; only reconciled concepts/records move into canonical registries, machine contracts, brain stages, tests or docs.

| Route | Asset | Post-review targets | Flags |
|---|---|---|---|
| `asi` | `12_ASI_DEFINITION_AND_HUMAN_AI_CONNECTIONS.md` | `registries/asi/`, `machine/`, `phase2/asi/`, `phase2/sources/` |  |
| `asi` | `13_ASI_BRAIN_PROGRAM_AND_SEVEN_PHASES.md` | `registries/asi/`, `machine/`, `phase2/asi/`, `phase2/sources/` |  |
| `asi` | `ASI-Brain.xlsx` | `registries/asi/`, `machine/`, `phase2/asi/`, `phase2/sources/` |  |
| `asi` | `ASI-Brain_Expansion_Containers_081-160_v1.xlsx` | `registries/asi/`, `machine/`, `phase2/asi/`, `phase2/sources/` |  |
| `asi` | `ASI-Brain_Merged_APPROVED_EVIDENT_v0_3.xlsx` | `registries/asi/`, `machine/`, `phase2/asi/`, `phase2/sources/` | contains_grok_reference |
| `asi` | `ASI-Brain_Task2_Approved_v0_1.xlsx` | `registries/asi/`, `machine/`, `phase2/asi/`, `phase2/sources/` |  |
| `asi` | `ASI_Core_Corpus_AI_Readable_v0_1.md` | `registries/asi/`, `machine/`, `phase2/asi/`, `phase2/sources/` | contains_grok_reference |
| `asi` | `SB_ASI_Worldwide_Research_Discovery_Registry_v0_1.xlsx` | `registries/asi/`, `machine/`, `phase2/asi/`, `phase2/sources/` |  |
| `asi` | `Sourceborn_ASI_Core_Understanding_and_Next_v0.1.md` | `registries/asi/`, `machine/`, `phase2/asi/`, `phase2/sources/` |  |
| `engines` | `02_ID_LAW_AND_SAMPLE_NODE.md` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `02_rd_world_raw_definition_engine_raw_thought_ex.md` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `10_SOURCEBORN_ENGINE_CODE_INTEGRATION.md` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `ARD_Doubt_Engine_Pass_Decode30.md` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `ARD_RGL_3.1_Decision_Engine_Spec.md` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` | contains_grok_reference |
| `engines` | `ASI-Brain_Core_Engine_Combined_v0_4.xlsx` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `ASI_Brain_Engine_Combined_Corpus_v1.xlsx` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `ASI_Engines_Catalog_ARD_SB_Sourceborn_v1.1.xlsx` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `ASI_Engines_Catalog_ARD_SB_Sourceborn_v1.1_Clubbed93.xlsx` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `ASI_Engines_Catalog_CoreZIP_APPROVED_EVIDENT_v2.xlsx` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `ASI_Unified_Engines_and_Brain_Catalog_v1.xlsx` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `Brain.+.Engine.Combined.Corpus.xlsx` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `Brain.+.Engine.Conversation.Record.docx` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `Brain.+.Engine.Library.Index.xlsx` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `Brain_+_Engine_Library_Record.md` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `Raw.Definition.Engine.Source.Code.V0.1.docx` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `RH.docx.extracted.txt` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `S-02_THE_ENGINE.md` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` | contains_grok_reference |
| `engines` | `SB_URR_Engine_Spec_70_25.md` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `sourceborn_asi_king_character_engine.xlsx` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `SRC-044__Raw_Definition_Engine_Source_Code_V0_1.txt` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `SRC-062__Sourceborn_URR_Orchestrator_Reusable_Components.txt` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `engines` | `Unified_Definer_Table.md` | `machine/`, `phase2/sources/`, `brain/12-optional-tool-rag/` |  |
| `operations` | `00_MASTER_WORKSTREAM_INDEX.md` | `docs/ops/`, `docs/deployment/` |  |
| `operations` | `09_RENDER_DEPLOYMENT_HOSTING_AND_APP_MAP.md` | `docs/ops/`, `docs/deployment/` |  |
| `operations` | `23_SITE_CONTROL_APP.md` | `docs/ops/`, `docs/deployment/` |  |
| `operations` | `DEPLOY.md` | `docs/ops/`, `docs/deployment/` |  |
| `operations` | `SRC-058__Site_control.txt` | `docs/ops/`, `docs/deployment/` |  |
| `operations` | `THE_PLAN.md` | `docs/ops/`, `docs/deployment/` |  |
| `parameters` | `03_parameter_bank_64.md` | `registries/human/`, `registries/ai/`, `registries/asi/`, `machine/parameters/` |  |
| `parameters` | `11_parameter_comparison_table.md` | `registries/human/`, `registries/ai/`, `registries/asi/`, `machine/parameters/` |  |
| `parameters` | `14_HUMAN_PARAMETERS_10_80_2560.md` | `registries/human/`, `registries/ai/`, `registries/asi/`, `machine/parameters/` |  |
| `parameters` | `15_AI_PARAMETERS_AND_MODEL_BRAINS.md` | `registries/human/`, `registries/ai/`, `registries/asi/`, `machine/parameters/` |  |
| `parameters` | `ARD_3.1_Parameter_Expansion.md` | `registries/human/`, `registries/ai/`, `registries/asi/`, `machine/parameters/` |  |
| `parameters` | `ARD_Parameter_Mapping_Comparison.md` | `registries/human/`, `registries/ai/`, `registries/asi/`, `machine/parameters/` |  |
| `parameters` | `ARD_Parameters_and_Filters_Master_List.md` | `registries/human/`, `registries/ai/`, `registries/asi/`, `machine/parameters/` | contains_grok_reference |
| `parameters` | `ARD_Parameters_Comparison.md` | `registries/human/`, `registries/ai/`, `registries/asi/`, `machine/parameters/` |  |
| `parameters` | `ASI-0001_tablet_run.xlsx` | `registries/human/`, `registries/ai/`, `registries/asi/`, `machine/parameters/` |  |
| `parameters` | `ASI-Brain_Task3_AI_Readable_11338_Records_v0_2.md` | `registries/human/`, `registries/ai/`, `registries/asi/`, `machine/parameters/` | contains_grok_reference |
| `parameters` | `ASI.Claude.Parameters.docx` | `registries/human/`, `registries/ai/`, `registries/asi/`, `machine/parameters/` |  |
| `parameters` | `ASI.GPT.Parameters.docx` | `registries/human/`, `registries/ai/`, `registries/asi/`, `machine/parameters/` |  |
| `parameters` | `ASI.Work.flow.docx` | `registries/human/`, `registries/ai/`, `registries/asi/`, `machine/parameters/` | contains_grok_reference |
| `parameters` | `SOURCEBORN_parameter_log.md` | `registries/human/`, `registries/ai/`, `registries/asi/`, `machine/parameters/` |  |
| `parameters` | `SOURCEBORN_Parameter_Pyramid_v0_1.xlsx` | `registries/human/`, `registries/ai/`, `registries/asi/`, `machine/parameters/` |  |
| `parameters` | `table.2.csv` | `registries/human/`, `registries/ai/`, `registries/asi/`, `machine/parameters/` |  |
| `parameters` | `table.3.csv` | `registries/human/`, `registries/ai/`, `registries/asi/`, `machine/parameters/` | contains_grok_reference |
| `parameters` | `table.csv` | `registries/human/`, `registries/ai/`, `registries/asi/`, `machine/parameters/` |  |
| `sequence` | `00_MASTER_MERGED_OUTCOME_Raw_Thought_and_Sequence_Map_ASIDE.md` | `raw/sequence/`, `machine/v2/`, `phase2/v2/`, `docs/` | contains_grok_reference |
| `sequence` | `01_PHASE_PLAN.md` | `raw/sequence/`, `machine/v2/`, `phase2/v2/`, `docs/` |  |
| `sequence` | `SOURCEBORN_Universal_Sequence_DRAFT_v0_1.md` | `raw/sequence/`, `machine/v2/`, `phase2/v2/`, `docs/` |  |
| `sequence` | `SRC-055__Secureborn.txt` | `raw/sequence/`, `machine/v2/`, `phase2/v2/`, `docs/` |  |
| `sequence` | `SRC-056__Sequence_to_Sequence__260512_011803.txt` | `raw/sequence/`, `machine/v2/`, `phase2/v2/`, `docs/` |  |
| `sequence` | `THE_REVERSE_WALKS.md` | `raw/sequence/`, `machine/v2/`, `phase2/v2/`, `docs/` |  |
| `sequence` | `THE_SEQUENCES.md` | `raw/sequence/`, `machine/v2/`, `phase2/v2/`, `docs/` |  |
| `sourceborn-core` | `00_MASTER_LEDGER.md` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `00_master_merged_outcome_raw_thought_and_sequenc.md` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `01_SB_URR_PRODUCT_APP.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `02_sourceborn_40q_example_bank_tracker_v0_1.xlsx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `02_SOURCEBORN_CORE_AND_UNIVERSAL_METHOD.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `02_unreal_to_real_rd_world_urr_verifyai_raw_thou.md` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `03_sourceborn_final_theory_point_zero_raw_though.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `03_sourceborn_handoff_readme_and_crunch_v0_1.docx` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `08_GIT_REPOS_BRANCHES_AND_PR_HYGIENE.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `26_MOM_WORKPLACE_AND_URR_REFRAMING.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `99_all_in_one_master.md` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `AGENTS.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `AI.behaviour.docx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `ARD_3.2_Penetration_x_Sourceborn.md` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `BIG_TABLE_COMPARISON.md` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `Build_An_AI.docx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Build_an_AI_Tool.docx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Core.Specification.for.the.SB-AGI.Application.v1.0.docx` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `COVER_NOTE_2_3_PAGES.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Example.docx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `example_bank.docx` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `Forensic_Benchmark_Autopsies_Compiled_Master_4_Models.xlsx` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `G.meta.4.docx` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `gg.txt` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `Human_ROle.docx` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `MASTER_LEDGER.jsonl` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `New.Microsoft.Word.Document.2.docx` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `New.Microsoft.Word.Document.3.docx` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `PROMPT_FOR_ANOTHER_AI_FETCH_ALL_SOURCEBORN.md` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `S-01_THE_METHOD.md` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `SB-AGI.Source.Instruction.File.docx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SB.+.URR.docx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SB.-.Artificial.General.Intelligence.Full.Framework.v1.0.docx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SB.URR.docx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SB_Core_Specification.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SB_URR_95_nodes_with_examples.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SB_URR_Core_Specification_v1.0.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SB_URR_Sourceborn_Core_Backbone_v0_1.docx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `sburr.pre.xlsx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `sourceborn-report.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Sourceborn.70.Dynamic.Local.Brains.Editable.v0.2.xlsx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Sourceborn.vs.Global.Agent.Systems.Full.Editable.Comparison.xlsx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Sourceborn_70_Dynamic_Local_Brains_Editable_v0_2.xlsx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Sourceborn_70_Unique_Local_Brains_Editable_v0_1.xlsx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Sourceborn_ANSWER_Angkor_Wat_RFID_Vetted_New_Meanings.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Sourceborn_ANSWER_Khufu_Cartouche_Vetted_New_Meanings.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Sourceborn_ANSWER_Worldwide_Civilization_Vetted_New_Meanings.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SOURCEBORN_ASI_MASTER_SEQUENCE_v2_START_HERE.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SOURCEBORN_ASO_TREE_AND_REASONING_PILLARS_v2.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Sourceborn_Baghdad_Battery_Dendera_Vast_Analysis_v1.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Sourceborn_Core_State_2026-07-16.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SOURCEBORN_corpus_manifest.xlsx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Sourceborn_Full_Conversation_Archive_2026-07-17.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Sourceborn_Full_Conversation_Archive_Complete.md` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `SOURCEBORN_HANDOFF_v1_START_HERE.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SOURCEBORN_HANDSHAKE.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Sourceborn_Handshake_v2_2026-07-17.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Sourceborn_Khufu_Cartouche_Transparency_Analysis_v1.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Sourceborn_King_Characters_Multiple_Brains_v0.1.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SOURCEBORN_MASTER.2.md` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `Sourceborn_Master_Data_Centre_v2.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Sourceborn_Pyramid_Skeleton_v0.1.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SOURCEBORN_SEQUENCE_FULL_EXAMPLES_v2.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `sourceborn_urr_file_inventory_link_map.xlsx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Sourceborn_URR_PASS_Khufu_Cartouche_v1.md` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `Sourceborn_vs_Global_Agent_Systems_Full_Editable_Comparison_2026-07-13.xlsx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SRC-016__full_uncompressed_sourceborn_ledger.txt` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SRC-017__G_meta_4.txt` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `SRC-047__SB_URR.txt` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SRC-048__SB_URR.txt` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SRC-050__SB-_URR_run.txt` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SRC-051__SB_URR_Sourceborn_Core_Backbone_v0_1.txt` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SRC-052__sburr_pre.txt` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `SRC-053__Secureborn_Instruction.txt` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SRC-057__Simulation.txt` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SRC-060__SOURCEBORN_CORPUS_MAP.txt` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `SRC-061__SOURCEBORN_PRINCIPLE.txt` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SRC-066__URR_02_core__260512_212559.txt` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `SRC-067__URR_Core.txt` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SRC-068__URR_final_table.txt` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `SRC-069__URR_Project_Plan_V1_Claude.txt` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SRC-070__URR_Source_samples_DS_RAW_THOUGHTS.txt` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SRC-071__URR_Appropriate_AI_Responses.txt` | `brain/`, `machine/`, `phase2/`, `docs/` | contains_grok_reference |
| `sourceborn-core` | `SRC-072__URR-07_Final_Clean_Core.txt` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SRC-074__UUR_with_MG.txt` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `SRC-075__UURRR.txt` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `URR-07_Final_Clean_Core.docx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `URR.final.table.xlsx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `URR.Project.Plan.V1.Claude.docx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `sourceborn-core` | `URR_Core_Control_Points_and_Pending_Tasks.docx` | `brain/`, `machine/`, `phase2/`, `docs/` |  |
| `tests-audits` | `03_Adversarial_Audit_Report_Full.md` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` | contains_grok_reference |
| `tests-audits` | `03_URR_RD_VERIFICATION_AND_FILTERS.md` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `tests-audits` | `09_response_scorecard_every_assistant_response.md` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `tests-audits` | `20_USER_EXAMPLE_TEST_BANK.md` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `tests-audits` | `31_ADVERSARIAL_AUDIT_FAILURES_AND_ANTI_DRIFT.md` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `tests-audits` | `AI.Current.flaws.docx` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `tests-audits` | `ARD_3.0_Review.xlsx` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `tests-audits` | `ASI-Brain_Task3_Review.Approved.xlsx` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` | contains_grok_reference |
| `tests-audits` | `Autonomous.LLM.Behavior.and.Core-Execution.Audit.docx` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `tests-audits` | `GG.-2.txt` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `tests-audits` | `GG_-2.txt` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `tests-audits` | `Mirror_Form_paper_Ripudaman.docx.extracted.txt` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `tests-audits` | `Part.-2.docx.extracted.txt` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `tests-audits` | `Purity.test.Grouping.docx` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `tests-audits` | `SB.core.Review.docx` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `tests-audits` | `SB_ASI_Combined_Core_Review_and_Theory_Examples_v0_1.docx` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` | contains_grok_reference |
| `tests-audits` | `Sourceborn.Sequence.Review.-.done.docx` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `tests-audits` | `SOURCEBORN_UNIVERSAL_SEQUENCE_V2_FINAL_REVIEW.md` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `tests-audits` | `SRC-006__ARD_3.0_Review.txt` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `tests-audits` | `SRC-043__Purity_test_Grouping.txt` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `tests-audits` | `SRC-049__SB_core_Review.txt` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `tests-audits` | `SRC-059__Sourceborn_Sequence_Review_-_done.txt` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `tests-audits` | `URR_Flaws_Questions_and_Suggestions.docx` | `phase2/tests/`, `phase2/reviews/`, `phase2/rfr/`, `generated/tests/` |  |
| `visuals` | `unified_catalog_flowchart.png` | `raw/visuals/`, `docs/visuals/` |  |
| `wisdom` | `18_HOLY_BOOKS_VEDAS_AND_CIVILIZATIONAL_SOURCES.md` | `raw/wisdom/`, `phase2/wisdom/`, `registries/wisdom/` |  |
| `wisdom` | `22_wisdom_bank.xlsx` | `raw/wisdom/`, `phase2/wisdom/`, `registries/wisdom/` |  |
| `wisdom` | `S-08_HOLY_BOOKS_and_ARCHETYPE.md` | `raw/wisdom/`, `phase2/wisdom/`, `registries/wisdom/` | contains_grok_reference |

## Safety boundary

`quarantine`, `off-project`, `research`, `model-evidence`, `archives-transcripts`, and generic `reference` assets stay outside canonical Sourceborn structures unless a later explicit review promotes a specific claim/record with provenance.
