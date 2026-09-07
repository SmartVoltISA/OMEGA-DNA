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

The current architectural test suite covers complementarity, maintenance feedback, typed relations, history-dependent memory, contextual relations, ablation/null controls, and relational invariance. The executed toy tests support the **capacity** of the architecture to carry information that sequence-only or untyped baselines can lose. They do **not** establish a new biological mechanism.

See:

- `03_EXPERIMENTS/FULL_DNA_PASS.md` — complete layer-by-layer pass.
- `03_EXPERIMENTS/OFFICIAL_COMPARISON.md` — comparison with established biology.
- `03_EXPERIMENTS/RELATIONAL_COMPLEMENTARITY_SUITE.py` — reproducible test code.
- `03_EXPERIMENTS/RELATIONAL_COMPLEMENTARITY_RESULTS.md` — results, nulls, limitations, and final scientific verdict.

### Current verdict

**Architecture-level complementarity: supported in controlled toy systems.**  
**Real biological predictive advantage: not yet established.**  
**New biological principle: no evidence yet.**

The decisive next gate is a real public functional-genomics benchmark comparing sequence-only against sequence + explicitly typed measured relations/state under matched splits, capacity controls, and relation-shuffle nulls.
