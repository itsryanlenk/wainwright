#!/usr/bin/env python3
"""Validate the plugin layout, skill/agent frontmatter, and copy rules. Stdlib only."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
EM_DASH = chr(0x2014)
# Private or project-specific strings that must never appear in skills, agents, or AGENTS.md.
LEAKS = [
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "email address"),
    (re.compile(r"\b(ryan|lenk|lenker|itsryanlenk|d0t0gg91\w*|eggbot)\b", re.I), "personal name or handle"),
    (re.compile(r"(^|\s)#[a-z][a-z0-9_-]{2,}\b"), "chat channel name"),
    (re.compile(r"[A-Za-z]:[\\/]Users[\\/]|/home/(?!box/)[a-z]+/"), "local user path"),
    (re.compile(r"github\.com/[A-Za-z0-9-]+/[A-Za-z0-9._-]+"), "repository link"),
    (re.compile(r"\b(sk-[A-Za-z0-9]{8,}|xai-[A-Za-z0-9]{8,}|ghp_[A-Za-z0-9]{8,})"), "API key shape"),
]


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, text
    fields, key = {}, None
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            fields[key] = "" if value in (">-", ">", "|", "|-") else value.strip('"')
        elif key and line.startswith("  "):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields, text[end + 5:]


def main():
    errors = []

    def err(msg):
        errors.append(msg)

    manifest_path = ROOT / ".cursor-plugin" / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"FAIL plugin.json: {e}")
        return 1
    if not KEBAB.match(manifest.get("name", "")):
        err("plugin.json: name must be kebab-case")
    for key in ("skills", "agents"):
        if key in manifest and not (ROOT / manifest[key]).is_dir():
            err(f"plugin.json: {key} path {manifest[key]} does not exist")

    try:
        market = json.loads((ROOT / ".cursor-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        for p in market.get("plugins", []):
            if not (ROOT / p.get("source", "")).is_dir():
                err(f"marketplace.json: source {p.get('source')} does not exist")
            if p.get("name") != manifest.get("name"):
                err("marketplace.json: plugin name differs from plugin.json")
    except (OSError, json.JSONDecodeError) as e:
        err(f"marketplace.json: {e}")

    skills = sorted(d for d in (ROOT / "skills").iterdir() if d.is_dir())
    for d in skills:
        if not KEBAB.match(d.name):
            err(f"skills/{d.name}: folder name must be kebab-case")
        if d.name.startswith("candor-"):
            err(f"skills/{d.name}: persona slugs use wainwright-, not the old prefix")
        f = d / "SKILL.md"
        if not f.is_file():
            err(f"skills/{d.name}: missing SKILL.md")
            continue
        fields, body = frontmatter(f)
        if fields is None:
            err(f"skills/{d.name}/SKILL.md: missing frontmatter")
            continue
        if not fields.get("name"):
            err(f"skills/{d.name}/SKILL.md: missing name")
        desc = fields.get("description", "")
        if not desc.startswith("Use when"):
            err(f"skills/{d.name}/SKILL.md: description must start with 'Use when'")
        if not re.search(r"auto-appl", desc, re.I):
            err(f"skills/{d.name}/SKILL.md: description must say whether it auto-applies")
        if len(desc) > 1024:
            err(f"skills/{d.name}/SKILL.md: description over 1024 chars ({len(desc)})")
        if not body.strip():
            err(f"skills/{d.name}/SKILL.md: empty body")

    agents = sorted((ROOT / "agents").glob("*.md"))
    for f in agents:
        if f.name.startswith("candor-"):
            err(f"agents/{f.name}: persona slugs use wainwright-, not the old prefix")
        fields, body = frontmatter(f)
        if not fields or not fields.get("name") or not fields.get("description"):
            err(f"agents/{f.name}: needs name and description frontmatter")
        elif not body.strip():
            err(f"agents/{f.name}: empty body")

    scanned = [p for p in ROOT.rglob("*") if p.is_file() and p.suffix in (".md", ".json")]
    for p in scanned:
        rel = p.relative_to(ROOT).as_posix()
        text = p.read_text(encoding="utf-8")
        if EM_DASH in text:
            err(f"{rel}: contains an em dash")
        if rel.startswith(("skills/", "agents/")) or rel == "AGENTS.md":
            for i, line in enumerate(text.splitlines(), 1):
                for pattern, label in LEAKS:
                    # Markdown headings start with "#" but are not channel names.
                    if label == "chat channel name" and re.match(r"^\s*#+\s", line):
                        continue
                    if pattern.search(line):
                        err(f"{rel}:{i}: {label}: {line.strip()[:80]}")

    for label in ("README.md", "AGENTS.md"):
        text = (ROOT / label).read_text(encoding="utf-8")
        m = re.search(r"(\d+) skills and (\d+) agents", text)
        if m and (int(m.group(1)), int(m.group(2))) != (len(skills), len(agents)):
            err(
                f"{label}: claims {m.group(1)} skills and {m.group(2)} agents, "
                f"found {len(skills)} and {len(agents)}"
            )

    if errors:
        for e in errors:
            print("FAIL", e)
        print(f"RESULT: FAIL ({len(errors)} problems)")
        return 1
    print(f"RESULT: PASS ({len(skills)} skills, {len(agents)} agents, {len(scanned)} files scanned)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
