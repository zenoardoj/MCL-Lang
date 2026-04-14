# MCL Roadmap

This roadmap outlines the evolution of MCL as a coordination language for AI agents.

The focus is not on adding features quickly, but on building a **clear, reliable, and governable execution model**.

---

## Phase 0 — Foundation

### Goal

Define the core language and validate that the execution model is coherent.

### Status

In progress

### Scope

* YAML-based DSL
* document models (Pydantic)
* semantic validation
* safe expression engine
* mock runtime
* mock MCP tool adapter
* mock resource adapter
* audit logging

---

## Phase 1 — Semantic Stabilization

### Goal

Remove ambiguity and define clear behavior.

### Priorities

* formalize workflow semantics
* define scope rules
* clarify `emit`, `transform`, and loops
* define resource read/write behavior
* improve error consistency

---

## Phase 2 — Contracts and Schemas

### Goal

Introduce stronger validation and contracts.

### Priorities

* validate tool input/output
* define resource query/value structure
* add lightweight shape/type validation
* improve error diagnostics

---

## Phase 3 — MCP Integration

### Goal

Align MCL more directly with MCP.

### Priorities

* map tools to MCP tool invocation
* define resource interaction model
* support capability discovery
* define adapter boundaries

---

## Phase 4 — CLI and Developer Experience

### Goal

Make MCL usable by developers.

### Priorities

* CLI commands (`validate`, `run`)
* better error messages
* improved examples
* quickstart documentation

---

## Phase 5 — Governance and Safety

### Goal

Make policy enforcement a core feature.

### Priorities

* approval workflows
* sensitive resource handling
* execution limits
* audit severity levels

---

## Phase 6 — Tooling

### Goal

Improve authoring and inspection.

### Priorities

* JSON Schema export
* editor support
* linting and formatting
* visualization tools

---

## Phase 7 — Production Readiness

### Goal

Evaluate real-world usage.

### Priorities

* deterministic execution guarantees
* observability integration
* performance considerations
* versioning strategy

---

## Guiding principle

MCL should remain:

* declarative
* explicit
* constrained
* predictable

The goal is not maximum flexibility.

The goal is **reliable agent workflows**.
