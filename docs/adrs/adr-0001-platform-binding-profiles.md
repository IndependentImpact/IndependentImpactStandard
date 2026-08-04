# ADR-0001 — Infrastructure-neutral core, with platform mechanics in binding profiles

**Status:** accepted — 2026-08-04

## Context

The Nova Institute Impact Accounting Standard operates as one standard on the Independent Impact platform (see `01-a-Introduction.md`). Independent Impact hosts many standards, and the Standard is owned by the Nova Institute rather than by the platform operator.

The canonical corpus does not currently reflect that. Platform mechanics are embedded in normative artefacts as mandatory constraints:

- `dataRequirements/artifact-identity-contract-shapes.ttl` requires a Hedera topic ID matching `^\d+\.\d+\.\d+$` (shard.realm.num) with `sh:minCount 1`, and names Hedera in the validation message. It also normatively constrains a mirror-node REST path, `/api/v1/topics/{topicId}/messages/{timestamp}`, inside a `sh:sparql` constraint.
- `dataRequirements/document-shapes.ttl` requires every workflow submission to link to a `hedera:TopicMessage`, with `sh:minCount 1`.
- `certificate-shapes.ttl`, `monitoring-report-shapes.ttl` and `pdd-certificate-shapes.ttl` require Hedera account IDs.
- `glossary/NovaImpactAccountingStandardOntology.ttl` imports the Hashgraph consensus and core ontologies, so every artefact in the corpus depends transitively on one distributed ledger's ontology.

The consequence is that an artefact cannot be shown to conform to this Standard without reference to a specific ledger and a specific service's HTTP routes. That is wrong in three ways. It makes a claim of conformance a claim about infrastructure rather than about content. It prevents the Standard from being validated anywhere other than one deployment, including in Nova's own tooling and in offline review. And it puts the platform operator's implementation choices inside artefacts the Nova Institute is responsible for, which is precisely the boundary the Introduction draws.

At the same time, the requirements themselves are not wrong. Artefacts *should* be content-addressed and tamper-evident; that is what makes impact accounting auditable, and it is a legitimate thing for a standard to require. What does not belong in the Standard is *which* ledger, *which* content-addressing scheme, and *which* URL shape satisfy that requirement.

## Decision

**The canonical corpus is infrastructure-neutral. Constraints that bind the Standard to a particular platform's mechanics live in a separate binding profile for that platform.**

Concretely:

1. **The core states the requirement abstractly.** Where an artefact must be identified, content-addressed, or anchored, the core shapes require the *fact* — a content address, an anchoring record — without constraining its syntax to any provider's format. Fields that only exist because of a particular platform are optional in the core (`sh:minCount 0`), not absent: the vocabulary is retained so that data carrying them is still described by the Standard.

2. **A binding profile supplies the platform's mandatory constraints.** Binding profiles live under `dataRequirements/bindings/<platform>/`. The Independent Impact profile is `dataRequirements/bindings/independent-impact/`. A profile may make core-optional properties mandatory, constrain their syntax, and add derivation rules over them.

3. **Profiles compose additively.** SHACL validation of core plus profile is the conjunction of both. A profile therefore never needs to override or relax the core — it only adds. Validating core plus the Independent Impact profile reproduces exactly the enforcement the corpus had before this split, which is the migration's correctness criterion.

4. **A standard may have more than one binding profile,** and the platform operator — not the Nova Institute — is the natural author of a profile for its own platform. The Independent Impact profile is maintained here for now because the constraints already existed here; that is a matter of convenience, not of ownership, and it may move.

5. **The Hashgraph ontology imports leave the core ontology** and become the binding profile's concern. Ontology terms describing ledger artefacts remain usable; they simply stop being a prerequisite of the Standard.

## Consequences

**Good.** A conformance claim becomes a claim about content. The corpus can be validated with no ledger, no pinning service, and no network access, which makes review, testing and offline use straightforward. The division of responsibility stated in the Introduction becomes visible in the corpus rather than only in prose. Independent Impact's enforcement is unchanged, because the profile carries it. Should a second platform ever host the Standard, the work is to write a profile, not to fork the corpus.

**Bad.** There are now two artefacts to keep in step, and a reader who validates against the core alone will see weaker constraints than the platform applies — so which profile is in force must be stated wherever conformance is asserted. Tooling that loaded a single shapes file must now load a set. The split also makes it possible to forget the profile in a deployment and silently under-validate; the mitigation is that the platform's own test suite must assert the profile is loaded.

**Neutral.** Nothing about the *data* changes. Existing artefacts carrying Hedera topic IDs and IPFS CIDs remain valid, and no IRI, property or class is renamed or removed.

## Scope of the first increment

`dataRequirements/artifact-identity-contract-shapes.ttl` is migrated first, because it carries the clearest cases: the Hedera topic-ID pattern, the consensus-timestamp requirement, the derived event key, and the mirror-node URL rule.

Deliberately not in the first increment, and tracked as follow-up issues:

- `document-shapes.ttl`'s mandatory `hedera:TopicMessage` link.
- The Hashgraph `owl:imports` in the core ontology, and the corresponding layer entries in `SemanticWebArtefactHierarchy.md`.
- The Hedera account-ID requirements in `certificate-shapes.ttl`, `monitoring-report-shapes.ttl` and `pdd-certificate-shapes.ttl`.
- Platform concepts modelled as standard artefacts: the Independent Impact agent licence in `license-shapes.ttl` and the corresponding ontology term.
- The generated Flutter validators that require IPFS-specific CID syntax.

## Related

- `01-a-Introduction.md` — the boundary between standard-setter and platform operator.
- `dev/Completed/linked-artifact-boundary-decisions.md` — the artefact identity contract this ADR splits.
- `IndependentImpact/ii-backend#91` — the companion decision that the standard-setter authors and owns its standard's SHACL. The two together define what the platform receives from a standard and what it supplies itself.
