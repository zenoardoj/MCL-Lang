# MCL Manifesto

AI agents are becoming more powerful.

They can:

* call tools
* access data
* interact with real systems

But their behavior is still often fragile.

---

## The problem

Most agent workflows today rely on:

* prompts
* glue code
* implicit logic

This leads to:

* unpredictable behavior
* hidden assumptions
* weak control over tools and data
* poor auditability

---

## Our position

We believe this is not just a tooling problem.

It is a **language problem**.

AI agents need a better way to express behavior.

---

## The idea

MCL is a coordination language for AI agents.

It defines:

* what an agent can read
* what it can do
* what rules apply
* how the workflow executes

---

## MCL + MCP

MCL is designed to work on top of MCP.

> MCP exposes capabilities.
> MCL defines behavior.

MCP connects AI to the world.
MCL defines how the AI operates within it.

---

## Design principles

### Explicit over implicit

Everything should be visible and declared.

### Validation over guesswork

Errors should be detected before execution.

### Constraints over flexibility

Less freedom, more reliability.

### Auditability by default

Every execution should be traceable.

### AI-first

The language should be easy for models to generate correctly.

---

## What MCL is not

MCL is not:

* a general-purpose programming language
* a replacement for Python
* a prompt format
* a code generator

MCL is a **coordination layer**.

---

## The tradeoff

MCL intentionally limits expressiveness.

In exchange, it provides:

* predictability
* control
* validation
* safety

---

## Why now

Because:

* LLMs can already orchestrate complex tasks
* MCP provides a standard interface to tools and data
* but there is still no clear orchestration layer

MCL explores that missing layer.

---

## Vision

AI agents should not just be powerful.

They should be:

* understandable
* controllable
* reliable

---

## Final statement

We do not need more complexity.

We need better structure.

MCL starts from that premise.
