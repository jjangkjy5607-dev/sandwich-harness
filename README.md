# Sandwich Harness Architecture

**Deterministic Constraint Framework for Autonomous AI Code Generation**

**Creator / Original Author:** Taejin Eom (TurboWork) · 엄태진

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](#mit-license)
[![Public Spec](https://img.shields.io/badge/Scope-Public_Spec-455a64.svg)](#public-scope)

## Why Sandwich Harness?

AI-generated code can drift from its specification, accumulate context confusion,
and introduce validation leakage. Sandwich Harness surrounds small implementation
units with explicit contracts and isolated evaluation. Its three-layer design
turns selected requirements into executable gates that stop a failing run.

"Deterministic" refers to explicit checks and fixed example inputs, not a guarantee
that AI generation is hallucination-free. Structural limits bound review scope;
they do not prove semantic correctness or prevent every kind of context loss.

## The three layers

### 1. Top Bread — Spec-Lock TDD Gate

Lock input/output contracts in tests before implementation. A failed contract
must block the build or execution gate. The example checks an exact five-row,
two-column input schema, zero missing/non-finite values, and prediction dimensions.
Runtime gates raise `ValueError`, including when Python runs with `-O`.
The public example is a runnable gate demonstration; a full CI/TDD suite is outside
this two-file release.

### 2. Core Filling — AST-Constrained Pure Units

Limit each function to **35 physical lines** and each source file to **200 lines**.
The example parses its own AST and checks these limits before fitting a model.
Its pure `features` unit returns a copy of the input feature column without
mutating the caller's DataFrame. Stateful model fitting stays in the orchestrator.
AST length checks enforce structure; purity still requires behavioral review.

### 3. Bottom Bread — Strict K-Fold Isolation

Split before learning preprocessing statistics. Each fold creates a fresh
`StandardScaler` + `LinearRegression` pipeline, fits only its training rows,
and predicts on held-out rows using that fold's fitted scaler.
This prevents the demonstrated preprocessing leakage across the fold boundary.
Group, temporal, and target leakage require additional domain-specific controls.

## Minimal proof of concept

[`example_sandwich_harness.py`](example_sandwich_harness.py) contains **40 lines**
and creates five synthetic rows in memory: `x = 0..4`, `y = 2x + 1`.
It performs five-fold cross-validation and prints one mean squared error per fold.
This tiny linear dataset illustrates isolation, not real-world model performance.

Requirements: Python 3.13, NumPy, pandas, and scikit-learn. Tested with NumPy 2.5.4,
pandas 3.1.0, and scikit-learn 1.9.1. Install [uv](https://docs.astral.sh/uv/) first.
The PowerShell example keeps its environment and temporary files outside this repo:

```powershell
Set-Location -LiteralPath 'D:\CodexProjects\sandwich-harness-public'
$env:UV_CACHE_DIR = 'D:\CodexProjects\.cache\uv'
$env:UV_PYTHON_INSTALL_DIR = 'D:\CodexProjects\.runtime\python'
$env:TEMP = 'D:\CodexProjects\.tmp'
$env:TMP = $env:TEMP
New-Item -ItemType Directory -Force -Path $env:TEMP | Out-Null
uv venv --python 3.13 'D:\CodexProjects\.runtime\sandwich-public'
uv pip install --python 'D:\CodexProjects\.runtime\sandwich-public\Scripts\python.exe' numpy==2.5.4 pandas==3.1.0 scikit-learn==1.9.1
& 'D:\CodexProjects\.runtime\sandwich-public\Scripts\python.exe' -B '.\example_sandwich_harness.py'
```

## Public scope

This release contains only this specification and a newly written synthetic example.
Production engines, competition implementations, private datasets, model parameters,
and paid product files are excluded from this repository and its MIT grant.

## 한국어 요약

샌드위치 하네스는 엄태진(Taejin Eom / TurboWork)이 제안하는 3중 개발 제약 구조입니다.
상단은 입출력 계약·결측치 0개 검증, 중간은 함수 35줄·파일 200줄 AST 제한과 순수 변환,
하단은 Fold별 독립 Fit/Transform으로 구성합니다. 예제는 가상 데이터 5행만 사용하며,
실전 코드·데이터·모델 파라미터는 공개하지 않습니다. AST와 작은 예제만으로 AI 환각 제거나
모든 유형의 데이터 누수 차단을 보장하지 않으며, 검증 가능한 제약을 실행하는 구조입니다.

## MIT License

Copyright (c) 2026 Taejin Eom / TurboWork

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Get the Sandwich Workflow Kit on Gumroad

Ready to apply a structured plan → build → review workflow to your own projects?
The **Sandwich Workflow Kit v2.7** provides editable English and Korean instructions,
a Windows quickstart, FAQs, and two 15-step project blueprints.

Choose Starter for personal noncommercial learning, Pro for one person's commercial
or client work, or Team for up to five named users in one organization.
The kit is delivered as editable Markdown documents and supporting assets in a ZIP.
Paid downloads follow the product's own license terms, separate from this public MIT release.

**[👉 Get the Sandwich Workflow Kit v2.7 on Gumroad](https://turboworkai.gumroad.com/l/sandwich-workflow-kit)**

한국어: 실제 판매 상품은 한영 지침·퀵스타트·FAQ·15단계 프로젝트 명세 두 종을 제공하는
v2.7 문서 키트입니다. 상품 구성과 이용권을 확인한 뒤 위 Gumroad 링크에서 구매할 수 있습니다.
