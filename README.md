# freelance-expense-cli

![Test CLI](https://github.com/kleogeos/freelance-expense-cli/actions/workflows/test.yml/badge.svg)
Track business expenses for tax reporting. No dependencies, no sign-up, no cloud account — just a local JSON file you can commit, back up, or diff.

```bash
python3 expense.py add 49.99 software --note "Figma subscription"
python3 expense.py add 120 equipment --note "monitor" --date 2026-09-15
python3 expense.py report --from-date 2026-01-01 --to-date 2026-12-31
```

```
equipment                  120.00
software                    65.49
----------------------------------
TOTAL                      185.49
```

### Install (optional)

```bash
pip install git+https://github.com/kleogeos/freelance-expense-cli
freelance-expense add 49.99 software
```

### Commands

| Command | What it does |
|---|---|
| `add AMOUNT CATEGORY [--date YYYY-MM-DD] [--note TEXT]` | Log an expense (date defaults to today) |
| `list [--category NAME] [--from-date DATE] [--to-date DATE]` | List logged expenses |
| `report [--from-date DATE] [--to-date DATE] [--json]` | Totals by category for a period, e.g. a tax quarter |
| `export-csv [--out FILE]` | Export everything to CSV for a bookkeeper or tax filing |

Global flag: `--file PATH` — use a different expenses file (default `expenses.json` in the current directory).

### Why a CLI instead of a spreadsheet or app

No account, no subscription, nothing phoning home. The expense log is a plain JSON file — script against it, diff it, or hand the CSV export to whoever does your taxes. Pairs with [freelance-time-cli](https://github.com/kleogeos/freelance-time-cli) for billable hours, [freelance-timesheet-to-invoice-cli](https://github.com/kleogeos/freelance-timesheet-to-invoice-cli) for turning those hours into an invoice.json, and [freelance-invoice-cli](https://github.com/kleogeos/freelance-invoice-cli) for rendering it.

If you're a Russian-speaking freelancer sorting out self-employment/IP tax status: [self-employment tax estimator](https://kleogeos.github.io/freelancer-tools/self-employment-tax-estimator.html) and the [RU crypto payments guide](https://kleogeos.github.io/freelancer-tools/kak-frilanseru-prinimat-kripto-oplatu.html) cover the related gotchas.

Free web tools (no install): [invoice generator](https://kleogeos.github.io/freelancer-tools/invoice.html) · [rate calculator](https://kleogeos.github.io/freelancer-tools/rate-calculator.html) · [contract checklist](https://kleogeos.github.io/freelancer-tools/contract-checklist.html)

Send the quote before the work starts: [freelance-proposal-cli](https://github.com/kleogeos/freelance-proposal-cli).

Need the paperwork beyond tracking — proposals, contracts, invoices, late-payment emails, client scripts? [Freelancer Starter Kit ($15, Telegram Stars or crypto, no KYC)](https://kleogeos.github.io/freelancer-tools/kit.html?src=cli-expense)

Free and will stay free. If it saved you time: [tip with crypto](https://kleogeos.github.io/freelancer-tools/donate.html).

## License

MIT — do whatever you want with it.
