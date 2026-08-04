"""Platform binding profile contract (ADR-0001).

The canonical identity contract is infrastructure-neutral: it requires an
artifact to be content-addressed and permits an anchoring record, without
fixing the syntax of a ledger anchor. The Independent Impact binding profile
adds the platform's mandatory Hedera anchoring.

These tests assert both halves: the core alone accepts an artifact carrying no
ledger anchor, and the core plus the profile still rejects everything the
pre-split corpus rejected.
"""

import unittest
from pathlib import Path

from pyshacl import validate
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import SH


REPO_ROOT = Path(__file__).resolve().parents[2]

CORE_SHAPES = REPO_ROOT / "dataRequirements/artifact-identity-contract-shapes.ttl"
II_PROFILE = (
    REPO_ROOT
    / "dataRequirements/bindings/independent-impact/artifact-anchoring-shapes.ttl"
)
PDD_ALPHA_FIXTURE = (
    REPO_ROOT / "dataRequirements/document-rendering/fixtures/pdd-alpha-input.jsonld"
)
ONTOLOGY_FILES = [
    REPO_ROOT / "glossary/NovaImpactAccountingStandardOntology.ttl",
    REPO_ROOT / "glossary/NovaImpactAccountingStandardGlossary.ttl",
]

NIAS = Namespace("https://nova.org.za/novaimpactaccountingstandard/")
PDD_SECTION_A = URIRef(f"{NIAS}reports/pdd-section-a")
NEUTRAL_ARTIFACT = URIRef(f"{NIAS}test/binding/neutral-artifact")

# A submitted artifact version that is content-addressed but carries no
# ledger-specific anchor. Valid under the neutral core; invalid once the
# Independent Impact profile is in force.
NEUTRAL_ARTIFACT_TTL = f"""
@prefix nias-o: <{NIAS}> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<{NEUTRAL_ARTIFACT}>
    nias-o:artifactContentCid "content-address-abc" ;
    nias-o:artifactSchemaCid "schema-address-def" ;
    nias-o:artifactSchemaVersionLabel "nias:pdd-schema:alpha:2026-08-04:abc" ;
    nias-o:artifactAuthor "Nova Institute NPC" ;
    nias-o:workflowSubject <{NIAS}test/binding/subject> .
"""

# The same artifact anchored the way the Independent Impact platform anchors it.
ANCHORED_ARTIFACT_TTL = (
    NEUTRAL_ARTIFACT_TTL.rstrip()[:-1]
    + f"""
    ;
    nias-o:submissionTopicId "0.0.1001" ;
    nias-o:submissionConsensusTimestamp "2026-08-04T10:00:00Z"^^xsd:dateTimeStamp .
"""
)

# Anchored, but with a topic identifier that is not in Hedera shard.realm.num
# form. Neutral core accepts any non-whitespace token; the profile must not.
FOREIGN_ANCHOR_TTL = (
    NEUTRAL_ARTIFACT_TTL.rstrip()[:-1]
    + f"""
    ;
    nias-o:submissionTopicId "some-other-ledger-reference" ;
    nias-o:submissionConsensusTimestamp "2026-08-04T10:00:00Z"^^xsd:dateTimeStamp .
"""
)

# Anchored correctly, but the derived message URL does not follow the
# mirror-node convention. Only the profile carries that rule.
BAD_MESSAGE_URL_TTL = (
    NEUTRAL_ARTIFACT_TTL.rstrip()[:-1]
    + f"""
    ;
    nias-o:submissionTopicId "0.0.1001" ;
    nias-o:submissionConsensusTimestamp "2026-08-04T10:00:00Z"^^xsd:dateTimeStamp ;
    nias-o:submissionMessageUrl "/wrong/route" .
"""
)


def _load_graph(paths):
    graph = Graph()
    for path in paths:
        fmt = "json-ld" if Path(path).suffix == ".jsonld" else "turtle"
        graph.parse(path, format=fmt)
    return graph


def _shape_graph(shape_files, shape, target):
    graph = _load_graph(shape_files)
    graph.add((shape, SH.targetNode, target))
    return graph


def _validate(data_ttl_or_graph, shape_files, shape, target):
    if isinstance(data_ttl_or_graph, Graph):
        data_graph = data_ttl_or_graph
    else:
        data_graph = Graph()
        data_graph.parse(data=data_ttl_or_graph, format="turtle")
    return validate(
        data_graph=data_graph,
        shacl_graph=_shape_graph(shape_files, shape, target),
        ont_graph=_load_graph(ONTOLOGY_FILES),
        inference="none",
        abort_on_first=False,
        allow_infos=False,
        allow_warnings=False,
        advanced=True,
    )


class PlatformBindingProfileTests(unittest.TestCase):
    def test_profile_parses(self):
        graph = _load_graph([II_PROFILE])

        self.assertGreater(len(graph), 0)

    def test_core_alone_accepts_an_artifact_with_no_ledger_anchor(self):
        """The point of ADR-0001: conformance does not require a ledger."""
        conforms, _, text = _validate(
            NEUTRAL_ARTIFACT_TTL,
            [CORE_SHAPES],
            NIAS.SubmittedArtifactIdentityShape,
            NEUTRAL_ARTIFACT,
        )

        self.assertTrue(conforms, msg=text)

    def test_core_alone_accepts_a_non_hedera_anchor(self):
        conforms, _, text = _validate(
            FOREIGN_ANCHOR_TTL,
            [CORE_SHAPES],
            NIAS.SubmittedArtifactIdentityShape,
            NEUTRAL_ARTIFACT,
        )

        self.assertTrue(conforms, msg=text)

    def test_profile_requires_an_anchor(self):
        conforms, _, text = _validate(
            NEUTRAL_ARTIFACT_TTL,
            [CORE_SHAPES, II_PROFILE],
            NIAS.SubmittedArtifactIdentityShape,
            NEUTRAL_ARTIFACT,
        )

        self.assertFalse(conforms)
        self.assertIn("Hedera topic ID", text)

    def test_profile_rejects_a_non_hedera_anchor(self):
        conforms, _, text = _validate(
            FOREIGN_ANCHOR_TTL,
            [CORE_SHAPES, II_PROFILE],
            NIAS.SubmittedArtifactIdentityShape,
            NEUTRAL_ARTIFACT,
        )

        self.assertFalse(conforms)
        self.assertIn("Hedera topic ID", text)

    def test_profile_accepts_a_hedera_anchored_artifact(self):
        conforms, _, text = _validate(
            ANCHORED_ARTIFACT_TTL,
            [CORE_SHAPES, II_PROFILE],
            NIAS.SubmittedArtifactIdentityShape,
            NEUTRAL_ARTIFACT,
        )

        self.assertTrue(conforms, msg=text)

    def test_profile_enforces_the_mirror_node_message_url_derivation(self):
        conforms, _, text = _validate(
            BAD_MESSAGE_URL_TTL,
            [CORE_SHAPES, II_PROFILE],
            NIAS.SubmittedArtifactIdentityShape,
            NEUTRAL_ARTIFACT,
        )

        self.assertFalse(conforms)
        self.assertIn("submissionMessageUrl", text)

    def test_core_alone_does_not_enforce_the_message_url_derivation(self):
        conforms, _, text = _validate(
            BAD_MESSAGE_URL_TTL,
            [CORE_SHAPES],
            NIAS.SubmittedArtifactIdentityShape,
            NEUTRAL_ARTIFACT,
        )

        self.assertTrue(conforms, msg=text)

    def test_real_pdd_fixture_still_conforms_with_the_profile_in_force(self):
        """Pre-split enforcement is preserved for data the platform produces."""
        conforms, _, text = _validate(
            _load_graph([PDD_ALPHA_FIXTURE]),
            [CORE_SHAPES, II_PROFILE],
            NIAS.SubmittedArtifactIdentityShape,
            PDD_SECTION_A,
        )

        self.assertTrue(conforms, msg=text)

    def test_anchor_derivation_accepts_either_utc_lexical_form(self):
        """Conformance must not depend on the validator's configuration.

        "...Z" and "...+00:00" denote the same instant, and RDF libraries
        differ on which one str() returns for an xsd:dateTimeStamp — rdflib
        switches from the first to the second once RDFS inference has run
        anywhere in the process. The event-key and message-URL rules
        concatenate that value, so accepting only one form would make a
        conformant artifact fail because of an unrelated earlier validation.

        Asserted with explicit lexical forms rather than by triggering
        inference, because triggering it rebinds rdflib globally and would
        corrupt every test that runs afterwards.
        """
        for label, timestamp in (
            ("Z", '"2026-08-04T10:00:00Z"^^xsd:dateTimeStamp'),
            ("+00:00", '"2026-08-04T10:00:00+00:00"^^xsd:dateTimeStamp'),
        ):
            with self.subTest(lexical_form=label):
                data = (
                    NEUTRAL_ARTIFACT_TTL.rstrip()[:-1]
                    + f"""
    ;
    nias-o:submissionTopicId "0.0.1001" ;
    nias-o:submissionConsensusTimestamp {timestamp} ;
    nias-o:submissionEventKey "0.0.1001@2026-08-04T10:00:00Z" ;
    nias-o:submissionMessageUrl "/api/v1/topics/0.0.1001/messages/2026-08-04T10:00:00Z" .
"""
                )
                conforms, _, text = _validate(
                    data,
                    [CORE_SHAPES, II_PROFILE],
                    NIAS.SubmittedArtifactIdentityShape,
                    NEUTRAL_ARTIFACT,
                )

                self.assertTrue(conforms, msg=text)


if __name__ == "__main__":
    unittest.main()
