# Reports Folder Structure Example

After running the analysis, your `reports/` folder will look like this:

```
reports/
│
├── README.md                                    # Documentation
├── FINAL_SUMMARY_20251016_143530.txt           # Complete overview
│
├── tier1_junior_analysts/
│   ├── 01_Sarah_Market_Sentiment_20251016_143022.txt
│   ├── 02_Marcus_Technical_Analyst_20251016_143045.txt
│   ├── 03_Elena_Risk_Manager_20251016_143108.txt
│   ├── 04_James_Fundamental_Analyst_20251016_143131.txt
│   └── 05_Priya_Intermarket_Analyst_20251016_143154.txt
│
├── tier2_senior_managers/
│   ├── 01_Senior_Trading_Desk_Manager_20251016_143217.txt
│   └── 02_Senior_Risk_Committee_20251016_143240.txt
│
└── tier3_executive_committees/
    ├── 01_Executive_Trading_Committee_20251016_143303.txt
    └── 02_Executive_Risk_Oversight_20251016_143326.txt
```

## File Content Example

**File**: `01_Sarah_Market_Sentiment_20251016_143022.txt`

```
================================================================================
Sarah
Role: Market Sentiment Analyst
Timestamp: 2025-10-16 14:30:22
================================================================================

[AI Analysis Output Here]

Based on the news aggregation provided, I observe several key market sentiment 
indicators...

[Full detailed analysis continues...]
```

## Final Summary Example

**File**: `FINAL_SUMMARY_20251016_143530.txt`

```
================================================================================
COMPLETE ANALYSIS SUMMARY
Generated: 2025-10-16 14:35:30
================================================================================

PIPELINE STATISTICS:
  • Junior Analysts: 5
  • Senior Managers: 2
  • Executive Committees: 2

================================================================================
EXECUTIVE DECISIONS (SENT TO DISCORD)
================================================================================

[Executive decisions that were posted to Discord...]

================================================================================
DETAILED BREAKDOWN
================================================================================

All individual reports are saved in:
  • C:\Repos\day-trader\reports\tier1_junior_analysts
  • C:\Repos\day-trader\reports\tier2_senior_managers
  • C:\Repos\day-trader\reports\tier3_executive_committees
```

## Reading Order Suggestion

1. Start with `FINAL_SUMMARY_*.txt` for the big picture
2. Check `tier3_executive_committees/` for final decisions
3. Review `tier2_senior_managers/` to see synthesis reasoning
4. Dive into `tier1_junior_analysts/` for detailed analysis

## Next Run

On the next run, the entire `reports/` folder is cleared (except README.md)
and populated with fresh reports from the new analysis.
