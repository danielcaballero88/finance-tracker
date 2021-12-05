# Finance Tracker

A simple app for personal finance tracking: income, expenses, investments, etc.

## Road Map

1. Backend using FastAPI.
   - Use some mock-up DB like `json-server`.
2. Frontend using Angular add a nice UI.
   - Just a web app is fine at first, no need for a mobile app yet.
   - Let's try to aim for mobile screen size and make responsive for laptop.
3. Data model using MongoDB.
   - Each account should have their own income and expenses.
   - Some users might want to share data, so that can mean shared accounts, or
   separate accounts with shared aggregation.
   - Eventually add accountability between different sub-accounts (e.g., one
   account can be splitted between several banks, or include equity, idk, have
   to research about accountability for this).
