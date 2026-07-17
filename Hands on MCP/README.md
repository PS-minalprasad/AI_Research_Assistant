# Bug Trend Analysis Using Atlassian MCP

L1 certification assignment submission — bug/defect data retrieved from Jira Cloud via
Anthropic's **Atlassian Remote MCP** integration, analyzed for trends, severity,
component concentration, resolution time, and root cause.

## Contents

| File | Description |
|---|---|
| `Bug_Trend_Analysis_Report.docx` | Full submission report (10 sections, cover page, tables, 5 charts) |
| `bug_dataset.csv` | 20-row dataset of bug records retrieved/enriched from Jira |
| `Bug_Trend_Analysis_Presentation.pptx` | 10-slide presentation summarizing the findings |
| `chart_trend.png` | Bug frequency trend by month |
| `chart_severity.png` | Severity distribution |
| `chart_component.png` | Defects by component/module |
| `chart_rootcause.png` | Root cause distribution |
| `chart_resolution.png` | Resolution time by issue |

## Jira source

- **Site:** `productsquads-team-p8xe5ds9.atlassian.net`
- **Project:** `SCRUM` — "My Software Team"
- **Issue range:** SCRUM-5 through SCRUM-24 (20 Bug-type issues)
- **Modules covered:** Authentication, Payment, Backend API, Database, Frontend, Notifications

## MCP tools used

| Tool | Purpose |
|---|---|
| `getAccessibleAtlassianResources` | Resolve the Jira Cloud ID for the connected site |
| `searchJiraIssuesUsingJql` | Bulk retrieval of bug issues (`issuetype = Bug`) |
| `createJiraIssue` | Create supplementary bug records for full module coverage |
| `getJiraIssue` | Single-issue field verification |

## Methodology note on dates

All 20 issues were created in Jira on the same day for this exercise, so their
system `created` timestamps have no historical spread. To produce a meaningful
multi-month trend, a simulated lifecycle layer (created date, resolved date,
testing phase found, root cause category, reporter, assignee) was generated on
top of the real Jira issue content. This is disclosed in Section 5.3 of the
report and is standard practice for a freshly-seeded demo project.

## Key findings

- **Trend:** Bug discovery rose from Dec 2025 into a peak of 5 bugs/month in
  March and May 2026, then tapered by July.
- **Severity:** 55% of bugs are High or Highest severity.
- **Components:** Payment, Authentication, and Backend API are tied as the
  most defect-prone modules (4 bugs each).
- **Resolution time:** Average 4.09 days; Highest-severity bugs resolve
  fastest (2.2 days avg), Low-severity slowest (7.8 days avg).
- **Root cause:** Coding Defects (30%) and Design/Architecture Issues (25%)
  account for over half of all defects.

