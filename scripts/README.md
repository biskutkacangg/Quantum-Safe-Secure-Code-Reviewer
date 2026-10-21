# Automation & Report Generation Scripts
**Project:** *Design and Development of a Post-Quantum Cryptography-Based Secure Code Review Tool*

This directory houses the automated PDF compilers for the active project deliverables. Each script uses headless Microsoft Edge to render pixel-perfect vector PDFs directly into [`reports/`](../reports) and automatically synchronizes a copy to the user's `Downloads` directory.

---

## ⚡ Active Scripts

| Script | Command | Output PDF |
| :--- | :--- | :--- |
| **`generate_all_reports.py`** | `python scripts/generate_all_reports.py` | **1-Click Master Builder:** Compiles all 7 active deliverables serially. |
| **`generate_proposal_pdf.py`** | `python scripts/generate_proposal_pdf.py` | `reports/Agentic_AI_Cyber_Defence_Proposal_Quantum_Safe_Reviewer.pdf`<br/>*(Official Hackathon Proposal & Technical Summary — 2-Page A4)* |
| **`generate_framework_and_architecture_pdf.py`** | `python scripts/generate_framework_and_architecture_pdf.py` | `reports/System_Framework_and_Architecture_Dossier.pdf`<br/>*(System Framework & Multi-Agent Architecture Technical Dossier — 2-Page A4)* |
| **`generate_pitch_deck_pdf.py`** | `python scripts/generate_pitch_deck_pdf.py` | `reports/Pitch_Deck_and_Presentation_Script_Quantum_Safe_Reviewer.pdf`<br/>*(Executive Pitch Deck — 6-Slide Widescreen A4 Landscape)* |
| **`generate_poster_pdf.py`** | `python scripts/generate_poster_pdf.py` | `reports/Digital_Poster_Quantum_Safe_Agent.pdf`<br/>*(High-Impact Digital Showcase Poster)* |
| **`generate_papers_comparison_pdf.py`** | `python scripts/generate_papers_comparison_pdf.py` | `reports/PQC_Model_Parameters_and_Results_Paper_Comparison.pdf`<br/>*(Literature Review & SOTA Empirical Benchmark against SECRYPT 2025)* |
| **`generate_catalog_pdf.py`** | `python scripts/generate_catalog_pdf.py` | `reports/PQC_Vulnerabilities_and_Replacements_Catalog.pdf`<br/>*(Complete Inventory of Deprecated Algorithms & NIST FIPS 203/204 Targets)* |
| **`generate_lecturer_presentation_pdf.py`** | `python scripts/generate_lecturer_presentation_pdf.py` | `reports/Lecturer_Presentation_PQC_System_Architecture_and_AST_DeepDive.pdf`<br/>*(Master Academic Presentation Slide Deck: AST Tree & Compiler Architecture — 9-Slide A4 Landscape, Canva-Ready)* |
| **`generate_presentation_script_companion_pdf.py`** | `python scripts/generate_presentation_script_companion_pdf.py` | `reports/Lecturer_Presentation_Master_Script_and_Companion_Guide.pdf`<br/>*(Master Spoken Script, Compiler Deep-Dive & Academic Defence Guide — A4 Portrait)* |
| **`generate_nota_ringkas_pdf.py`** | `python scripts/generate_nota_ringkas_pdf.py` | `reports/NOTA_RINGKAS_ALL_TERMS_AND_CODING.pdf`<br/>*(NOTA RINGKAS ALL TERMS AND CODING — A4 Portrait Master Study Companion)* |
