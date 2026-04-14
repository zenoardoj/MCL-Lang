from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from pprint import pprint

from mcl.audit.logger import AuditLogger
from mcl.parser.loader import load_document
from mcl.runtime.executor import ExecutionError, Executor
from mcl.runtime.mcp_adapter import MockMcpAdapter
from mcl.runtime.resource_adapter import MockResourceAdapter
from mcl.validator.errors import SemanticValidationError
from mcl.validator.semantic_validator import validate_semantics


DEFAULT_EXAMPLE = "examples/vip_report_agent.yaml"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run an MCL workflow using mock adapters."
    )
    parser.add_argument(
        "workflow",
        nargs="?",
        default=DEFAULT_EXAMPLE,
        help=f"Path to an MCL workflow file (default: {DEFAULT_EXAMPLE})",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print final outputs as JSON instead of pretty text.",
    )
    parser.add_argument(
        "--show-context",
        action="store_true",
        help="Print the final runtime context.",
    )
    parser.add_argument(
        "--show-audit",
        action="store_true",
        help="Print the audit log.",
    )
    parser.add_argument(
        "--show-calls",
        action="store_true",
        help="Print tool calls and resource adapter calls.",
    )
    return parser.parse_args()


def print_banner(workflow_path: Path) -> None:
    print("=" * 72)
    print("MCL Demo Runner")
    print("=" * 72)
    print(f"Workflow file : {workflow_path}")
    print()


def print_section(title: str) -> None:
    print()
    print("-" * 72)
    print(title)
    print("-" * 72)


def ensure_file_exists(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Workflow file not found: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Workflow path is not a file: {path}")


def run_workflow(workflow_path: Path) -> int:
    print_banner(workflow_path)

    try:
        ensure_file_exists(workflow_path)

        print("[1/4] Loading workflow...")
        document = load_document(workflow_path)

        print("[2/4] Validating semantics...")
        validate_semantics(document)

        print("[3/4] Initializing mock adapters...")
        tool_adapter = MockMcpAdapter()
        resource_adapter = MockResourceAdapter()
        audit_logger = AuditLogger()

        print("[4/4] Executing workflow...")
        executor = Executor(
            document=document,
            adapter=tool_adapter,
            resource_adapter=resource_adapter,
            audit_logger=audit_logger,
        )

        outputs = executor.execute()

        print()
        print("✅ Execution completed successfully.")
        print(f"Agent name    : {document.agent.name}")
        if document.agent.description:
            print(f"Description   : {document.agent.description}")

        print_section("Final outputs")
        return_data = {
            "outputs": outputs,
            "context": executor.context.snapshot(),
            "audit": audit_logger.dump(),
            "tool_calls": tool_adapter.calls,
            "resource_reads": resource_adapter.read_calls,
            "resource_writes": resource_adapter.write_calls,
        }

        args = parse_args()

        if args.json:
            print(json.dumps(outputs, indent=2, ensure_ascii=False))
        else:
            pprint(outputs)

        if args.show_context:
            print_section("Runtime context")
            pprint(return_data["context"])

        if args.show_audit:
            print_section("Audit log")
            pprint(return_data["audit"])

        if args.show_calls:
            print_section("Tool calls")
            pprint(return_data["tool_calls"])

            print_section("Resource reads")
            pprint(return_data["resource_reads"])

            print_section("Resource writes")
            pprint(return_data["resource_writes"])

        return 0

    except FileNotFoundError as exc:
        print()
        print(f"❌ File error: {exc}", file=sys.stderr)
        return 1

    except SemanticValidationError as exc:
        print()
        print("❌ Semantic validation failed.", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 2

    except ExecutionError as exc:
        print()
        print("❌ Workflow execution failed.", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 3

    except Exception as exc:
        print()
        print("❌ Unexpected error.", file=sys.stderr)
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return 99


if __name__ == "__main__":
    cli_args = parse_args()
    workflow = Path(cli_args.workflow)
    raise SystemExit(run_workflow(workflow))
