# Grader answer key — 057-apex-accounting-ar-reconciliation

Keep this file hidden from the agent during a blind run.

## Upstream expert response

AR Reconciliation, Clio to QBO - December 31, 2024

Total AR comparison: The correct QBO AR balance is $1,729,138.00 per the General Ledger account 1100 ending balance. The Clio outstanding balance per the billing export is also $1,729,138.00, so the total-level variance is $0.00. The AR Aging Summary shows $1,729,013.00, which is $125.00 low due to the Bayshore subledger error noted below.

Matter-level variance evaluation:
Bayshore (M-2024-0005): The $125.00 difference is an aging subledger error, not a real AR discrepancy. Clio and the General Ledger agree. The correct QBO AR for Bayshore is $23,818.10.
Northbridge (M-2024-0009): The draft variance of $8,773.31 is incorrect. The IOLTA payment is already reflected in the aging, so deducting it again double counts. The correct QBO AR for Northbridge is $22,010.66.
Cascade Foods (M-2024-0020): The draft variance of $7,059.28 is a draft error. The Clio balance already reflects the INV-2024-0232 write-down, so no processing lag exists. The correct QBO AR for Cascade Foods is $77,588.63.

December write-down and write-off totals: The draft's combined $126,770.82 includes one misclassified item. Hartwell Construction INV-2024-0226 $897.44 is a write-off misclassified as a write-down. The correct December write-down total is $125,873.38 and the correct December write-off total is $897.44.

Final reconciliation result: After correcting the draft errors, Clio at $1,729,138.00 and QBO at $1,729,138.00 reconcile with a variance of $0.00.
