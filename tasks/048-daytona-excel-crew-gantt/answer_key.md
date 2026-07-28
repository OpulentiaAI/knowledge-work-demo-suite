# Deterministic answer contract

## Scenario KPIs

| Scenario | Crews | Total headcount | Peak package volume | Peak people on shift | Coverage |
|---|---:|---:|---:|---:|---|
| Base | 8 | 130 | 1,150 | 66 | PASS |
| Peak | 10 | 212 | 1,840 | 96 | PASS |
| Lean | 7 | 88 | 828 | 46 | PASS |

Peak package volume occurs at week hour 109, Friday 13:00, in every scenario.
The first peak-staffing hours are Base week hour 33, Peak week hour 10, and Lean
week hour 108.

## Expected row order

- Base: B-B, B-F, B-C, B-A, B-D, B-E, B-G, B-H.
- Peak: P-B, P-F, P-C, P-A, P-E, P-D, P-G, P-H, P-I, P-J.
- Lean: L-B, L-C, L-E, L-A, L-D, L-F, L-G.

## Shift interpretation

The workday flags identify the day on which a shift starts. When Shift End is
earlier than or equal to Shift Start, the scheduled bar continues after
midnight on the following day. No crew should appear outside its listed
workdays, except for that after-midnight continuation.

The chart must contain all 168 selected-scenario hourly observations for both
package volume and calculated headcount on shift.
