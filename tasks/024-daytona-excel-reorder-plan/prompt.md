# Build a Store Reorder Plan

## Assignment

You are the inventory planner for Cedar Corner Market. Use the source documents to create `reorder_plan.xlsx` for the next supplier order.

Create a workbook with a `Reorder Plan` sheet. For every SKU, include the on-hand units, average daily units, safety stock, target stock, case pack, a recommended order quantity, and a clear priority. Calculate recommended quantity as the amount needed to reach target stock, rounded **up** to a whole case pack. Mark an item `Urgent` when its on-hand quantity is below safety stock; otherwise mark it `Routine`. Sort urgent items before routine items, then by recommended quantity descending.

Include a short `Notes` sheet naming the two urgent SKUs and the order-quantity rule. Preserve formulas for the recommended quantity and priority rather than typing derived values.

## Source documents

Read every file in `source_docs/`. They are the authoritative workspace.

## Expected deliverable

- `reorder_plan.xlsx`
