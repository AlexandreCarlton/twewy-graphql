# twewy-graphql
A [GraphQL](https://graphql.org/) endpoint for data from The World Ends With You.

> :warning: This is a very rough work in progress!

All data is scraped from [The World Ends with You Wiki](http://twewy.fandom.com/).

To start the endpoint:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

./main.py
```

A GraphiQL endpoint will be available on http://localhost:5000/graphql.
