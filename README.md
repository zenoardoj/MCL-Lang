# MCL — MCP Coordination Language

**A declarative coordination language for AI agents.**
**The orchestration layer on top of MCP.**
![MCL demo](https://github.com/zenoardoj/mcl-lang/blob/main/mcl_demo.gif)

---

## What is MCL

MCL is a declarative language for defining how AI agents operate over:

* tools
* data (resources)
* policies
* structured workflows

It does not replace Python.
It does not replace MCP.

> MCL defines **how an AI agent should behave**, not just what it can do.

---

## Why MCL exists

Today, most AI agent workflows are built using:

* prompts
* tool calling
* glue code
* implicit logic

This works — but often leads to:

* fragile orchestration
* unpredictable behavior
* hidden side effects
* runtime-only failures
* limited auditability

MCL addresses this by introducing a **structured, validated workflow layer**.

---

## MCL + MCP

MCL is designed to work naturally with MCP (Model Context Protocol).

> **MCP gives AI systems capabilities.**
> **MCL defines how those capabilities are used.**

### Conceptual model

* MCP = integration layer (tools, data access)
* MCL = orchestration layer (workflow, rules, control)

Or more simply:

* MCP = what an AI *can do*
* MCL = what an AI *should do*

---

## Core concepts

MCL is built around a small set of explicit primitives:

### Resources

Data sources and destinations.

Examples:

* databases
* files
* APIs

Defined with explicit access modes:

* `read`
* `write`
* `read_write`

---

### Tools

Executable capabilities exposed via MCP.

Examples:

* find customer
* update record
* send request

---

### Policies

Constraints and governance rules:

* retries
* execution limits
* approval conditions

---

### Workflow

The ordered sequence of steps the agent must follow.

Supported actions include:

* `read_resource`
* `write_resource`
* `tool_call`
* `assign`
* `transform`
* `condition`
* `for_each`
* `emit`

---

### Outputs

Controlled projection of final results.

---

## Example

```yaml
version: "0.1"

agent:
  name: "vip_report_agent"

resources:
  - id: orders_db
    type: database
    uri: "postgres://sales/orders"
    mode: read

  - id: reports_store
    type: service
    uri: "crm://reports"
    mode: write

tools:
  - id: find_customer
    mcp_tool: "find_customer"

workflow:
  - step: load_orders
    action: read_resource
    resource: orders_db
    query:
      days: 7
    output: recent_orders

  - step: select_vip_orders
    action: transform
    input: recent_orders
    operation: filter
    where: "${item['total'] > 1000}"
    output: vip_orders

  - step: write_report
    action: write_resource
    resource: reports_store
    value: "${vip_orders}"
```

---

## What makes MCL different

Without MCL:

* agents rely on prompts and implicit logic
* behavior varies between executions
* errors are discovered late
* tool and data usage is loosely controlled

With MCL:

* workflows are explicit and structured
* behavior is predictable
* validation happens before execution
* tool and data access is controlled
* execution is auditable

---

## Current status

MCL is currently a **prototype / research project**.

Already implemented:

* declarative workflow DSL
* Pydantic models
* semantic validation
* safe expression engine
* static expression analysis
* mock runtime
* mock MCP tool adapter
* mock resource adapter
* audit logging

Still evolving:

* contracts and schema validation
* MCP-native runtime integration
* CLI tooling
* developer experience

---

## Getting started

Clone the repository:

```bash
git clone https://github.com/zenoardoj/MCL-Lang.git
cd MCL-Lang
```

Install:

```bash
pip install -e .
```

Run an example:

```bash
python main.py
```

Run tests:

```bash
pytest
```

---


## Example workflows

- [order_analysis.yaml](examples/order_analysis.yaml)
- [vip_update_collection.yaml](examples/vip_update_collection.yaml)
- [vip_report_agent.yaml](examples/vip_report_agent.yaml)

## Quick demo

Run the default example:

```bash
python main.py
```

Run a specific example:

```bash
python main.py examples/order_analysis.yaml
```

Show audit details:

```bash
python main.py --show-audit --show-calls
```
---

## Why this matters

Most AI systems today rely on:

* prompts
* loosely structured orchestration
* runtime assumptions

MCL explores a different approach:

> define agent behavior in a **structured, validated, inspectable language**

This makes agents:

* more predictable
* easier to debug
* easier to govern
* safer to run in real environments

---

## Roadmap

See [ROADMAP.md](ROADMAP.md)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## Manifesto

See [MANIFESTO.md](MANIFESTO.md)

---

## Final note

MCL is not about making AI agents more powerful.

It is about making them:

* predictable
* governable
* auditable
* reliable

---

## One-line summary

> MCP exposes capabilities.
> MCL defines behavior.
