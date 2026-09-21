# POS Agent Cash-Out: The Machine That Must Never Crash

A Python exception-handling assignment for the Python Advanced cohort at NITDA.

## The Story

Mama Ngozi runs a POS (agent-banking) stand in Aba. Every morning she loads
her machine with a cash float, and customers come to withdraw money from
their accounts. Some requests are messy: bad amounts, missing information,
or more cash than the customer's balance or the machine's float can cover.

This program processes a queue of cash-out requests and makes sure the
machine never crashes, no matter how broken a request is. Every bad request
is rejected with a clear reason, and the machine moves on to the next
customer.

## What It Does

- Validates each request's amount (must be a number, positive, and a
  multiple of ₦100).
- Checks the customer's account balance and the agent's cash float.
- Charges a POS fee on successful cash-outs.
- Uses custom exceptions (`TransactionError`, `InsufficientFundsError`) to
  model business rules.
- Uses `try` / `except` / `else` / `finally` to process each request safely.
- Prints an end-of-day summary: successful cash-outs, failed cash-outs, and
  the final float.

## Running It
