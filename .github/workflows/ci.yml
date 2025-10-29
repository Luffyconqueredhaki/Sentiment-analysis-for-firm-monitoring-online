name: Pipeline CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      # 1. Scarica il codice
      - name: Check out repository
        uses: actions/checkout@v4

      # 2. Installa Python
      - name: Set up Python 3.10
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      # 3. Installa le librerie
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # 4. Esegue i test
      - name: Run tests
        run: |
          python -m pytest tests/
