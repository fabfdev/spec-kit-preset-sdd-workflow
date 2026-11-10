import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import sdd  # noqa: E402

APPROVED = '**Approved:** 2026-11-09 — user: "ok"\n'
PRD = """# PRD — Drafts
{approvals}**Size:** {size}

## 2. Requirements
- RF-01: Users can save drafts.
- AC-01 (RF-01): When saving valid content, the system shall persist the draft.
"""
TASKS = """{approval}**Final gate:** `{final}`

## T1 — Persist drafts
**Status:** {status}
**Requirements:** RF-01
**Criteria:** AC-01
**Depends on:** none
**Files:** `src/drafts.py`
**Gate:** `{gate}`

- Implement it.

## Checks
| Criterion | Task | Proof command |
|-----------|------|---------------|
| AC-01 | T1 | `{gate}` |
"""


class SddTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.spec = self.root / "specs" / "drafts"
        self.spec.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def write_full(self, status="pending", gate="true", final="true", approved=True):
        approval = APPROVED if approved else ""
        (self.spec / "prd.md").write_text(PRD.format(approvals=approval, size="full"), encoding="utf-8")
        (self.spec / "techspec.md").write_text("# Techspec\n", encoding="utf-8")
        (self.spec / "tasks.md").write_text(
            TASKS.format(approval=approval, status=status, gate=gate, final=final), encoding="utf-8")

    def call(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = sdd.main(list(args) + ["--root", str(self.root)])
            except sdd.GateError as error:
                return 1, str(error)
        return code, out.getvalue()

    def test_valid_full_plan_reports_next_task(self):
        self.write_full()
        code, out = self.call("validate", "drafts")
        self.assertEqual(code, 0)
        self.assertIn("tasks 0/1 done; next: T1 — Persist drafts", out)

    def test_execute_requires_approvals(self):
        self.write_full(approved=False)
        self.assertEqual(self.call("validate", "drafts", "--stage", "tasks")[0], 0)
        code, message = self.call("validate", "drafts")
        self.assertEqual(code, 1)
        self.assertIn("approvals", message)

    def test_small_plan_inline_needs_an_approval(self):
        body = PRD.format(approvals=APPROVED, size="small") + TASKS.format(
            approval="", status="pending", gate="true", final="true")
        (self.spec / "prd.md").write_text(body, encoding="utf-8")
        self.assertEqual(self.call("validate", "drafts")[0], 0)
        (self.spec / "prd.md").write_text(body.replace(APPROVED, ""), encoding="utf-8")
        self.assertEqual(self.call("validate", "drafts")[0], 1)

    def test_uncovered_criterion_fails(self):
        self.write_full()
        prd = self.spec / "prd.md"
        prd.write_text(prd.read_text() + "- AC-02 (RF-01): When empty, the system shall reject it.\n")
        code, message = self.call("validate", "drafts")
        self.assertEqual(code, 1)
        self.assertIn("criterion", message)

    def test_v3_four_column_checks_accepted(self):
        self.write_full()
        tasks = self.spec / "tasks.md"
        tasks.write_text(tasks.read_text().replace("| AC-01 | T1 | `true` |", "| AC-01 | T1 | tests::x | `true` |"))
        self.assertEqual(self.call("validate", "drafts")[0], 0)

    def test_check_task_pass_and_fail_tail(self):
        self.write_full(gate="true")
        self.assertEqual(self.call("check", "drafts", "--task", "T1"), (0, "PASS  true\n"))
        script = "for i in $(seq 1 100); do echo line$i; done; exit 3"
        self.write_full(gate=script)
        code, out = self.call("check", "drafts", "--task", "T1")
        self.assertEqual(code, 1)
        self.assertIn("(exit 3)", out)
        self.assertIn("line100", out)
        self.assertNotIn("line60\n", out)

    def test_final_requires_done_and_dedupes(self):
        self.write_full()
        self.assertEqual(self.call("check", "drafts", "--final")[0], 1)
        self.write_full(status="done")
        code, out = self.call("check", "drafts", "--final")
        self.assertEqual((code, out), (0, "PASS  true\n"))

    def test_baseline_runs_final_gate(self):
        self.write_full(final="echo hi")
        self.assertEqual(self.call("check", "drafts", "--baseline"), (0, "PASS  echo hi\n"))


if __name__ == "__main__":
    unittest.main()
