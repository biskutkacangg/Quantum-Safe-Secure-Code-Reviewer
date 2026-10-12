"""
test_graph_e2e.py — End-to-end verification of LangGraph State Machine with HITL interrupt
"""
import sys
from pathlib import Path
from langgraph.types import Command

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from pqc_agent.graph import build_graph
from langgraph.checkpoint.memory import MemorySaver

print("=" * 60)
print("Testing LangGraph End-to-End Workflow with HITL Interrupt...")
print("=" * 60)

with open("sample_files/vulnerable_python.py", "r", encoding="utf-8") as f:
    source_code = f.read()

checkpointer = MemorySaver()
graph = build_graph(checkpointer=checkpointer)
config = {"configurable": {"thread_id": "test-e2e-thread-1"}}

initial_state = {
    "source_code": source_code,
    "file_name": "vulnerable_python.py",
    "language": "python",
    "findings": [],
    "scan_summary": "",
    "chain_of_thought": "",
    "uncertainty_statement": "",
    "risk_assessment": "",
    "patches": [],
    "human_decision": "pending",
    "human_feedback": "",
    "audit_trail": [],
    "current_phase": "start",
    "error": "",
    "messages": [],
}

print("\nStep 1: Running graph until HITL interrupt...")
# Stream until interrupt
state_snapshot = None
for event in graph.stream(initial_state, config, stream_mode="values"):
    phase = event.get("current_phase", "unknown")
    print(f"  -> State reached phase: {phase}")
    state_snapshot = event

# Check if interrupted
state = graph.get_state(config)
print(f"\nGraph interrupted at: {state.next}")
assert "human_approval" in state.next or "finalise" in state.next, "Expected graph to pause at HITL node"

findings = state.values.get("findings", [])
patches = state.values.get("patches", [])
print(f"Captured {len(findings)} findings and {len(patches)} patches before interrupt.")
assert len(findings) > 0, "No findings in state"
assert len(patches) > 0, "No patches in state"

print("\nStep 2: Resuming graph with Human Approval via Command(resume=...)...")
resume_payload = {
    "decision": "approved",
    "feedback": "Approved by Senior Cryptographer for ML-KEM and ML-DSA transition pilot."
}

final_state = None
for event in graph.stream(Command(resume=resume_payload), config, stream_mode="values"):
    phase = event.get("current_phase", "unknown")
    print(f"  -> Resumed state phase: {phase}")
    final_state = event

assert final_state.get("human_decision") == "approved"
assert final_state.get("current_phase") == "complete"
audit = final_state.get("audit_trail", [])
print(f"\nFinal Audit Trail ({len(audit)} entries):")
for entry in audit:
    print(f"  - [{entry['actor'].upper()}] {entry['action']}: {entry['detail'][:60]}...")

print("\n" + "=" * 60)
print("[PASS] Complete LangGraph HITL interrupt & resume lifecycle verified!")
print("=" * 60)
