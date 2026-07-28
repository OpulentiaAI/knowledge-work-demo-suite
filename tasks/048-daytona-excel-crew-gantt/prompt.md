# Build a Dynamic 168-Hour Crew Gantt

## Assignment

Open `source_docs/crew_coverage_inputs.xlsx` and save the completed workbook as
`crew_coverage_model.xlsx`. Preserve the four input sheets and add a
presentation-ready `Crew Gantt` sheet.

Build the `Crew Gantt` sheet with all of these requirements:

- Use `Scenario Control!B3` as the single scenario selector. Every row, KPI,
  shift bar, coverage result, and chart series must update when the user
  selects `Base`, `Peak`, or `Lean`.
- Create a 168-hour weekly coverage grid running left to right from Monday
  00:00 through Sunday 23:00. Add distinct day banners and readable hour
  markers.
- Show one row per crew in the selected scenario, ordered by headcount
  descending and then Crew ID ascending.
- Pin the left block and the time headers so they remain visible while
  scrolling. The left block must contain Crew ID, Role, FT/PT, Shift Pattern,
  Shift Window, and Headcount.
- Draw each crew's scheduled hours as a colored bar across the grid. Use a
  consistent visual system that communicates both Role and FT/PT status, and
  include a legend.
- Respect workday flags. Shifts whose end time is earlier than or equal to
  their start time must wrap correctly across midnight into the next day.
- Add a formula-driven header showing the active scenario, total crews, total
  headcount, peak package volume, peak people on shift, and a 168-hour coverage
  check. The coverage check passes only when staffing is greater than zero in
  every hour.
- Below the grid, add a readable chart comparing package volume with headcount
  on shift for all 168 hours of the active scenario. A secondary axis is
  acceptable.

Use formulas, tables, dynamic ranges, conditional formatting, or clearly
documented helper areas so another analyst can trace and update the model.
Do not use macros, manually painted scenario results, or hardcoded KPI values.
The finished workbook must open without formula errors.

## Source documents

Read the workbook and its `Data Dictionary` sheet before building the output.
The supplied crew schedules and hourly volumes are authoritative synthetic
inputs.

## Expected deliverable

- `crew_coverage_model.xlsx`
