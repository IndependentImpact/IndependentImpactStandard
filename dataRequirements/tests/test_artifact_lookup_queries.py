"""Guard tests for dataRequirements/fluree/artifact-lookup-queries.md.

The query templates are documentation, so nothing executes them in CI —
which is how the methodologies-by-knowledge-domain template shipped
matching on skos:broader and selecting dcterms:title, neither of which
occurs in the register data (the real link is the multi-valued
nias-o:requiresKnowledgeDomain, the real label skos:prefLabel). These
tests ground the register-backed templates against the repository's own
TTL so that kind of drift fails loudly.

Only the register queries are grounded: the workflow/artifact templates
(document schemas, PDD sections, approved reviews) target runtime ledger
content that has no complete instance data in the repository.
"""

import json
import re
import unittest
from pathlib import Path

from rdflib import RDF, Graph, URIRef

REPO_ROOT = Path(__file__).resolve().parents[2]
QUERIES_MD = REPO_ROOT / "dataRequirements/fluree/artifact-lookup-queries.md"
CONTEXT_JSONLD = REPO_ROOT / "dataRequirements/fluree/context.jsonld"

REGISTER_DATA = {
    "Indicator Concepts": [
        REPO_ROOT / "indicators/GHGIndicators.ttl",
    ],
    "Methodologies By Knowledge Domain": [
        REPO_ROOT / "methodologies/GHGMethodologies.ttl",
        REPO_ROOT / "knowledgeDomains/GHGKnowledgeDomains.ttl",
    ],
}

SKOS = "http://www.w3.org/2004/02/skos/core#"
NIAS_O = "https://nova.org.za/novaimpactaccountingstandard/"
REQUIRES_DOMAIN = URIRef(NIAS_O + "requiresKnowledgeDomain")
PREF_LABEL = URIRef(SKOS + "prefLabel")
CONCEPT = URIRef(SKOS + "Concept")


def fenced_json_blocks(markdown: str):
    """Yield (nearest preceding ## heading, parsed JSON) per fenced block."""
    heading = "(intro)"
    block = None
    for line in markdown.splitlines():
        if line.startswith("## "):
            heading = line[3:].strip()
        elif line.strip() == "```json":
            block = []
        elif line.strip() == "```" and block is not None:
            yield heading, json.loads("\n".join(block))
            block = None
        elif block is not None:
            block.append(line)


def load_prefixes():
    with open(CONTEXT_JSONLD) as f:
        return json.load(f)["@context"]


def expand(term: str, prefixes: dict) -> str | None:
    """A prefixed term's full IRI; None for keywords, variables, and placeholders."""
    if term.startswith(("@", "?", "$")):
        return None
    match = re.fullmatch(r"([A-Za-z][\w-]*):(\S+)", term)
    if not match or match.group(1) not in prefixes:
        return None
    return prefixes[match.group(1)] + match.group(2)


def query_terms(query: dict):
    """(predicates, types) used by a template's where and select clauses."""
    predicates, types = set(), set()
    where = query.get("where", [])
    for pattern in where if isinstance(where, list) else [where]:
        for key, value in pattern.items():
            if key == "@type":
                types.add(value)
            elif key != "@id":
                predicates.add(key)
    for selected in query.get("select", {}).values():
        predicates.update(term for term in selected if term != "@id")
    return predicates, types


class ArtifactLookupQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.blocks = list(fenced_json_blocks(QUERIES_MD.read_text()))
        cls.prefixes = load_prefixes()

    def test_every_fenced_block_parses(self):
        self.assertGreaterEqual(len(self.blocks), 6)

    def register_queries(self):
        for heading, query in self.blocks:
            if heading in REGISTER_DATA and "where" in query:
                yield heading, query

    def test_register_queries_use_predicates_the_data_actually_has(self):
        seen = set()
        for heading, query in self.register_queries():
            seen.add(heading)
            graph = Graph()
            for ttl in REGISTER_DATA[heading]:
                graph.parse(ttl, format="turtle")
            data_predicates = {str(p) for p in graph.predicates()}
            data_types = {str(o) for o in graph.objects(None, RDF.type)}
            predicates, types = query_terms(query)
            for term in predicates:
                iri = expand(term, self.prefixes)
                if iri is None:
                    continue
                self.assertIn(
                    iri,
                    data_predicates,
                    f"{heading}: template uses {term} ({iri}), which occurs "
                    f"nowhere in {[str(p) for p in REGISTER_DATA[heading]]} — "
                    "the query would never return that property",
                )
            for term in types:
                iri = expand(term, self.prefixes)
                if iri is None:
                    continue
                self.assertIn(
                    iri,
                    data_types,
                    f"{heading}: template matches @type {term} ({iri}), which "
                    "no resource in the register data declares",
                )
        self.assertEqual(
            seen,
            set(REGISTER_DATA),
            "register template missing from artifact-lookup-queries.md",
        )

    def test_methodology_domain_cascade_returns_labelled_rows(self):
        graph = Graph()
        for ttl in REGISTER_DATA["Methodologies By Knowledge Domain"]:
            graph.parse(ttl, format="turtle")

        domains = set(graph.objects(None, REQUIRES_DOMAIN))
        self.assertTrue(domains, "no methodology links to any knowledge domain")

        for domain in domains:
            self.assertIsNotNone(
                graph.value(domain, PREF_LABEL),
                f"{domain} is required by a methodology but has no prefLabel",
            )
            methodologies = [
                m
                for m in graph.subjects(REQUIRES_DOMAIN, domain)
                if (m, RDF.type, CONCEPT) in graph
            ]
            self.assertTrue(methodologies, f"no methodology matches domain {domain}")
            for m in methodologies:
                self.assertIsNotNone(
                    graph.value(m, PREF_LABEL),
                    f"{m} matches the domain query but has no prefLabel",
                )


if __name__ == "__main__":
    unittest.main()
