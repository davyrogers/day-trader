# Analysis Reports

This folder contains all AI analyst reports from your latest analysis run.

## Structure

Each run automatically:
1. **Clears this folder** - Only the most recent run's reports are kept
2. **Creates three tier folders**:
   - `tier1_junior_analysts/` - Individual reports from each junior analyst
   - `tier2_senior_managers/` - Synthesis reports from senior managers
   - `tier3_executive_committees/` - Final executive committee decisions

3. **Saves a final summary** - `FINAL_SUMMARY_YYYYMMDD_HHMMSS.txt` with:
   - Pipeline statistics
   - Executive decisions (what was sent to Discord)
   - References to all detailed reports

## Report Format

Each individual report includes:
- Analyst/Manager name
- Role and focus area
- Timestamp
- Full AI analysis output

## File Naming

Reports are numbered and timestamped:
- `01_Analyst_Name_20251016_143022.txt`
- `02_Another_Analyst_20251016_143045.txt`

The numbering shows the execution order, making it easy to review the analysis flow.

## Why This Matters

You can now:
- **Review all AI decisions** - See exactly what each analyst concluded
- **Track reasoning** - Understand how junior analysts' insights fed into senior decisions
- **Verify quality** - Ensure the AI team is making sound judgments
- **Learn patterns** - Identify which analysts are most valuable for different news types

## Tips

- Check the `FINAL_SUMMARY` file first for a quick overview
- Dive into individual tier folders to see detailed analyst reasoning
- Compare reports across tiers to see how insights evolved
- Use reports to refine analyst configurations in `analyst_team.json`
