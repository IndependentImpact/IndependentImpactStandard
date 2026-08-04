# Semantic Web Artefact Hierarchy

This document describes the full hierarchy of semantic web artefacts in the Nova Institute Impact Accounting Standard (NIAS) corpus — which artefact uses which, the order in which they are defined, and the part of the process each one belongs to. It also provides a complete, deduplicated index of every `.ttl` file with its function, prerequisites and dependents.

## Contents

1. [Overview](#overview)
2. [Artefact Layers](#artefact-layers)
   - [Layer 0 — External Ontologies](#layer-0--external-ontologies)
   - [Layer 1 — Core OWL Ontology](#layer-1--core-owl-ontology)
   - [Layer 2 — Concept Schemes & Controlled Vocabularies](#layer-2--concept-schemes--controlled-vocabularies)
   - [Layer 3 — SHACL Validation Shapes](#layer-3--shacl-validation-shapes)
   - [Layer 3a — VVS Requirement Shapes & Mappings](#layer-3a--vvs-requirement-shapes--mappings)
   - [Layer 4 — UI Projection Shapes](#layer-4--ui-projection-shapes)
3. [Dependency Diagram](#dependency-diagram)
4. [Artefact Index](#artefact-index)
5. [Deduplication Status](#deduplication-status)
6. [Context-Specific Shapes (Intentional Variance)](#context-specific-shapes-intentional-variance)

---

## Overview

The NIAS semantic artefacts are arranged in four hierarchical layers. Each layer builds strictly on the layer(s) below it. No artefact may redefine a class, property, concept or shape that is already defined at a lower layer.

```
Layer 0   External Ontologies          (imported, not modified)
   │
Layer 1   Core OWL Ontology            glossary/NovaImpactAccountingStandardOntology.ttl
   │
Layer 2   Concept Schemes              glossary/{Principle, ScoringRules, ReputationRules,
   │       & Controlled Vocabs         ReviewMandateConcepts, GuidingReviewQuestions,
   │                                   NovaImpactAccountingStandardGlossary,
   │                                   ValidationVerificationStandard}.ttl
   │         (validated by)
   │       Concept Scheme Shapes       glossary/{PrincipleShapes, ScoringRulesShapes,
   │                                   ReputationRulesShapes, NovaImpactAccountingStandardShapes}.ttl
   │
Layer 3   SHACL Validation Shapes      dataRequirements/common-shapes.ttl  (base)
   │                                   dataRequirements/{document-reference, document,
   │                                   project-design, impact-declaration, stakeholder-engagement,
   │                                   report, review, certificate, pdd-certificate,
   │                                   license, data-lineage, project-listing,
   │                                   monitoring-report, artifact-anchor,
   │                                   artifact-identity-contract,
   │                                   requirement-coverage-proof}.ttl
   │
Layer 3a  VVS Requirement Shapes       dataRequirements/vvs-requirement-shapes.ttl
   │       & Requirement Mappings      dataRequirements/mappings/{pdd,dlr,mr}-anchor-definitions.ttl
   │                                   dataRequirements/mappings/{pdd,dlr,mr}-requirement-map.ttl
   │                                   dataRequirements/mappings/{vvs-requirement-anchor-map,
   │                                                              vvs-deprecation-map}.ttl
   │
Layer 4   UI Projection Shapes         dataRequirements/shape2form/common-ui-shapes.ttl  (base)
           (shape2form bundles)     dataRequirements/shape2form/{pdd-design,
                                       pdd-workflow, monitoring-report,
                                       validation-report, verification-report}-ui-shapes.ttl
```

---

## Artefact Layers

### Layer 0 — External Ontologies

These ontologies are imported by the NIAS core ontology and are **not** modified. They provide foundational vocabulary reused throughout the corpus.

| IRI | Purpose |
|---|---|
| `http://independentimpact.org/methont/methont.ttl/1.1.0` | Impact methodology ontology (Independent Impact) |
| `http://w3id.org/aiao` | Additionality, Attributability, and Impact Ontology |
| `http://w3id.org/claimont` | Claim ontology |
| `http://w3id.org/impactont` | Impact ontology |
| `http://w3id.org/infocomm` | Information and communication ontology |
| `https://hashgraphontology.xyz/consensus` | Hedera/Hashgraph consensus ontology |
| `https://hashgraphontology.xyz/core` | Hedera/Hashgraph core ontology |

---

### Layer 1 — Core OWL Ontology

Defined first. All NIAS classes, object properties and data properties are declared here. Nothing else may declare new OWL classes or properties.

**File:** `glossary/NovaImpactAccountingStandardOntology.ttl`  
**Ontology IRI:** `https://nova.org.za/novaimpactaccountingstandard/`

Key artefacts defined here include: `Project`, `ProjectDesign`, `CreditingPeriod`, `TechnologyOrMeasure`, `SpatialLocation`, `Objective`, `DataParameterRequirement`, `IndicatorValue`, `StateWithIndicatorValue`, `ImpactRequirement`, `ImpactClaim`, `ImpactSummary`, `MonitoringReport`, `ValidationReport`, `VerificationReport`, `ProjectParty`, `DocumentReference`, `DocumentSchema`, `Dataset`, `ReviewMandate`, `OperationalVocabularyTerm`, and all associated properties.

---

### Layer 2 — Concept Schemes & Controlled Vocabularies

SKOS concept schemes and concepts are defined at this layer after the OWL ontology. Each scheme populates the controlled vocabularies used by the shape constraints in Layer 3.

**SKOS concept schemes** (defined using `skos:ConceptScheme` and `skos:Concept`):

| File | Schemes defined |
|---|---|
| `glossary/Principle.ttl` | `ImpactPrinciple`, `AccountingPrinciple` |
| `glossary/ScoringRules.ttl` | Scoring rule concepts |
| `glossary/ReputationRules.ttl` | Reputation rule concepts |
| `glossary/ReviewMandateConcepts.ttl` | `ReviewMandate` concepts |
| `glossary/GuidingReviewQuestions.ttl` | `GuidingReviewQuestionCatalog` |
| `glossary/NovaImpactAccountingStandardGlossary.ttl` | `BeneficialOrAdverse`, `AuthProof`, `TechMeasType`, `ImpactIntentionality`, `MonitoredOrFixed`, `ReportStatus`, `ReviewDecision` and others |
| `glossary/ValidationVerificationStandard.ttl` | `RequirementStatus` |

**SHACL shapes validating the concept schemes** (also Layer 2):

| File | Validates |
|---|---|
| `glossary/PrincipleShapes.ttl` | `Principle.ttl` concept scheme structure |
| `glossary/ScoringRulesShapes.ttl` | `ScoringRules.ttl` concept scheme structure |
| `glossary/ReputationRulesShapes.ttl` | `ReputationRules.ttl` concept scheme structure |
| `glossary/NovaImpactAccountingStandardShapes.ttl` | Glossary concept scheme structure |

---

### Layer 3 — SHACL Validation Shapes

Core SHACL constraint shapes for all data submissions. Built in dependency order — shapes lower in the stack import those above.

**Base shapes** (no internal dependencies beyond Layer 1):

- `dataRequirements/common-shapes.ttl` — time intervals, crediting periods, technologies, spatial locations, project parties, data parameters, indicator values, state objects
- `dataRequirements/artifact-anchor-shapes.ttl` — base anchor shape for artifact identity
- `dataRequirements/vvs-requirement-shapes.ttl` — VVS requirement catalogue shapes

**Mid-level shapes** (import `CommonShapes` or `ArtifactAnchorShapes`):

- `dataRequirements/document-reference-shapes.ttl` → imports `CommonShapes`
- `dataRequirements/impact-declaration-shapes.ttl` → imports `CommonShapes`
- `dataRequirements/project-design-shapes.ttl` → imports `CommonShapes`

**Upper-level shapes** (import `DocumentReferenceShapes` or `DocumentShapes`):

- `dataRequirements/document-shapes.ttl` → imports `CommonShapes`, `DocumentReferenceShapes`
- `dataRequirements/report-shapes.ttl` → imports `CommonShapes`, `DocumentReferenceShapes`, `DocumentShapes`
- `dataRequirements/review-shapes.ttl` → imports `ArtifactAnchorShapes`, `DocumentReferenceShapes`
- `dataRequirements/certificate-shapes.ttl` → imports `DocumentReferenceShapes`, `DocumentShapes`
- `dataRequirements/pdd-certificate-shapes.ttl` → imports `DocumentReferenceShapes`, `DocumentShapes`
- `dataRequirements/license-shapes.ttl` → imports `DocumentReferenceShapes`, `DocumentShapes`
- `dataRequirements/data-lineage-shapes.ttl` → imports `DocumentReferenceShapes`, `DocumentShapes`
- `dataRequirements/project-listing-shapes.ttl` → imports `DocumentShapes`
- `dataRequirements/stakeholder-engagement-shapes.ttl` → imports `DocumentShapes`, `DocumentReferenceShapes`
- `dataRequirements/monitoring-report-shapes.ttl` → imports `DocumentReferenceShapes`, `DocumentShapes`

**Artifact identity shapes** (import upper-level shapes):

- `dataRequirements/artifact-identity-contract-shapes.ttl` → imports `DocumentShapes`, `ReviewShapes`
- `dataRequirements/requirement-coverage-proof-shapes.ttl` → imports `ArtifactAnchorShapes`

---

### Layer 3a — VVS Requirement Shapes & Mappings

The Validation, Verification and Certification Standard (VVS) requirement catalogue and its traceability mappings are defined here. These describe the formal requirements that PDD, Data Lineage and Monitoring Report artefacts must fulfil to be certified.

**VVS catalogue:**

- `dataRequirements/vvs-requirement-shapes.ttl` — shapes for VVS requirement instances

**Anchor definitions** (define section anchors for each document type):

- `dataRequirements/mappings/pdd-anchor-definitions.ttl`
- `dataRequirements/mappings/dlr-anchor-definitions.ttl`
- `dataRequirements/mappings/monitoring-anchor-definitions.ttl`

**Requirement traceability maps** (map requirements to document sections):

- `dataRequirements/mappings/pdd-requirement-map.ttl`
- `dataRequirements/mappings/dlr-requirement-map.ttl`
- `dataRequirements/mappings/mr-requirement-map.ttl`

**Utility maps:**

- `dataRequirements/mappings/vvs-requirement-anchor-map.ttl` — maps requirements to their anchor concepts
- `dataRequirements/mappings/vvs-deprecation-map.ttl` — tracks deprecated VVS requirement IRIs

---

### Layer 4 — UI Projection Shapes

`sh:NodeShape` definitions used by the `shape2form` tool to generate Flutter UI forms and JSON-LD schemas. These shapes are **projections** of the Layer 3 shapes; they do not redefine classes or properties.

**Shared base (new — deduplication result):**

- `dataRequirements/shape2form/common-ui-shapes.ttl` — 17 UI node shapes that are identical across all workflow bundles. Every bundle imports this file at build time (via file merge in the build scripts).

**Workflow-specific bundles** (each is a self-contained UI bundle for one workflow context):

| File | Workflow | Context-specific shapes |
|---|---|---|
| `dataRequirements/shape2form/pdd-design-ui-shapes.ttl` | PDD Design capture tool | `PddSectionA/B/CUiShape`, `PddSectionA/BReportContentUiShape` |
| `dataRequirements/shape2form/pdd-workflow-ui-shapes.ttl` | PDD workflow shell (create + validate) | `PddSectionA/B/CUiShape`, `DocumentFieldReviewUiShape`, `GlobalQualitativeDocumentReviewUiShape` |
| `dataRequirements/shape2form/monitoring-report-ui-shapes.ttl` | Monitoring Report capture | `MonitoringReportUiShape`, `ReviewTargetUiShape`, `MonitoringReportSectionContentUiShape` |
| `dataRequirements/shape2form/validation-report-ui-shapes.ttl` | Validation Report workflow | `ValidationReportSectionUiShape`, `DocumentFieldReviewUiShape`, `GlobalQualitativeDocumentReviewUiShape`, `ReviewTargetUiShape` |
| `dataRequirements/shape2form/verification-report-ui-shapes.ttl` | Verification Report workflow | `VerificationReportSectionUiShape`, `VerifiedImpactCertificateIssuanceRequestReviewShape`, `ReviewTargetUiShape` |

---

## Dependency Diagram

```
External Ontologies (Layer 0)
         │
         ▼
NovaImpactAccountingStandardOntology.ttl  (Layer 1)
         │
         ├──► Principle.ttl / PrincipleShapes.ttl
         ├──► ScoringRules.ttl / ScoringRulesShapes.ttl
         ├──► ReputationRules.ttl / ReputationRulesShapes.ttl
         ├──► ReviewMandateConcepts.ttl
         ├──► GuidingReviewQuestions.ttl
         ├──► NovaImpactAccountingStandardGlossary.ttl / NovaImpactAccountingStandardShapes.ttl
         └──► ValidationVerificationStandard.ttl               (Layer 2)
                        │
                        ▼
                 common-shapes.ttl
                 artifact-anchor-shapes.ttl
                 vvs-requirement-shapes.ttl                     (Layer 3 — base)
                        │
                        ├──► document-reference-shapes.ttl
                        ├──► impact-declaration-shapes.ttl
                        └──► project-design-shapes.ttl          (Layer 3 — mid)
                                      │
                                      ▼
                              document-shapes.ttl               (Layer 3 — upper)
                                      │
                        ┌────────────┬┴──────────────┬──────────────────────┐
                        ▼            ▼               ▼                      ▼
                  report-shapes  review-shapes  certificate-shapes     stakeholder-
                  data-lineage   pdd-cert       license-shapes         engagement-shapes
                  monitoring-    project-listing-shapes                project-listing
                  report-shapes
                        │
                        ├──► artifact-identity-contract-shapes.ttl
                        └──► requirement-coverage-proof-shapes.ttl  (Layer 3 — top)
                                      │
                  ┌───────────────────┼────────────────────────┐
                  ▼                   ▼                        ▼
         pdd-anchor-definitions  dlr-anchor-definitions  monitoring-anchor-definitions
         pdd-requirement-map     dlr-requirement-map     mr-requirement-map
         vvs-requirement-anchor-map / vvs-deprecation-map       (Layer 3a)
                                      │
                                      ▼
                          common-ui-shapes.ttl  (Layer 4 — base)
                                      │
              ┌───────────┬───────────┼────────────┬──────────────────┐
              ▼           ▼           ▼            ▼                  ▼
        pdd-design  pdd-workflow  monitoring  validation         verification
        -ui-shapes  -ui-shapes   -report-    -report-           -report-
        .ttl        .ttl         ui-shapes   ui-shapes          ui-shapes
                                 .ttl        .ttl               .ttl       (Layer 4 — bundles)
```

---

## Artefact Index

### Layer 1 — Core OWL Ontology

| File | Type | Function | Prerequisites | Dependents |
|---|---|---|---|---|
| `glossary/NovaImpactAccountingStandardOntology.ttl` | OWL Ontology | Declares all NIAS OWL classes and properties | Layer 0 external ontologies | All Layer 2–4 artefacts |

### Layer 2 — Concept Schemes

| File | Type | Function | Prerequisites | Dependents |
|---|---|---|---|---|
| `glossary/Principle.ttl` | SKOS ConceptScheme | Impact and accounting principles vocabulary | Core Ontology | `PrincipleShapes.ttl`, Layer 3 shapes |
| `glossary/PrincipleShapes.ttl` | SHACL Shapes | Validates `Principle.ttl` structure | Core Ontology | CI validation |
| `glossary/ScoringRules.ttl` | SKOS ConceptScheme | Scoring rules vocabulary | Core Ontology | `ScoringRulesShapes.ttl`, Layer 3 shapes |
| `glossary/ScoringRulesShapes.ttl` | SHACL Shapes | Validates `ScoringRules.ttl` structure | Core Ontology | CI validation |
| `glossary/ReputationRules.ttl` | SKOS ConceptScheme | Reputation rules vocabulary | Core Ontology | `ReputationRulesShapes.ttl`, Layer 3 shapes |
| `glossary/ReputationRulesShapes.ttl` | SHACL Shapes | Validates `ReputationRules.ttl` structure | Core Ontology | CI validation |
| `glossary/ReviewMandateConcepts.ttl` | SKOS ConceptScheme | Review mandate concepts | Core Ontology | Layer 3 review shapes |
| `glossary/GuidingReviewQuestions.ttl` | SKOS ConceptScheme | Guiding review question catalogue (GQ-001…) | Core Ontology | Validation/verification UI shapes |
| `glossary/NovaImpactAccountingStandardGlossary.ttl` | SKOS ConceptScheme | Master NIAS concept glossary (status codes, decision types, etc.) | Core Ontology | `NovaImpactAccountingStandardShapes.ttl`, all shape files |
| `glossary/NovaImpactAccountingStandardShapes.ttl` | SHACL Shapes | Validates NIAS glossary concept scheme structure | Core Ontology | CI validation |
| `glossary/ValidationVerificationStandard.ttl` | SKOS ConceptScheme | VVS requirement status vocabulary | Core Ontology | `vvs-requirement-shapes.ttl` |

### Layer 3 — SHACL Validation Shapes (base)

| File | Type | Function | Prerequisites | Dependents |
|---|---|---|---|---|
| `dataRequirements/common-shapes.ttl` | SHACL Shapes | Core reusable shapes: time instants, intervals, crediting periods, technologies, spatial locations, parties, data parameters, indicators, state objects | Core Ontology | All other shape files |
| `dataRequirements/artifact-anchor-shapes.ttl` | SHACL Shapes | Base shape for artifact identity anchors used in VVS traceability | Core Ontology | `review-shapes.ttl`, `requirement-coverage-proof-shapes.ttl` |
| `dataRequirements/vvs-requirement-shapes.ttl` | SHACL Shapes | VVS requirement catalogue shapes | Core Ontology, `ValidationVerificationStandard.ttl` | VVS requirement maps |

### Layer 3 — SHACL Validation Shapes (mid-level)

| File | Type | Function | Prerequisites | Dependents |
|---|---|---|---|---|
| `dataRequirements/document-reference-shapes.ttl` | SHACL Shapes | Document reference and IPFS artifact shapes | `common-shapes.ttl` | `document-shapes.ttl`, `certificate-shapes.ttl`, `pdd-certificate-shapes.ttl`, `license-shapes.ttl`, `data-lineage-shapes.ttl`, `monitoring-report-shapes.ttl`, `stakeholder-engagement-shapes.ttl` |
| `dataRequirements/impact-declaration-shapes.ttl` | SHACL Shapes | Impact claim and impact requirement shapes | `common-shapes.ttl` | `project-design-shapes.ttl` |
| `dataRequirements/project-design-shapes.ttl` | SHACL Shapes | Project Design Document (PDD) shapes | `common-shapes.ttl` | `artifact-identity-contract-shapes.ttl` |

### Layer 3 — SHACL Validation Shapes (upper-level)

| File | Type | Function | Prerequisites | Dependents |
|---|---|---|---|---|
| `dataRequirements/document-shapes.ttl` | SHACL Shapes | Document schema, workflow submission, document author shapes | `common-shapes.ttl`, `document-reference-shapes.ttl` | `certificate-shapes.ttl`, `pdd-certificate-shapes.ttl`, `license-shapes.ttl`, `data-lineage-shapes.ttl`, `monitoring-report-shapes.ttl`, `stakeholder-engagement-shapes.ttl`, `report-shapes.ttl`, `project-listing-shapes.ttl`, `artifact-identity-contract-shapes.ttl` |
| `dataRequirements/report-shapes.ttl` | SHACL Shapes | Generic report shapes shared by monitoring, validation, verification | `common-shapes.ttl`, `document-reference-shapes.ttl`, `document-shapes.ttl` | `monitoring-report-shapes.ttl` |
| `dataRequirements/review-shapes.ttl` | SHACL Shapes | Review mandate, review decision, document field review shapes | `artifact-anchor-shapes.ttl`, `document-reference-shapes.ttl` | `artifact-identity-contract-shapes.ttl` |
| `dataRequirements/certificate-shapes.ttl` | SHACL Shapes | Impact certificate shapes | `document-reference-shapes.ttl`, `document-shapes.ttl` | `pdd-certificate-shapes.ttl` |
| `dataRequirements/pdd-certificate-shapes.ttl` | SHACL Shapes | PDD-specific certificate shapes | `document-reference-shapes.ttl`, `document-shapes.ttl` | Layer 4 validation UI bundle |
| `dataRequirements/license-shapes.ttl` | SHACL Shapes | License artefact shapes | `document-reference-shapes.ttl`, `document-shapes.ttl` | Layer 4 verification UI bundle |
| `dataRequirements/data-lineage-shapes.ttl` | SHACL Shapes | Data Lineage Record (DLR) shapes | `document-reference-shapes.ttl`, `document-shapes.ttl` | Layer 3a mappings |
| `dataRequirements/monitoring-report-shapes.ttl` | SHACL Shapes | Monitoring Report shapes | `document-reference-shapes.ttl`, `document-shapes.ttl` | Layer 3a mappings, Layer 4 monitoring UI bundle |
| `dataRequirements/project-listing-shapes.ttl` | SHACL Shapes | Project listing shapes | `document-shapes.ttl` | Layer 4 PDD UI bundles |
| `dataRequirements/stakeholder-engagement-shapes.ttl` | SHACL Shapes | Stakeholder engagement record shapes | `document-shapes.ttl`, `document-reference-shapes.ttl` | Layer 4 PDD design UI bundle |

### Layer 3 — SHACL Validation Shapes (top-level)

| File | Type | Function | Prerequisites | Dependents |
|---|---|---|---|---|
| `dataRequirements/artifact-identity-contract-shapes.ttl` | SHACL Shapes | Submitted artifact identity contract (links PDD, DLR, MR) | `document-shapes.ttl`, `review-shapes.ttl` | Layer 3a VVS mappings |
| `dataRequirements/requirement-coverage-proof-shapes.ttl` | SHACL Shapes | Proof that all VVS requirements are covered by document sections | `artifact-anchor-shapes.ttl` | Layer 3a VVS mappings |

### Layer 3a — VVS Requirement Shapes & Mappings

| File | Type | Function | Prerequisites | Dependents |
|---|---|---|---|---|
| `dataRequirements/mappings/pdd-anchor-definitions.ttl` | OWL/SKOS | PDD section anchor concept definitions | Core Ontology | `pdd-requirement-map.ttl`, `vvs-requirement-anchor-map.ttl` |
| `dataRequirements/mappings/dlr-anchor-definitions.ttl` | OWL/SKOS | DLR section anchor concept definitions | Core Ontology | `dlr-requirement-map.ttl`, `vvs-requirement-anchor-map.ttl` |
| `dataRequirements/mappings/monitoring-anchor-definitions.ttl` | OWL/SKOS | Monitoring Report section anchor definitions | Core Ontology | `mr-requirement-map.ttl`, `vvs-requirement-anchor-map.ttl` |
| `dataRequirements/mappings/pdd-requirement-map.ttl` | OWL/RDF | Maps VVS requirements to PDD section anchors | `pdd-anchor-definitions.ttl`, `vvs-requirement-shapes.ttl` | Validation tooling |
| `dataRequirements/mappings/dlr-requirement-map.ttl` | OWL/RDF | Maps VVS requirements to DLR section anchors | `dlr-anchor-definitions.ttl`, `vvs-requirement-shapes.ttl` | Validation tooling |
| `dataRequirements/mappings/mr-requirement-map.ttl` | OWL/RDF | Maps VVS requirements to Monitoring Report section anchors | `monitoring-anchor-definitions.ttl`, `vvs-requirement-shapes.ttl` | Validation tooling |
| `dataRequirements/mappings/vvs-requirement-anchor-map.ttl` | OWL/RDF | Master map from requirements to their canonical anchor concepts | All anchor definitions | Requirement coverage tooling |
| `dataRequirements/mappings/vvs-deprecation-map.ttl` | OWL/RDF | Tracks deprecated VVS requirement IRIs and their replacements | `vvs-requirement-shapes.ttl` | Migration tooling |

### Layer 4 — UI Projection Shapes

| File | Type | Function | Prerequisites | Dependents |
|---|---|---|---|---|
| `dataRequirements/shape2form/common-ui-shapes.ttl` | SHACL NodeShapes (UI) | 17 shared UI shapes used identically across all workflow bundles | Layer 3 shapes | All 5 workflow bundles (merged at build time) |
| `dataRequirements/shape2form/pdd-design-ui-shapes.ttl` | SHACL NodeShapes (UI) | PDD capture forms for the standalone PDD design tool | `common-ui-shapes.ttl`, `project-design-shapes.ttl` | `build-pdd-design.sh` output |
| `dataRequirements/shape2form/pdd-workflow-ui-shapes.ttl` | SHACL NodeShapes (UI) | PDD workflow shell forms (PDD creation + validation review) | `common-ui-shapes.ttl`, `project-design-shapes.ttl`, `review-shapes.ttl` | `build-pdd-workflow.sh` output |
| `dataRequirements/shape2form/monitoring-report-ui-shapes.ttl` | SHACL NodeShapes (UI) | Monitoring Report capture forms | `common-ui-shapes.ttl`, `monitoring-report-shapes.ttl` | `build-monitoring-report.sh` output |
| `dataRequirements/shape2form/validation-report-ui-shapes.ttl` | SHACL NodeShapes (UI) | Validation Report workflow forms | `common-ui-shapes.ttl`, `review-shapes.ttl`, `pdd-certificate-shapes.ttl` | `build-validation-report.sh` output |
| `dataRequirements/shape2form/verification-report-ui-shapes.ttl` | SHACL NodeShapes (UI) | Verification Report workflow forms | `common-ui-shapes.ttl`, `review-shapes.ttl`, `certificate-shapes.ttl` | `build-verification-report.sh` output |

---

## Deduplication Status

### Core Semantic Artefacts (Layers 1–3a)

All 37 core semantic artefact files (`glossary/*.ttl`, `dataRequirements/*.ttl`, `dataRequirements/mappings/*.ttl`) are **fully deduplicated**. No OWL class, OWL property, SKOS concept scheme, SKOS concept, or SHACL `NodeShape`/`PropertyShape` IRI appears more than once across the corpus.

### UI Projection Shapes (Layer 4)

Prior to this deduplication effort, the 5 workflow UI bundle files collectively contained **17 identical `sh:NodeShape` definitions** duplicated across multiple files. These have been consolidated into `dataRequirements/shape2form/common-ui-shapes.ttl` and removed from all 5 bundle files.

The 17 shapes moved to `common-ui-shapes.ttl`:

| Shape IRI | Previously in |
|---|---|
| `nias-ui:TimeInstantUiShape` | pdd-design, pdd-workflow, monitoring-report, validation-report, verification-report |
| `nias-ui:DateTimeIntervalUiShape` | pdd-design, pdd-workflow, monitoring-report, validation-report, verification-report |
| `nias-ui:HederaTopicMessageUiShape` | pdd-design, pdd-workflow, monitoring-report, validation-report, verification-report |
| `nias-ui:WorkflowDocumentSubmissionUiShape` | pdd-design, pdd-workflow, monitoring-report, validation-report, verification-report |
| `nias-ui:DocumentReferenceUiShape` | pdd-design, pdd-workflow, monitoring-report, validation-report, verification-report |
| `nias-ui:ResourceArtifactUiShape` | pdd-design, pdd-workflow (as `DocumentReferenceUiShape`), monitoring-report, validation-report, verification-report |
| `nias-ui:ObjectiveUiShape` | pdd-design, pdd-workflow |
| `nias-ui:SpatialLocationUiShape` | pdd-design, pdd-workflow |
| `nias-ui:TechnologyOrMeasureUiShape` | pdd-design, pdd-workflow |
| `nias-ui:ProjectPartyUiShape` | pdd-design, pdd-workflow |
| `nias-ui:ProjectDesignUiShape` | pdd-design, pdd-workflow |
| `nias-ui:CreditingPeriodUiShape` | pdd-design, pdd-workflow |
| `nias-ui:DataParameterRequirementUiShape` | pdd-design, pdd-workflow |
| `nias-ui:IndicatorValueUiShape` | pdd-design, pdd-workflow |
| `nias-ui:StateWithIndicatorValueUiShape` | pdd-design, pdd-workflow |
| `nias-ui:ImpactRequirementUiShape` | pdd-design, pdd-workflow |
| `nias-ui:ImpactClaimUiShape` | pdd-design, pdd-workflow |

**Build-time merging:** Because `shape2form` consumes a single self-contained TTL file, the build scripts (`build-*.sh`) concatenate `common-ui-shapes.ttl` with the bundle-specific file into a temporary merged file before invoking shape2form. This means each bundle remains independently deployable.

---

## Context-Specific Shapes (Intentional Variance)

Eight `sh:NodeShape` IRIs appear in more than one bundle file with **intentionally different** property definitions. These are not duplicates — each bundle is an independent UI artefact for a different workflow context, and the differing property sets reflect the different data capture or review requirements in each context.

| Shape IRI | Files | Intentional difference |
|---|---|---|
| `nias-ui:PddSectionAUiShape` | pdd-design, pdd-workflow | Design: full IPFS + content fields; Workflow: content subform only |
| `nias-ui:PddSectionBUiShape` | pdd-design, pdd-workflow | Design: full IPFS + content fields; Workflow: content subform only |
| `nias-ui:PddSectionCUiShape` | pdd-design, pdd-workflow | Design: full IPFS + content fields; Workflow: content subform only |
| `nias-ui:PddSectionAReportContentUiShape` | pdd-design, pdd-workflow | Design: captures full section A content; Workflow: simplified for shell |
| `nias-ui:PddSectionBReportContentUiShape` | pdd-design, pdd-workflow | Design: captures full section B content; Workflow: simplified for shell |
| `nias-ui:DocumentFieldReviewUiShape` | pdd-workflow, validation-report | PDD workflow: omits `reviewTarget` (system-managed); Validation: includes `reviewTarget` |
| `nias-ui:GlobalQualitativeDocumentReviewUiShape` | pdd-workflow, validation-report | Different label ordering and guiding question sets for PDD vs validation context |
| `nias-ui:ReviewTargetUiShape` | validation-report, verification-report | Different `ui:help` text: PDD-specific for validation; Monitoring Report-specific for verification |

These intentional variances are preserved and documented here. They must not be "fixed" by further consolidation without careful review of the corresponding workflow UIs.
