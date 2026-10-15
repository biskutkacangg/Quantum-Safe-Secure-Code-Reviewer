# Automation & Report Generation Scripts
**Project:** *Design and Development of a Post-Quantum Cryptography-Based Secure Code Review Tool*

This directory houses the automated PDF compilers for the active project deliverables. Each script uses headless Microsoft Edge to render pixel-perfect vector PDFs directly into [`reports/`](../reports) and automatically synchronizes a copy to `C:\Users\User\Downloads\`.

---

## ⚡ Active Scripts

| Script | Command | Output PDF |
| :--- | :--- | :--- |
| **`generate_all_reports.py`** | `python scripts/generate_all_reports.py` | **1-Click Master Builder:** Compiles both active deliverables serially. |
| **`generate_papers_comparison_pdf.py`** | `python scripts/generate_papers_comparison_pdf.py` | `reports/PQC_Model_Parameters_and_Results_Paper_Comparison.pdf`<br/>*(System Parameters, Empirical Benchmark Results & Literature Review)* |
| **`generate_catalog_pdf.py`** | `python scripts/generate_catalog_pdf.py` | `reports/PQC_Vulnerabilities_and_Replacements_Catalog.pdf`<br/>*(Complete Inventory of Deprecated Algorithms • NIST FIPS 203 / 204 Migration Targets)* |
