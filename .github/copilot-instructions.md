# Copilot Instructions for Biologger Pseudotrack Project

## ⚠️ CRITICAL: Environment Setup

- **ALWAYS activate the micromamba environment FIRST** before any Python commands
- **MANDATORY**: Run `micromamba activate biologger-pseudotrack` at the start of EVERY shell session
- Use the environment defined in `environment.yml`
- **ALL Python/pip commands MUST be run within the activated micromamba environment**

## ⚠️ CRITICAL: Git Operations

### File Operations

- **ALWAYS use `git mv` for renaming tracked files** - preserves git history and file tracking
- **NEVER use simple `mv` commands** on tracked files - breaks git history
- **Only use `mv` for untracked files** that haven't been added to git yet
- **Check `git status` first** to verify file tracking status before any move operations

### Staging Changes

- **NEVER use `git add .`** - this stages everything indiscriminately including unrelated changes
- **ALWAYS stage files explicitly** - use `git add <specific-file>` for each file you modified in this session
- **Scope commits to current session** - only stage changes you made during the active conversation
- **Review before staging** - use `git status` and `git diff` to verify what you're about to stage
- **Atomic commits** - each commit should contain a single logical change, not multiple unrelated modifications

## Coding Standards & Philosophy

- **Avoid excessive error checking** - prefer clean, readable code over defensive programming
- **Trust controlled environments** - validate at boundaries (data load functions, API entry points), not at every internal function
- **Don't create synthetic data** if input datasets are missing - fail gracefully instead
- Follow existing code patterns in the project
- Prioritize clarity over cleverness

### Error Checking Strategy

- **Validate at boundaries**: Check inputs in public API functions and data loaders
- **Trust internal calls**: Skip redundant checks in functions that receive pre-validated data
- **Document assumptions**: Use docstrings to clarify input expectations (e.g., "Assumes data loaded via load_behavioral_data()")
- **Example**: `load_behavioral_data()` guarantees `DateTimeP` column exists and is datetime-formatted, so downstream visualization functions don't need to re-check
- **Benefits**: Cleaner code, better performance, clearer contracts between functions

## Project Context

- This is a biologger data processing pipeline for marine animal tracking
- Key data flows: sensor data → calibration → pseudotrack generation
- Main entry point: `biologger_pseudotrack/__main__.py`
- Configuration files are in `biologger_pseudotrack/config/`

## Core Commands Quick Reference

### Development Setup

```bash
# Create micromamba environment
micromamba env create -f environment.yml
micromamba activate biologger-pseudotrack

# Install package in development mode
pip install -e .

# Verify installation
python -m biologger_pseudotrack --help
```

### Testing

```bash
# Unit tests only (fast, ~5-10s)
pytest tests/unit/

# Full test suite
pytest tests/

# With coverage
make test-coverage
```

### Linting and Formatting

```bash
# Auto-format code
make format

# Run linters
make lint
```

## Testing Philosophy

- **Unit tests** (`tests/unit/`): Fast validation (~5-10s), no external dependencies
- **Integration tests** (`tests/integration/`): Full pipeline tests with real data
- **Always run unit tests** before committing config/API changes
- **Target 80%+ coverage** for core functions

## Tooling Configuration

- **pytest**: Config in `pytest.ini`, markers for slow tests
- **ruff**: Linting and formatting via `make format` and `make lint`
- **mypy**: Type checking (if configured)
- **micromamba**: Environment management via `environment.yml`

## Development Workflow

Follow this step-by-step process for all code changes:

1. **Activate environment**: `micromamba activate biologger-pseudotrack`
2. **Create branch**: `git checkout -b feature-name`
3. **Make changes**: Edit code, document in `next_commit.md`
4. **Run tests**: `pytest tests/unit/` for quick validation
5. **Format code**: `make format`
6. **Walkthrough & Review**: Explain changes to user and WAIT for approval to stage ⚠️
7. **Stage changes**: `git add <specific-file>` (ONLY after user approval)
8. **Show diff**: `git diff --cached --stat`
9. **Commit**: Only after user approval
10. **Clean up**: `echo "" > next_commit.md` after successful commit

⚠️ **Never skip step 6** - always pause for user review before using `git add`.

## Common Pitfalls

1. **Don't use `git add .`**: Stage files explicitly, one at a time, only for changes made in this session
2. **Don't forget micromamba activation**: All Python commands require `micromamba activate biologger-pseudotrack`
3. **Don't use plain `mv` on tracked files**: Use `git mv` to preserve history
4. **Don't create synthetic data**: If input data is missing, fail gracefully
5. **Don't add excessive error checking**: Validate at boundaries, trust internal calls
6. **Don't use copilot_getNotebookSummary**: It hangs indefinitely - use `grep` instead
7. **Don't forget to document changes**: Update `next_commit.md` during work
8. **Don't stage/commit without review**: Walkthrough changes first, wait for user approval, THEN `git add`

## Git Operations & Change Tracking

- Use `get_changed_files` tool for checking git status and viewing diffs
- **Automated PR creation is encouraged** - use available GitHub tools for pull request creation
- Prefer GitHub tools over manual git commands when available

### Commit Message Format

Use conventional commit format:

```bash
# Examples
git commit -m "feat: add magnetometer calibration diagnostics"
git commit -m "fix: correct attachment angle calculation"
git commit -m "docs: update dead-reckoning methodology"
```

**Rules:**

- Use conventional commit format: `type: description`
- Valid types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`
- **NO** "Generated with..." or "Co-Authored-By" footers
- No emojis in commit messages
- Keep commits focused and atomic
- Commit message body (if used) should explain "why", not "what"

### Commit Review Policy

- **ALWAYS PAUSE FOR USER REVIEW before committing changes** made during the current session
- **TEST LOCALLY FIRST**: Before staging or asking to commit, verify changes with `make lint`, `pytest`, or by running the code locally.
- **DO NOT STAGE AUTOMATICALLY**: Do not run `git add` until you have provided a walkthrough of the changes and the user has approved them.
- **Stage files explicitly** (`git add <specific-file>`), then **STOP and wait for user approval** before running `git commit`
- **Exception**: Only auto-commit if user explicitly says "commit this" or "go ahead and commit"
- **Show summary**: When staging is complete, show `git diff --cached --stat` and wait for user to review
- **User has final say**: Let user decide when they're ready to commit, don't rush to commit automatically

### Change Documentation Workflow

- **ALWAYS document significant changes in `next_commit.md`** - this file spans chat sessions and maintains a running log of agent modifications
- **Structure changes by category**: Use sections like "### Algorithm Implementation", "### Infrastructure Changes", "### Testing & Validation", etc.
- **Include technical details**: Line counts, file impacts, method explanations, and validation results
- **Persist across sessions**: The file accumulates changes until commit, allowing comprehensive documentation of multi-session work
- **Post-commit cleanup**: After successful commit, zero out `next_commit.md` with `echo "" > next_commit.md`
- **Use for commit messages**: Extract comprehensive commit messages from accumulated `next_commit.md` content
- **Track incremental progress**: Document both completed changes and work-in-progress for better session continuity
- **Ignore linting errors**: `next_commit.md` is an untracked scratch file - do not waste cycles fixing markdown linting errors in it

## Data Handling

- Real data is in `data/` directory
- Respect the structure of biologger metadata
- Always validate data shapes and types before processing
- Use existing utility functions in `biologger_pseudotrack/functions/`

## Communication Style

- Be concise and technical
- Reference specific files and functions when relevant
- Assume familiarity with marine biology and animal tracking concepts
- Focus on practical solutions over theoretical explanations

## Visualization Standards

- **Prefer single-column timeseries layouts** with `sharex=True` for better temporal correlation
- Use `plt.subplots(n, 1, figsize=(14, 16), sharex=True)` instead of complex grid layouts
- Stack diagnostic plots vertically to align time axes
- Remove plot padding with `ax.set_xlim()` or `ax.margins(x=0)`
- **Use mermaid diagrams for flowcharts and process visualization** - `render_mermaid_diagram()` available in notebook_utils for any flowchart, sequence diagram, or process visualization
- **mermaid-py included in environment.yml** - no additional setup required for diagram rendering

## Notebook Handling

- **NEVER USE copilot_getNotebookSummary tool** - it hangs indefinitely and is explicitly forbidden
- **NEVER attempt to summarize raw/full .ipynb files** - encoded images consume excessive tokens
- **ALWAYS use unix file tools instead** to understand notebook structure: `grep`, `head`, `tail`, `cat`, etc.

## Python Development Tools

- **AVOID mcp_pylance_* tools** - they are slow and inefficient for quick operations
- **PREFER run_in_terminal with python -c** for quick Python code execution and testing
- **USE install_python_packages** for package installation in the correct environment
- **For finding cells**: Use `grep -n "VSCode.Cell" notebook.ipynb` to find cell boundaries and IDs
- **For finding code**: Use `grep -A5 -B5 "function_name"` to find specific code in notebooks
- **For cell content**: Use `grep -A20 "id=\"cell_id\"" notebook.ipynb` to read specific cells
- **For markdown cells**: Use `grep -A10 "language=\"markdown\"" notebook.ipynb`
- **For python cells**: Use `grep -A10 "language=\"python\"" notebook.ipynb`
- **Remove cell outputs before analysis** when possible using `jupyter nbconvert --clear-output`
- **Focus on code content** rather than execution outputs when analyzing notebooks
- **If you catch yourself trying to use copilot_getNotebookSummary, STOP and use grep instead**

## Shell Command Safety

- **AVOID exclamation marks (!) in shell commands** - bash interprets `!` as history expansion which causes command failures
- **Use period (.) instead of exclamation mark** in print statements: `print('Import successful.')` not `print('Import successful!')`
- **Avoid ! in comments** within shell-executed Python code: `# Success` not `# Success!`
- **Test commands safely** by avoiding special characters that trigger shell interpretation

### Notebook Editing Best Practices

- **PREFER edit_notebook_file tool** - this is the primary method for notebook editing and works reliably for content modifications
- **Cell ID vs Ordinal Position**: Most cells do NOT have explicit IDs and instead use implicit cell-order ordinals to match with attachment metadata - "Cell 16" refers to the 16th cell in the .ipynb file, not a cell with id="16"
- **Cell ID handling**: VS Code notebooks have cell IDs even when they appear missing - the edit_notebook_tool can find and use them correctly
- **User references by ordinal**: When users mention "Cell 16" or "cell #16", they mean the 16th cell in sequential order, which may or may not have an explicit ID attribute
- **For analysis/understanding**: Use unix tools (`grep`, `python -c` JSON parsing) to understand notebook structure before editing
- **Fallback methods when needed**: If edit_notebook_file fails, can use `grep`/`sed` or Python JSON manipulation as alternatives
- **For major refactoring**: Edit multiple cells sequentially using edit_notebook_file rather than trying to add new cells
- **Verify changes**: Use `grep` or `read_file` to confirm edits were applied correctly after using edit_notebook_file
- **Test functionality**: Run modified cells to ensure changes work as expected

### Notebook Content Standards

- **Focus on analysis, not implementation** - notebooks should present scientific analysis, not code development history
- **Remove implementation details** - eliminate references to API changes, function refactoring, or development iterations
- **No self-congratulatory messaging** - avoid marketing-style language about code quality or implementation improvements
- **Scientific tone** - maintain professional, analytical tone focused on research findings and biological insights
- **Use next_commit.md for development tracking** - document implementation changes in commit messages, not in analysis notebooks
- **Clean presentation** - remove historical comments about code evolution or function updates that don't serve analysis goals

## PDF to Markdown Conversion

- **Use uvx with markitdown for PDF conversion** - `uvx --with markitdown[all] markitdown input.pdf --output output.md`
- **Preserve original filenames** - change only the extension from `.pdf` to `.md`
- **Example conversion**: `uvx --with markitdown[all] markitdown "refs/publications/Paper Title.pdf" --output "refs/publications/Paper Title.md"`
- **For literature PDFs**: Always convert to markdown for better searchability and text analysis

## Markdown & Documentation Standards

- **Follow markdown linting rules** - ensure clean, consistent formatting
- **Ordered lists**: Each list under a new heading should restart at 1 (avoid MD029 errors)
- **Blank lines**: Surround lists, tables, and headings with blank lines (MD032, MD022, MD058)
- **Fenced code blocks**: Always specify language (`text`, `python`, `yaml`, etc.) to avoid MD040 errors
- **Avoid emphasis as headings**: Use proper heading levels (`##`, `###`) instead of `**bold**` for section headers (avoid MD036 errors)
- **Unique headings**: Avoid duplicate heading text at the same or different levels (MD024 errors) - add contextual prefixes to disambiguate (e.g., "StreamingProcessor: Key Methods" vs "PerformanceTelemetry: Key Methods")
- **For query strings/code**: Use fenced code blocks with `text` language instead of italic emphasis (`*text*`)
- **For literature review docs**: Use semantic numbering in content but respect markdown list conventions
- **Check formatting**: Run markdown linter or use editor extensions to catch issues early

## Emoji Usage Policy

- **Professional scientific tone required** - documentation should be pragmatic and grounded in science
- **Remove decorative emojis** - avoid emojis used for visual appeal or to make content "fun" (e.g., 🧲📉💪🐾📁🎯🧭📏⚡🔍)
- **Retain functional symbols** - keep check marks (✅✓), x marks (❌), and similar symbols when they enhance clarity in:
  - Comparison tables (e.g., "Python: ✅" vs "R: ❌")
  - Validation lists (e.g., "✓ Tests pass")
  - Status indicators (e.g., "❌ Known limitation")
- **Unicode range detection**: Use `grep -P '[\x{1F300}-\x{1F9FF}\x{2600}-\x{26FF}\x{2700}-\x{27BF}]'` to find emojis systematically
- **Exception for critical warnings**: ⚠️ acceptable in CRITICAL section headings for emphasis (e.g., "## ⚠️ CRITICAL: Environment Setup")
- **Apply systematically**: When cleaning up documentation, search entire files rather than spot-checking individual sections
