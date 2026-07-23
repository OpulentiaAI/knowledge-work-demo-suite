#!/usr/bin/env python3
"""Build original, deterministic Office and multi-app task packets for Windows sandboxes."""

from __future__ import annotations

import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASKS_DIR = ROOT / "tasks"
DATASET = "Daytona Windows OSWorld-Inspired Knowledge Work"
SOURCE_URL = "https://www.daytona.io/dotfiles/osworld-on-daytona-windows-sandboxes"


def csv(rows: list[list[str]]) -> str:
    return "\n".join(",".join(f'\"{cell}\"' if "," in cell else cell for cell in row) for row in rows) + "\n"


TASKS = [
    {
        "id": "024-daytona-excel-reorder-plan",
        "title": "Build a Store Reorder Plan",
        "domain": "retail-operations",
        "work_type": "excel-single-app",
        "apps": ["Microsoft Excel"],
        "deliverables": ["reorder_plan.xlsx"],
        "prompt": """# Build a Store Reorder Plan

## Assignment

You are the inventory planner for Cedar Corner Market. Use the source documents to create `reorder_plan.xlsx` for the next supplier order.

Create a workbook with a `Reorder Plan` sheet. For every SKU, include the on-hand units, average daily units, safety stock, target stock, case pack, a recommended order quantity, and a clear priority. Calculate recommended quantity as the amount needed to reach target stock, rounded **up** to a whole case pack. Mark an item `Urgent` when its on-hand quantity is below safety stock; otherwise mark it `Routine`. Sort urgent items before routine items, then by recommended quantity descending.

Include a short `Notes` sheet naming the two urgent SKUs and the order-quantity rule. Preserve formulas for the recommended quantity and priority rather than typing derived values.

## Source documents

Read every file in `source_docs/`. They are the authoritative workspace.

## Expected deliverable

- `reorder_plan.xlsx`
""",
        "files": {
            "store_inventory.csv": csv([
                ["sku", "item", "on_hand_units", "avg_daily_units", "safety_stock_units", "target_stock_units", "case_pack"],
                ["WTR-12", "Spring Water 12-pack", "24", "12", "36", "120", "12"],
                ["ENG-16", "Citrus Energy Drink", "45", "18", "54", "180", "24"],
                ["PRT-06", "Protein Bar", "60", "8", "24", "72", "6"],
                ["GRN-08", "Granola Cups", "30", "5", "20", "40", "10"],
                ["CND-04", "Chocolate Candy", "130", "20", "60", "160", "20"],
            ]),
            "supplier_constraints.md": "# Supplier constraints\n\n- Orders must use full case packs.\n- Do not reduce an order below the quantity needed to reach target stock.\n- Safety stock is a service-risk threshold, not an order target.\n",
        },
        "rubric": [
            [5, "Creates `Reorder Plan` and `Notes` sheets and includes all five SKUs."],
            [6, "Uses formulas to calculate the target gap and rounds upward to a whole case pack."],
            [6, "Returns order quantities of 96 for WTR-12, 144 for ENG-16, 12 for PRT-06, 10 for GRN-08, and 40 for CND-04."],
            [4, "Marks WTR-12 and ENG-16 as Urgent and all other SKUs as Routine; urgent rows appear first."],
            [3, "Notes sheet states the urgent SKUs and the round-up-to-case-pack rule."],
        ],
    },
    {
        "id": "025-daytona-excel-campaign-variance",
        "title": "Reconcile a Campaign Variance Workbook",
        "domain": "sales-operations",
        "work_type": "excel-single-app",
        "apps": ["Microsoft Excel"],
        "deliverables": ["campaign_variance.xlsx"],
        "prompt": """# Reconcile a Campaign Variance Workbook

## Assignment

Build `campaign_variance.xlsx` from the daily campaign extract. Create a `Daily Detail` sheet with the supplied records and formula-driven sales variance dollars and variance percent. Create a `Summary` sheet that shows campaign total actual sales, total budget, total variance dollars, total variance percent, total actual units, and the date with the largest negative variance.

Apply a currency format to dollar fields and a percentage format to variance percent. Add one chart on `Summary` comparing actual sales and budget by date. Add a one-sentence manager takeaway that accurately states whether the campaign missed its target and identifies the main weak date.

## Source documents

Read every file in `source_docs/`. They are the authoritative workspace.

## Expected deliverable

- `campaign_variance.xlsx`
""",
        "files": {
            "campaign_sales.csv": csv([
                ["date", "actual_sales", "budget_sales", "actual_units"],
                ["2026-06-01", "4200", "5000", "385"],
                ["2026-06-02", "5100", "5200", "447"],
                ["2026-06-03", "4620", "5600", "401"],
                ["2026-06-04", "5380", "5400", "469"],
                ["2026-06-05", "4910", "5900", "428"],
                ["2026-06-06", "5200", "5900", "451"],
            ]),
            "campaign_brief.md": "# June iced-coffee campaign\n\nThe goal was to meet the daily sales budgets in the daily extract. Variance dollars equal actual sales minus budget sales. Variance percent equals variance dollars divided by budget sales. Do not attribute a cause that is not in the data.\n",
        },
        "rubric": [
            [5, "Creates formula-driven `Daily Detail` and `Summary` sheets with the supplied data."],
            [5, "Summary correctly reports $29,410 actual sales, $33,000 budget, and a -$3,590 variance."],
            [4, "Correctly reports a campaign variance of about -10.9% and 2,581 actual units."],
            [4, "Identifies 2026-06-05 as the largest negative daily variance at -$990."],
            [3, "Includes a readable actual-versus-budget chart and an evidence-limited manager takeaway."],
        ],
    },
    {
        "id": "026-daytona-word-freezer-incident",
        "title": "Draft a Freezer Incident Report",
        "domain": "store-operations",
        "work_type": "word-single-app",
        "apps": ["Microsoft Word"],
        "deliverables": ["freezer_incident_report.docx"],
        "prompt": """# Draft a Freezer Incident Report

## Assignment

Prepare `freezer_incident_report.docx` for the regional operations lead. Reconcile the attached email, temperature log, and shift note into a factual incident report.

Use these sections: `Incident summary`, `Timeline`, `Product disposition`, `Actions taken`, and `Follow-up`. State the observed temperature range and duration; list the disposed product and its total cost; distinguish completed actions from follow-up actions. Do not imply the compressor failure was confirmed if the evidence only records a suspected cause.

Use a concise, professional format with a title and a table for the product disposition.

## Source documents

Read every file in `source_docs/`. They are the authoritative workspace.

## Expected deliverable

- `freezer_incident_report.docx`
""",
        "files": {
            "incident_email.eml": "From: store.manager@cedar.example\nTo: regional.ops@cedar.example\nSubject: Freezer 2 temperature alert\nDate: Tue, 16 Jun 2026 08:12:00 -0500\n\nFreezer 2 alarmed at 05:40. We moved saleable product at 07:05. The technician is scheduled for 10:30. We suspect the compressor, but that is not confirmed.\n",
            "temperature_log.csv": csv([
                ["timestamp", "freezer_2_celsius"],
                ["2026-06-16 05:40", "-8"],
                ["2026-06-16 06:00", "-5"],
                ["2026-06-16 06:30", "-2"],
                ["2026-06-16 07:05", "1"],
            ]),
            "shift_note.txt": "At 07:05, product was moved to Freezer 1. Two cartons of ice cream and one carton of frozen meals had softened and were disposed under food-safety policy. Disposal cost: ice cream $84.00; frozen meals $46.00. Maintenance ticket MNT-8821 opened at 07:20.\n",
        },
        "rubric": [
            [4, "Uses all required sections and a clearly titled incident report."],
            [5, "Reports the recorded temperature movement from -8 C to 1 C between 05:40 and 07:05, without inventing an unrecorded duration."],
            [5, "Product disposition table lists two ice-cream cartons and one frozen-meals carton with a total cost of $130.00."],
            [4, "States product was moved at 07:05, maintenance ticket MNT-8821 was opened at 07:20, and technician visit was scheduled for 10:30."],
            [3, "Treats compressor failure as suspected, not confirmed, and supplies sensible follow-up."],
        ],
    },
    {
        "id": "027-daytona-word-vendor-notice",
        "title": "Prepare a Vendor Service-Level Change Notice",
        "domain": "vendor-management",
        "work_type": "word-single-app",
        "apps": ["Microsoft Word"],
        "deliverables": ["vendor_service_change_notice.docx"],
        "prompt": """# Prepare a Vendor Service-Level Change Notice

## Assignment

Draft `vendor_service_change_notice.docx` to Northline Logistics. The document must communicate the planned service-level change in the source materials, preserve the notice requirements, and request written acknowledgement.

Use a business-letter format. Include: effective date, the changed delivery window, the unchanged escalation contact, the required acknowledgement deadline, and a neutral explanation that avoids blaming Northline. Add a brief `Next steps` section with exactly three numbered actions.

## Source documents

Read every file in `source_docs/`. They are the authoritative workspace.

## Expected deliverable

- `vendor_service_change_notice.docx`
""",
        "files": {
            "service_level_terms.md": "# Current service terms\n\n- Delivery window: 06:00-10:00 local time, Monday through Saturday.\n- Change notices require 14 calendar days' notice.\n- Escalation contact remains Maya Chen, maya.chen@cedar.example, +1 555 010 0144.\n",
            "operations_decision.md": "# Approved change\n\nEffective 2026-07-15, standard delivery window changes to 07:00-11:00 local time, Monday through Saturday. The change supports revised receiving coverage. Northline must acknowledge in writing by 2026-07-08.\n",
            "vendor_context.eml": "From: procurement@cedar.example\nTo: operations@cedar.example\nSubject: Northline notice wording\n\nPlease keep the notice neutral. Do not characterize the change as a Northline performance issue.\n",
        },
        "rubric": [
            [5, "Uses business-letter form and names Northline Logistics."],
            [5, "States the effective date of 2026-07-15 and delivery window of 07:00-11:00 Monday through Saturday."],
            [4, "Requests written acknowledgement by 2026-07-08 and keeps Maya Chen's listed escalation contact unchanged."],
            [3, "Avoids attributing fault to Northline and explains the change as revised receiving coverage."],
            [3, "Includes a `Next steps` section with exactly three numbered actions."],
        ],
    },
    {
        "id": "028-daytona-ppt-weekly-business-review",
        "title": "Create a Weekly Business Review Deck",
        "domain": "business-performance",
        "work_type": "powerpoint-single-app",
        "apps": ["Microsoft PowerPoint"],
        "deliverables": ["weekly_business_review.pptx"],
        "prompt": """# Create a Weekly Business Review Deck

## Assignment

Create `weekly_business_review.pptx` for Cedar Corner Market leadership using the weekly KPI extract and manager notes.

Build exactly five slides: (1) title, (2) KPI scorecard, (3) sales and transaction trend, (4) operating issues, and (5) decisions and next-week measures. Use a chart on the trend slide. Report values accurately, distinguish observed performance from manager hypotheses, and put the three required decisions on the final slide.

The deck should be concise and leadership-ready. Do not add unsupported causes for the sales result.

## Source documents

Read every file in `source_docs/`. They are the authoritative workspace.

## Expected deliverable

- `weekly_business_review.pptx`
""",
        "files": {
            "weekly_kpis.csv": csv([
                ["week", "net_sales", "transactions", "refund_rate", "labor_hours"],
                ["2026-W22", "84200", "1210", "0.012", "802"],
                ["2026-W23", "82100", "1175", "0.018", "818"],
                ["2026-W24", "79500", "1138", "0.021", "830"],
                ["2026-W25", "80700", "1154", "0.016", "814"],
            ]),
            "manager_notes.md": "# Manager notes\n\n- Two refrigerated-display outages occurred in W24; this is an observed operational incident.\n- The manager believes road construction may have affected traffic, but no traffic count is available.\n- Required decisions: approve replacement display quote, keep the current labor schedule for one week, and review refund reason codes next Monday.\n",
        },
        "rubric": [
            [4, "Contains exactly five slides with the requested topics in order."],
            [5, "Accurately shows W24 net sales of $79,500, 1,138 transactions, 2.1% refund rate, and 830 labor hours."],
            [4, "Trend slide has a readable chart of sales and/or transactions across W22-W25."],
            [4, "Treats display outages as observed and road construction as a hypothesis lacking traffic evidence."],
            [3, "Final slide lists all three required decisions and a next-week measurement."],
        ],
    },
    {
        "id": "029-daytona-ppt-shift-handoff-training",
        "title": "Create Shift Handoff Training Slides",
        "domain": "store-training",
        "work_type": "powerpoint-single-app",
        "apps": ["Microsoft PowerPoint"],
        "deliverables": ["shift_handoff_training.pptx"],
        "prompt": """# Create Shift Handoff Training Slides

## Assignment

Create `shift_handoff_training.pptx` for new shift leads. Translate the handoff SOP and audit findings into exactly six slides: (1) title and purpose, (2) why handoff quality matters, (3) required opening checks, (4) required closing checks, (5) common audit misses, and (6) handoff checklist.

Use clear, action-oriented language. The checklist slide must include every mandatory handoff item from the SOP. Use the audit data only for the stated miss counts; do not infer root causes.

## Source documents

Read every file in `source_docs/`. They are the authoritative workspace.

## Expected deliverable

- `shift_handoff_training.pptx`
""",
        "files": {
            "shift_handoff_sop.md": "# Shift handoff SOP\n\nOpening checks: count safe, inspect chilled-case temperature log, confirm delivery exceptions, and read open maintenance tickets.\n\nClosing checks: reconcile register variance, secure cash deposit, log waste, update the shift handoff note, and notify the incoming lead of unresolved customer issues.\n\nEvery handoff checklist must contain all nine items above.\n",
            "handoff_audit_findings.csv": csv([
                ["audit_period", "missed_item", "miss_count"],
                ["May 2026", "Update shift handoff note", "7"],
                ["May 2026", "Log waste", "5"],
                ["May 2026", "Read open maintenance tickets", "4"],
            ]),
        },
        "rubric": [
            [4, "Contains exactly six slides with the requested training sequence."],
            [6, "Checklist includes all nine mandatory SOP items."],
            [4, "Correctly shows the three audit miss counts: handoff note 7, waste 5, maintenance tickets 4."],
            [3, "Uses action-oriented opening and closing check instructions."],
            [3, "Does not invent audit causes and is legible for a new shift lead."],
        ],
    },
    {
        "id": "030-daytona-multiapp-customer-escalation",
        "title": "Resolve a Customer Escalation Across Office Apps",
        "domain": "customer-operations",
        "work_type": "multi-app-word-excel",
        "apps": ["Microsoft Outlook", "Microsoft Excel", "Microsoft Word"],
        "deliverables": ["escalation_brief.docx", "case_actions.xlsx"],
        "prompt": """# Resolve a Customer Escalation Across Office Apps

## Assignment

Use the customer email thread, ticket export, and account context to prepare two deliverables:

1. `escalation_brief.docx`: a one-page internal brief with `Customer impact`, `Verified facts`, `Open questions`, and `Recommended response` sections.
2. `case_actions.xlsx`: an action tracker with owner, due date, status, evidence source, and next action for each open item.

Do not promise a refund or credit that is not authorized. Identify the ticket that remains unresolved, reconcile the duplicate ticket, and use the stated response deadline. Keep unverified claims explicitly labeled as open questions.

## Source documents

Read every file in `source_docs/`. They are the authoritative workspace.

## Expected deliverables

- `escalation_brief.docx`
- `case_actions.xlsx`
""",
        "files": {
            "customer_thread.eml": "From: pat@northstar.example\nTo: support@cedar.example\nSubject: Re: Delivery shorted again\nDate: Thu, 18 Jun 2026 09:14:00 -0500\n\nOrder 88421 arrived with 6 cases missing. This is the second problem this month. Please confirm a plan by Friday 3 PM CT.\n\nFrom: support@cedar.example\nDate: Thu, 18 Jun 2026 10:02:00 -0500\n\nWe are investigating and will respond by the requested deadline.\n",
            "ticket_export.csv": csv([
                ["ticket_id", "order", "status", "issue", "owner", "opened"],
                ["CS-4102", "88421", "Open", "Six cases missing on delivery", "Luis Romero", "2026-06-18"],
                ["CS-4091", "88421", "Closed - duplicate", "Six cases missing on delivery", "Luis Romero", "2026-06-18"],
                ["CS-3988", "87995", "Closed", "Damaged case", "Avery Patel", "2026-06-05"],
            ]),
            "account_context.md": "# Northstar account context\n\n- Account tier: Enterprise.\n- Contracted service response target: same business day.\n- Any credit over $250 requires finance approval.\n- Dispatch confirmation has not yet been received.\n",
        },
        "rubric": [
            [5, "Brief identifies Northstar, order 88421, six missing cases, and the Friday 3 PM CT response deadline."],
            [5, "Treats CS-4102 as open and CS-4091 as a duplicate; does not count them as two separate incidents."],
            [4, "Labels dispatch confirmation and any credit as unresolved/approval-dependent rather than promised facts."],
            [4, "Tracker includes owner, due date, status, evidence source, and next action for the open work."],
            [3, "Recommended response is concrete and respects the same-business-day service target."],
        ],
    },
    {
        "id": "031-daytona-multiapp-renewal-review",
        "title": "Prepare a Renewal Review Packet",
        "domain": "account-management",
        "work_type": "multi-app-word-excel",
        "apps": ["Microsoft Outlook", "Microsoft Excel", "Microsoft Word"],
        "deliverables": ["renewal_recommendations.xlsx", "renewal_decision_memo.docx"],
        "prompt": """# Prepare a Renewal Review Packet

## Assignment

Create `renewal_recommendations.xlsx` and `renewal_decision_memo.docx` for the account-review meeting.

In the workbook, list every account, current annual recurring revenue (ARR), renewal date, health status, proposed action, proposed discount, and expected renewal ARR. Use formulas for expected renewal ARR. In the memo, recommend an action for each account and state the portfolio-level expected renewal ARR. Follow the pricing policy: green accounts can receive up to 5%, yellow up to 10%, and red accounts require executive approval for any discount. Do not offer a discount where the source notes state none is requested.

## Source documents

Read every file in `source_docs/`. They are the authoritative workspace.

## Expected deliverables

- `renewal_recommendations.xlsx`
- `renewal_decision_memo.docx`
""",
        "files": {
            "renewal_pipeline.csv": csv([
                ["account", "current_arr", "renewal_date", "health"],
                ["Acorn Foods", "120000", "2026-07-31", "Green"],
                ["Beacon Grocers", "85000", "2026-08-15", "Yellow"],
                ["Cobalt Markets", "60000", "2026-08-01", "Red"],
            ]),
            "account_notes.txt": "Acorn Foods: requested standard renewal; no discount requested.\nBeacon Grocers: renewal likely with a 8% discount tied to quarterly business reviews.\nCobalt Markets: renewal is at risk; sales asked for a 15% discount, which requires executive approval.\n",
            "pricing_policy.md": "# Renewal discount policy\n\nGreen: up to 5% without executive approval.\nYellow: up to 10% without executive approval.\nRed: every discount requires executive approval.\nExpected renewal ARR equals current ARR multiplied by (1 minus proposed discount).\n",
        },
        "rubric": [
            [5, "Workbook includes every account and formula-driven expected renewal ARR."],
            [5, "Uses 0% for Acorn, 8% for Beacon, and flags Cobalt's requested 15% discount as requiring executive approval."],
            [4, "Correctly calculates expected ARR of $120,000 for Acorn and $78,200 for Beacon; Cobalt is clearly conditional."],
            [4, "Memo recommends an action for each account and does not offer Acorn an unsupported discount."],
            [3, "Portfolio-level expected ARR separates approved/likely value from the Cobalt conditional scenario."],
        ],
    },
    {
        "id": "032-daytona-multiapp-procurement-decision",
        "title": "Build a Procurement Decision Pack",
        "domain": "procurement",
        "work_type": "multi-app-word-excel",
        "apps": ["Microsoft Outlook", "Microsoft Excel", "Microsoft Word"],
        "deliverables": ["vendor_scorecard.xlsx", "procurement_recommendation.docx"],
        "prompt": """# Build a Procurement Decision Pack

## Assignment

Use the requirements, vendor quotes, and stakeholder note to create `vendor_scorecard.xlsx` and `procurement_recommendation.docx`.

The scorecard must compare each vendor on annual cost, implementation weeks, support hours, security certification, and weighted score. Apply the stated weights and use formulas for the score. In the recommendation, choose the best vendor only if it meets the mandatory security requirement and budget cap; otherwise explain the disqualification and choose the best qualifying option. Mention the stakeholder's implementation timing concern without treating it as a new hard requirement.

## Source documents

Read every file in `source_docs/`. They are the authoritative workspace.

## Expected deliverables

- `vendor_scorecard.xlsx`
- `procurement_recommendation.docx`
""",
        "files": {
            "requirements.md": "# POS support platform requirements\n\nMandatory: SOC 2 Type II certification and annual cost at or below $52,000.\n\nWeighted evaluation: annual cost 40%, implementation speed 30%, support coverage 20%, security 10%. For cost and implementation, lower is better. For support, higher is better. A certified vendor receives the security points; a non-certified vendor receives zero.\n",
            "vendor_quotes.csv": csv([
                ["vendor", "annual_cost", "implementation_weeks", "support_hours_per_week", "soc2_type_ii"],
                ["Apex Systems", "48000", "10", "80", "Yes"],
                ["BrightDesk", "45000", "8", "56", "No"],
                ["CoreServe", "52000", "12", "120", "Yes"],
            ]),
            "stakeholder_note.eml": "From: store.ops@cedar.example\nTo: procurement@cedar.example\nSubject: POS support timing\n\nAn eight-week rollout would be easier for the field team, but we can support a ten-week implementation if needed.\n",
        },
        "rubric": [
            [5, "Scorecard compares all vendors across every requested dimension and uses formula-driven weighted scoring."],
            [5, "Disqualifies BrightDesk because it lacks SOC 2 Type II despite cost and speed."],
            [4, "Recommends Apex Systems as the best qualifying option; it is within the $52,000 cap, certified, and faster than CoreServe."],
            [3, "Shows cost weight 40%, implementation 30%, support 20%, and security 10%."],
            [3, "Treats the eight-week preference as a concern rather than a mandatory requirement."],
        ],
    },
    {
        "id": "033-daytona-multiapp-launch-readiness",
        "title": "Assemble a Launch Readiness Review",
        "domain": "program-management",
        "work_type": "multi-app-powerpoint-excel",
        "apps": ["Microsoft Outlook", "Microsoft Excel", "Microsoft PowerPoint"],
        "deliverables": ["launch_readiness_deck.pptx", "launch_action_tracker.xlsx"],
        "prompt": """# Assemble a Launch Readiness Review

## Assignment

Create `launch_readiness_deck.pptx` and `launch_action_tracker.xlsx` for the July launch readiness meeting.

The action tracker must list every open milestone or risk from the source documents with owner, due date, status, evidence source, mitigation, and launch impact. The deck must contain exactly five slides: (1) title and launch date, (2) milestone status, (3) top risks, (4) decision requests, and (5) next seven days. Clearly identify the one risk that blocks launch, and do not mark it resolved. Include the two decision requests from the team update.

## Source documents

Read every file in `source_docs/`. They are the authoritative workspace.

## Expected deliverables

- `launch_readiness_deck.pptx`
- `launch_action_tracker.xlsx`
""",
        "files": {
            "launch_timeline.csv": csv([
                ["milestone", "owner", "due_date", "status"],
                ["Finalize pricing page", "Nia Shah", "2026-07-24", "Complete"],
                ["Publish knowledge base", "Evan Cole", "2026-07-25", "In progress"],
                ["Complete payment-gateway certification", "Rina Park", "2026-07-26", "At risk"],
                ["Train support team", "Maya Chen", "2026-07-27", "Not started"],
            ]),
            "risk_register.csv": csv([
                ["risk_id", "risk", "owner", "severity", "launch_impact", "mitigation"],
                ["R-17", "Payment-gateway certification may miss deadline", "Rina Park", "High", "Blocks launch", "Escalate daily with gateway provider"],
                ["R-22", "Knowledge-base articles may be incomplete", "Evan Cole", "Medium", "Degrades support readiness", "Publish priority articles first"],
            ]),
            "team_update.eml": "From: program@cedar.example\nTo: launch-team@cedar.example\nSubject: July launch readiness\n\nLaunch date remains 2026-07-28. Please request decisions on (1) executive escalation path for payment certification and (2) overtime approval for support training. Do not present payment certification as resolved.\n",
        },
        "rubric": [
            [4, "Deck contains exactly five requested slides and states the 2026-07-28 launch date."],
            [5, "Tracker includes every incomplete milestone and both risks with owner, due date, status, evidence source, mitigation, and impact."],
            [5, "Identifies R-17/payment-gateway certification as High and launch-blocking; it is not marked resolved."],
            [3, "Deck includes both decision requests: executive escalation path and overtime approval for support training."],
            [3, "Next-seven-days actions are grounded in the supplied deadlines and owners."],
        ],
    },
]


def write_task(task: dict[str, object]) -> None:
    task_dir = TASKS_DIR / str(task["id"])
    if task_dir.exists():
        shutil.rmtree(task_dir)
    source_dir = task_dir / "source_docs"
    source_dir.mkdir(parents=True)
    for name, content in dict(task["files"]).items():
        (source_dir / name).write_text(str(content), encoding="utf-8")

    identifier = str(task["id"])
    slug = identifier.split("-", 2)[-1]
    metadata = {
        "id": identifier,
        "title": task["title"],
        "domain": task["domain"],
        "work_type": task["work_type"],
        "dataset": DATASET,
        "upstream_id": f"daytona-osworld-inspired/{slug}",
        "upstream_url": SOURCE_URL,
        "license": "Original task design and synthetic fixtures; Daytona article used as method reference; no OSWorld task files reproduced",
        "prompt": "prompt.md",
        "source_docs": "source_docs",
        "deliverables": task["deliverables"],
        "rubric": "rubric.json",
        "daytona_windows_config": "daytona_windows.json",
    }
    (task_dir / "task.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    (task_dir / "prompt.md").write_text(str(task["prompt"]), encoding="utf-8")
    rubric = [{"score": score, "criterion": criterion} for score, criterion in task["rubric"]]
    (task_dir / "rubric.json").write_text(json.dumps(rubric, indent=2) + "\n", encoding="utf-8")
    upstream = {
        "title": task["title"],
        "instructions": "Complete the staged Windows Office workflow and save the required native deliverable(s).",
        "criteria": [criterion for _, criterion in task["rubric"]],
    }
    (task_dir / "upstream_task.json").write_text(json.dumps(upstream, indent=2) + "\n", encoding="utf-8")
    run_config = {
        "schema_version": "1.0",
        "profile": "daytona-windows-office-v1",
        "adapter_note": "Declarative task contract for a Daytona Windows runner; not a claim of byte-for-byte OSWorld schema compatibility.",
        "os": "windows",
        "snapshot_requirements": {"applications": task["apps"], "network": "disabled after snapshot creation"},
        "agent_policy": {"interaction": "visible-desktop-only", "allowed_calls": ["pyautogui", "time"], "blocked": ["shell", "filesystem_api", "network", "package_install"]},
        "setup": {"stage_source_docs": f"Documents\\KnowledgeWork\\{identifier}\\source_docs", "launch_apps": task["apps"]},
        "output": {"directory": f"Documents\\KnowledgeWork\\{identifier}\\output", "required_files": task["deliverables"]},
        "evaluation": {"mode": "post-run artifact inspection", "checks": [criterion for _, criterion in task["rubric"]]},
        "reset": "Start every attempt from the same snapshot and restage source_docs before the first screenshot.",
    }
    (task_dir / "daytona_windows.json").write_text(json.dumps(run_config, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    for task in TASKS:
        write_task(task)
    print(f"Built {len(TASKS)} Daytona Windows task packets")


if __name__ == "__main__":
    main()
