# EvidenceRoute

EvidenceRoute is an evidence-aware multimodal task orchestration project for auditing long videos against an SOP and supporting each finding with traceable evidence.

**Week 1 status:** Contract-first engineering skeleton. The project does not yet process real videos or images or call AI models.

See [product.md](product.md) for the product scope, target users, and non-goals.

### Fake SOP inspection

- `run_fake_inspection(job)` does not read media or call external services.
- Each SOP step returns `uncertain`, empty evidence IDs, and requires human review.
- SOP steps receive positional IDs: `step-001`, `step-002`, etc.
- The input hash is SHA-256 of the normalized job JSON, not media bytes.
- Cost is zero; latency is a fixed simulated value of 1 ms.
- Identical inputs produce identical reports.