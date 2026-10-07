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
- `templates/elevenlabs-theme.css`: variables CSS listas para importar.
- `templates/elevenlabs-tailwind-theme.css`: tokens Tailwind v4 equivalentes.
- `downloads/ElevenLabs-DESIGN.md` y `downloads/ElevenLabs-theme.css`: copias locales de los artefactos disponibles en los paneles públicos.

## Flujo obligatorio

1. Abrir la URL indicada en el navegador del usuario, sin iniciar sesión si no es necesario.
2. Capturar primero la identidad visual, luego las pestañas `DESIGN.md`, `Tailwind v4`, `CSS Variables` y `Design Tokens`.
3. Registrar valores exactos y separar hechos observados de recomendaciones interpretadas.
4. En una galería, registrar categorías, nombres, descripciones y enlaces públicos visibles; no afirmar que se revisaron páginas individuales que no se abrieron.
5. Convertir la referencia a tokens semánticos antes de escribir componentes.
6. Implementar con Next.js App Router, TypeScript y Tailwind CSS; evitar CSS monolítico y valores hardcodeados fuera de tokens.
7. Verificar contraste, responsive behavior, estados hover/focus/disabled, accesibilidad y rendimiento.

## Reglas de interpretación

- Tratar HTML de ejemplo como reconstrucción visual, no como código fuente del producto.
- Conservar la separación entre colores de UI y colores decorativos; no convertir un acento gráfico en CTA sin evidencia.
- Preferir variables semánticas (`--color-surface`, `--color-text-primary`) y mapear los valores de Refero a ellas.
- Si una tipografía no está disponible, documentar fallback y mantener peso, tracking y line-height.
- No copiar marcas, logos, fotografías, fuentes propietarias o código privado; reutilizar tokens, patrones y prompts como referencia de diseño y mantener atribución a Refero/ElevenLabs.
- No modificar archivos preexistentes del repositorio: añadir únicamente archivos dentro de esta skill.

## Formato de salida recomendado

Entregar un Blueprint en español con: intención visual, tokens, layout, componentes, estados, responsive, prompts utilizados, fuentes y límites de la extracción. Para código, incluir tamaños exactos, clases Tailwind y criterios de QA.
