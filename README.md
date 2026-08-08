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
