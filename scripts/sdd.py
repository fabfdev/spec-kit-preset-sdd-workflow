#!/usr/bin/env python3
"""SDD workflow v4 helper: structural validation and compact check runner.

Python 3.8+, standard library only. Semantic review stays with the agent.

  sdd.py validate SLUG [--stage spec|tasks|execute]
  sdd.py check SLUG (--task Tn | --baseline | --final)
"""
import argparse
import re
import subprocess
import sys
from collections import deque
from pathlib import Path

VERSION = "4.2.0"
RF = r"RF-\d+(?:\.\d+)*"
AC = r"AC-\d+"
TAIL_LINES = 40
APPROVAL = r'^\*\*Approved:\*\*\s*\d{4}-\d{2}-\d{2}\s+[—-]\s+user:\s*".+"\s*$'


class GateError(Exception):
    pass


def text(path):
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def field(body, name):
    match = re.search(r"^\*\*" + re.escape(name) + r":\*\*[ \t]*(.+)$", body, re.M)
    return match.group(1).strip() if match else ""


def command(value):
    match = re.fullmatch(r"`([^`\n]+)`", value.strip())
    return match.group(1) if match else ""


def inside(root, value):
    path = (root / value).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        raise GateError("Path escapes project root: " + value)


def load(root, slug):
    directory = root / "specs" / slug
    prd = text(directory / "prd.md")
    if not prd:
        raise GateError("Missing specs/{}/prd.md; run /speckit.specify first".format(slug))
    tasks_path = directory / "tasks.md"
    tasks_text = text(tasks_path) or prd
    tasks = []
    for match in re.finditer(r"^## (T\d+) [—-] ([^\n]+)\n(.*?)(?=^## |\Z)", tasks_text, re.M | re.S):
        task_id, title, body = match.groups()
        tasks.append({"id": task_id, "title": title.strip(), "status": field(body, "Status"),
                      "requirements": re.findall(RF, field(body, "Requirements")),
                      "criteria": re.findall(AC, field(body, "Criteria")),
                      "dependencies": re.findall(r"\bT\d+\b", field(body, "Depends on")),
                      "files": re.findall(r"`([^`]+)`", field(body, "Files")),
                      "gate": command(field(body, "Gate"))})
    checks = []
    section = re.search(r"^## Checks\s*\n(.*?)(?=^## |\Z)", tasks_text, re.M | re.S)
    for line in section.group(1).splitlines() if section else []:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and re.fullmatch(AC, cells[0]):
            # why: v3 plans carry an extra evidence column; the command is always last.
            if len(cells) not in (3, 4):
                raise GateError("Checks rows need Criterion | Task | Proof command; "
                                "move shell pipelines into a project script")
            checks.append({"id": cells[0], "task": cells[1], "command": command(cells[-1])})
    return {"prd": prd, "tasks_text": tasks_text, "full": tasks_path.is_file(),
            "techspec": (directory / "techspec.md").is_file(),
            "requirements": re.findall(r"^- (" + RF + r"): .+", prd, re.M),
            "criteria": re.findall(r"^- (" + AC + r") \((" + RF + r")\): .+", prd, re.M),
            "tasks": tasks, "checks": checks, "final": command(field(tasks_text, "Final gate"))}


def validate(root, slug, stage="execute"):
    data = load(root, slug)
    reqs = data["requirements"]
    criteria = [row[0] for row in data["criteria"]]
    if not reqs or len(reqs) != len(set(reqs)):
        raise GateError("PRD needs unique '- RF-01: ...' requirement lines")
    if not criteria or len(criteria) != len(set(criteria)):
        raise GateError("PRD needs unique '- AC-01 (RF-01): ...' criterion lines")
    if any(row[1] not in reqs for row in data["criteria"]):
        raise GateError("An acceptance criterion references an unknown requirement")
    if set(reqs) != {row[1] for row in data["criteria"]}:
        raise GateError("Every requirement needs at least one acceptance criterion")
    size = field(data["prd"], "Size")
    if size not in ("small", "full"):
        raise GateError("PRD needs **Size:** small or full")
    if stage == "spec":
        return data
    if size == "full" and not (data["techspec"] and data["full"]):
        raise GateError("Full size requires techspec.md and tasks.md")
    tasks = data["tasks"]
    ids = [task["id"] for task in tasks]
    if not tasks or len(ids) != len(set(ids)):
        raise GateError("Need unique '## T1 — Title' task sections")
    if size == "small" and len(tasks) > 3:
        raise GateError("More than three tasks: promote the feature to full size")
    seen = set()
    for task in tasks:
        name = task["id"]
        if task["status"] not in ("pending", "done"):
            raise GateError(name + " **Status:** must be pending or done")
        if not task["gate"] or not task["files"]:
            raise GateError(name + " needs **Files:** and a backticked **Gate:** command")
        for path in task["files"]:
            inside(root, path)
        if not task["requirements"] or not set(task["requirements"]) <= set(reqs):
            raise GateError(name + " has missing or unknown Requirements")
        if not task["criteria"] or not set(task["criteria"]) <= set(criteria):
            raise GateError(name + " has missing or unknown Criteria")
        if not set(task["dependencies"]) <= seen:
            raise GateError(name + " depends on a missing, later or cyclic task")
        seen.add(name)
    if {r for task in tasks for r in task["requirements"]} != set(reqs):
        raise GateError("Uncovered requirement: every RF needs a task")
    if {c for task in tasks for c in task["criteria"]} != set(criteria):
        raise GateError("Uncovered criterion: every AC needs a task")
    if sorted(row["id"] for row in data["checks"]) != sorted(criteria):
        raise GateError("## Checks needs exactly one row per AC")
    by_id = {task["id"]: task for task in tasks}
    for row in data["checks"]:
        task = by_id.get(row["task"])
        if not task or row["id"] not in task["criteria"] or not row["command"]:
            raise GateError("Invalid task or proof command for " + row["id"])
    if not data["final"]:
        raise GateError("Need **Final gate:** `project lint/typecheck/test command`")
    if stage == "execute":
        # why: v3 small features carry one approval covering PRD and inline tasks.
        prd_ok = re.search(APPROVAL, data["prd"], re.M)
        tasks_ok = re.search(APPROVAL, data["tasks_text"], re.M)
        if not prd_ok or not tasks_ok:
            raise GateError("Execution needs recorded user approvals of the PRD and of the tasks")
    return data


def run(root, commands):
    for cmd in dict.fromkeys(commands):
        # hazard: commands come from the user-approved plan and run through the shell.
        process = subprocess.Popen(cmd, cwd=str(root), shell=True, text=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        tail = deque(process.stdout, maxlen=TAIL_LINES)
        code = process.wait()
        if code:
            print("FAIL  {}  (exit {})".format(cmd, code))
            print("".join(tail).rstrip())
            return 1
        print("PASS  " + cmd)
    return 0


def summary(data):
    done = [t for t in data["tasks"] if t["status"] == "done"]
    pending = [t for t in data["tasks"] if t["status"] != "done"]
    ready = next((t for t in pending if all(d in {x["id"] for x in done} for d in t["dependencies"])), None)
    line = "tasks {}/{} done".format(len(done), len(data["tasks"]))
    return line + ("; next: {} — {}".format(ready["id"], ready["title"]) if ready else "; all done")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("action", choices=["validate", "check"])
    parser.add_argument("slug")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--stage", choices=["spec", "tasks", "execute"], default="execute")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--task")
    group.add_argument("--baseline", action="store_true")
    group.add_argument("--final", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
        raise GateError("Feature slug must be lowercase kebab-case")
    if args.action == "validate":
        data = validate(root, args.slug, args.stage)
        print("valid ({})".format(args.stage) + ("" if args.stage == "spec" else "; " + summary(data)))
        return 0
    data = validate(root, args.slug)
    if args.baseline:
        return run(root, [data["final"]])
    if args.final:
        if any(t["status"] != "done" for t in data["tasks"]):
            raise GateError("All tasks must be done before --final")
        return run(root, [row["command"] for row in data["checks"]] + [data["final"]])
    if not args.task:
        raise GateError("check needs --task Tn, --baseline or --final")
    task = next((t for t in data["tasks"] if t["id"] == args.task), None)
    if not task:
        raise GateError("Unknown task " + args.task)
    return run(root, [task["gate"]])


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (GateError, OSError) as error:
        print("SDD: " + str(error), file=sys.stderr)
        sys.exit(1)
