#!/usr/bin/env python3
"""Validate the local multi-skill repository without third-party dependencies."""
from __future__ import annotations
import argparse, ast, json, re, sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESERVED_RE = re.compile(r"(?:claude|anthropic)", re.I)
RESOURCE_RE = re.compile(r"(?:`|\()((?:scripts|references|assets)/[^\s`)]+)")
LOCAL_PATH_RE = re.compile(r"(?:[A-Za-z]:\\Users\\|/c/Users/|/home/[^/\s]+/)", re.I)
PLACEHOLDERS = (
    "Describe when this skill should be used.",
    "First step\n2. Second step",
    "A brief description of what this skill does",
)

def parse_frontmatter(path: Path) -> tuple[dict[str,str], str]:
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        raise ValueError('missing opening YAML frontmatter delimiter')
    end = text.find('\n---\n', 4)
    if end < 0:
        raise ValueError('missing closing YAML frontmatter delimiter')
    raw = text[4:end]
    data: dict[str,str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith('#') or line.startswith((' ', '\t')):
            continue
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        data[key.strip()] = value
    return data, text[end+5:]

def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill = skill_dir / 'SKILL.md'
    if not skill.is_file():
        return [f'{skill_dir.name}: missing SKILL.md']
    try:
        fm, body = parse_frontmatter(skill)
    except Exception as exc:
        return [f'{skill_dir.name}: {exc}']
    name = fm.get('name','')
    desc = fm.get('description','')
    if not NAME_RE.fullmatch(name): errors.append(f'{skill_dir.name}: invalid name {name!r}')
    if name != skill_dir.name: errors.append(f'{skill_dir.name}: name must match parent directory')
    if not (1 <= len(desc) <= 1024): errors.append(f'{skill_dir.name}: description must be 1..1024 characters')
    if RESERVED_RE.search(name) or RESERVED_RE.search(desc): errors.append(f'{skill_dir.name}: reserved term found in name/description')
    lines = skill.read_text(encoding='utf-8').splitlines()
    if len(lines) > 500: errors.append(f'{skill_dir.name}: SKILL.md has {len(lines)} lines (>500)')
    whole = skill.read_text(encoding='utf-8')
    for marker in PLACEHOLDERS:
        if marker in whole: errors.append(f'{skill_dir.name}: template placeholder remains: {marker!r}')
    if LOCAL_PATH_RE.search(whole): errors.append(f'{skill_dir.name}: absolute user-local path found in SKILL.md')
    if '../' in whole or '..\\' in whole: errors.append(f'{skill_dir.name}: parent traversal reference found in SKILL.md')
    for match in RESOURCE_RE.finditer(whole):
        ref = re.sub(r"[`\]\)'\",.;:]+$", '', match.group(1))
        if not (skill_dir / ref).exists(): errors.append(f'{skill_dir.name}: referenced resource does not exist: {ref}')
    eval_file = skill_dir / 'evals' / 'evals.json'
    if not eval_file.is_file():
        errors.append(f'{skill_dir.name}: missing evals/evals.json')
    else:
        try:
            data = json.loads(eval_file.read_text(encoding='utf-8'))
            if data.get('skill_name') != skill_dir.name: errors.append(f'{skill_dir.name}: eval skill_name mismatch')
            cases = data.get('evals', [])
            if not isinstance(cases, list) or len(cases) < 2: errors.append(f'{skill_dir.name}: evals must contain at least 2 cases')
        except Exception as exc:
            errors.append(f'{skill_dir.name}: invalid evals/evals.json: {exc}')
    for script in (skill_dir / 'scripts').glob('*.py') if (skill_dir / 'scripts').is_dir() else []:
        try: ast.parse(script.read_text(encoding='utf-8'), filename=str(script))
        except SyntaxError as exc: errors.append(f'{skill_dir.name}: Python syntax error in {script.name}: {exc}')
    return errors

def main() -> int:
    ap=argparse.ArgumentParser(description='Validate all Agent Skills in this repository.')
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1], help='Repository root')
    ap.add_argument('--json', action='store_true', help='Emit JSON')
    args=ap.parse_args()
    root=args.root.resolve(); skills=root/'skills'; errors=[]
    for required in ('README.md','docs/SKILLS_GUIDE.md','docs/AUTHORING.md'):
        if not (root/required).exists(): errors.append(f'repository: missing {required}')
    if not skills.is_dir(): errors.append('repository: missing skills/ directory')
    else:
        dirs=sorted(p for p in skills.iterdir() if p.is_dir())
        if not dirs: errors.append('repository: no skill directories found')
        for d in dirs: errors.extend(validate_skill(d))
    result={'ok': not errors, 'skill_count': len([p for p in skills.iterdir() if p.is_dir()]) if skills.is_dir() else 0, 'errors': errors}
    if args.json: print(json.dumps(result, indent=2))
    else:
        if errors:
            print('Validation failed:')
            for e in errors: print(f' - {e}')
        else: print(f"Validation passed for {result['skill_count']} skills.")
    return 0 if not errors else 1
if __name__=='__main__': raise SystemExit(main())
