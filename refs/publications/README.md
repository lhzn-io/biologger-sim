# Research Publications

This directory contains research publications and academic papers relevant to the biologger pseudotrack project.

## Organization by Research Area

### Animal Behavior Classification

Committed markdown summaries for machine learning approaches to automated behavior classification:

- `Agarwal et. al. - 2024 - Leveraging machine learning and accelerometry to classify animal behaviours with uncertainty.md`
- `Brewster et al. - 2021 - Classifying goliath grouper (Epinephelus itajara) behaviors from a novel, multi-sensor tag.md`

### Marine Animal Tracking

Committed markdown summaries for marine animal telemetry and tracking research:

- `Rudd et. al. - 2025 - Use of accelerometry to measure the dynamics of activity patterns of Atlantic bluefin tuna after tagging and release.md`

### Research Areas with PDF-Only Papers

Additional research papers are available locally as PDFs (not committed to repository):

**Sensor Fusion & Navigation**: Al-Fahoum et al. (2018), Cohen et. al. (2024), Merveille et. al. (2024), Shaukat et. al. (2021), Zhuang et. al. (2023)

**Animal Behavior Classification**: Arablouei et. al. (2023), Brewster et al. (2018)

**Marine Animal Tracking**: Kawatsu et. al. (2009), Skubel et al. (2020)

## File Management Strategy

This strategy is intentionally designed to be **GitHub Copilot Spaces friendly**, leveraging the latest Copilot features for enhanced research workflow integration.

**PDF Files:**

- Original research papers (PDF format) are stored locally but excluded from git repository via `.gitignore`
- PDFs should be downloaded/obtained separately as needed for detailed reading and citation
- Excluded from repository as Copilot Spaces cannot directly process PDF content or visual elements

**Markdown Files:**

- Markdown summaries and key findings extractions are committed to the repository
- These provide quick reference and searchable content for the research papers
- Markdown files capture essential information without large binary file overhead
- **Copilot-optimized**: Text-based format enables Copilot Spaces to analyze, reference, and integrate research content into coding workflows
- Enables semantic search and contextual assistance across the research knowledge base

**Workflow:**

1. Download PDF papers locally to this directory
2. Create markdown summaries for important papers
3. Commit only the markdown files to git
4. Reference both formats in documentation as available
5. **Copilot Integration**: Markdown content becomes searchable and referenceable within Copilot Spaces for research-informed development

## Related Documentation

- Literature reviews: [`../`](../)
- Technical documentation: [`../technical/`](../technical/)
- Project documentation: [`../../docs/`](../../docs/)
