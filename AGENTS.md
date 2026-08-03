# Repository Guidance

- This repository contains impact/accounting-standard, semantic web, and generated workflow work. Preserve traceability from standards to data requirements, ontology/SHACL constraints, generated forms, tests, and implementation code.
- Treat SHACL shapes, ontology files, RDF fixtures, and unpublished standards-analysis artifacts as local-only private data unless explicitly told otherwise.
- Before modifying generated or generated-looking files, find the generator or source artifact and update that instead when practical.
- For Go components, prefer the repo's documented commands. Otherwise run `gofmt`, `go test ./...`, `go vet ./...`, configured lint, and `go build ./...`.
- For Flutter components, run `dart format`, `flutter analyze`, and `flutter test` for relevant changes.
- For web UI changes, run the local app and test changed controls in a browser, including mobile and desktop widths when layout changes.
- Keep implementation plans tied to architecture/flow artifacts such as LikeC4 models and workflow diagrams when present.
