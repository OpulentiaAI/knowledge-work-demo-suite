#!/usr/bin/env python3
"""Build seven deterministic, public-safe tax strategy evaluation packets."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TASKS_DIR = ROOT / "tasks"
DATASET = "Tax Strategy Execution Manual-Inspired Advisory Work"
LICENSE = (
    "Original task design and synthetic client fixtures under repository MIT license; "
    "United States government guidance is cited by URL and not redistributed; "
    "the confidential methodology manual is not included"
)
MANUAL_SHA256 = "ef3d19962640979ecab443432fc2c6605f213744e516cf86e11d2fb51940b9d2"


COMMON_PROMPT = """\
## Working rules

- Treat the synthetic client facts in `source_docs/` as authoritative.
- Apply the cited 2026 federal rules. Identify assumptions and any state-law,
  plan-document, payroll-provider, or tax-adviser confirmation still required.
- Show calculations and distinguish a planning estimate from a filed tax result.
- Do not invent facts, guarantees, deductions, or compliance steps.
- Create both required deliverables with the exact filenames below.
- The workbook must preserve formulas in calculation cells and include a short
  `Sources & Assumptions` sheet.
"""


def guidance(*items: tuple[str, str]) -> str:
    lines = [
        "# Official guidance",
        "",
        "Use the rules below for this evaluation. Confirm later-law changes before",
        "using the work product for an actual taxpayer.",
        "",
    ]
    for title, detail in items:
        lines.extend([f"## {title}", "", detail.strip(), ""])
    return "\n".join(lines)


def rubric(*criteria: tuple[int, str]) -> list[dict[str, Any]]:
    assert sum(points for points, _ in criteria) == 100
    return [{"score": points, "criterion": text} for points, text in criteria]


TASKS: list[dict[str, Any]] = [
    {
        "id": "041-tax-529-plan-execution",
        "title": "Build a 529 Funding and Distribution Plan",
        "domain": "tax-education-planning",
        "work_type": "tax-advisory-memo-and-model",
        "manual_pages": [6],
        "deliverables": ["529_strategy_memo.md", "529_funding_schedule.xlsx"],
        "assignment": """\
Advise the Rivera family on a 2026 529 plan execution decision. Classify every
proposed school expense, calculate the maximum qualified distribution, model
the grandmother's five-year gift-tax election, and assess the requested
529-to-Roth IRA rollover. Include an implementation checklist and explicit
guardrails against double counting education tax benefits.""",
        "facts": """\
# Synthetic client facts — Rivera family

- Planning year: 2026; all amounts are federal-only planning inputs.
- Beneficiary Maya is 17 and attends an eligible private high school.
- Proposed 2026 payments: tuition $12,500; required curriculum materials $900;
  qualified-subject tutoring $2,400; AP exam fee $100; general-purpose laptop
  $1,800; school transportation $1,200; athletics fee $750.
- The 529 account can pay no more than the federally qualified amount.
- Grandmother Elena wants to contribute $95,000 in 2026 and make the five-year
  gift-tax averaging election. She makes no other gifts to Maya in 2026–2030.
- The 529 account was opened in June 2009.
- Maya has $8,000 of 2026 earned income, makes no other IRA contribution, and
  requests a direct $10,000 529-to-Roth IRA rollover.
- No scholarship, American Opportunity Credit, Lifetime Learning Credit, or
  other tax-free reimbursement applies to these expenses.
""",
        "inputs": [
            ["expense", "amount_usd", "evaluation_note"],
            ["High-school tuition", "12500", "potentially qualified K-12 expense"],
            ["Required curriculum materials", "900", "potentially qualified in 2026"],
            ["Qualified-subject tutoring", "2400", "potentially qualified in 2026"],
            ["AP examination fee", "100", "potentially qualified in 2026"],
            ["General-purpose laptop", "1800", "not a listed K-12 qualified expense"],
            ["School transportation", "1200", "not a qualified expense"],
            ["Athletics fee", "750", "not a listed qualified expense"],
        ],
        "guidance": guidance(
            (
                "IRS Topic 313 — Qualified tuition programs",
                """For 2026, qualified K–12 expenses include tuition and an expanded
list of curriculum materials, books, online educational materials, tutoring,
standardized-test fees, and certain dual-enrollment and educational-therapy
costs. The annual K–12 distribution cap is $20,000 per beneficiary.
https://www.irs.gov/taxtopics/tc313""",
            ),
            (
                "2026 annual gift exclusion",
                """The 2026 annual gift-tax exclusion is $19,000. A 529 contribution
may be elected to be treated ratably over five years; the election is reported
on Form 709.
https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill""",
            ),
            (
                "529-to-Roth IRA transfer guardrails",
                """A qualifying direct transfer is constrained by the annual Roth IRA
limit, earned income, the $35,000 lifetime limit, the 15-year account-age rule,
and the rule excluding recent contributions and earnings. The 2026 IRA
contribution limit is $7,500.
https://www.irs.gov/publications/p590a
https://www.irs.gov/retirement-plans/cola-increases-for-dollar-limitations-on-benefits-and-contributions""",
            ),
        ),
        "expected": """\
# Output expectations

The memo should conclude:

- Qualified 2026 K–12 expenses: **$15,900**.
- Nonqualified proposed expenses: **$3,750**.
- Maximum 2026 qualified distribution under the facts: **$15,900**.
- The $95,000 gift election allocates **$19,000** to each of 2026–2030, with a
  Form 709 election and tracking required.
- The requested $10,000 Roth transfer is capped at **$7,500** for 2026 before
  testing all other statutory conditions, including recent-contribution and
  lifetime-limit records.

The workbook should include `Expense Review`, `Gift Election`, `Roth Rollover`,
and `Sources & Assumptions` sheets.
""",
        "rubric": rubric(
            (20, "Correctly classifies all seven expenses and calculates $15,900 qualified and $3,750 nonqualified."),
            (20, "Limits the distribution to $15,900 and explains the $20,000 K–12 ceiling and no-double-benefit rule."),
            (20, "Models the $95,000 five-year election as $19,000 per year for 2026–2030 and flags Form 709."),
            (20, "Caps the proposed 2026 Roth transfer at $7,500 and states the earned-income, annual, lifetime, account-age, and recent-contribution constraints."),
            (20, "Produces an auditable formula-driven workbook plus a practical implementation and records checklist."),
        ),
    },
    {
        "id": "042-tax-solo-401k-contribution-plan",
        "title": "Calculate and Execute a Solo 401(k) Contribution Plan",
        "domain": "tax-retirement-planning",
        "work_type": "tax-advisory-memo-and-model",
        "manual_pages": [342, 480],
        "deliverables": ["solo_401k_execution_memo.md", "solo_401k_contribution_workbook.xlsx"],
        "assignment": """\
Calculate the owner's maximum modeled 2026 one-participant 401(k)
contribution, taking an outside-plan deferral into account. Separate the
employee, catch-up, and employer components and prepare an execution calendar
covering plan documents, deposits, records, and Form 5500-EZ monitoring.""",
        "facts": """\
# Synthetic client facts — Northstar Design

- Northstar Design is Jordan's Schedule C sole proprietorship with no employees.
- 2026 net profit before the deductible half of self-employment tax and plan
  contribution: $180,000.
- For this evaluation, calculate net earnings subject to self-employment tax as
  92.35% of profit and apply 15.3%; ignore the Social Security wage-base split
  because the supplied deterministic model uses that combined rate.
- Jordan is age 54 at year-end 2026.
- Jordan already deferred $10,000 into an unrelated employer's 401(k) in 2026.
- No employer contribution was made by that unrelated employer.
- Use a 20% self-employed employer-contribution rate after deducting one-half
  of modeled self-employment tax.
- Assume no other plan balances and no controlled-group or affiliated-service-
  group issue. Flag these assumptions for adviser confirmation.
""",
        "inputs": [
            ["input", "value"],
            ["Schedule C profit", "180000"],
            ["Net earnings factor", "0.9235"],
            ["Modeled SE tax rate", "0.153"],
            ["Outside-plan elective deferral", "10000"],
            ["2026 regular elective-deferral limit", "24500"],
            ["2026 age-50 catch-up limit", "8000"],
            ["Employer contribution rate", "0.20"],
            ["2026 defined-contribution limit", "72000"],
        ],
        "guidance": guidance(
            (
                "IRS one-participant 401(k) guidance",
                """The business owner acts in two capacities: employee and employer.
Self-employed employer contributions require the adjusted earned-income
calculation. A one-participant plan generally files Form 5500-EZ once total
plan assets reach $250,000.
https://www.irs.gov/retirement-plans/one-participant-401k-plans""",
            ),
            (
                "IRS 2026 limits",
                """For 2026 the elective-deferral limit is $24,500, the age-50
catch-up limit is $8,000, and the defined-contribution limit is $72,000.
https://www.irs.gov/retirement-plans/cola-increases-for-dollar-limitations-on-benefits-and-contributions
https://www.irs.gov/pub/irs-drop/n-25-67.pdf""",
            ),
            (
                "IRS Publication 560",
                """Use the deduction worksheet and current plan-adoption/deposit
rules for a real filing.
https://www.irs.gov/publications/p560""",
            ),
        ),
        "expected": """\
# Output expectations

Under the supplied deterministic model:

- Net earnings subject to SE tax: **$166,230.00**.
- Modeled SE tax: **$25,433.19**; deductible half: **$12,716.60**.
- Adjusted plan compensation: **$167,283.40**.
- Employer contribution at 20%: **$33,456.68**.
- Remaining regular deferral: **$14,500.00**; catch-up: **$8,000.00**.
- Total proposed contribution to this solo plan: **$55,956.68**.
- Amount counted toward the $72,000 section 415 limit: **$47,956.68**.

The workbook should include `Inputs`, `Contribution Model`, `Deadlines`, and
`Sources & Assumptions` sheets.
""",
        "rubric": rubric(
            (25, "Reproduces the supplied model: $166,230 net earnings, $25,433.19 SE tax, and $12,716.60 deductible half."),
            (20, "Calculates $167,283.40 adjusted compensation and a $33,456.68 employer contribution."),
            (20, "Coordinates the shared elective-deferral limit, yielding $14,500 regular deferral plus $8,000 catch-up."),
            (15, "Reports $55,956.68 to this plan and $47,956.68 counted toward the $72,000 section 415 limit."),
            (20, "Provides formula-driven schedules, plan/deposit steps, and Form 5500-EZ and employee-assumption guardrails."),
        ),
    },
    {
        "id": "043-tax-employer-401k-design",
        "title": "Compare Small-Employer 401(k) Designs",
        "domain": "benefits-plan-design",
        "work_type": "benefits-advisory-memo-and-model",
        "manual_pages": [159],
        "deliverables": ["employer_401k_design_memo.md", "employer_401k_cost_model.xlsx"],
        "assignment": """\
Compare a 3% safe-harbor nonelective design with the basic safe-harbor matching
formula for Harbor Works. Determine eligible employees, estimate employer
costs, identify startup credits, and recommend a design with an implementation
calendar and fiduciary/administrative controls.""",
        "facts": """\
# Synthetic client facts — Harbor Works LLC

- Calendar-year plan; design and implementation analysis is for 2026.
- The owners want all otherwise eligible employees included and immediate
  vesting of safe-harbor contributions.
- Eligible employees and 2026 compensation: Alex $160,000; Blair $145,000;
  Casey $120,000; Devon $105,000; Emerson $90,000; Finley $75,000; Gray
  $65,000; Harper $55,000; Indigo $45,000; Jamie $30,000.
- Jamie is a long-term part-time employee with at least 500 hours in both 2024
  and 2025.
- Skyler, compensation $25,000, was hired October 1, 2026 and has not met the
  plan's stated age/service eligibility rules; exclude Skyler for this model.
- Total eligible compensation is $890,000.
- Employee elective-deferral rates in the same order are 10%, 8%, 6%, 5%, 4%,
  3%, 2%, 1%, 0%, and 0%.
- Nine eligible employees are non-highly compensated for the simplified
  startup-credit count supplied here.
- Assume qualifying startup costs are at least the calculated credit and the
  employer otherwise satisfies credit rules. Model the separate automatic-
  enrollment credit as $500, subject to adviser confirmation.
""",
        "inputs": [
            ["employee", "eligible", "compensation", "deferral_rate"],
            ["Alex", "yes", "160000", "0.10"],
            ["Blair", "yes", "145000", "0.08"],
            ["Casey", "yes", "120000", "0.06"],
            ["Devon", "yes", "105000", "0.05"],
            ["Emerson", "yes", "90000", "0.04"],
            ["Finley", "yes", "75000", "0.03"],
            ["Gray", "yes", "65000", "0.02"],
            ["Harper", "yes", "55000", "0.01"],
            ["Indigo", "yes", "45000", "0.00"],
            ["Jamie", "yes", "30000", "0.00"],
            ["Skyler", "no", "25000", "0.00"],
        ],
        "guidance": guidance(
            (
                "Department of Labor — 401(k) plans for small businesses",
                """Plan sponsors must select and monitor providers, transmit
contributions timely, provide disclosures, and operate the plan according to
its documents.
https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/resource-center/publications/401k-plans-for-small-businesses""",
            ),
            (
                "IRS safe-harbor design overview",
                """The basic safe-harbor match is 100% of deferrals up to 3% of
compensation plus 50% of deferrals from 3% through 5%. A 3% nonelective design
contributes for eligible employees whether or not they defer.
https://www.irs.gov/retirement-plans/401k-plan-fix-it-guide-401k-plan-overview""",
            ),
            (
                "IRS startup-cost credit",
                """Qualifying small employers may claim a retirement-plan startup
credit, subject to the statutory limits and eligibility requirements.
https://www.irs.gov/retirement-plans/retirement-plans-startup-costs-tax-credit""",
            ),
        ),
        "expected": """\
# Output expectations

- Model **10 eligible employees**, including Jamie and excluding Skyler.
- Eligible compensation: **$890,000**.
- 3% nonelective cost: **$26,700**.
- Basic safe-harbor match using supplied deferral rates: **$28,450**.
- Nonelective design is **$1,750 less** under these facts.
- Simplified startup-credit model: 9 × $250 = **$2,250**, plus a separately
  identified potential **$500** automatic-enrollment credit.

The workbook should include `Eligibility`, `Nonelective`, `Basic Match`,
`Credits`, and `Sources & Assumptions` sheets.
""",
        "rubric": rubric(
            (20, "Includes 10 eligible employees, correctly treats Jamie as eligible and Skyler as excluded, and totals $890,000 compensation."),
            (20, "Calculates the 3% nonelective cost as $26,700."),
            (20, "Applies the basic match formula employee by employee and calculates $28,450."),
            (15, "Shows the $1,750 cost difference and the $2,250 startup-credit model plus separate potential $500 credit."),
            (25, "Makes a reasoned recommendation and supplies a formula-driven workbook, implementation calendar, fiduciary controls, and qualification caveats."),
        ),
    },
    {
        "id": "044-tax-hiring-owner-child",
        "title": "Design a Compliant Owner-Child Employment Plan",
        "domain": "family-business-payroll",
        "work_type": "tax-advisory-memo-and-payroll-model",
        "manual_pages": [163],
        "deliverables": ["child_employment_memo.md", "child_payroll_schedule.xlsx"],
        "assignment": """\
Evaluate a sole proprietor's proposal to employ a minor child. Determine
reasonable wages from comparables, classify the federal payroll taxes, model
the child's federal income-tax position and Roth IRA capacity, and create a
documentation-first implementation plan.""",
        "facts": """\
# Synthetic client facts — Patel Creative Studio

- Priya operates a sole proprietorship; no corporation or partnership employs
  the child.
- Her child Arjun is age 15 and will perform 160 documented hours of real
  product-photography tagging and file-organization work during 2026.
- Local comparable hourly rates for substantially similar entry-level work are
  $16, $18, and $20. Use the median unless a documented fact supports otherwise.
- The proposed owner budget was $8,000, but pay must reflect actual services.
- Arjun has no other income, is claimed as a dependent, and has no IRA
  contribution for 2026.
- Assume all work is lawful under applicable child-labor rules only after
  counsel/payroll confirmation; this task does not resolve state labor law.
""",
        "inputs": [
            ["item", "value"],
            ["Child age", "15"],
            ["Documented hours", "160"],
            ["Comparable hourly rate 1", "16"],
            ["Comparable hourly rate 2", "18"],
            ["Comparable hourly rate 3", "20"],
            ["Owner proposed budget", "8000"],
            ["2026 dependent standard deduction floor", "1350"],
            ["2026 dependent earned-income addition", "450"],
            ["2026 dependent standard deduction cap", "16100"],
        ],
        "guidance": guidance(
            (
                "IRS family employees",
                """Wages paid by a parent to a child under age 18 in a parent's sole
proprietorship generally are not subject to Social Security and Medicare
taxes; wages to a child under age 21 generally are not subject to FUTA. Federal
income-tax withholding and reporting rules still apply. Entity type matters.
https://www.irs.gov/businesses/small-businesses-self-employed/family-employees""",
            ),
            (
                "IRS Publication 15",
                """Use current payroll procedures, withholding forms, deposit rules,
and Form W-2 reporting.
https://www.irs.gov/publications/p15""",
            ),
            (
                "2026 dependent standard deduction",
                """For 2026 the dependent standard deduction is generally the greater
of $1,350 or earned income plus $450, capped at $16,100.
https://www.irs.gov/irb/2025-45_IRB""",
            ),
        ),
        "expected": """\
# Output expectations

- Median comparable wage: **$18 per hour**.
- Defensible modeled wages: 160 × $18 = **$2,880**; reject an unsupported
  $8,000 payment.
- Under the supplied sole-proprietor facts: no employee/employer FICA and no
  FUTA, while ordinary payroll records, withholding analysis, and Form W-2
  reporting remain required.
- 2026 dependent standard deduction: **$3,330**; absent other income, modeled
  federal taxable income is zero.
- Modeled Roth IRA contribution capacity: **$2,880**, subject to a timely
  contribution and all ordinary IRA requirements.

The workbook should include `Time & Pay`, `Payroll Taxes`, `Child Tax`, and
`Sources & Assumptions` sheets.
""",
        "rubric": rubric(
            (25, "Uses the $18 median rate and 160 hours to calculate $2,880 reasonable wages and rejects the unsupported $8,000 amount."),
            (20, "Correctly applies the sole-proprietor child rules: no FICA under 18 and no FUTA under 21, with ordinary payroll/W-2 controls."),
            (20, "Calculates the dependent standard deduction as $3,330 and zero modeled taxable income absent other income."),
            (15, "Limits modeled Roth IRA capacity to $2,880 of earned income and states qualification caveats."),
            (20, "Provides a formula-driven payroll schedule plus timesheet, job-description, rate-support, labor-law, and records controls."),
        ),
    },
    {
        "id": "045-tax-employing-owner-spouse",
        "title": "Model Owner-Spouse Wages and Benefits",
        "domain": "family-business-payroll",
        "work_type": "tax-advisory-memo-and-payroll-model",
        "manual_pages": [500],
        "deliverables": ["spouse_employment_memo.md", "spouse_payroll_budget.xlsx"],
        "assignment": """\
Evaluate an S corporation's proposed compensation for the owner's spouse.
Establish a supportable cash-wage amount, calculate payroll taxes, show the
specified more-than-2% shareholder health-insurance reporting treatment, and
prepare an implementation and documentation plan.""",
        "facts": """\
# Synthetic client facts — Lakeview Consulting Inc.

- Lakeview is an S corporation wholly owned by Morgan.
- Morgan's spouse Riley performs 750 documented hours of bookkeeping and
  operations work during 2026.
- Comparable hourly rates are $28, $30, and $34; use the median.
- The proposed cash wage is $48,000, but pay must be reasonable for services.
- The corporation pays $12,000 of qualifying health-insurance premiums for
  Riley under an arrangement satisfying the supplied reporting assumptions.
- For this task, Morgan's ownership is attributed to Riley, making Riley a
  more-than-2% S corporation shareholder for the health-premium analysis.
- Use 7.65% for both employee and employer FICA. Estimate FUTA at 0.6% on the
  first $7,000 after full state-credit assumptions.
- Ignore state payroll taxes and income-tax withholding amounts, but identify
  them as implementation requirements.
""",
        "inputs": [
            ["item", "value"],
            ["Documented hours", "750"],
            ["Comparable hourly rate 1", "28"],
            ["Comparable hourly rate 2", "30"],
            ["Comparable hourly rate 3", "34"],
            ["Proposed cash wage", "48000"],
            ["Health premiums", "12000"],
            ["Employee FICA rate", "0.0765"],
            ["Employer FICA rate", "0.0765"],
            ["FUTA effective rate", "0.006"],
            ["FUTA wage base", "7000"],
        ],
        "guidance": guidance(
            (
                "IRS family employees",
                """Corporate wages paid to a spouse are generally subject to federal
income-tax withholding, Social Security and Medicare taxes, and FUTA. The
special sole-proprietor spouse rule does not remove corporate payroll taxes.
https://www.irs.gov/businesses/small-businesses-self-employed/family-employees""",
            ),
            (
                "IRS S corporation compensation and medical insurance",
                """Health premiums paid for a more-than-2% shareholder-employee are
generally included in Form W-2 Box 1 but not Boxes 3 and 5 when the stated
requirements are satisfied.
https://www.irs.gov/businesses/small-businesses-self-employed/s-corporation-compensation-and-medical-insurance-issues
https://www.irs.gov/irb/2008-02_IRB""",
            ),
            (
                "IRS Publication 15",
                """Use current payroll deposit, reporting, withholding, and Form W-2
procedures for implementation.
https://www.irs.gov/publications/p15""",
            ),
        ),
        "expected": """\
# Output expectations

- Median market rate: **$30 per hour**.
- Reasonable modeled cash wages: 750 × $30 = **$22,500**; reject unsupported
  $48,000 compensation.
- Employee FICA: **$1,721.25**; employer FICA: **$1,721.25**.
- Estimated FUTA with full credit: **$42.00**.
- With $12,000 qualifying health premiums, modeled Form W-2 Box 1 is
  **$34,500**, while Boxes 3 and 5 remain **$22,500** under the supplied
  assumptions.

The workbook should include `Reasonable Pay`, `Payroll Budget`, `W-2 Mapping`,
and `Sources & Assumptions` sheets.
""",
        "rubric": rubric(
            (20, "Uses the $30 median and 750 hours to calculate $22,500 supportable wages and rejects unsupported $48,000 pay."),
            (20, "Correctly identifies corporate wages as subject to FIT/FICA/FUTA and calculates $1,721.25 employee and employer FICA."),
            (15, "Calculates estimated FUTA as $42 under the stated full-credit assumption."),
            (25, "Maps $12,000 health premiums to modeled Box 1 of $34,500 and Boxes 3/5 of $22,500, with more-than-2% shareholder caveats."),
            (20, "Provides an auditable workbook and documentation, payroll, benefits, and reasonable-compensation implementation controls."),
        ),
    },
    {
        "id": "046-tax-augusta-rule-execution",
        "title": "Document a Section 280A(g) Home-Rental Arrangement",
        "domain": "tax-business-expense-planning",
        "work_type": "tax-advisory-memo-and-recordkeeping-model",
        "manual_pages": [28],
        "deliverables": ["augusta_rule_execution_memo.md", "rental_event_log.xlsx"],
        "license": (
            "Original task design and synthetic client facts under repository MIT license; "
            "dated factual asking-rate observations are attributed to their public listing "
            "pages and those pages are not redistributed; United States government guidance "
            "is cited by URL; the confidential methodology manual is not included"
        ),
        "facts_provenance": (
            "Synthetic taxpayer and meeting facts; dated Chicago asking-rate observations "
            "derived from public listing pages cited in calculation_inputs.csv"
        ),
        "source_description": """\
The taxpayer and residence facts are synthetic. `calculation_inputs.csv`
contains dated factual asking-rate observations from the linked Chicago
listing pages; the linked pages themselves are not redistributed. The official
guidance links freeze the evaluation's 2026 federal-law answer contract.""",
        "assignment": """\
Evaluate a proposed company rental of an owner's residence for documented
business meetings. Establish a supportable daily rate, calculate the annual
payment, explain the distinct owner and company tax analyses, and build a
contemporaneous event-and-documentation log.""",
        "facts": """\
# Synthetic client facts — Willow Strategy Inc., Chicago

- Willow Strategy Inc. is an S corporation legally separate from owner Taylor.
- Taylor's residence is in Chicago's West Loop. The taxpayer and residence are
  fictional; no actual home address is supplied.
- Taylor's residence is not otherwise rented during 2026.
- The company proposes 14 one-day leadership and client-planning meetings at
  the residence in 2026. Each meeting runs from 9:00 a.m. to 5:00 p.m., has
  eight attendees, and has a documented business agenda.
- The proposed rate is $1,800 per day.
- `calculation_inputs.csv` contains five real, publicly listed Chicago
  meeting-space asking rates retrieved on July 27, 2026. Use the median
  normalized eight-hour daily rate as the frozen planning benchmark.
- Treat the listings as dated asking-rate evidence, not proof of completed
  arm's-length transactions. Discuss comparability, taxes, booking fees,
  amenities, capacity, and the need to refresh quotes before implementation.
- The company will execute a written rental agreement, approve the arrangement
  through disinterested corporate action where possible, invoice each event,
  and pay from the corporate account.
- No overnight lodging, personal entertainment, or mixed personal event is
  included. State and local lodging or sales taxes are outside this evaluation.
""",
        "inputs": [
            [
                "comparable_id",
                "venue",
                "chicago_location",
                "capacity",
                "listed_rate",
                "normalization",
                "normalized_day_rate_usd",
                "retrieved_on",
                "source_url",
            ],
            [
                "CHI-01",
                "Large Focus Room Located On Michigan Avenue",
                "Near North Side / North Michigan Avenue",
                "8",
                "$40/hour with 10% discount for 8+ hours",
                "$40 x 8 hours x 90%",
                "288",
                "2026-07-27",
                "https://www.peerspace.com/pages/listings/57a0c3d8abe58d09009f4ca2",
            ],
            [
                "CHI-02",
                "VC Studio — Regus West Loop Riverside Plaza Center",
                "West Loop / Riverside Plaza",
                "6",
                "from $363/day",
                "Direct listed day rate",
                "363",
                "2026-07-27",
                "https://book.workin.space/en/united-states/chicago/meeting-room",
            ],
            [
                "CHI-03",
                "Small Boardroom — Regus 125 South Wacker",
                "125 South Wacker Drive",
                "8",
                "from $385/day",
                "Direct listed day rate",
                "385",
                "2026-07-27",
                "https://book.workin.space/en/united-states/chicago/meeting-room",
            ],
            [
                "CHI-04",
                "MR-15B — Spaces 1 North State Street",
                "1 North State Street",
                "8",
                "from $553/day",
                "Direct listed day rate",
                "553",
                "2026-07-27",
                "https://book.workin.space/en/united-states/chicago/meeting-room",
            ],
            [
                "CHI-05",
                "MR03 — Signature 110 North Wacker Drive",
                "110 North Wacker Drive",
                "8",
                "from $754/day",
                "Direct listed day rate",
                "754",
                "2026-07-27",
                "https://book.workin.space/en/united-states/chicago/meeting-room",
            ],
        ],
        "guidance": guidance(
            (
                "Internal Revenue Code section 280A(g)",
                """When a dwelling unit used as a residence is rented for fewer than
15 days during the taxable year, rental income is excluded from gross income
and rental-use deductions are not allowed.
https://uscode.house.gov/view.xhtml?edition=prelim&num=0&req=granuleid%3AUSC-prelim-title26-section280A""",
            ),
            (
                "IRS Publication 527",
                """The publication describes the fewer-than-15-days rule for a home
used as a residence and related reporting treatment.
https://www.irs.gov/publications/p527""",
            ),
            (
                "Internal Revenue Code section 162",
                """The company's deduction is a separate question: an expense must be
ordinary and necessary, and compensation-like or related-party amounts require
particular support for business purpose and reasonableness.
https://uscode.house.gov/view.xhtml?edition=prelim&num=0&req=granuleid%3AUSC-prelim-title26-section162""",
            ),
        ),
        "expected": """\
# Output expectations

- Sort the normalized Chicago asking rates as $288, $363, $385, $553, and
  $754. Use the median of **$385 per day**, not the unsupported $1,800.
- Total modeled rent: 14 × $385 = **$5,390**.
- Identify that these are dated public asking rates with differing amenities
  and one six-person room. Recommend refreshed, saved quotes and documented
  adjustments before using the benchmark for an actual related-party payment.
- Under the supplied facts, the owner-side section 280A(g) analysis excludes
  the rental income and disallows rental-use deductions.
- Treat the corporation's section 162 deduction as a separate, conditional
  analysis requiring actual business purpose, reasonable rate, corporate
  approval, invoices, proof of payment, agendas, attendees, and no 15th day.

The workbook should include `Rate Support`, `Event Log`, `Payment Register`,
`Annual Test`, and `Sources & Assumptions` sheets.
""",
        "rubric": rubric(
            (20, "Preserves all five dated Chicago listing observations, normalizes the Peerspace rate to $288, and calculates the $385 median."),
            (20, "Rejects the unsupported $1,800 rate, calculates total modeled rent as $5,390 for exactly 14 days, and includes a formula-driven annual day-count control."),
            (20, "Correctly states the owner-side section 280A(g) income exclusion and rental-deduction prohibition under the facts."),
            (20, "Keeps the company's section 162 analysis separate and conditional on business purpose and reasonable, substantiated related-party pricing, while explaining asking-rate and comparability limitations."),
            (20, "Creates an auditable event log and implementation checklist covering agreement, approval, invoices, payments, agendas, attendees, refreshed listing evidence, adjustments, and Chicago/state/local review."),
        ),
    },
    {
        "id": "047-tax-hsa-optimization",
        "title": "Model HSA Eligibility and Funding Choices",
        "domain": "tax-health-benefits",
        "work_type": "tax-advisory-memo-and-model",
        "manual_pages": [213],
        "deliverables": ["hsa_eligibility_funding_memo.md", "hsa_contribution_schedule.xlsx"],
        "assignment": """\
Determine a family's month-by-month 2026 HSA eligibility, calculate both the
prorated contribution and the optional last-month-rule amount, quantify the
remaining employee funding after employer contributions, and evaluate a
documented dental reimbursement.""",
        "facts": """\
# Synthetic client facts — Chen family

- Taxpayer Lee, age 56 at year-end 2026, has family HDHP coverage for all of 2026.
- The 2026 plan deductible is $3,600 family and maximum out-of-pocket is $16,500.
- Lee's spouse has a general-purpose health FSA that covers Lee from January 1
  through June 30, 2026. It has no grace period or carryover and ends June 30.
- No other disqualifying coverage applies July through December.
- Employer HSA contributions for 2026 total $2,000.
- Lee is HSA-eligible on December 1, 2026 and is considering the last-month rule.
- Apply a December 31, 2027 testing-period end for this evaluation and describe
  the income inclusion and 10% additional-tax risk if the test is failed.
- Lee incurred and paid $3,200 of unreimbursed dental work in September 2026,
  after the HSA was established. No deduction or other reimbursement is claimed.
""",
        "inputs": [
            ["input", "value"],
            ["2026 family HSA limit", "8750"],
            ["Age-55 catch-up", "1000"],
            ["Eligible months", "6"],
            ["Months in year", "12"],
            ["Employer contribution", "2000"],
            ["Family HDHP minimum deductible", "3400"],
            ["Family HDHP maximum out-of-pocket", "17000"],
            ["Client deductible", "3600"],
            ["Client maximum out-of-pocket", "16500"],
            ["Dental expense", "3200"],
        ],
        "guidance": guidance(
            (
                "Revenue Procedure 2025-19 — 2026 HSA figures",
                """For 2026 the family HSA contribution limit is $8,750. A family
HDHP must have at least a $3,400 deductible and no more than $17,000 maximum
out-of-pocket exposure.
https://www.irs.gov/irb/2025-21_IRB""",
            ),
            (
                "IRS Publication 969",
                """General-purpose health FSA coverage can disqualify an individual
from HSA contributions. Eligibility is generally tested monthly. The
last-month rule may allow a full-year amount but creates a testing period and
income-inclusion/additional-tax consequences if eligibility is not maintained.
Employer contributions count against the annual limit.
https://www.irs.gov/publications/p969""",
            ),
            (
                "IRS Notice 2026-5",
                """Review current statutory changes affecting HDHP and HSA
eligibility before implementation.
https://www.irs.gov/irb/2026-02_IRB""",
            ),
        ),
        "expected": """\
# Output expectations

- The supplied plan satisfies the 2026 family HDHP deductible and out-of-pocket
  thresholds.
- The general-purpose FSA makes Lee ineligible January–June and eligible
  July–December: **6 eligible months**.
- Prorated contribution limit including catch-up:
  ($8,750 + $1,000) × 6/12 = **$4,875**; after $2,000 employer funding,
  remaining employee capacity is **$2,875**.
- Last-month-rule alternative: **$9,750** total and **$7,750** remaining after
  employer funding, with testing through December 31, 2027 and explicit
  income-inclusion/10% additional-tax risk.
- The $3,200 September dental expense is potentially a qualified, tax-free HSA
  reimbursement because it arose after establishment, subject to records and
  no double benefit.

The workbook should include `Monthly Eligibility`, `Contribution Options`,
`Expense Review`, and `Sources & Assumptions` sheets.
""",
        "rubric": rubric(
            (20, "Confirms the supplied $3,600 deductible and $16,500 out-of-pocket maximum satisfy the 2026 family HDHP thresholds."),
            (20, "Correctly marks January–June ineligible and July–December eligible because of the general-purpose FSA."),
            (20, "Calculates a $4,875 prorated limit and $2,875 remaining employee capacity after the $2,000 employer contribution."),
            (20, "Calculates the $9,750 last-month-rule alternative and $7,750 remaining, with the December 31, 2027 testing period and 10% risk."),
            (20, "Treats the $3,200 dental expense as potentially qualified with no-double-benefit records and provides an auditable formula-driven workbook."),
        ),
    },
]


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerows(rows)


def build_task(spec: dict[str, Any]) -> None:
    task_dir = TASKS_DIR / spec["id"]
    source_dir = task_dir / "source_docs"
    source_dir.mkdir(parents=True, exist_ok=True)

    if "source_description" in spec:
        source_section = (
            "Read every file in `source_docs/`.\n\n"
            + spec["source_description"].strip()
        )
    else:
        source_section = """Read every file in `source_docs/`. The client packet is synthetic. The official
guidance links identify the governing public sources used to freeze this
evaluation's 2026 answer contract."""
    prompt = f"""# {spec["title"]}

## Assignment

{spec["assignment"].strip()}

{COMMON_PROMPT}

## Source documents

{source_section}

## Expected deliverables

""" + "\n".join(f"- `{name}`" for name in spec["deliverables"]) + "\n"
    (task_dir / "prompt.md").write_text(prompt, encoding="utf-8")

    task = {
        "id": spec["id"],
        "title": spec["title"],
        "domain": spec["domain"],
        "work_type": spec["work_type"],
        "dataset": DATASET,
        "upstream_id": f"original/{spec['id']}",
        "upstream_url": "https://www.irs.gov/",
        "license": spec.get("license", LICENSE),
        "prompt": "prompt.md",
        "source_docs": "source_docs",
        "deliverables": spec["deliverables"],
        "rubric": "rubric.json",
        "tax_strategy_config": "tax_strategy.json",
    }
    write_json(task_dir / "task.json", task)
    write_json(task_dir / "rubric.json", spec["rubric"])
    write_json(
        task_dir / "tax_strategy.json",
        {
            "schema_version": 1,
            "effective_tax_year": 2026,
            "jurisdiction": "United States federal",
            "manual_method_reference": {
                "title": "Tax Strategy Execution Manual",
                "edition": "July 2026",
                "pages_consulted": spec["manual_pages"],
                "sha256": MANUAL_SHA256,
                "confidential_manual_redistributed": False,
            },
            "blind_run": {
                "agent_visible": ["prompt.md", "task.json", "tax_strategy.json", "source_docs/"],
                "grader_hidden": ["rubric.json", "answer_key.md"],
            },
            "output": {"required_files": spec["deliverables"]},
        },
    )
    write_json(
        task_dir / "upstream_task.json",
        {
            "type": "original_public_safe_derivative",
            "method_reference": "User-supplied Tax Strategy Execution Manual, July 2026",
            "method_reference_sha256": MANUAL_SHA256,
            "method_reference_pages": spec["manual_pages"],
            "confidential_source_included": False,
            "facts": spec.get("facts_provenance", "Synthetic and original"),
            "law_sources": "Official IRS, DOL, and U.S. Code links in source_docs/official_guidance.md",
        },
    )
    (source_dir / "client_facts.md").write_text(spec["facts"].strip() + "\n", encoding="utf-8")
    (source_dir / "official_guidance.md").write_text(spec["guidance"].strip() + "\n", encoding="utf-8")
    (task_dir / "answer_key.md").write_text(spec["expected"].strip() + "\n", encoding="utf-8")
    write_csv(source_dir / "calculation_inputs.csv", spec["inputs"])


def main() -> int:
    for spec in TASKS:
        build_task(spec)
    print(f"Built {len(TASKS)} tax strategy task packets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
