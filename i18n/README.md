# Traduções / Translations

`qgis_studio_themes_pt_BR.ts` holds the plugin's Brazilian Portuguese texts;
`qgis_studio_themes_pt_BR.qm` is the compiled file the plugin loads
(`studio_i18n.py`) when QGIS runs in Portuguese (Settings > Options >
General > Locale, or the system's language). Every other language shows
the English texts.

## Como as traduções foram escolhidas

Cada mensagem do `.ts` traz, em `translatorcomment`, a sua origem:

1. **QGIS** – a tradução pt_BR oficial do QGIS (`i18n/qgis_pt_BR.ts` do
   repositório qgis/QGIS) para o mesmo texto;
   **QGIS (termo)** – o termo que o QGIS usa num texto mais longo
   (ex.: "Reselect" → "Reselecionar", de "Reselecionar feições").
2. **QRibbonSkin** – o catálogo pt-BR do plugin QRibbonSkin, quando o QGIS
   não tem o texto.
3. **Tradução própria** – quando nenhum dos dois tem.

**Correção da tradução do QGIS** marca os poucos casos em que a tradução do
QGIS existe mas está errada para este uso (ex.: "Selection Toolbar" →
"barra de ferramentas", "Stretch" → "Trecho", "Duplicate" → "Duplicata");
o comentário cita a tradução original.

Os nomes internos (nomes das abas salvos nas configurações, objectNames,
valores das configurações) continuam em inglês: só o texto exibido é
traduzido.

## Editar / compilar

Edit the `.ts` with Qt Linguist (context `QgisStudioThemes`), then compile:

```bash
lrelease i18n/qgis_studio_themes_pt_BR.ts -qm i18n/qgis_studio_themes_pt_BR.qm
```

(`pyside6-lrelease` from `pip install PySide6-Essentials` works too.)
A new text in the code goes through `studio_i18n.tr()` where it is shown and
needs an entry in the `.ts`. Texts used with two meanings carry a
disambiguation (`<comment>`): `toolbar name`, `short toolbar name`,
`toolbar abbreviation`.
