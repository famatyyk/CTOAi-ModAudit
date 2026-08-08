# CTOAi-ModAudit

Statyczny audyt modów gier (Factorio / Minecraft / ogólny).

## Co sprawdza
- ✅ Obecność i poprawność manifestu (info.json / manifest.json)
- ✅ Ryzykowne wzorce w Lua (`load`, `loadstring`, `os.execute`, `socket`)
- ✅ Podejrzanie duże pliki binarne
- ❌ NIE uruchamia moda, NIE instalguje, NIE czyta sekretów

## Użycie
```bash
python src/auditor.py sciezka/do/moda
```

## Bezpieczeństwo
Audyt jest static-only. Pomaga modderom wykryć ryzyka w ich własnych
modach przed publikacją. Nie służy do łamania cudzych modów.

## Powiązane
- Audyt Lua/C++: https://ctoai-funnel.fly.dev/ (Mod Audit 19 €)


## Free Tool & Pro Version

Start free: **[CTOAi-Lint](https://github.com/famatyyk/CTOAi-Lint)** — `pip install git+https://github.com/famatyyk/CTOAi-Lint` (C++/Lua/Python static linter, zero deps).

Need a full audit (C++, Lua, Python, JS, TS, CMake, GitHub Action CI)? → **[CTOAi Funnel](https://ctoai-funnel.fly.dev/)**
