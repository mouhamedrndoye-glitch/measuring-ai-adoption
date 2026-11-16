# Measuring AI Adoption

A three-agent system built in IBM watsonx Orchestrate that helps early-career bank associates use AI safely on stakeholder projects.

---

## The Problem

Early-career bank associates are expected to use AI on research and reporting projects, but they often aren't sure:

- **Where AI fits** — which parts of the work AI should do versus which parts need human judgment.
- **What data is safe** — what can be fed into an AI system and what must stay private.

Without clear guardrails, associates risk either avoiding AI entirely or accidentally sharing restricted customer data.

---

## The Solution

A three-agent system in IBM watsonx Orchestrate where the associate stays in control at every step.

### Agents

| Agent | File | Role |
|---|---|---|
| **Planner** | `agents/measuring_ai_adoption_agent.md` | Reads the project brief, proposes a plan splitting work between AI and the associate, and routes tasks to the other agents only after the associate approves. |
| **Data Guardrail Agent** | `agents/data_guardrail_agent.md` | Checks every file or dataset before it is used. Returns `APPROVED`, `BLOCKED`, or `NEEDS REVIEW` with a one-sentence reason. |
| **Research and Drafting Agent** | `agents/research_drafting_agent.md` | Uses the `count_complaints` tool to count complaint data and writes a sourced summary. Never estimates numbers itself. |

### How they work together

1. The associate sends a project brief to the Planner.
2. The Planner shows a plan — "AI will do / You will do" — and waits for approval before doing anything else.
3. Once approved, any data shared is sent to the Data Guardrail Agent first.
4. Approved data goes to the Research and Drafting Agent, which runs `count_complaints` and writes the summary.
5. The Planner hands the draft back to the associate to add recommendations and give final approval before sharing.

---

## The Tool

### `count_complaints` — `tools/count_complaints.py`

A Python tool registered with the IBM watsonx Orchestrate ADK. It reads the cleaned CFPB complaints CSV and returns complaint statistics by company.

**Input:** an optional company name (partial match, case-insensitive). Omit to get all companies.

**Output:** for each matching company —
- `company` — exact company name from the data
- `total_complaints` — total number of complaint records
- `top_5_issues` — the five most-reported issues, each with rank, issue text, raw count, and percentage of that company's total

The Research and Drafting Agent must use this tool for every number or percentage in its summaries. It never counts or estimates on its own.

---

## The Data

All data files live in the `data/` folder.

| File | Description |
|---|---|
| `complaints-2026-11-07_22_17.csv` | Raw download from the CFPB Consumer Complaint Database, filtered to credit card complaints for JPMorgan Chase, Citibank, and Bank of America. Public data. |
| `complaints_clean.csv` | Cleaned version used by the `count_complaints` tool. Columns standardised, blank rows removed. |
| `CONFIDENTIAL_customer_accounts.csv` | A fake file with customer names, account numbers, and balances. Used in demos to show the Data Guardrail Agent blocking restricted data. Not real data. |

A copy of `complaints_clean.csv` also lives in `tools/` so it is bundled correctly when the tool is uploaded to Orchestrate.

---

## Folder Guide

```
agents/        Agent instruction files (.md) imported into IBM watsonx Orchestrate
data/          Source data files (raw CFPB download, cleaned CSV, fake confidential file)
tools/         Python tool (count_complaints.py) and its bundled CSV
docs/          Supporting documentation (empty placeholder for now)
```

---

## How IBM Bob Was Used

IBM Bob (the AI coding assistant) was used throughout the build:

- **Cleaning the data** — wrote and ran the `clean_data.py` script to standardise columns and remove blank rows from the raw CFPB download.
- **Writing the counting tool** — wrote `count_complaints.py`, including the ADK `@tool` decorator, CSV loading, issue counting with `collections.Counter`, and percentage calculation.
- **Creating files** — created all three agent `.md` files and the folder structure.
- **Saving agent instructions** — pasted in instructions from IBM watsonx Orchestrate and wrote them directly into the agent files.

---

## Demo Flow

A typical demo runs through four steps:

1. **Plan** — The associate pastes a brief ("Summarise credit card complaints for JPMorgan Chase, Citibank, and Bank of America"). The Planner replies with an AI/associate split and asks for approval. No tools run yet.

2. **Approval** — The associate says "approved." The Planner sends the data source to the Data Guardrail Agent.

3. **Sourced summary** — The CFPB data is marked `APPROVED`. The Research and Drafting Agent runs `count_complaints`, then writes a summary with counts and percentages, each labelled "Source: CFPB Credit Card Complaints."

4. **Blocked file** — The associate shares `CONFIDENTIAL_customer_accounts.csv`. The Data Guardrail Agent replies `BLOCKED` — the file contains customer names and account numbers — and suggests using the approved public data instead. The Planner stops and tells the associate.
