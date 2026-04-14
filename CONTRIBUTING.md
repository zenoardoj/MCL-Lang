# Contributing to MCL

Thanks for your interest in contributing.

MCL is still in an early stage, so contributions are highly valuable — but require alignment with the core philosophy.

---

## Project philosophy

MCL aims to be:

* declarative
* explicit
* constrained
* predictable

When contributing, prefer:

* clarity over cleverness
* simplicity over abstraction
* validation over flexibility

---

## Where to contribute

### Language design

* improving semantics
* clarifying behavior
* reducing ambiguity

### Validation

* improving static checks
* better error messages
* catching more issues before runtime

### Runtime

* execution behavior
* error handling
* audit improvements

### MCP alignment

* tool integration
* resource modeling
* adapter design

### Examples

* real-world workflows
* minimal reproducible cases

### Documentation

* clarity improvements
* better explanations
* reducing ambiguity

---

## What to avoid (for now)

* adding complex syntax
* embedding general-purpose code
* introducing uncontrolled flexibility
* large refactors without discussion

If in doubt, open an issue first.

---

## Development setup

```bash
git clone <repo>
cd mcl
pip install -e .
pytest
```

Run example:

```bash
python main.py
```

---

## How to propose changes

### Small changes

* open a PR
* include explanation
* add tests if needed

### Larger changes

1. open an issue
2. describe:

   * the problem
   * the proposal
   * why it fits MCL

---

## Code guidelines

* keep code simple and explicit
* avoid hidden logic
* prefer small functions
* fail early with clear errors

---

## Testing

Important contributions should include:

* semantic validation tests
* execution tests
* edge cases

---

## Final note

MCL is intentionally constrained.

If something feels missing, it may be by design.

The goal is not maximum power.

The goal is **reliable, governable AI workflows**.
