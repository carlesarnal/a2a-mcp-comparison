# Presentation guide

A2A or MCP? Choosing an Interface for the Same Capability

## Audience and central claim

The same summarization work can be exposed as an MCP tool or an A2A agent. Choosing an interface from the words tool and agent alone hides the questions the caller must answer: how to discover inputs, represent progress, cancel work and interpret a failed invocation. Apicurio can store discovery metadata, but that does not make these interfaces interchangeable.

## 30-minute run of show

### 0:00 — Hold the capability constant

Say: The same summarization work can be exposed as an MCP tool or an A2A agent. Choosing an interface from the words tool and agent alone hides the questions the caller must answer: how to discover inputs, represent progress, cancel work and interpret a failed invocation. Apicurio can store discovery metadata, but that does not make these interfaces interchangeable.

Show the corresponding diagram, source record or actual command output. Pause to identify the observation that supports the claim.

### 4:00 — Trace the caller contract

Say: Begin with one deterministic summarization fixture and the same input on both paths. Pin the protocol and SDK versions and record the actual messages. Introduce a model only after transport behavior is understood, otherwise different generated summaries can obscure an interface-level comparison. The existing connected briefing uses different capabilities and is not evidence of parity.

Show the corresponding diagram, source record or actual command output. Pause to identify the observation that supports the claim.

### 9:00 — Compare one successful invocation

Say: For each requirement, record specification support, advertised implementation support, observed behavior and unsupported behavior. Untested is not synonymous with unsupported. The repository includes a small validator and a delivery gate that refuses an evidence table with untested rows. It currently fails that delivery gate because the paired implementation is still preparation work.

Show the corresponding diagram, source record or actual command output. Pause to identify the observation that supports the claim.

### 15:00 — Record a failure and uncertainty

Say: This article presents the comparison method and its evidence requirements. It does not claim an implemented cross-protocol benchmark or a universal recommendation. Exposing both interfaces adds contract tests and lifecycle obligations. Choose that extra surface only when distinct callers need it, rather than because both protocols are fashionable.

Show the corresponding diagram, source record or actual command output. Pause to identify the observation that supports the claim.

### 21:00 — Separate unsupported from untested

Say: Use the evidence boundary to choose the next action.

Show the corresponding diagram, source record or actual command output. Pause to identify the observation that supports the claim.

### 26:00 — Questions and buffer

Ask what the demonstration establishes and what it leaves open. Do not add another feature if time is short.

## Setup and fallback

```sh
python3 compare.py
```

Evidence-table validator passes. Paired A2A/MCP transport implementation is not complete. The --require-observed delivery gate deliberately fails; no interface-parity result is claimed.

Prebuild/download dependencies. Keep a recording of an actual successful run; if unavailable, use the documented walkthrough and say it is not live execution. Never substitute fabricated success output.

## Questions to prepare

- What is the simplest alternative?
- Which failure was actually exercised?
- Which guarantee belongs to the application rather than the infrastructure?
- Which result changes with versions or workload?

## 25-minute adaptation

Use one central trace, shorten setup and reserve three minutes for questions. Move the secondary implementation example to backup.
