---
name: refero-design-research
description: Investigación y adaptación de patrones UI/UX inspirados en Refero. Usar para auditar referencias de Refero, extraer tokens, colores, tipografía, layout, componentes y prompts de diseño, y convertirlos en especificaciones Next.js/Tailwind reutilizables sin inventar valores.
---

# Refero Design Research

Aplicar esta skill cuando el usuario proporcione una página de Refero/Refero Styles o pida convertir una referencia visual en un sistema de diseño implementable.

## Fuentes recopiladas

- `references/elevenlabs-style-reference.md`: extracción de la página ElevenLabs Style Reference indicada por el usuario.
- `references/refero-web-apps-catalog.md`: catálogo público visible en Refero Web Apps al momento de la investigación.
- `references/prompt-pack.md`: prompts de componentes y de composición derivados de la referencia.
- `references/refero-style-library-30.md`: DESIGN.md completo de 49 fichas públicas adicionales, incluyendo Notion, Stripe, Figma, Anthropic, Cohere, Linear, Vercel, OpenAI, Cursor y otras.
- `references/refero-style-library-30.json`: dataset estructurado con marca, URL, estado y colores detectados.
- `references/refero-style-library-expanded.md`: índice legible de **656 fichas únicas** descubiertas en las búsquedas públicas solicitadas: Kids & family product, Non-boring enterprise, Neon crypto dark, Friendly startup, Immersive 3D scenes, Like Stripe, Newsletter landing y Bauhaus geometry.
- `references/refero-style-library-expanded.jsonl`: dataset completo, una línea por ficha, con URL, consultas de descubrimiento, colores hex detectados y DESIGN.md público completo; las 656 fichas respondieron correctamente.
- `references/refero-web-apps-full-catalog.md` y `references/refero-ios-apps-full-catalog.md`: capturas legibles de los catálogos y categorías visibles de ambas galerías.
- `references/refero-search-sources.md`: inventario de las capturas de búsqueda realizadas desde la pestaña activa.
- `scripts/collect_refero_styles.py`: extractor reproducible con concurrencia acotada para nuevas búsquedas de la biblioteca.
- `scripts/collect_refero_expanded.py`: extractor en lote para consolidar múltiples búsquedas y preservar cada DESIGN.md como JSONL sin truncarlo.
- `templates/elevenlabs-theme.css`: variables CSS listas para importar.
- `templates/elevenlabs-tailwind-theme.css`: tokens Tailwind v4 equivalentes.
- `downloads/ElevenLabs-DESIGN.md` y `downloads/ElevenLabs-theme.css`: copias locales de los artefactos disponibles en los paneles públicos.
- `downloads/Ramp-DESIGN.md`: DESIGN.md completo de la ficha Ramp solicitada explícitamente.
- `downloads/Ramp-public-page.html`: snapshot público de Ramp que conserva el contenido serializado de DESIGN.md, Tailwind v4, CSS Variables, Design Tokens, Compact y Extended.

## Flujo obligatorio

1. Abrir la URL indicada en el navegador del usuario, sin iniciar sesión si no es necesario.
2. Para lotes de 10+ referencias, descubrir los enlaces desde la biblioteca y procesar las fichas con `scripts/collect_refero_styles.py` o `scripts/collect_refero_expanded.py`; conservar errores explícitos.
3. Capturar primero la identidad visual, luego las pestañas `DESIGN.md`, `Tailwind v4`, `CSS Variables`, `Design Tokens`, `Compact` y `Extended`. Cuando una captura serializa paneles no activos, conservar también el HTML fuente para permitir su extracción posterior.
4. Registrar valores exactos y separar hechos observados de recomendaciones interpretadas.
5. En una galería, registrar categorías, nombres, descripciones y enlaces públicos visibles; no afirmar que se revisaron páginas individuales que no se abrieron. Los lotes ampliados se identifican como fichas públicas descubiertas y descargadas, no como auditorías visuales manuales de cada producto.
6. Convertir la referencia a tokens semánticos antes de escribir componentes.
7. Implementar con Next.js App Router, TypeScript y Tailwind CSS; evitar CSS monolítico y valores hardcodeados fuera de tokens.
8. Verificar contraste, responsive behavior, estados hover/focus/disabled, accesibilidad y rendimiento.

## Reglas de interpretación

- Tratar HTML de ejemplo como reconstrucción visual, no como código fuente del producto.
- Conservar la separación entre colores de UI y colores decorativos; no convertir un acento gráfico en CTA sin evidencia.
- Preferir variables semánticas (`--color-surface`, `--color-text-primary`) y mapear los valores de Refero a ellas.
- Si una tipografía no está disponible, documentar fallback y mantener peso, tracking y line-height.
- No copiar marcas, logos, fotografías, fuentes propietarias o código privado; reutilizar tokens, patrones y prompts como referencia de diseño y mantener atribución a Refero/ElevenLabs.
- No modificar archivos preexistentes del repositorio: añadir únicamente archivos dentro de esta skill.

## Formato de salida recomendado

Entregar un Blueprint en español con: intención visual, tokens, layout, componentes, estados, responsive, prompts utilizados, fuentes y límites de la extracción. Para código, incluir tamaños exactos, clases Tailwind y criterios de QA.
