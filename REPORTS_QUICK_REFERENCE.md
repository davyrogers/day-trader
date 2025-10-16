# Quick Reference: Reviewing AI Analysis Reports

## At a Glance

| What You Want | Where to Look |
|--------------|---------------|
| **Quick overview** | `FINAL_SUMMARY_*.txt` |
| **What was sent to Discord** | `FINAL_SUMMARY_*.txt` (Executive Decisions section) |
| **Final trading decisions** | `tier3_executive_committees/` |
| **How decisions were synthesized** | `tier2_senior_managers/` |
| **Detailed analysis by specialty** | `tier1_junior_analysts/` |

## File Naming Convention

```
[Order]_[Analyst_Name]_[Timestamp].txt
  ↓        ↓              ↓
  01    Sarah_Market   20251016_143022
```

- **Order**: Execution sequence (01, 02, 03...)
- **Name**: Analyst/Manager/Committee name
- **Timestamp**: When the report was generated

## Common Review Workflows

### Verify Trading Signal Quality
1. Open `tier3_executive_committees/01_*.txt`
2. Check recommendation clarity and confidence
3. Verify risk assessment
4. Compare against market context in `tier1_junior_analysts/02_Marcus_Technical_*.txt`

### Understand Risk Assessment
1. Review `tier1_junior_analysts/03_Elena_Risk_*.txt`
2. Check senior synthesis in `tier2_senior_managers/02_*Risk*.txt`
3. Validate final risk decision in `tier3_executive_committees/02_*Risk*.txt`

### Track Sentiment Analysis
1. Start with `tier1_junior_analysts/01_Sarah_*.txt`
2. See how sentiment influenced managers in `tier2_senior_managers/`
3. Check if sentiment drove executive decision in `tier3_executive_committees/`

### Identify Analyst Blind Spots
- Compare multiple runs
- Look for patterns in missed opportunities
- Check if certain analysts consistently add value
- Use to refine `analyst_team.json` configuration

## Console During Run

Watch for these messages:
```
✓ Reports directory cleared and ready: C:\Repos\day-trader\reports
═══ TIER 1: JUNIOR ANALYSTS ═══
✓ Sarah report complete
  → Saved report: 01_Sarah_Market_Sentiment_20251016_143022.txt
✓ Marcus report complete
  → Saved report: 02_Marcus_Technical_Analyst_20251016_143045.txt
...
✓ Complete analysis saved to: FINAL_SUMMARY_20251016_143530.txt
```

## Tips

💡 **Use a text editor with search** - VSCode, Notepad++, etc.  
💡 **Compare timestamp patterns** - Are some analysts consistently slower?  
💡 **Look for consensus** - When all analysts agree, signal strength increases  
💡 **Check for conflicts** - Disagreements may indicate uncertainty  
💡 **Review error patterns** - If something goes wrong, reports show where  

## Folder Auto-Management

✅ Reports folder is **automatically cleared** on each run  
✅ Only the **latest analysis** is kept  
✅ No manual cleanup needed  
✅ Fresh start every time  

## Integration with Discord

The `FINAL_SUMMARY_*.txt` file shows exactly what was sent to your Discord channel.
Individual reports show the underlying reasoning that led to those decisions.

---

**Location**: All reports are in `c:\Repos\day-trader\reports\`
