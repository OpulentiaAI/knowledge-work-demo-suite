# Sales packet data dictionary

`daily_store_metrics.csv` contains one row per store and date. Sales and profit are USD. `Payment Net Sales` covers payment line items; `Refund Net Sales` is negative; `Net Sales After Refunds` combines both. `Discounts` is negative in the source export, so `Discount Rate` is shown as a positive share. A transaction is counted once per payment transaction ID.

`target_store_category_metrics.csv` contains payment-only metrics by category for the named target store. `retail_calendar.csv` provides calendar context, not causal proof.
