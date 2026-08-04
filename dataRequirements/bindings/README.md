# Platform binding profiles

The canonical corpus in `dataRequirements/` is infrastructure-neutral: an artefact must be content-addressed and must carry its anchoring record, but no shape fixes *which* ledger, content-addressing scheme, or resolver URL satisfies that requirement. See [ADR-0001](../../docs/adrs/adr-0001-platform-binding-profiles.md).

The constraints that hold only because the Standard is operated on a particular platform live here, one directory per platform.

## What is here

| Directory | Platform |
| --- | --- |
| [`independent-impact/`](independent-impact/) | The Independent Impact platform: Hedera consensus topics for anchoring, mirror-node message resolution. |

## How a profile works

A profile adds `sh:property` and `sh:sparql` constraints to shape IRIs already declared in the core. SHACL composes the two graphs additively, so a profile only ever tightens — it never has to override or relax the core. Validating the core together with a profile therefore reproduces exactly the enforcement that profile's platform applies.

Concretely, `independent-impact/artifact-anchoring-shapes.ttl` extends `nias-o:SubmittedArtifactIdentityShape`, `nias-o:ReviewedArtifactIdentityShape` and `nias-o:MonitoringArtifactIdentityShape` from `../artifact-identity-contract-shapes.ttl`.

## When to work here

- Add to a profile when a constraint is true of one platform's mechanics rather than of the Standard's subject matter — ledger identifier formats, resolver URL shapes, account identifier syntax, pinning-service specifics.
- Do **not** add to a profile a constraint about what the Standard requires of an activity, an impact, or a claim. That belongs in the canonical corpus.
- Whenever conformance is asserted, state which profile is in force. Core-only validation is weaker than any deployment's, by design.

## Testing

`dataRequirements/tests/test_platform_binding_profile.py` asserts both halves of the contract: that the core alone accepts an artefact carrying no ledger-specific anchor, and that the core plus the Independent Impact profile still rejects the cases the pre-split corpus rejected.
