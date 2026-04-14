# MCL Specification

## Version 0.6 (Draft)
> Draft specification. The language is still evolving.
---

## 1. Overview

MCL (**MCP Coordination Language**) is a declarative language for defining AI agent workflows over:

* resources
* tools
* policies
* structured execution steps
* controlled outputs

MCL is designed to work naturally on top of **MCP (Model Context Protocol)**.

> MCP exposes capabilities.
> MCL defines behavior.

MCL is **not** a general-purpose programming language.
It is a coordination language for expressing agent workflows in a way that is:

* explicit
* validatable
* governable
* auditable
* easier for LLMs to generate reliably

---

## 2. Design goals

MCL is designed around the following goals:

### 2.1 Declarative workflow definition

A workflow should describe *what the agent does* and *in what order*, without requiring arbitrary code.

### 2.2 Explicit operational boundaries

Resources, tools, policies, and outputs should all be declared explicitly.

### 2.3 Pre-execution validation

Where possible, errors should be detected before execution.

### 2.4 Safe expression evaluation

Dynamic expressions should be limited to a constrained, safe subset.

### 2.5 Auditability

Every execution step should be inspectable and traceable.

### 2.6 AI-first structure

The language should be easy for LLMs to produce consistently.

---

## 3. Relationship to MCP

MCL is not a replacement for MCP.

### MCP provides:

* access to tools
* access to external systems
* data connectivity
* operational capabilities

### MCL provides:

* orchestration
* sequencing
* policy-aware execution
* explicit control over data and action flow

Conceptually:

* **MCP** = capability layer
* **MCL** = coordination layer

---

## 4. Source format

The canonical source format of MCL v0.6 is **YAML**.

Future representations may include:

* JSON
* visual editors
* alternative text syntaxes

The semantic model of MCL is independent of YAML as a format.

---

## 5. Document structure

An MCL document is a single structured object with the following top-level sections:

```yaml
version: "0.1"
agent: {}
resources: []
tools: []
policies: {}
workflow: []
outputs: {}
```

### Required fields

* `version`
* `agent`
* `workflow`

### Optional fields

* `resources`
* `tools`
* `policies`
* `outputs`

---

## 6. Core concepts

### 6.1 Agent

Defines the logical identity of the workflow.

### 6.2 Resources

Define where the agent can read or write data.

### 6.3 Tools

Define executable external capabilities.

### 6.4 Policies

Define constraints such as retries, approvals, and limits.

### 6.5 Workflow

Defines the ordered set of execution steps.

### 6.6 Outputs

Defines which runtime values are exposed as final output.

---

## 7. Agent definition

Example:

```yaml
agent:
  name: "vip_report_agent"
  description: "Reads recent orders and stores a VIP report"
```

### Fields

#### `name`

String. Required.
Logical identifier of the workflow.

#### `description`

String. Optional.
Human-readable explanation of the workflow purpose.

---

## 8. Resources

Resources define data sources or destinations.

Example:

```yaml
resources:
  - id: orders_db
    type: database
    uri: "postgres://sales/orders"
    mode: read

  - id: reports_store
    type: service
    uri: "crm://reports"
    mode: write
```

### Fields

#### `id`

String. Required.
Unique resource identifier within the document.

#### `type`

String. Required.
Semantic category of the resource.

Suggested values:

* `database`
* `service`
* `file`
* `folder`
* `document_store`
* `api`
* `queue`

#### `uri`

String. Required.
Canonical location or identifier of the resource.

#### `mode`

String. Required.
Access mode.

Allowed values:

* `read`
* `write`
* `read_write`

---

## 9. Tools

Tools define executable external capabilities.

Example:

```yaml
tools:
  - id: find_customer
    mcp_tool: "find_customer"
```

### Fields

#### `id`

String. Required.
Unique identifier used inside the workflow.

#### `mcp_tool`

String. Required.
Underlying MCP tool name.

#### `description`

String. Optional.

#### `input_schema`

Object. Optional.
Reserved for future contract validation.

#### `output_schema`

Object. Optional.
Reserved for future contract validation.

---

## 10. Policies

Policies define execution constraints.

Example:

```yaml
policies:
  retries:
    max_attempts: 1
  limits:
    max_steps: 100
    max_tool_calls: 20
  approvals:
    - tool: update_customer_status
      when: "payload['status'] == 'vip'"
```

### Policy sections

#### `retries`

Controls retry behavior.

Supported fields:

* `max_attempts`

#### `limits`

Controls execution bounds.

Supported fields:

* `max_items`
* `max_steps`
* `max_tool_calls`

#### `approvals`

Defines approval conditions for tool invocation.

Each entry may contain:

* `tool`
* `when`

Approval expressions are evaluated in a scope where `payload` is available.

---

## 11. Workflow

The `workflow` section is an ordered list of steps.

Each step must include:

* `step`
* `action`

Example:

```yaml
workflow:
  - step: load_orders
    action: read_resource
    resource: orders_db
    query:
      days: 7
    output: recent_orders
```

---

## 12. Supported actions

MCL v0.6 supports the following actions:

* `read_resource`
* `write_resource`
* `tool_call`
* `assign`
* `transform`
* `condition`
* `for_each`
* `emit`

---

## 13. `read_resource`

Reads data from a declared resource.

Example:

```yaml
- step: load_orders
  action: read_resource
  resource: orders_db
  query:
    days: 7
  output: recent_orders
```

### Fields

* `resource` — resource identifier
* `query` — optional structured query object
* `output` — required output variable name

### Semantics

The runtime must:

1. verify the resource exists
2. verify the resource mode allows reading
3. resolve interpolations in `query`
4. read via the resource adapter
5. save the result in `output`

---

## 14. `write_resource`

Writes data to a declared resource.

Example:

```yaml
- step: write_report
  action: write_resource
  resource: reports_store
  value: "${vip_report}"
  output: write_result
```

### Fields

* `resource` — resource identifier
* `value` — data to write
* `output` — optional result variable

### Semantics

The runtime must:

1. verify the resource exists
2. verify the resource mode allows writing
3. resolve interpolations in `value`
4. write via the resource adapter
5. optionally store the adapter result in `output`

---

## 15. `tool_call`

Invokes a declared tool.

Example:

```yaml
- step: load_customer
  action: tool_call
  tool: find_customer
  input:
    customer_id: "${order['customer_id']}"
  output: customer
```

### Fields

* `tool` — declared tool identifier
* `input` — optional input object
* `output` — optional output variable

### Semantics

The runtime must:

1. verify the tool exists
2. evaluate policy constraints
3. resolve interpolations in input
4. invoke the MCP tool
5. optionally store the result in `output`

---

## 16. `assign`

Stores a resolved value in the runtime context.

Example:

```yaml
- step: set_threshold
  action: assign
  value: 1000
  output: vip_threshold
```

### Fields

* `value`
* `output`

### Semantics

The runtime resolves the value and stores it in the global runtime context.

---

## 17. `transform`

Performs a structured transformation on an input collection.

Supported operations:

* `filter`
* `map`
* `count`

### Example: filter

```yaml
- step: select_vip_orders
  action: transform
  input: recent_orders
  operation: filter
  where: "${item['total'] > vip_threshold}"
  output: vip_orders
```

### Example: map

```yaml
- step: extract_customer_ids
  action: transform
  input: vip_orders
  operation: map
  expr: "${item['customer_id']}"
  output: vip_customer_ids
```

### Example: count

```yaml
- step: count_vips
  action: transform
  input: vip_orders
  operation: count
  output: vip_count
```

### Fields

* `input`
* `operation`
* `where` (required for `filter`)
* `expr` (required for `map`)
* `output`

### Scope

During `filter` and `map`, the symbol `item` is available.

---

## 18. `condition`

Defines a conditional branch.

Example:

```yaml
- step: check_high_value
  action: condition
  if: "${order['total'] > vip_threshold}"
  then:
    - step: mark_vip
      action: emit
      target: vip_orders
      value: "${order}"
  else: []
```

### Fields

* `if`
* `then`
* `else` (optional)

### Semantics

The condition expression must evaluate to a boolean value.

---

## 19. `for_each`

Iterates over a list.

Example:

```yaml
- step: iterate_vip_orders
  action: for_each
  items: vip_orders
  as: order
  do:
    - step: load_customer
      action: tool_call
      tool: find_customer
      input:
        customer_id: "${order['customer_id']}"
      output: customer
```

### Fields

* `items`
* `as`
* `do`

### Scope

Inside the loop body, the symbol named in `as` is available.

---

## 20. `emit`

Appends a resolved value to a named collection.

Example:

```yaml
- step: collect_report_row
  action: emit
  target: vip_report
  value:
    order_id: "${order['id']}"
    customer_id: "${customer['id']}"
```

### Fields

* `target`
* `value`

### Semantics

If the target collection does not exist, it is created as a list.
The resolved value is appended to that list.

---

## 21. Outputs

The `outputs` section defines which values are exposed at the end of execution.

Example:

```yaml
outputs:
  format: json
  include:
    - vip_report
    - write_result
```

### Fields

#### `format`

Currently supported:

* `json`

#### `include`

List of variable names to expose.

If omitted, the runtime may expose the full context snapshot depending on implementation.

---

## 22. Expressions

MCL supports a restricted expression language for interpolation and conditions.

Expressions are used inside the form:

```yaml
"${ ... }"
```

Example:

```yaml
"${order['total'] > vip_threshold}"
```

### Supported capabilities

* variable references
* dictionary/list subscript access
* arithmetic operators
* comparison operators
* boolean operators
* inline conditional expressions
* selected whitelisted functions

### Allowed functions

* `len`
* `sum`
* `min`
* `max`

### Not allowed

* attribute access (`customer.id`)
* method calls
* arbitrary Python execution
* imports
* lambdas
* comprehensions
* keyword arguments

Use:

```yaml
"${customer['id']}"
```

instead of:

```yaml
"${customer.id}"
```

---

## 23. Scope rules

MCL has explicit runtime scopes.

### Global scope

Contains values produced by previous steps.

### `for_each` scope

Adds the loop variable declared in `as`.

### `transform` scope

Adds the symbol `item`.

### Approval scope

When evaluating policy approval expressions, `payload` is available.

---

## 24. Validation model

MCL validation has two levels:

### 24.1 Structural validation

Checks:

* required fields
* field types
* step shape
* allowed action structure

### 24.2 Semantic validation

Checks:

* duplicate identifiers
* unknown tools
* unknown resources
* invalid resource access mode
* undefined symbols in expressions
* invalid expressions
* undefined outputs
* invalid step references

---

## 25. Error model

MCL implementations should distinguish between:

### Parse errors

Invalid YAML or invalid source format.

### Schema errors

Invalid document structure.

### Semantic errors

Invalid references, symbols, permissions, or expressions.

### Runtime errors

Failures during actual execution.

### Policy violations

Execution blocked by declared constraints or approvals.

---

## 26. Execution model

An MCL runtime should:

1. load the document
2. validate structure
3. validate semantics
4. initialize runtime context
5. execute steps in order
6. apply policies
7. collect outputs
8. emit audit information

---

## 27. Auditability

Every execution should be auditable.

At minimum, each step should record:

* step name
* action type
* start timestamp
* end timestamp
* success/failure
* related tool or resource, if applicable
* error, if any
* retry count, if applicable

---

## 28. Conformance expectations

An implementation can be considered minimally compatible with MCL v0.6 if it supports:

* YAML source parsing
* all actions defined in this spec
* structural validation
* semantic validation
* restricted expression evaluation
* audit logging
* resources and tools as distinct concepts

---

## 29. Non-goals

MCL is not intended to support:

* arbitrary scripting
* general-purpose application development
* classes or inheritance
* embedded unrestricted Python
* free-form execution logic
* unconstrained extensibility

---

## 30. Future directions

Planned or possible future directions include:

* stronger schema contracts for tools and resources
* richer policy model
* CLI tooling
* MCP-native runtime adapters
* conformance profiles
* editor support
* visualization tools

---

## 31. Summary

MCL is a declarative coordination language for AI agents.

It exists to make agent workflows:

* more explicit
* more predictable
* more governable
* more auditable
* easier to validate before execution

Its role is not to replace programming languages or MCP.

Its role is to provide the missing orchestration layer above capability exposure.
