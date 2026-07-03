# story-to-carousel · carruseles de marca desde un JSON

Genera carruseles de Instagram (1080×1080 PNG) **desde un archivo de contenido** (JSON), sin diseñar a mano y sin escribir HTML. Corre sobre [forge-studio-lite](https://github.com/) (el generador de la comunidad): tú describes la historia y la marca en un JSON, este script arma los slides HTML, y forge los captura a PNG con Playwright. **100% local, determinístico, $0.**

> Aporte a la comunidad Imperio Agéntico por **FIBISER**. Nació de necesitar sacar contenido de marca consistente rápido, para dos líneas de negocio distintas, sin pelear con HTML cada vez.

## Por qué

forge-studio-lite ya captura HTML a PNG de forma impecable. Lo que faltaba: que **el contenido y la marca sean datos**, no código. Con esto, hacer un carrusel nuevo = editar un JSON de 30 líneas y correr un comando. Cambiar de marca = cambiar la paleta. Ideal para agencias que manejan varios clientes o varias líneas.

## Cómo se usa

1. Ten clonado y con dependencias instaladas `forge-studio-lite` (Node + Playwright).
2. Coloca `story-to-carousel.py` donde quieras y apunta `FORGE_ROOT` al repo de forge:
   ```bash
   export FORGE_ROOT=/ruta/a/forge-studio-lite   # (en Windows: $env:FORGE_ROOT=...)
   ```
3. Escribe tu `story.json` (ver `ejemplo-story.json`).
4. Genera los slides y captúralos:
   ```bash
   python3 story-to-carousel.py story.json
   cd "$FORGE_ROOT" && npx tsx --env-file=.env src/pipelines/carousel.ts .
   ```
   Salida: `slides/slide-01.png … slide-NN.png`.

## El formato de la historia (JSON)

```jsonc
{
  "palette": "dark-orange",          // preset, o un objeto con tus hex
  "brand": "TU <span class=\"b\">MAR</span>CA",  // el <span class="b"> se pinta con el color primario
  "tag": "LO QUE VA EN EL PIE",
  "slides": [
    { "kicker": "...", "headline": "Texto con [hl]resaltado[/hl]", "support": "Texto con [b]negrita[/b]" },
    { "kicker": "...", "headline": "...", "list": ["punto 1", "punto 2", "punto 3"] },
    { "kicker": "...", "chips": ["Etiqueta A", "Etiqueta B"], "support": "..." },
    { "kicker": "...", "quote": "Una cita destacada", "support": "..." },
    { "kicker": "...", "headline": "...", "support": "...", "cta": "Tu llamado a la acción" }
  ]
}
```

**Bloques por slide** (usa los que quieras, en el orden que quieras): `kicker`, `big` (número/símbolo gigante), `headline`, `quote`, `list`, `chips`, `support`, `cta`.
**Marcado en textos:** `[hl]...[/hl]` = color primario · `[b]...[/b]` = texto fuerte · saltos de línea con `\n`.

## Paletas

Trae dos presets listos (`dark-orange` y `dark-blue`). Para tu marca, pasa un objeto en `palette` con tus hex: `bg`, `surface`, `primary`, `primary_deep`, `accent`, `steel`, `glow`.

## Estructura recomendada de un carrusel (5 slides)

Hook → problema → cómo funciona (lista) → prueba/caso → CTA. El valor está en la **historia** y tu **marca**, no en efectos.

## Licencia

MIT. Úsalo, adáptalo, comparte lo que construyas. Si te sirvió, cuéntalo en el grupo 🙌
