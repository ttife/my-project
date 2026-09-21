"""
POS Agent Cash-Out — Exception Handling Assignment
Python Advanced Cohort 35

You are writing the software for a neighbourhood POS (agent-banking) machine
in Nigeria. Customers walk up to withdraw cash. The machine processes a queue
of cash-out requests against the agent's float (cash on hand) and each
customer's account balance.

THE GOLDEN RULE: the machine must NEVER crash, no matter how broken a request
is. Every bad request should be rejected with a clear reason, and the machine
should move on to the next customer.

This assignment is PURE exception handling — no files, no regex, no internet.

------------------------------------------------------------------------------
TODO SUMMARY (details are in the docstrings and comments below):
  TODO 1: Define the custom exceptions TransactionError and
          InsufficientFundsError.
  TODO 2: validate_amount()   -> convert + check positive + check multiple of 100
  TODO 3: check_balance()     -> raise InsufficientFundsError if too poor
  TODO 4: check_agent_float() -> raise TransactionError if agent can't pay
  TODO 5: charge_fee()        -> compute the POS fee (integer division)
  TODO 6: process_cashout()   -> try / except / else / finally orchestration
  TODO 7: main()              -> loop the queue, tally results, print summary
------------------------------------------------------------------------------
Run it any time with:  python starter.py
Right now it runs without crashing but does not do the real work yet.
"""

# ---------------------------------------------------------------------------
# No imports are needed for the exception-handling work itself — that is built
# into Python, which is the whole point! (You may add imports for stretch goals.)
#
# The two lines below just make sure the Naira symbol (₦) prints correctly on
# Windows terminals. You do not need to touch or understand them for this
# assignment — leave them as they are.
# ---------------------------------------------------------------------------
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass  # older Pythons / unusual terminals: safe to ignore


# ---------------------------------------------------------------------------
# EMBEDDED DATA
# This is the queue of cash-out requests waiting at the POS stand.
# It is DELIBERATELY messy — several entries are broken so your exception
# handling has something to catch. Do NOT "fix" the data; fix your code so it
# survives the data.
#
# Each request is a dict with: customer, phone, amount, account_balance.
# (One entry is intentionally missing a key — that is on purpose!)
# ---------------------------------------------------------------------------
CASHOUT_REQUESTS = [
    {"customer": "Chinedu Okafor", "phone": "08031234567", "amount": 5000,  "account_balance": 20000},
    {"customer": "Aisha Bello",    "phone": "07061234567", "amount": "five thousand", "account_balance": 15000},
    {"customer": "Emeka Nwosu",    "phone": "08101234567", "amount": 40000, "account_balance": 2000},
    {"customer": "Fatima Sani",    "phone": "09021234567", "amount": 2550,  "account_balance": 30000},
    {"customer": "Tunde Adeyemi",  "phone": "08051234567", "amount": 75000, "account_balance": 90000},
    {"customer": "Blessing Eze",   "phone": "07031234567", "amount": 10000, "account_balance": 50000},
    {"customer": "Unknown Customer","phone": "08099887766", "amount": 3000},  # <-- missing "account_balance"!
    {"customer": "Ibrahim Musa",   "phone": "08122334455", "amount": -3000, "account_balance": 10000},
    {"customer": "Ngozi Uche",     "phone": "09033445566", "amount": 0,     "account_balance": 8000},
]

# The note denominations the POS can dispense. Any amount must be a multiple
# of the smallest note (₦100).
NOTE_UNIT = 100

# The float Mama Ngozi loads into the machine at the start of the day.
OPENING_FLOAT = 50000


# ---------------------------------------------------------------------------
# TODO 1: CUSTOM EXCEPTIONS
# ---------------------------------------------------------------------------
class TransactionError(Exception):
    pass  # TODO: nothing more is needed here, but keep this class.
class InsufficientFundsError(TransactionError):
    pass  # TODO: keep this class; it should inherit from TransactionError.

# ---------------------------------------------------------------------------
# TODO 2: VALIDATE THE AMOUNT
# ---------------------------------------------------------------------------
def validate_amount(amount):
    try:
        number = int(amount)
    except (TypeError, ValueError):
        raise TransactionError ("Amount is not a number")

    if number <= 0:
        raise TransactionError("Amount is zero or negative")
    if number % NOTE_UNIT != 0:
        raise TransactionError("Amount must be a multiple of ₦100")

    return number

# ---------------------------------------------------------------------------
# TODO 3: CHECK THE CUSTOMER'S ACCOUNT BALANCE
# ---------------------------------------------------------------------------
def check_balance(amount, account_balance):
    if account_balance < amount:
        raise InsufficientFundsError("Your account balance is low")

# ---------------------------------------------------------------------------
# TODO 4: CHECK THE AGENT'S FLOAT (CASH ON HAND)
# ---------------------------------------------------------------------------
def check_agent_float(amount, agent_float):
    if agent_float < amount:
        raise TransactionError("Funds in the machine not enough for transaction")

# ---------------------------------------------------------------------------
# TODO 5: CHARGE THE POS FEE
# ---------------------------------------------------------------------------
def charge_fee(amount):
    return (amount // 5000) * 100

# ---------------------------------------------------------------------------
# TODO 6: PROCESS ONE CASH-OUT (the heart of the assignment)
# ---------------------------------------------------------------------------
def process_cashout(request, agent_float):
    new_float = agent_float
    try:
        amount = validate_amount(request["amount"])
        balance = request["account_balance"]
        check_balance(amount, balance)
        check_agent_float(amount, agent_float)
    except TransactionError as error:
        print("Rejected:", error)
    except KeyError as missing:
        print("Rejected: the form is missing", missing)
    except Exception as unexpected:
        print("Rejected: unexpected problem -", unexpected)
    else:
        fee = charge_fee(amount)
        new_float = agent_float - amount
        print("Approved, Fee:", fee, "Paid:", amount, "Float left:", new_float)
        
    finally:
        print("--- transaction ended ---")
    return new_float

# ---------------------------------------------------------------------------
# TODO 7: MAIN — run the whole day
# ---------------------------------------------------------------------------
def main():
    agent_float = OPENING_FLOAT

    print("====== MAMA NGOZI POS TERMINAL ======")
    print(f"Opening float: ₦{agent_float:,}")
    print()

    successes = 0
    failures = 0
    for request in CASHOUT_REQUESTS:
        name = request.get("customer", "Unknown")
        phone = request.get("phone", "")
        print(f"Processing cash-out for {name} ({phone})...")

        old_float = agent_float
        agent_float = process_cashout(request, agent_float)
        if agent_float != old_float:
            successes += 1
        else:
            failures += 1
        print()

    print("============ END OF DAY ============")
    print(f"Successful cash-outs: {successes}")
    print(f"Failed cash-outs:     {failures}")
    print(f"Final float: ₦{agent_float:,}")


if __name__ == "__main__":
    main()
