# IBM Bob Log: Measuring AI Adoption

Every task I gave IBM Bob while building this project, what it produced, and how I checked it. I approved Bob's actions one at a time and verified each result before moving on.

| # | Task given to Bob | What Bob produced | How I checked it |
|---|---|---|---|
| 1 | Set up the project structure | Folders for `agents`, `data`, `tools` and `docs`, a starter README, and a Git repository | Confirmed the folders appeared in my GitHub repo |
| 2 | Clean the raw CFPB credit card complaint download | `clean_data.py` and `complaints_clean.csv`: 498 complaints, 166 per bank, 8 columns | Confirmed the file had 8 columns and 166 complaints each for JPMorgan Chase, Citibank and Bank of America |
| 3 | Fix the agent's miscounting with an exact counting tool | `tools/count_complaints.py`, built with the Agent Development Kit, plus steps to import it into Orchestrate | Adjusted one upload command before running it; the agent then reported 166 per bank instead of wrong percentages |
| 4 | Create a fake confidential file to test the guardrail | `data/CONFIDENTIAL_customer_accounts.csv` | The Data Guardrail Agent blocked it and explained why |
| 5 | Save each agent's instructions to the repo | Three instruction files in the `agents` folder | Pushed them to GitHub alongside the live 2.0.0 system |
| 6 | Write the final README | `README.md` explaining the system | Added the demo video link myself and pushed it |
