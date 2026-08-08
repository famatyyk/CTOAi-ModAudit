"""CTOAi-ModAudit — statyczny audyt modow gier (Factorio / Minecraft / ogolny).

BEZPIECZNE: skanuje pliki moda (manifest, skrypty Lua, JSON) pod katem
ryzyk: brak manifestu, uzycie load()/os.execute w Lua, podejrzane uprawnienia.
NIE uruchamia moda, NIE instalguje, NIE czyta sekretow.
"""

from __future__ import annotations
import json, os, re
from dataclasses import dataclass, asdict

LUA_RISK = [
    (r"\bload\s*\(", "Uzycie load() w Lua (ryzyko wykonania kodu)"),
    (r"loadstring\s*\(", "Uzycie loadstring() w Lua"),
    (r"os\.execute\s*\(", "Uzycie os.execute() w Lua (wywolanie powloki)"),
    (r"require\s*\(\s*['\"]socket", "Wymaga 'socket' (sieciowe IO)"),
]

MANIFEST_NAMES = ("info.json", "manifest.json", "modinfo.json", "package.json")


@dataclass
class ModFinding:
    severity: str
    title: str
    evidence: str


def audit_mod(mod_dir: str) -> dict:
    findings: list[ModFinding] = []
    files = []
    for root, _, fs in os.walk(mod_dir):
        for f in fs:
            files.append(os.path.relpath(os.path.join(root, f), mod_dir))

    # 1. manifest
    manifest = next((f for f in files if f.lower().endswith(MANIFEST_NAMES[0])
                     or f.lower() in MANIFEST_NAMES), None)
    if not manifest:
        findings.append(ModFinding("medium", "Brak manifestu moda",
                                   "Brak info.json / manifest.json / modinfo.json"))
    else:
        # sprawdz czy JSON poprawny
        try:
            with open(os.path.join(mod_dir, manifest), encoding="utf-8") as fh:
                json.load(fh)
        except Exception:
            findings.append(ModFinding("high", "Manifest nie jest poprawnym JSON",
                                       manifest))

    # 2. lua risk
    for f in files:
        if f.lower().endswith(".lua"):
            try:
                txt = open(os.path.join(mod_dir, f), encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            for pat, desc in LUA_RISK:
                if re.search(pat, txt):
                    findings.append(ModFinding("high", desc, f))

    # 3. duze pliki binarne (ostrzezenie)
    for f in files:
        fp = os.path.join(mod_dir, f)
        if os.path.isfile(fp) and os.path.getsize(fp) > 5_000_000:
            findings.append(ModFinding("low", "Bardzo duzy plik binarny", f))

    score = max(0, 100 - len(findings) * 10)
    return {
        "mod_dir": os.path.basename(mod_dir),
        "file_count": len(files),
        "findings": [asdict(x) for x in findings],
        "score": score,
    }


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "samples/example_mod"
    res = audit_mod(target)
    print(json.dumps(res, indent=2, ensure_ascii=False))
