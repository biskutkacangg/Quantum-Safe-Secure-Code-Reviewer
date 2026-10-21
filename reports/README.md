# Research Deliverables & PDF Reports Catalog
**Project:** *Design and Development of a Post-Quantum Cryptography-Based Secure Code Review Tool*

This directory houses the official, publication-grade research reports and technical catalogs for the project.

> **Directory Cleanliness:**  
> All finalized PDF deliverables are located directly in this directory for immediate 1-click access. All HTML rendering source templates are kept in [`html/`](./html) to maintain a clutter-free structure.

---

## 📚 Active Research Deliverables

| Document | Format & Length | Subtitle / Primary Focus |
| :--- | :--- | :--- |
| **[Agentic_AI_Cyber_Defence_Proposal_Quantum_Safe_Reviewer.pdf](./Agentic_AI_Cyber_Defence_Proposal_Quantum_Safe_Reviewer.pdf)** | **2 Pages (A4) [REQUIRED]** | **Official Hackathon Proposal & Technical Summary**<br/>*Comprehensive problem definition, target users, 5-node LangGraph architecture, data flow, safeguards, limitations, and implementation scope.* |
| **[System_Framework_and_Architecture_Dossier.pdf](./System_Framework_and_Architecture_Dossier.pdf)** | **2 Pages (A4 Academic)** | **Technical Dossier: System Framework & Multi-Agent Architecture**<br/>*Formal specification in English for Academic Supervisor / Dr. presentation covering the Hybrid Neuro-Symbolic paradigm, 4-tier model, and 5-node LangGraph pipeline.* |
| **[Pitch_Deck_and_Presentation_Script_Quantum_Safe_Reviewer.pdf](./Pitch_Deck_and_Presentation_Script_Quantum_Safe_Reviewer.pdf)** | **6 Slides (A4 Landscape)** | **Official Executive Pitch Deck**<br/>*High-impact visual story covering the post-quantum threat, 5-node LangGraph architecture, PQC CIA Triad, MTU packet bloat, Zero-Trust HITL, and SECRYPT 2025 benchmarks.* |
| **[Digital_Poster_Quantum_Safe_Agent.pdf](./Digital_Poster_Quantum_Safe_Agent.pdf)** | **1 Page (A4 Poster)** | **High-Impact Digital Showcase Poster**<br/>*Visual architectural showcase, key metrics, and agentic cyber defence workflow summary.* |
| **[Digital_Poster_Quantum_Safe_Agent.jpg](./Digital_Poster_Quantum_Safe_Agent.jpg)** | **High-Res Graphic (3:4)** | **Official Digital Showcase Poster Image**<br/>*Ready for upload under POC / Source code / Images.* |
| **[PQC_Model_Parameters_and_Results_Paper_Comparison.pdf](./PQC_Model_Parameters_and_Results_Paper_Comparison.pdf)** | **4 Pages (A4)** | **System Parameters, Empirical Benchmark Results & Literature Review (Google Scholar 2020–2025)**<br/>*Comprehensive comparative review matching our framework against 6 state-of-the-art papers (anchored by Masood & Vargas Martin, SECRYPT 2025).* |
| **[PQC_Vulnerabilities_and_Replacements_Catalog.pdf](./PQC_Vulnerabilities_and_Replacements_Catalog.pdf)** | **Full Reference (A4)** | **Complete Inventory of Deprecated Algorithms • NIST FIPS 203 / 204 Migration Targets**<br/>*Complete inventory of deprecated cryptographic algorithms and their recommended post-quantum replacements.* |
| **[Lecturer_Presentation_PQC_System_Architecture_and_AST_DeepDive.pdf](./Lecturer_Presentation_PQC_System_Architecture_and_AST_DeepDive.pdf)** | **9 Slides (A4 Landscape, Canva-Ready)** | **Master Academic Presentation Slide Deck: System Architecture, Compiler AST Tree & PQC Governance**<br/>*Tailored for academic supervisor / lecturer presentations and Canva editing. Features the 4 Compiler Phases, visual SVG inverted AST compiler tree, Python & Java comparative discovery, PQC MTU bloat, Zero-Trust HITL gate, and SHA-256 Merkle chain verification.* |
| **[Lecturer_Presentation_Master_Script_and_Companion_Guide.pdf](./Lecturer_Presentation_Master_Script_and_Companion_Guide.pdf)** | **6-9 Pages (A4 Portrait)** | **Master Spoken Script, Compiler Deep-Dive & Academic Defence Guide**<br/>*Complete study and review companion containing the word-for-word spoken scripts (Slides 1–9) with timing and delivery notes, compiler 4-stage pipeline, AST inverted tree anatomy, function-by-function code breakdown, PQC MTU bloat analysis, and lecturer Q&A cheat sheet.* |
| **[NOTA_RINGKAS_ALL_TERMS_AND_CODING.pdf](./NOTA_RINGKAS_ALL_TERMS_AND_CODING.pdf)** | **8 Pages (A4 Portrait)** | **NOTA RINGKAS ALL TERMS AND CODING**<br/>*Panduan ulang kaji komprehensif mengandungi nyahkod semua akronim A–Z, bedah siasat setiap fungsi kod (ast.parse, ast.NodeVisitor, visit_Call, ast.unparse, interrupt, _compute_chain_hash) dengan analogi mudah faham, teori pokok terbalik, analogi lori pos MTU bloat, dan skrip pertuturan santai.* |

---

## ⚡ How to Rebuild Deliverables

To re-compile these reports and automatically sync them to your `Downloads` folder, run:

```bash
python scripts/generate_all_reports.py
```
