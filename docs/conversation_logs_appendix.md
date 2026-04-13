# Conversation Logs Appendix

## Purpose

This appendix records representative GenAI-assisted interactions used during the coursework. It is not a raw full transcript dump. Instead, it summarizes the prompts, the type of AI support received, the human decision that followed, and the resulting project outcome.

## Log Extract 1: Requirement Extraction

- User intent: read the coursework PDF and extract every requirement, score criterion, fail condition, and deliverable.
- AI support: structured the assignment into hard requirements, scoring factors, GenAI rules, submission components, and high-score recommendations for a Django plus SQLite stack.
- Human decision: use the extracted checklist as the working submission baseline rather than relying on memory.
- Outcome: a complete requirement summary document was created and used as the project control document.

## Log Extract 2: Topic and Scope Selection

- User intent: choose a safer high-scoring topic based on Django and SQLite.
- AI support: compared options and proposed a book recommendation API with catalog CRUD, bookshelf tracking, reviews, explainable recommendations, and analytics.
- Human decision: accept the domain, but keep the recommendation engine rule-based and explainable.
- Outcome: the project scope was fixed around Google Books ingestion plus local user activity.

## Log Extract 3: Google Books Data Strategy

- User intent: add a public dataset and fit it into the coursework requirements.
- AI support: recommended treating Google Books as an external metadata source rather than a live proxy backend.
- Human decision: normalize imported data into local SQLite tables and build all CRUD, recommendation, and analytics endpoints on top of local data.
- Outcome: the project gained a defendable data-ingestion pipeline and a clear explanation for database ownership.

## Log Extract 4: Delivery Planning and Git Strategy

- User intent: finish the project in a compressed two-day window and still show clear version control practice.
- AI support: proposed a staged execution plan and later converted the finished working tree into five logical commits instead of one large dump.
- Human decision: keep the commit history grouped by runtime setup, seed data, tests, documentation sources, and generated assets.
- Outcome: the final repository history reflects feature-grouped progress rather than a single final upload.

## Log Extract 5: Implementation and Verification

- User intent: complete the codebase, tests, supporting documents, and presentation materials.
- AI support: helped structure the implementation into accounts, catalog, engagement, and analytics modules; drafted tests; generated documentation; and built submission assets.
- Human decision: verify output locally with Django checks, tests, schema export, asset generation, and repository inspection before treating the work as submission-ready.
- Outcome: the repository now contains source code, tests, generated deliverables, and a public commit history.

## Log Extract 6: Final Compliance Review

- User intent: check whether anything was still missing before final submission.
- AI support: identified missing report links, deployment discussion, GenAI analysis depth, and conversation log evidence.
- Human decision: update README, report, appendices, deployment readiness files, and the presentation deck rather than submitting with known gaps.
- Outcome: the submission package was strengthened to align more closely with the coursework checklist.

## Summary of AI Impact

- AI accelerated requirement parsing, implementation sequencing, and documentation drafting.
- Human review remained essential for scope control, correctness, testing, and final submission judgment.
- The strongest value came from high-level comparison and structuring, not from blindly accepting generated outputs.
