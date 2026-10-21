# ============================================================
# scripts/generate_nota_ringkas_pdf.py
# Generates a publication-grade A4 Portrait Study Companion PDF:
# "NOTA RINGKAS ALL TERMS AND CODING"
# Project: Design and Development of a Post-Quantum Cryptography-Based Secure Code Review Tool
# Track 1: Agentic Cyber Defence (hackai.my)
# ============================================================

import re
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
WORKSPACE = SCRIPTS_DIR.parent
REPORTS_DIR = WORKSPACE / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
HTML_DIR = REPORTS_DIR / "html"
HTML_DIR.mkdir(parents=True, exist_ok=True)

HTML_FILE = HTML_DIR / "NOTA_RINGKAS_ALL_TERMS_AND_CODING.html"
PDF_FILE = REPORTS_DIR / "NOTA_RINGKAS_ALL_TERMS_AND_CODING.pdf"
DOWNLOADS_PDF = Path.home() / "Downloads" / "NOTA_RINGKAS_ALL_TERMS_AND_CODING.pdf"
EDGE_EXE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

MAIN_TITLE = "NOTA RINGKAS ALL TERMS AND CODING"
SUB_TITLE = "Panduan Ulang Kaji Komprehensif: Nyahkod Semua Akronim, Teori Compiler, Fungsi Kod & Analogi Mudah"

html_content = f"""<!DOCTYPE html>
<html lang="ms">
<head>
<meta charset="UTF-8">
<title>{MAIN_TITLE} — Panduan Ulang Kaji PQC</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    @page {{
        size: A4 portrait;
        margin: 10mm 12mm 10mm 12mm;
    }}

    * {{
        box-sizing: border-box;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }}

    body {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #0f172a;
        background: #ffffff;
        margin: 0;
        padding: 0;
        line-height: 1.5;
        font-size: 8.8pt;
    }}

    .page-break {{
        page-break-after: always;
    }}

    /* ── Header Bar ── */
    .header-bar {{
        border-bottom: 3.5px solid #4338ca;
        padding-bottom: 6px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }}

    .title-block h1 {{
        font-size: 16pt;
        color: #1e1b4b;
        margin: 0 0 2px 0;
        font-weight: 900;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }}

    .title-block .subtitle {{
        font-size: 8.8pt;
        color: #4338ca;
        font-weight: 700;
    }}

    .meta-box {{
        text-align: right;
        font-size: 7.5pt;
        color: #64748b;
        line-height: 1.35;
        white-space: nowrap;
    }}

    /* ── Badges ── */
    .badge-pill {{
        display: inline-block;
        font-size: 7.2pt;
        font-weight: 800;
        padding: 2px 8px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-right: 4px;
    }}
    .badge-blue {{ background: #e0e7ff; color: #3730a3; border: 1px solid #c7d2fe; }}
    .badge-cyan {{ background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }}
    .badge-green {{ background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }}
    .badge-rose {{ background: #ffe4e6; color: #9f1239; border: 1px solid #fecdd3; }}
    .badge-amber {{ background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }}

    /* ── Section Titles ── */
    .section-title {{
        font-size: 11pt;
        font-weight: 800;
        color: #1e1b4b;
        border-left: 4.5px solid #4f46e5;
        padding-left: 8px;
        margin: 14px 0 8px 0;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}

    /* ── Cards & Callouts ── */
    .card {{
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 10px;
        page-break-inside: avoid;
    }}

    .card-dark {{
        background: #0f172a;
        color: #f8fafc;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 10px;
        page-break-inside: avoid;
    }}

    .card-title {{
        font-size: 9.8pt;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 6px;
    }}

    .card-dark .card-title {{
        color: #38bdf8;
    }}

    .analogy-box {{
        background: #fefce8;
        border-left: 4px solid #eab308;
        border-radius: 0 6px 6px 0;
        padding: 6px 12px;
        font-size: 8.2pt;
        color: #713f12;
        margin: 6px 0;
        line-height: 1.45;
    }}

    .speech-box {{
        background: #eef2ff;
        border-left: 4px solid #4f46e5;
        border-radius: 0 8px 8px 0;
        padding: 10px 14px;
        margin: 8px 0 10px 0;
        font-size: 8.8pt;
        color: #1e1b4b;
        line-height: 1.55;
        page-break-inside: avoid;
    }}

    .speech-box em {{
        color: #4338ca;
        font-style: normal;
        font-weight: 700;
    }}

    /* ── Code Box ── */
    .code-box {{
        font-family: 'JetBrains Mono', Consolas, monospace;
        font-size: 7.8pt;
        background: #090e18;
        color: #e2e8f0;
        padding: 8px 12px;
        border-radius: 6px;
        border: 1px solid #1e293b;
        line-height: 1.45;
        margin: 6px 0;
        white-space: pre;
        page-break-inside: avoid;
    }}
    .code-kw {{ color: #f43f5e; font-weight: bold; }}
    .code-fn {{ color: #38bdf8; font-weight: bold; }}
    .code-str {{ color: #34d399; }}
    .code-cmt {{ color: #64748b; font-style: italic; }}

    /* ── Tables ── */
    table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 8pt;
        margin: 6px 0 10px 0;
        page-break-inside: avoid;
    }}

    th {{
        background: #1e1b4b;
        color: #ffffff;
        font-weight: 700;
        padding: 6px 9px;
        text-align: left;
        border: 1px solid #312e81;
    }}

    td {{
        padding: 5.5px 9px;
        border: 1px solid #cbd5e1;
        color: #334155;
        vertical-align: top;
        background: #ffffff;
    }}

    tr:nth-child(even) td {{
        background: #f8fafc;
    }}

    .grid-2col {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
    }}

    .footer {{
        border-top: 1px solid #cbd5e1;
        padding-top: 4px;
        margin-top: 10px;
        display: flex;
        justify-content: space-between;
        font-size: 7.2pt;
        color: #64748b;
    }}
</style>
</head>
<body>

<!-- ====================================================================== -->
<!-- PAGE 1: TITLE, GAMBARAN BESAR & KAMUS AKRONIM LENGKAP (A-J)            -->
<!-- ====================================================================== -->
<div class="header-bar">
    <div class="title-block">
        <h1>{MAIN_TITLE}</h1>
        <div class="subtitle">{SUB_TITLE}</div>
    </div>
    <div class="meta-box">
        <div><strong>Dokumen Rujukan:</strong> Pembentangan Penilai / Pensyarah</div>
        <div><strong>Track 1:</strong> Agentic Cyber Defence &bull; hackai.my</div>
        <div><strong>Format:</strong> A4 Master Study Reference</div>
    </div>
</div>

<div style="margin-bottom:10px;">
    <span class="badge-pill badge-blue">Kamus Akronim A–Z</span>
    <span class="badge-pill badge-green">Bedah Siasat Setiap Function</span>
    <span class="badge-pill badge-cyan">Analogi Orang Awam</span>
    <span class="badge-pill badge-rose">Teori Pokok Terbalik</span>
    <span class="badge-pill badge-amber">Skrip Pertuturan Santai</span>
</div>

<div class="section-title">BAHAGIAN 1: GAMBARAN BESAR (APA PROJEK KITA SEBENARNYA?)</div>

<div class="card" style="background:#f0fdf4; border-color:#bbf7d0;">
    <div class="card-title" style="color:#166534;">
        🩺 Analogi: "Doktor Pakar Imbasan X-Ray untuk Kod Komputer"
    </div>
    <p style="margin:0 0 6px 0; font-size:8.6pt; color:#14532d; line-height:1.5;">
        Bayangkan semua sistem perbankan, kata laluan kerajaan, dan laman web di dunia hari ini dikunci menggunakan <strong>"mangga kunci lama"</strong> bernama <strong>RSA</strong> dan <strong>ECC</strong>.
    </p>
    <ul style="margin:0; padding-left:18px; font-size:8.3pt; color:#166534;">
        <li><strong>Ancaman Masa Depan:</strong> Komputer Kuantum (*Quantum Computer*) bakal tiba. Komputer ini mempunyai formula matematik bernama <strong>Shor's Algorithm</strong> yang boleh memecahkan mangga kunci lama ini dalam beberapa saat sahaja!</li>
        <li><strong>Serangan HNDL (Curi Dulu, Pecah Nanti):</strong> Penjenayah siber sedang memuat turun data rahsia hari ini, simpan dalam storan mereka, dan tunggu komputer kuantum siap untuk membukanya.</li>
        <li><strong>Tugas Projek Kita:</strong> Sebelum diserang, perisian kita mengimbas kod sumber (*source code*) perisian lama, mengesan bahagian mana yang masih menggunakan mangga kunci purba, dan mencadangkan gantian mangga kebal kuantum terkini dunia (**NIST PQC FIPS 203 &amp; 204**) — dengan kawalan mutlak manusia (*Zero-Trust Human-in-the-Loop*).</li>
    </ul>
</div>

<div class="section-title">BAHAGIAN 2: KAMUS LENGKAP AKRONIM &amp; SINGKATAN (BAHAGIAN 1)</div>

<p style="margin:0 0 6px 0;">
    Setiap kali anda membentang, pensyarah suka menguji sama ada anda tahu maksud singkatan yang anda sebut. Jadual ini menyenaraikan maksud penuh dan huraian bahasa mudahnya:
</p>

<table>
    <thead>
        <tr>
            <th style="width:16%;">Akronim</th>
            <th style="width:34%;">Maksud Penuh *(Full Term)*</th>
            <th style="width:50%;">Penerangan Bahasa Mudah (Orang Awam Boleh Faham)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>PQC</strong></td>
            <td><em>Post-Quantum Cryptography</em></td>
            <td><strong>Kriptografi Kebal Kuantum.</strong> Kaedah kunci keselamatan baharu yang direka khas supaya komputer kuantum pun tidak mampu memecahkannya.</td>
        </tr>
        <tr>
            <td><strong>AST</strong></td>
            <td><em>Abstract Syntax Tree</em></td>
            <td><strong>Pokok Struktur Tatabahasa Kod.</strong> Susunan kod dalam bentuk pokok (Pangkal ➔ Dahan ➔ Daun) supaya komputer faham struktur hubungan kod.</td>
        </tr>
        <tr>
            <td><strong>SAST</strong></td>
            <td><em>Static Application Security Testing</em></td>
            <td><strong>Ujian Sekuriti Kod Statik.</strong> Mengimbas dan mencari kelemahan dalam baris teks kod <em>tanpa perlu menjalankan (run)</em> fail perisian tersebut.</td>
        </tr>
        <tr>
            <td><strong>CPU</strong></td>
            <td><em>Central Processing Unit</em></td>
            <td><strong>Otak Komputer.</strong> Cip pemproses elektronik utama dalam komputer yang hanya faham nombor perduaan <code>0</code> dan <code>1</code> (Bahasa Mesin).</td>
        </tr>
        <tr>
            <td><strong>PEG Parser</strong></td>
            <td><em>Parsing Expression Grammar Parser</em></td>
            <td><strong>Enjin Pembaca Tatabahasa Python.</strong> Enjin moden dalam CPython (sejak Python 3.9+) yang membaca kod baris-demi-baris dan membina pokok AST dengan sangat tepat.</td>
        </tr>
        <tr>
            <td><strong>JCA</strong></td>
            <td><em>Java Cryptography Architecture</em></td>
            <td><strong>Rangka Kerja Keselamatan Java.</strong> Format rasmi bahasa Java untuk memanggil fungsi sekuriti (contohnya: <code>KeyPairGenerator.getInstance("RSA")</code>).</td>
        </tr>
        <tr>
            <td><strong>JVM</strong></td>
            <td><em>Java Virtual Machine</em></td>
            <td><strong>Mesin Maya Java.</strong> Enjin perisian yang berat (makan ratusan MB RAM) yang wajib dipasang jika komputer mahu mengkompil atau menjalankan kod Java.</td>
        </tr>
        <tr>
            <td><strong>DFA / NFA</strong></td>
            <td><em>Deterministic / Non-Deterministic Finite Automaton</em></td>
            <td><strong>Mesin Logik Pencari Teks.</strong> Model matematik enjin Regex yang membaca huruf satu demi satu dari kiri ke kanan untuk memadankan corak perkataan.</td>
        </tr>
        <tr>
            <td><strong>Regex</strong></td>
            <td><em>Regular Expression</em></td>
            <td><strong>Formula Pencari Teks.</strong> Kaedah carian corak rentetan perkataan mendatar seperti fungsi carian teks <code>Ctrl + F</code>.</td>
        </tr>
        <tr>
            <td><strong>RSA</strong></td>
            <td><em>Rivest-Shamir-Adleman</em></td>
            <td><strong>Kunci Kriptografi Lama (1977).</strong> Algoritma mangga kunci purba berasaskan pendaraban nombor perdana yang bakal dihancurkan oleh komputer kuantum.</td>
        </tr>
    </tbody>
</table>

<div class="footer">
    <span>NOTA RINGKAS ALL TERMS AND CODING &bull; Track 1: Agentic Cyber Defence</span>
    <span>Halaman 1 daripada 5 &bull; Gambaran Besar &amp; Kamus Akronim (1)</span>
</div>

<div class="page-break"></div>

<!-- ====================================================================== -->
<!-- PAGE 2: KAMUS AKRONIM (BAHAGIAN 2) & BEDAH KOD SETIAP FUNCTION         -->
<!-- ====================================================================== -->
<div class="header-bar">
    <div class="title-block">
        <h1>{MAIN_TITLE}</h1>
        <div class="subtitle">Sambungan Kamus Akronim &amp; Bedah Siasat Setiap Function Yang Ditaip</div>
    </div>
    <div class="meta-box">
        <div>Kamus Akronim K–Z &bull; Function Deep-Dive</div>
        <div>tools.py &bull; workflow.py &bull; audit.py</div>
    </div>
</div>

<div class="section-title">KAMUS LENGKAP AKRONIM &amp; SINGKATAN (BAHAGIAN 2: K HINGGA Z)</div>

<table>
    <thead>
        <tr>
            <th style="width:16%;">Akronim</th>
            <th style="width:34%;">Maksud Penuh *(Full Term)*</th>
            <th style="width:50%;">Penerangan Bahasa Mudah (Orang Awam Boleh Faham)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>ECC / ECDSA</strong></td>
            <td><em>Elliptic Curve Digital Signature Algorithm</em></td>
            <td><strong>Tandatangan Kunci Lengkung.</strong> Digunakan dalam Bitcoin dan kad pintar. Saiz kuncinya kecil, tetapi tetap boleh dipecahkan oleh komputer kuantum.</td>
        </tr>
        <tr>
            <td><strong>HNDL</strong></td>
            <td><em>Harvest Now, Decrypt Later</em></td>
            <td><strong>Curi Dulu, Buka Nanti.</strong> Strategi intipan di mana musuh mencuri data internet hari ini, dan simpan sehingga komputer kuantum siap dibina untuk membukanya.</td>
        </tr>
        <tr>
            <td><strong>KEM</strong></td>
            <td><em>Key Encapsulation Mechanism</em></td>
            <td><strong>Sampul Kunci Rahsia.</strong> Kaedah membungkus kunci rahsia seperti surat dalam peti keluli sebelum dihantar melalui kabel internet yang tidak selamat.</td>
        </tr>
        <tr>
            <td><strong>ML-KEM</strong></td>
            <td><em>Module-Lattice Key Encapsulation (FIPS 203)</em></td>
            <td><strong>Piawaian Mangga Kunci Baharu Dunia.</strong> Nama asalnya <em>Kyber</em>. Standard rasmi NIST untuk enkripsi data secara kebal kuantum.</td>
        </tr>
        <tr>
            <td><strong>ML-DSA</strong></td>
            <td><em>Module-Lattice Digital Signature (FIPS 204)</em></td>
            <td><strong>Piawaian Tandatangan Baharu Dunia.</strong> Nama asalnya <em>Dilithium</em>. Standard rasmi NIST untuk menandatangani dokumen digital secara kebal kuantum.</td>
        </tr>
        <tr>
            <td><strong>MTU</strong></td>
            <td><em>Maximum Transmission Unit</em></td>
            <td><strong>Had Muatan Maksimum Paket Internet.</strong> Had berat satu kotak data yang boleh lalu dalam kabel rangkaian internet (standardnya tepat **1,500 bait**).</td>
        </tr>
        <tr>
            <td><strong>IND-CCA2</strong></td>
            <td><em>Indistinguishability under Adaptive Chosen Ciphertext Attack</em></td>
            <td><strong>Gred Kebal Paling Tinggi.</strong> Jaminan matematik bahawa walaupun penjenayah mencuba berjuta kali membedah kod rahsia, mereka tiada peluang meneka.</td>
        </tr>
        <tr>
            <td><strong>HITL</strong></td>
            <td><em>Human-in-the-Loop</em></td>
            <td><strong>Manusia Memegang Kuasa Veto.</strong> Sistem sekuriti di mana AI dilarang mengubah kod sesuka hati; ia wajib berhenti dan menunggu tandatangan manusia.</td>
        </tr>
        <tr>
            <td><strong>RBAC</strong></td>
            <td><em>Role-Based Access Control</em></td>
            <td><strong>Akses Mengikut Pangkat.</strong> Pembahagian kuasa: Pegawai semak kod hanya boleh membaca &amp; meluluskan, Pegawai Admin boleh melihat status sistem.</td>
        </tr>
        <tr>
            <td><strong>RAM</strong></td>
            <td><em>Random Access Memory</em></td>
            <td><strong>Memori Ingatan Sementara.</strong> Tempat sistem kita menggantung dan membekukan proses AI semasa menunggu manusia membuat keputusan.</td>
        </tr>
        <tr>
            <td><strong>SHA-256</strong></td>
            <td><em>Secure Hash Algorithm (256-bit)</em></td>
            <td><strong>Cap Jari Digital Unik.</strong> Formula matematik yang menukar fail kepada rentetan 64 aksara. Mengubah satu titik pun akan merosakkan seluruh cap jari tersebut.</td>
        </tr>
        <tr>
            <td><strong>NIST / FIPS</strong></td>
            <td><em>National Institute of Standards and Technology</em></td>
            <td><strong>Badan Piawaian Amerika Syarikat.</strong> Institut yang meluluskan piawaian keselamatan rasmi dunia (*Federal Information Processing Standards*).</td>
        </tr>
        <tr>
            <td><strong>CoT</strong></td>
            <td><em>Chain-of-Thought</em></td>
            <td><strong>Pemikiran Berturutan AI.</strong> Teknik di mana model AI menaakul langkah demi langkah secara logik, bukan meneka secara semberono.</td>
        </tr>
    </tbody>
</table>

<div class="section-title">BAHAGIAN 3: BEDAH SETIAP ISTILAH KOD YANG KITA TAIP (DENGAN ANALOGI)</div>

<p style="margin:0 0 6px 0;">
    Berikut adalah penjelasan mendalam tentang fungsi sebenar yang kita taip dalam fail kod projek (<code>pqc_agent/tools.py</code>, <code>workflow.py</code>, dan <code>audit.py</code>):
</p>

<!-- FUNCTION 1 -->
<div class="card">
    <div class="card-title">
        <span class="badge-pill badge-blue">KOD 01</span> <code>ast.parse(source_code, filename=file_name)</code>
    </div>
    <div style="font-size:8.2pt; color:#334155;">
        <strong>Apa Dia:</strong> Fungsi bawaan Python yang membaca fail teks kod manusia dan menukarkannya menjadi "objek pokok di dalam memori".<br/>
        <strong>Kenapa Kita Taip:</strong> Ini adalah Fasa 2 (*Syntax Analysis*) compiler CPython. Ia menyemak tatabahasa kod dan jika ada kod rosak, ia terus keluarkan <code>SyntaxError</code>.
    </div>
    <div class="analogy-box">
        🚗 <strong>Analogi LEGO:</strong> Bayangkan orang bawa sebuah kereta mainan LEGO. <code>ast.parse</code> ialah mesin pengimbas yang melukis cetak biru (*blueprint*) bahagian mana tayar, enjin, dan pintu kereta tersebut.
    </div>
</div>

<!-- FUNCTION 2 -->
<div class="card">
    <div class="card-title">
        <span class="badge-pill badge-blue">KOD 02</span> <code>class _PythonCryptoVisitor(ast.NodeVisitor)</code>
    </div>
    <div style="font-size:8.2pt; color:#334155;">
        <strong>Apa Dia:</strong> Kelas khas yang kita cipta dengan mewarisi kelas <code>ast.NodeVisitor</code> bawaan Python. Ini menggunakan konsep reka bentuk <strong>Visitor Pattern</strong>.<br/>
        <strong>Kenapa Kita Taip:</strong> Membolehkan kita menyelinap dan memintas nod tertentu dalam pokok tanpa perlu menulis kod pencarian manual yang panjang.
    </div>
    <div class="analogy-box">
        🏥 <strong>Analogi Inspektor Hospital:</strong> Pokok kod ibarat sebuah hospital besar yang mempunyai beratus-ratus bilik. <code>_PythonCryptoVisitor</code> ialah seorang Inspektor Kesihatan yang melawat bilik-bilik itu untuk mencari sama ada ubat tamat tempoh (*kriptografi lama*) digunakan.
    </div>
</div>

<div class="footer">
    <span>NOTA RINGKAS ALL TERMS AND CODING &bull; Track 1: Agentic Cyber Defence</span>
    <span>Halaman 2 daripada 5 &bull; Kamus Akronim (2) &amp; Bedah Siasat Kod (1)</span>
</div>

<div class="page-break"></div>

<!-- ====================================================================== -->
<!-- PAGE 3: BEDAH KOD SETIAP FUNCTION (SAMBUNGAN)                          -->
<!-- ====================================================================== -->
<div class="header-bar">
    <div class="title-block">
        <h1>{MAIN_TITLE}</h1>
        <div class="subtitle">Sambungan Bedah Siasat Kod: Alias Tracking, Interception, Brek interrupt() &amp; Lejar</div>
    </div>
    <div class="meta-box">
        <div>tools.py &bull; workflow.py &bull; audit.py</div>
        <div>Penjelasan Setiap Baris Yang Ditaip</div>
    </div>
</div>

<!-- FUNCTION 3 -->
<div class="card">
    <div class="card-title">
        <span class="badge-pill badge-cyan">KOD 03</span> <code>visit_Import(self, node)</code> &amp; <code>visit_ImportFrom(self, node)</code>
    </div>
    <div style="font-size:8.2pt; color:#334155;">
        <strong>Apa Dia:</strong> Pintu perangkap automatik (*hook method*). Bila pengimbas ternampak baris <code>import ...</code> atau <code>from ... import ...</code>, fungsi ini akan menyala dan dipanggil secara automatik.<br/>
        <strong>Kenapa Kita Taip:</strong> Untuk merekodkan modul kriptografi lama yang dimasukkan ke dalam fail perisian.
    </div>
    <div class="analogy-box">
        🚪 <strong>Analogi Pengimbas Kastam:</strong> Seperti mesin pengimbas di pintu masuk sempadan. Bila ada orang bawa barang larangan masuk, loceng amaran terus berbunyi.
    </div>
</div>

<!-- FUNCTION 4 -->
<div class="card">
    <div class="card-title">
        <span class="badge-pill badge-cyan">KOD 04</span> <code>self._import_aliases[local_name] = full_module</code>
    </div>
    <div style="font-size:8.2pt; color:#334155;">
        <strong>Apa Dia:</strong> Buku catatan nama samaran (*alias lookup table*). Contohnya jika pengaturcara taip: <code>from Crypto.PublicKey import RSA as kunci_rahsia</code>.<br/>
        <strong>Kenapa Kita Taip:</strong> Pengaturcara sering menukar nama modul. Scanner biasa akan tertipu kerana mencari perkataan "RSA". Tetapi kod kita mencatat bahawa <code>kunci_rahsia</code> itu sebenarnya adalah <code>RSA</code>!
    </div>
    <div class="analogy-box">
        🕵️ <strong>Analogi Nama Samaran Penjenayah:</strong> Walaupun penjenayah bernama "Kassim" menukar nama kembarnya kepada "Mat Sabu", detektif polis telah mencatat nama sebenarnya dalam buku rekod. Bila "Mat Sabu" buat jenayah, polis tetap tahu dia adalah Kassim.
    </div>
</div>

<!-- FUNCTION 5 -->
<div class="card">
    <div class="card-title">
        <span class="badge-pill badge-rose">KOD 05</span> <code>self.generic_visit(node)</code> — <em>(SANGAT KRITIKAL!)</em>
    </div>
    <div style="font-size:8.2pt; color:#334155;">
        <strong>Apa Dia:</strong> Perintah khas di hujung fungsi visitor yang menyuruh pelawat: *"Sila teruskan melawat nod-nod anak di bahagian dalam!"*<br/>
        <strong>Kenapa Wajib Ditaip:</strong> Jika kita tertinggal baris ini, pelawat kita akan berhenti di pintu depan sahaja dan gagal mengimbas kod yang terletak di dalam fungsi, gelung (*loops*), atau blok *if-else*!
    </div>
    <div class="analogy-box">
        🔍 <strong>Analogi Pengawal Keselamatan:</strong> Jika pengawal memeriksa pintu pagar utama tetapi lupa memeriksa bilik tidur dan dapur di dalam rumah, pencuri di dalam bilik tidur tidak akan dijumpai.
    </div>
</div>

<!-- FUNCTION 6 -->
<div class="card">
    <div class="card-title">
        <span class="badge-pill badge-rose">KOD 06</span> <code>visit_Call(self, node: ast.Call)</code> — <em>(TEMPAT TANGKAP KERENTANAN!)</em>
    </div>
    <div style="font-size:8.2pt; color:#334155;">
        <strong>Apa Dia:</strong> Pintu perangkap yang dipanggil apabila kod membuat panggilan fungsi sebenar: <code>rsa.generate_private_key(key_size=2048)</code>.<br/>
        <strong>Bagaimana Ia Menangkap RSA:</strong>
        <ul style="margin:2px 0; padding-left:16px;">
            <li>Menyemak fungsi: <code>node.func</code> (Attribute) ➔ Reconstruct jadi string <code>rsa.generate_private_key</code>.</li>
            <li>Menyemak parameter: <code>node.keywords</code> ➔ Mencari <code>key_size</code> dan membaca nilainya dari <code>ast.Constant(value=2048)</code>.</li>
            <li>Bila sah fungsi RSA bersaiz 2048-bit, ia menjana rekod kerentanan berkeyakinan tinggi (**Confidence: 0.85**).</li>
        </ul>
    </div>
    <div class="analogy-box">
        🎯 <strong>Analogi Perangkap Tikus:</strong> Tikus boleh lalu merata-rata, tetapi bila ia menyentuh umpan makanan (*fungsi pembuat kunci*), perangkap terus tertutup dan menangkapnya.
    </div>
</div>

<!-- FUNCTION 7 -->
<div class="card">
    <div class="card-title">
        <span class="badge-pill badge-amber">KOD 07</span> <code>ast.unparse(node)</code>
    </div>
    <div style="font-size:8.2pt; color:#334155;">
        <strong>Apa Dia:</strong> Fungsi penterjemah songsang. Objek nod AST adalah format dalaman komputer yang rumit. <code>ast.unparse(node)</code> menukarkannya kembali menjadi teks kod Python asal (cth: <code>"rsa.generate_private_key"</code>).<br/>
        <strong>Kenapa Kita Taip:</strong> Supaya kita boleh memadankannya dengan mudah terhadap pangkalan data algoritma lama (<code>LEGACY_CRYPTO_DB</code>).
    </div>
    <div class="analogy-box">
        🗣️ <strong>Analogi Jurubahasa:</strong> Menterjemah semula kod isyarat tangan komputer kembali kepada perkataan bahasa Inggeris yang mudah dibaca oleh manusia.
    </div>
</div>

<!-- FUNCTION 8 -->
<div class="card">
    <div class="card-title">
        <span class="badge-pill badge-green">KOD 08</span> <code>interrupt(...)</code> &amp; <code>Command(resume={{"decision": "approved"}})</code>
    </div>
    <div style="font-size:8.2pt; color:#334155;">
        <strong>Apa Dia:</strong> Tombol brek kecemasan fizikal daripada pustaka LangGraph dalam <code>node_human_approval()</code>.<br/>
        <strong>Bagaimana Ia Berfungsi:</strong>
        <ul style="margin:2px 0; padding-left:16px;">
            <li><code>interrupt()</code>: Membekukan pelaksanaan ejen AI di dalam memori komputer (RAM / <code>MemorySaver</code>). AI dilarang sama sekali menulis kod ke dalam fail sistem.</li>
            <li><code>Command(resume=...)</code>: Kunci penyahbekuan yang hanya dihantar apabila pegawai manusia menekan butang <strong>"Approve"</strong> di Cyber SOC Dashboard selepas menyemak Monaco Diff.</li>
        </ul>
    </div>
    <div class="analogy-box">
        🛑 <strong>Analogi Palang Kereta Api:</strong> Kereta api (*Ejen AI*) wajib berhenti di lampu merah. Palang keselamatan tidak akan terbuka secara automatik sehinggalah Renjer Stesen (*Manusia*) memeriksa trek dan menekan suis hijau.
    </div>
</div>

<!-- FUNCTION 9 -->
<div class="card">
    <div class="card-title">
        <span class="badge-pill badge-green">KOD 09</span> <code>_compute_chain_hash(entries)</code> &amp; <code>json.dumps(..., sort_keys=True)</code>
    </div>
    <div style="font-size:8.2pt; color:#334155;">
        <strong>Apa Dia:</strong> Formula lejar rantaian cap jari SHA-256 yang menyusun data secara kanonikal (*canonical*).<br/>
        <strong>Formula Matematik:</strong> $\\text{{Hash}}_n = \\text{{SHA256}}(\\text{{CanonicalJSON}}(\\text{{Entry}}_n) + \\text{{Hash}}_{{n-1}})$<br/>
        <strong>Kesan Runtuhan Salji (*Avalanche Effect*):</strong> Bermula dari Genesis Hash <code>"0"*64</code>. Jika mana-mana staf syarikat cuba mengedit rekod lama, perbezaan satu aksara akan menyebabkan seluruh nombor hash di bawahnya rosak dan mencetuskan amaran <strong>"TAMPER DETECTED"</strong>. <code>sort_keys=True</code> memastikan susunan huruf kunci sentiasa seragam mengikut A-Z.
    </div>
    <div class="analogy-box">
        ⛓️ <strong>Analogi Buku Cek Bertali Dawai Besi:</strong> Setiap halaman diikat dengan mangga bernombor yang bergantung pada nombor mangga halaman sebelum ini. Jika anda koyak satu muka surat di tengah, seluruh tali dawai buku itu terputus.
    </div>
</div>

<div class="footer">
    <span>NOTA RINGKAS ALL TERMS AND CODING &bull; Track 1: Agentic Cyber Defence</span>
    <span>Halaman 3 daripada 5 &bull; Bedah Siasat Kod (2) &amp; Logik Lejar SHA-256</span>
</div>

<div class="page-break"></div>

<!-- ====================================================================== -->
<!-- PAGE 4: POKOK TERBALIK AST & PENEMUAN PQC MTU PACKET BLOAT             -->
<!-- ====================================================================== -->
<div class="header-bar">
    <div class="title-block">
        <h1>{MAIN_TITLE}</h1>
        <div class="subtitle">Bahagian 4: Anatomi Pokok Terbalik AST &amp; Bahagian 5: Penemuan PQC MTU Bloat</div>
    </div>
    <div class="meta-box">
        <div>Inverted Tree Anatomy</div>
        <div>1,500-Byte Ethernet MTU &bull; Availability Attack</div>
    </div>
</div>

<div class="section-title">BAHAGIAN 4: KENAPA POKOK AST INI DIPANGGIL "POKOK TERBALIK"?</div>

<div class="card-dark">
    <div class="card-title">
        🌳 Pokok Salasilah Kod Terbalik (Inverted Tree)
    </div>
    <div style="font-size:8.2pt; color:#cbd5e1; line-height:1.5;">
        Dalam sains komputer, pokok struktur tidak tumbuh dari tanah ke atas, sebaliknya ia tumbuh dari langit ke bawah. Bayangkan pokok salasilah keluarga di mana moyang paling tua berada di bahagian atas sekali, dan cicit-cicit berada di bawah:
    </div>
    <div class="code-box">
[1. PANGKAL POKOK / ROOT (Paling Atas)]: ast.Module
      └── Mewakili keseluruhan fail kod anda.
      │
      └── [2. BATANG POKOK / BRANCH]: ast.FunctionDef ('generate_rsa_keypair')
            └── Menunjukkan kawasan fungsi perisian bermula.
            │
            └── [3. DAHAN POKOK / BRANCH]: ast.Assign (private_key = ...)
                  └── Arahan meletakkan sesuatu ke dalam pembolehubah.
                  │
                  ├── [4A. DAUN KIRI / LEAF]: ast.Name ('private_key')
                  │     └── Nama pembolehubah di sebelah kiri.
                  │
                  └── [4B. DAHAN KANAN / INTERCEPTION NODE]: 🎯 ast.Call
                        └── Enjin _PythonCryptoVisitor kita memintas di sini!
                        │
                        ├── [5A. RANTING / ATTRIBUTE]: rsa.generate_private_key
                        │     └── Diterjemah kembali guna ast.unparse(node).
                        │
                        └── [5B. DAUN PALING HUJUNG / LEAF]: ast.Constant (2048)
                              └── Saiz kunci RSA 2048-bit dikesan & dibongkar!
    </div>
</div>

<div class="section-title">BAHAGIAN 5: PENEMUAN UNIK KITA: APA ITU "PQC MTU PACKET BLOAT"?</div>

<div class="card" style="background:#fffbeb; border-color:#fef08a;">
    <div class="card-title" style="color:#b45309;">
        🚚 Analogi Lori Pos &amp; Had Lebuhraya Internet (1,500 Bait)
    </div>
    <p style="font-size:8.4pt; color:#78350f; margin:0 0 6px 0;">
        Ini adalah penemuan paling unik projek kita yang membezakannya daripada projek pelajar lain. Terangkan kepada pensyarah menggunakan <strong>Analogi Lori Pos</strong>:
    </p>

    <div class="grid-2col" style="font-size:8.2pt; margin-bottom:8px;">
        <div style="background:#ffffff; padding:8px 10px; border-radius:6px; border:1px solid #fef3c7;">
            <strong style="color:#1e1b4b;">1. Had Lori Pos (Ethernet MTU 1,500 Bait):</strong><br/>
            Di lebuhraya internet, setiap kabel dan router mempunyai had muatan fizikal yang dipanggil <strong>MTU (Maximum Transmission Unit)</strong> iaitu tepat <strong>1,500 bait</strong>. Bayangkan lori pos yang hanya boleh muatkan barang seberat 1,500 kg.
        </div>
        <div style="background:#ffffff; padding:8px 10px; border-radius:6px; border:1px solid #fef3c7;">
            <strong style="color:#166534;">2. Zaman Kunci Lama (RSA - 256 Bait):</strong><br/>
            Tandatangan digital RSA lama saiznya hanya <strong>256 bait</strong> (256 kg). Saiznya kecil, jadi satu lori pos boleh muat dengan sangat mudah dan pantas.
        </div>
    </div>

    <table>
        <thead>
            <tr>
                <th style="width:30%;">Jenis Algoritma</th>
                <th style="width:25%;">Saiz Tandatangan / Kunci</th>
                <th style="width:45%;">Kesan Terhadap Had Lori Pos (1,500 Bait MTU)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Legacy RSA-2048</strong></td>
                <td>256 Bait</td>
                <td><span class="badge-pill badge-green">Muat Dalam 1 Lori (Hanya guna 17% ruang)</span></td>
            </tr>
            <tr>
                <td><strong>NIST ML-KEM-768</strong></td>
                <td>1,184 Bait (Kunci Awam)</td>
                <td><span class="badge-pill badge-amber">Amaran: Guna 79% muatan lori</span></td>
            </tr>
            <tr>
                <td><strong>NIST ML-DSA-65</strong></td>
                <td><strong>3,309 Bait</strong> (Tandatangan)</td>
                <td><span class="badge-pill badge-rose">💥 220% MELEBIHI HAD LORI! (Lori Terbelah 3)</span></td>
            </tr>
        </tbody>
    </table>

    <div style="font-size:8.2pt; color:#92400e; line-height:1.45;">
        <strong>Apa Bahayanya Kepada Sistem Syarikat? (*The Availability Threat*):</strong><br/>
        Kerana saiz kunci kebal kuantum ML-DSA adalah 3,309 bait, sistem rangkaian terpaksa memotong data tersebut menjadi <strong>3 paket berasingan (IP Packet Fragmentation)</strong>. Banyak firewall bank secara automatik akan membuang (*drop*) paket yang terpotong-potong ini kerana mengesyaki ia serangan penggodam. Akibatnya: Laman web menjadi *loading* tanpa henti, sambungan terputus (*timeout*), dan perkhidmatan tergendala! Ejen kita adalah yang pertama dalam industri yang memberi amaran tentang isu ini!
    </div>
</div>

<div class="footer">
    <span>NOTA RINGKAS ALL TERMS AND CODING &bull; Track 1: Agentic Cyber Defence</span>
    <span>Halaman 4 daripada 5 &bull; Pokok Terbalik AST &amp; Analogi Lori Pos MTU</span>
</div>

<div class="page-break"></div>

<!-- ====================================================================== -->
<!-- PAGE 5: SKRIP PERTUTURAN SANTAI & CARA MENJAWAB PENSYARAH              -->
<!-- ====================================================================== -->
<div class="header-bar">
    <div class="title-block">
        <h1>{MAIN_TITLE}</h1>
        <div class="subtitle">Bahagian 6: Contoh Skrip Pertuturan Santai Kepada Pensyarah &amp; Soalan Cepumas</div>
    </div>
    <div class="meta-box">
        <div>Contoh Perbualan Spontan</div>
        <div>Tips Menjawab Soalan Panel</div>
    </div>
</div>

<div class="section-title">BAHAGIAN 6: CONTOH CARA ANDA CAKAP KEPADA PENSYARAH (GAYA SANTAI TAPI PADAT)</div>

<p style="margin:0 0 6px 0;">
    Gunakan gaya pertuturan ini jika pensyarah meminta anda menerangkan keseluruhan sistem dalam 2 minit secara lisan:
</p>

<div class="speech-box">
    "Dr., secara ringkasnya projek kami ini membina satu sistem pengimbas pintar berkonsepkan <em>Neuro-Symbolic</em>.
    <br><br>
    Bahagian <em>Symbolic</em> ialah kami meminjam otak pengkompil Python iaitu <em>CPython PEG Parser</em>. Melalui modul <code>ast</code>, kami menukarkan kod kepada struktur pokok hierarki. Kami cipta satu kelas pelawat bernama <code>_PythonCryptoVisitor</code> yang menggunakan <em>Visitor Pattern</em>. Kelas ini akan melawat nod <code>visit_Call</code>, membongkar fungsi itu menggunakan <code>ast.unparse</code>, dan membaca daun pokoknya untuk memeriksa sama ada saiz kunci itu 2048-bit atau kriptografi purba yang boleh dipecahkan oleh komputer kuantum.
    <br><br>
    Kalau pengaturcara cuba menukar nama pustaka menggunakan 'alias' seperti <code>import RSA as kunci_saya</code>, fungsi <code>visit_ImportFrom</code> kami akan menyimpannya ke dalam <code>self._import_aliases</code>, jadi sistem kami tidak boleh ditipu. Dan hebatnya AST ini berbanding Regex biasa, jika ada komen seperti <code># TODO: buang RSA</code>, AST akan abaikan 100% kerana komen tidak dimasukkan ke dalam pokok tatabahasa.
    <br><br>
    Kemudian, bahagian <em>Neural (AI)</em> kami akan menjana kod gantian terkini piawaian dunia iaitu <em>NIST FIPS 203 (ML-KEM)</em>. Tetapi kami tidak benarkan AI menulis kod sesuka hati. Kami pasang brek fizikal menggunakan fungsi <code>interrupt()</code> daripada pustaka LangGraph. Proses akan terhenti sepenuhnya di dalam RAM sehingga pegawai manusia menyemak perbezaan kod merah dan hijau di dashboard Monaco kami dan menekan punat <code>Command(resume='approved')</code>.
    <br><br>
    Akhir sekali, setiap kelulusan manusia itu akan dikunci ke dalam rantaian cap jari SHA-256 melalui fungsi <code>_compute_chain_hash</code>. Jika ada mana-mana pihak cuba mengubah log audit tersebut, kesan <em>Avalanche Effect</em> akan serta-merta merosakkan rantaian hash dan membongkar cubaan menipu tersebut.
    <br><br>
    Kami juga menemui isu ketersediaan rangkaian di mana saiz tandatangan baharu ML-DSA mencecah 3,309 bait—melebihi had piawaian <em>Ethernet MTU 1,500 bait sebanyak 220%</em>, yang boleh melumpuhkan rangkaian jika tidak dikawal. Itulah intipati lengkap projek kami, Dr."
</div>

<div class="section-title">BAHAGIAN 7: 3 SOALAN CEPUMAS PENSYARAH &amp; JAWAPAN MANTAP</div>

<div class="card">
    <div style="font-size:8.8pt; font-weight:800; color:#1e1b4b; margin-bottom:3px;">
        ❓ Soalan 1: "Kenapa awak guna AST untuk Python, tapi untuk Java awak guna Regex?"
    </div>
    <div style="font-size:8.2pt; color:#334155;">
        <strong>Jawapan:</strong> "Untuk Python, kodnya sangat dinamik (boleh tukar nama import sesuka hati), jadi pokok AST wajib digunakan untuk ketepatan 96.8%. Tetapi untuk Java, standard industri menggunakan rangka kerja JCA di mana semua fungsi pembuat kunci dipanggil secara seragam (contoh: <code>KeyPairGenerator.getInstance</code>). Jika kita pasang compiler Java penuh (JVM), ia makan 200MB RAM dan mengambil masa lama. Dengan regex DFA/NFA, kita dapat kelajuan di bawah 20 milisaat tanpa perlu pasang perisian tambahan yang berat."
    </div>
</div>

<div class="card">
    <div style="font-size:8.8pt; font-weight:800; color:#1e1b4b; margin-bottom:3px;">
        ❓ Soalan 2: "Kalau saya letak perkataan RSA dalam komen, sistem awak detect tak?"
    </div>
    <div style="font-size:8.2pt; color:#334155;">
        <strong>Jawapan:</strong> "Tidak sama sekali, Dr.! Kerana compiler CPython akan membuang semua komen semasa fasa membina pokok AST. Pokok AST hanya mengandungi baris arahan yang sebenar, jadi amaran palsu (*false positive*) daripada komen adalah 0%."
    </div>
</div>

<div class="card">
    <div style="font-size:8.8pt; font-weight:800; color:#1e1b4b; margin-bottom:3px;">
        ❓ Soalan 3: "Bagaimana sistem awak pastikan AI tak ubah kod projek tanpa izin?"
    </div>
    <div style="font-size:8.2pt; color:#334155;">
        <strong>Jawapan:</strong> "Kami guna fungsi <code>interrupt()</code> dari LangGraph. Pelaksanaan ejen AI dibekukan secara fizikal di dalam RAM. Ejen tiada kuasa menulis ke fail sehinggalah pegawai manusia memeriksa kod di skrin Monaco Diff kami dan klik punat Approve."
    </div>
</div>

<div class="footer">
    <span>NOTA RINGKAS ALL TERMS AND CODING &bull; Track 1: Agentic Cyber Defence</span>
    <span>Halaman 5 daripada 5 &bull; Skrip Pertuturan Santai &amp; Jawapan Soalan Cepumas</span>
</div>

</body>
</html>
"""

HTML_FILE.write_text(html_content, encoding="utf-8")
print(f"[OK] Wrote Nota Ringkas HTML to {HTML_FILE}")

cmd = [
    EDGE_EXE,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={PDF_FILE}",
    str(HTML_FILE.resolve()),
]

print(f"[RUNNING] Compiling Nota Ringkas PDF via Microsoft Edge headless...")
result = subprocess.run(cmd, capture_output=True, text=True)

if PDF_FILE.exists() and PDF_FILE.stat().st_size > 0:
    print(f"[SUCCESS] PDF generated: {PDF_FILE} ({PDF_FILE.stat().st_size} bytes)")
    try:
        shutil.copy2(PDF_FILE, DOWNLOADS_PDF)
        print(f"[COPIED] Copied to Downloads: {DOWNLOADS_PDF}")
    except Exception as e:
        print(f"[WARN] Could not copy to Downloads: {e}")
        
    pdf_bytes = PDF_FILE.read_bytes()
    page_matches = re.findall(rb"/Type\s*/Page\b", pdf_bytes)
    page_count = len(page_matches)
    print(f"[INFO] Verified Page Count: {page_count} page(s)")
else:
    print(f"[ERROR] Failed to generate PDF: {result.stderr}")
    sys.exit(1)
