# OMEGA-DNA

## RU
Исследование ДНК как многоуровневой системы связей, памяти и информации. Цель — проверить, можно ли описывать организацию ДНК через универсальную архитектуру: **элемент → связь → узел → структура → память → функция → обратная связь**.

## EN
Researching DNA as a multi-level system of relations, memory, and information. The goal is to test whether DNA organization can be described through a universal architecture: **element → relation → node → structure → memory → function → feedback**.

## 中文
将 DNA 研究为多层次的关系、记忆与信息系统。目标是检验 DNA 的组织是否可以通过通用架构描述：**元素 → 关系 → 节点 → 结构 → 记忆 → 功能 → 反馈**。

## Status

Research repository. Hypotheses are not treated as established facts. Every claim must be separated into known evidence, model assumption, prediction, test, result, and limitation.

## Research levels

1. Chemical bonds and molecular interactions.
2. Nucleotide structure.
3. Base pairing and double-stranded organization.
4. Sequence and information representation.
5. DNA packaging and chromatin.
6. Replication, repair, transcription, and regulation.
7. Mutation, selection, inheritance, and persistence of information.
8. Network representation of dependencies and constraints.

## Core rule

Do not force DNA into the theory. Build the representation from observed structure first, then test whether the architecture adds explanatory or predictive power.

## Full experimental pass

The controlled suite now covers complementarity, maintenance feedback, typed relations, local physical structure, nucleosome-like structure, accessibility state, typed regulatory relations, enhancer–promoter relations, regulatory network topology, cellular state, memory/persistence, causal perturbation controls, and relational invariance.

The executed computational gates repeatedly show that explicitly represented relations/history can add predictive information when the synthetic data-generating process contains that information. These are architecture tests, not biological proof.

See:

- `03_EXPERIMENTS/FULL_DNA_PASS.md` — complete layer-by-layer pass.
- `03_EXPERIMENTS/FULL_EXECUTION_AUDIT_2026-09-07.md` — execution audit and open gates.
- `03_EXPERIMENTS/E5_MEMORY_CAUSAL_PERSISTENCE_RESULTS.md` — memory/persistence gate.
- `03_EXPERIMENTS/E6_REAL_BIOLOGICAL_GATE_PROTOCOL.md` — biological benchmark protocol.
- `03_EXPERIMENTS/E6_REAL_BIOLOGICAL_GATE_RUNNER.py` — reproducible runner for the real-data gate.
- `03_EXPERIMENTS/E14_ABSTRACTION_MEMORY_PROTOCOL.md` — abstract-form memory pilot protocol.
- `03_EXPERIMENTS/E14_ABSTRACTION_MEMORY_RUNNER.py` — reproducible E14 runner.
- `03_EXPERIMENTS/E14_ABSTRACTION_MEMORY_RESULTS.md` — E14 results and limitations.
- `03_EXPERIMENTS/E15_ABSTRACTION_CONFIRMATORY_PROTOCOL.md` — frozen E15 protocol and transparent record of an invalid first implementation run.
- `03_EXPERIMENTS/E15_ABSTRACTION_CONFIRMATORY_RUNNER.py` — corrected E15 runner.
- `03_EXPERIMENTS/E15_ABSTRACTION_CONFIRMATORY_RESULTS.md` — corrected rerun results; independent reproduction pending.
- `03_EXPERIMENTS/RESEARCH_STABILITY_IDENTITY_MIRROR_LIFE.md` — separate research proposal on system stability, identity under component turnover, and the scientific context of mirror life.
- `HYPOTHESES.md` — includes H-DNA-05, memory of abstract form.

## Current verdict

**Architecture-level relational capacity: supported in controlled computational systems.**  
**Hand-designed abstract-form transfer: provisionally supported in E14/E15 synthetic tests.**  \n**Learned abstract-form transfer: not demonstrated by E16; the tested message-passing model failed on global-form distinctions.**  
**Real biological predictive advantage: still open.**  
**New biological principle: no evidence yet.**

The decisive biological gate remains a real public functional-genomics benchmark comparing a capacity-matched sequence-only model against sequence + independently measured typed relations/state under chromosome-level holdouts, relation-shuffle nulls, and leakage controls.

Public datasets identified for this gate include GSE188405 (matched ATAC-seq, RNA-seq and H3K27ac HiChIP across human cell types) and the GSE113480/GSE113481/GSE113482 family (ATAC-seq, promoter-capture Hi-C and RNA-seq in human neural cell types).
