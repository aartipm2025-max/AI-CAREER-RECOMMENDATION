# AI Career Market Value Advisor — System Architecture

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Core Design Principles](#2-core-design-principles)
3. [Agent Responsibilities](#3-agent-responsibilities)
4. [Data Pipeline](#4-data-pipeline)
5. [Ranking Logic](#5-ranking-logic)
6. [Folder Structure](#6-folder-structure)
7. [Implementation Phases](#7-implementation-phases)
8. [Testing Strategy](#8-testing-strategy)
9. [Architecture Diagram](#9-architecture-diagram)

---

## 1. System Overview

The **AI Career Market Value Advisor** is a multi-agent, data-driven recommendation system designed to help undergraduate students identify the highest-value degree programmes based on real-world labour market indicators.

### How It Works

1. A student selects their academic stream — **Science**, **Commerce**, or **Arts**.
2. The system retrieves all undergraduate degrees belonging to that stream.
3. Salary and demand data is attached to each degree from structured datasets.
4. A deterministic **Market Value Score** is computed using a weighted formula.
5. Degrees are ranked from highest to lowest market value.
6. An LLM generates a concise, evidence-based explanation for each degree.
7. The final ranked table is presented to the student.

### Key Constraint

> **The LLM does NOT determine rankings.** Rankings are computed programmatically using structured data. The LLM is solely responsible for generating short natural-language explanations grounded in the retrieved evidence.

### Supported Streams

| Stream   | Example Degrees                              |
|----------|----------------------------------------------|
| Science  | BSc Data Science, BTech AI, MBBS, BSc BioTech |
| Commerce | BBA, BCom, CA, BMS                           |
| Arts     | BA Economics, BA Psychology, LLB, BDes       |

---

## 2. Core Design Principles

| Principle                    | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| **Deterministic Ranking**    | Scores are computed solely from dataset values; no LLM inference is used for ranking. |
| **Separation of Concerns**   | Each agent handles exactly one responsibility, making the system modular and testable. |
| **Data-First Architecture**  | All recommendations trace back to sourced, structured datasets.             |
| **Explainability**           | Every ranked degree includes an evidence-backed explanation citing the data source. |
| **Incremental Build**        | The system is built and validated phase by phase to ensure correctness at every layer. |

---

## 3. Agent Responsibilities

The system is composed of **six agents**, each with a clearly scoped role.

---

### 3.1 Input Agent

| Attribute   | Detail                                               |
|-------------|------------------------------------------------------|
| **Role**    | Accept and validate the student's stream selection.  |
| **Input**   | Raw user input (string or UI selection).             |
| **Output**  | Normalised stream value: `"Science"`, `"Commerce"`, or `"Arts"`. |
| **Logic**   | Normalise casing; reject invalid streams with a clear error message. |

```
Input: "science"  →  Output: "Science"
Input: "xyz"      →  Output: ValidationError("Invalid stream")
```

---

### 3.2 Degree Agent

| Attribute   | Detail                                                         |
|-------------|----------------------------------------------------------------|
| **Role**    | Retrieve all undergraduate degrees for the validated stream.   |
| **Input**   | Normalised stream string.                                      |
| **Output**  | List of degree records: `[{degree, domain, industry}, ...]`.   |
| **Source**  | `datasets/degrees_dataset.csv`                                 |
| **Logic**   | Filter `degrees_dataset.csv` by the `stream` column.           |

---

### 3.3 Market Intelligence Agent

| Attribute   | Detail                                                                     |
|-------------|----------------------------------------------------------------------------|
| **Role**    | Attach salary and demand statistics to each degree.                        |
| **Input**   | List of degree records from the Degree Agent.                              |
| **Output**  | Enriched degree records with salary and demand fields appended.            |
| **Sources** | `datasets/salary_dataset.csv`, `datasets/demand_dataset.csv`               |
| **Logic**   | Left-join salary data on `degree`; left-join demand data on `domain`.      |

**Enriched Record Schema:**

```json
{
  "degree": "BSc Data Science",
  "domain": "Data Science & AI",
  "industry": "Technology",
  "median_salary_lpa": 7.0,
  "salary_range_lpa": "5–12 LPA",
  "demand_growth_percent": 34.0,
  "hiring_volume_score": 8.5,
  "evidence": "Data science roles projected to grow 34% by 2030",
  "primary_source": "BLS"
}
```

---

### 3.4 Ranking Engine

| Attribute   | Detail                                                              |
|-------------|---------------------------------------------------------------------|
| **Role**    | Compute the Market Value Score for each degree and sort the list.  |
| **Input**   | List of enriched degree records.                                    |
| **Output**  | Ranked list (highest score first) with scores appended.            |
| **Logic**   | Apply the weighted scoring formula (see Section 5).                |

> This agent contains **no LLM calls**. It is pure deterministic Python logic.

---

### 3.5 Explanation Agent

| Attribute   | Detail                                                                                |
|-------------|---------------------------------------------------------------------------------------|
| **Role**    | Generate a short, evidence-grounded explanation for each ranked degree.              |
| **Input**   | Single enriched degree record (salary, demand, evidence, source).                    |
| **Output**  | One-sentence explanation string per degree.                                          |
| **Logic**   | Constructs a structured prompt using only the values from the dataset record; the LLM formats and phrases the explanation, it does not infer any numbers. |

**Prompt Contract:**

```
Given this structured data:
  Degree: {degree}
  Median Salary: ₹{median_salary_lpa} LPA
  Demand Growth: {demand_growth_percent}%
  Evidence: {evidence}
  Source: {primary_source}

Write ONE sentence explaining why this degree has strong market value.
Use only the numbers above. Do not add external information.
```

---

### 3.6 Response Agent

| Attribute   | Detail                                                          |
|-------------|-----------------------------------------------------------------|
| **Role**    | Format and return the final ranked recommendations table.       |
| **Input**   | Ranked list of degrees with scores and explanations.            |
| **Output**  | Formatted table (Markdown / JSON / UI-ready dict).              |
| **Logic**   | Assigns rank numbers; maps fields to the output schema.         |

**Output Schema:**

| Field           | Source                           |
|-----------------|----------------------------------|
| `Rank`          | Computed by Ranking Engine       |
| `Degree`        | `degrees_dataset.csv`            |
| `Median Salary` | `salary_dataset.csv`             |
| `Reason`        | Generated by Explanation Agent   |
| `Source`        | `demand_dataset.csv`             |

---

## 4. Data Pipeline

```
Student Input
     │
     ▼
┌─────────────┐
│ Input Agent │  → Validates and normalises stream
└─────────────┘
     │
     ▼
┌──────────────┐
│ Degree Agent │  → Filters degrees_dataset.csv by stream
└──────────────┘
     │
     ▼
┌────────────────────────────┐
│ Market Intelligence Agent  │  → Joins salary_dataset.csv + demand_dataset.csv
└────────────────────────────┘
     │
     ▼
┌────────────────┐
│ Ranking Engine │  → Applies weighted formula; sorts descending
└────────────────┘
     │
     ▼
┌───────────────────┐
│ Explanation Agent │  → Calls LLM with structured prompt per degree
└───────────────────┘
     │
     ▼
┌────────────────┐
│ Response Agent │  → Formats final ranked table for output
└────────────────┘
     │
     ▼
Final Recommendation Table
```

### Dataset Join Map

```
degrees_dataset.csv
  └── degree  ──────────────┐
  └── domain  ──────────────┼──→ salary_dataset.csv  (joined on: degree)
                            └──→ demand_dataset.csv   (joined on: domain)
```

---

## 5. Ranking Logic

### Formula

```
Market Value Score = (0.5 × Normalised Salary)
                   + (0.3 × Normalised Demand Growth)
                   + (0.2 × Normalised Hiring Volume)
```

### Normalisation

All three input metrics are normalised to a **0–10 scale** using min-max normalisation across all degrees within the selected stream before computing the score. This ensures that salary (in LPA), demand growth (in percent), and hiring volume (a 0–10 score) are comparable.

```
Normalised(x) = 10 × (x − min(x)) / (max(x) − min(x))
```

If all values for a metric are identical (zero range), the normalised value defaults to **5.0** for all degrees.

### Tie-Breaking

When two degrees share the same Market Value Score (to two decimal places), they are ranked by:
1. **Median Salary (descending)** — higher salary breaks the tie first.
2. **Demand Growth Percent (descending)** — higher growth breaks remaining ties.

### Example Calculation (Science Stream)

| Degree            | Salary (LPA) | Demand Growth (%) | Hiring Vol. | Score  |
|-------------------|:------------:|:-----------------:|:-----------:|:------:|
| BSc Data Science  | 7.0          | 34                | 8.5         | **~8.2** |
| BTech AI          | 7.0          | 28                | 8.0         | **~7.6** |
| MBBS              | 6.0          | 18                | 7.5         | **~6.1** |

*(Illustrative values; actual scores depend on full dataset range.)*

---

## 6. Folder Structure

```
AI STUDENT CAREER RECOMMENDATION/
│
├── architecture.md                  ← This document
│
├── datasets/                        ← Structured input data
│   ├── degrees_dataset.csv
│   ├── salary_dataset.csv
│   └── demand_dataset.csv
│
├── agents/                          ← One file per agent
│   ├── input_agent.py
│   ├── degree_agent.py
│   ├── market_intelligence_agent.py
│   ├── ranking_engine.py
│   ├── explanation_agent.py
│   └── response_agent.py
│
├── core/                            ← Shared utilities and data loading
│   ├── data_loader.py               ← Loads and validates all CSVs
│   ├── normaliser.py                ← Min-max normalisation logic
│   └── config.py                   ← Scoring weights, dataset paths, constants
│
├── pipeline/                        ← Orchestration layer
│   └── orchestrator.py             ← Calls agents in sequence; passes data between them
│
├── interface/                       ← Student-facing UI
│   └── app.py                      ← Streamlit (or CLI) interface
│
├── tests/                           ← Test suite
│   ├── test_data_loader.py
│   ├── test_degree_agent.py
│   ├── test_market_intelligence_agent.py
│   ├── test_ranking_engine.py
│   ├── test_explanation_agent.py
│   └── test_response_agent.py
│
├── requirements.txt                 ← Python dependencies
└── README.md                        ← Project overview and setup guide
```

---

## 7. Implementation Phases

### Phase 1 — Data Layer

**Goal:** Load all three datasets and validate their schemas.

**Files involved:** `core/data_loader.py`, `core/config.py`

**Tasks:**
- Implement `load_degrees()`, `load_salary()`, `load_demand()` functions.
- Validate required columns are present, types are correct, and no critical nulls exist.
- Raise clear errors if datasets fail validation.

**Acceptance Criteria:**
- All three datasets load without error.
- Missing or malformed columns raise a `DataValidationError` with a descriptive message.

---

### Phase 2 — Degree Retrieval

**Goal:** Filter and return degrees for a given stream.

**Files involved:** `agents/input_agent.py`, `agents/degree_agent.py`

**Tasks:**
- Implement stream normalisation and validation in the Input Agent.
- Implement stream-based filtering in the Degree Agent.

**Acceptance Criteria:**
- `"science"`, `"Science"`, `"SCIENCE"` all return the same degree list.
- An invalid stream raises a `ValidationError`.
- Returned records match exactly those in the dataset for that stream.

---

### Phase 3 — Market Data Integration

**Goal:** Enrich degree records with salary and demand data.

**Files involved:** `agents/market_intelligence_agent.py`

**Tasks:**
- Merge salary data onto degree records via `degree` key.
- Merge demand data onto degree records via `domain` key.
- Handle missing joins gracefully (log warning; apply neutral defaults).

**Acceptance Criteria:**
- Every degree record has all six market data fields populated.
- A degree with no salary match logs a warning and uses a configurable default value.

---

### Phase 4 — Ranking Engine

**Goal:** Compute Market Value Score and produce a sorted ranked list.

**Files involved:** `agents/ranking_engine.py`, `core/normaliser.py`

**Tasks:**
- Implement min-max normalisation across the stream's degree set.
- Apply the weighted formula: `0.5×Salary + 0.3×DemandGrowth + 0.2×HiringVolume`.
- Sort degrees descending by score.
- Apply tie-breaking rules.

**Acceptance Criteria:**
- Scores remain within the 0–10 range for any valid dataset.
- The degree with the highest combined metrics always ranks first.
- Changing weights in `config.py` changes the ranking deterministically.

---

### Phase 5 — Explanation Layer

**Goal:** Generate a one-sentence LLM explanation per degree using structured evidence.

**Files involved:** `agents/explanation_agent.py`

**Tasks:**
- Construct a structured prompt from the degree's data fields.
- Call the LLM API and capture the response.
- Validate that the response is non-empty; retry once if empty.
- Attach the explanation string to the degree record.

**Acceptance Criteria:**
- Every ranked degree has a non-empty explanation.
- The explanation cites figures present in the dataset (validated by string-matching salary/growth values).
- The LLM prompt strictly limits the model from adding external data.

---

### Phase 6 — Response Formatting

**Goal:** Package the ranked list into the final output format.

**Files involved:** `agents/response_agent.py`

**Tasks:**
- Assign sequential rank numbers (1, 2, 3…).
- Map internal fields to the output schema: Rank, Degree, Median Salary, Reason, Source.
- Support both Markdown table output and JSON output.

**Acceptance Criteria:**
- Output table has exactly five columns in the correct order.
- Rank 1 is always the highest-scored degree.
- Both output formats (Markdown, JSON) are valid and parseable.

---

### Phase 7 — Interface

**Goal:** Provide a student-facing interface to select stream and view results.

**Files involved:** `interface/app.py`, `pipeline/orchestrator.py`

**Tasks:**
- Build a Streamlit app (or CLI fallback) with a stream selector (dropdown or radio buttons).
- On selection, call `orchestrator.py` which runs agents 1–6 in sequence.
- Display the ranked recommendations table in the UI.

**Acceptance Criteria:**
- A student can select exactly one stream from the three options.
- The ranked table renders correctly for all three streams.
- The UI is responsive and displays source attributions.

---

### Phase 8 — Testing

**Goal:** Validate every module in isolation with automated tests.

**Files involved:** All files in `tests/`

| Test File                           | What It Tests                                              |
|-------------------------------------|------------------------------------------------------------|
| `test_data_loader.py`               | Schema validation, error handling for malformed CSV        |
| `test_degree_agent.py`              | Correct filtering, case-insensitivity, invalid stream      |
| `test_market_intelligence_agent.py` | Join correctness, missing match defaults                   |
| `test_ranking_engine.py`            | Score formula, sort order, tie-breaking, edge cases        |
| `test_explanation_agent.py`         | Prompt structure, non-empty output, retry logic            |
| `test_response_agent.py`            | Output schema, rank ordering, Markdown and JSON validity   |

**Acceptance Criteria:**
- All tests pass with `pytest` and produce a coverage report ≥ 80%.

---

## 8. Testing Strategy

### Approach

The system uses **unit testing per agent** with a shared set of **fixture datasets** stored in `tests/fixtures/`. These are small, controlled CSV files that allow precise assertion of expected outputs without relying on the production datasets.

### Fixture Strategy

```
tests/
  fixtures/
    sample_degrees.csv      ← 3–5 degrees per stream, all three streams
    sample_salary.csv       ← Salary data matching fixture degrees
    sample_demand.csv       ← Demand data matching fixture domains
```

### Test Categories

| Category              | Description                                                        |
|-----------------------|--------------------------------------------------------------------|
| **Happy Path**        | Valid inputs produce correct, deterministic outputs.               |
| **Edge Cases**        | Empty streams, missing CSVs, ties in scores, null values.          |
| **Boundary Tests**    | All degrees tied in score; only one degree in a stream.            |
| **Integration Tests** | Full pipeline run from stream input to formatted table (end-to-end). |

### Key Invariants to Assert

1. **Ranking Determinism**: The same datasets always produce the same ranked order.
2. **Score Bounds**: All Market Value Scores are in the range `[0, 10]`.
3. **No LLM Ranking**: The Ranking Engine must contain zero calls to any LLM API.
4. **Source Attribution**: Every output row has a non-empty `Source` field.
5. **Schema Compliance**: Output always contains exactly: Rank, Degree, Median Salary, Reason, Source.

---

## 9. Architecture Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                      STUDENT INTERFACE                         │
│              (Streamlit UI / CLI — interface/app.py)           │
└───────────────────────────┬────────────────────────────────────┘
                            │  stream: "Science"
                            ▼
┌────────────────────────────────────────────────────────────────┐
│                       ORCHESTRATOR                             │
│                   (pipeline/orchestrator.py)                   │
└──┬──────────┬──────────┬──────────┬──────────┬────────────────┘
   │          │          │          │          │
   ▼          ▼          ▼          ▼          ▼
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
│Input │→ │Degree│→ │Mkt   │→ │Rank  │→ │Expl. │→ │Resp. │
│Agent │  │Agent │  │Intel.│  │Engine│  │Agent │  │Agent │
└──────┘  └──────┘  │Agent │  └──────┘  └──────┘  └──────┘
                    └──────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
  degrees_dataset  salary_dataset  demand_dataset
       .csv             .csv           .csv
```

### Data Flow Summary

```
Stream Input
  → [Input Agent]         Validate + normalise stream
  → [Degree Agent]        Filter degrees_dataset.csv
  → [Market Intel Agent]  Join salary + demand datasets
  → [Ranking Engine]      Normalise → Score → Sort (NO LLM)
  → [Explanation Agent]   LLM generates 1 sentence per degree
  → [Response Agent]      Format and return final table
```

---

*Document Version: 1.0 | Created: 2026-03-16 | Project: AI Career Market Value Advisor*
