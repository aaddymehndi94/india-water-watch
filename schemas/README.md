# Canonical contracts

JSON Schema 2020-12 record schemas, not a claim that data has been gathered. Collections in `data/` start as empty arrays. Implement full validation in the production pipeline and TypeScript boundary; generate types rather than duplicating contracts by hand.

Schema validation is necessary, not sufficient. Add semantic checks: IDs refer to real records; published claims have inspected supporting evidence; dates/cutoffs agree; missing values have reasons; synthetic data cannot publish; forecast issue/validity order is sensible; probability partitions sum correctly when complete; comparisons with mismatch/unknown cannot be allowed; humans cannot be simulated by booleans; and all public artifacts derive from the same approved snapshot.

Resolve external references locally if schemas are extended. New metric definitions and crosswalk schemas require reviewed versioned migrations. The starter validator checks JSON/structure and required files, not the full JSON Schema vocabulary. Production must use a conformant validator.
