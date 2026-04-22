# Fede — Catálogo Salvador Perfumería

Catálogo web de perfumes con backend en Google Sheets. El vendedor edita un sheet online; el catálogo se actualiza solo. Hosting gratis en Vercel.

## Cómo funciona

```
Vendedor edita                HTML lee el sheet         Cliente ve
Google Sheet        ───▶      al cargar la página  ───▶ el catálogo
(online, desde                (fetch CSV cada vez                 
 celular o PC)                 que alguien entra)                 
```

Sin servidores, sin base de datos, sin que nadie toque código cuando cambia un precio.

## Setup inicial

**Seguí los pasos en [SETUP.md](SETUP.md)** — lleva 15 minutos, una vez y listo.

Resumen:
1. Crear una cuenta de Google (si no tenés).
2. Importar `data/catalogo.xlsx` a Google Sheets.
3. Publicar ese sheet como CSV → copiar la URL.
4. Pegar la URL en `index.html` (en el bloque `CONFIG.sheetCsvUrl`).
5. Subir el proyecto a GitHub y conectarlo con Vercel.

## Archivos del proyecto

```
fede/
├── index.html           → el catálogo web (todo en uno)
├── data/catalogo.xlsx   → seed para importar a Google Sheets la primera vez
├── build_excel.py       → script para regenerar el xlsx base (no se usa en producción)
├── SETUP.md             → guía paso a paso de configuración
├── vercel.json          → config de Vercel
├── .gitignore
└── README.md
```

## Flujo de uso (después del setup)

Para el **vendedor**:
- Abre el Google Sheet.
- Cambia `Stock` a SI/NO para activar/desactivar un perfume.
- Cambia el valor en `Precio (UYU)`.
- Para una promo: `Promocion` → SI, y opcionalmente completa `Precio antes (UYU)` para mostrar el precio tachado.
- Guarda. En 30 segundos - 5 minutos los cambios se reflejan en el catálogo web.
- No hay que avisar a nadie, no hay que correr nada.

Para **vos**:
- Compartís la URL de Vercel (ej: `salvador-perfumeria.vercel.app`).
- La pegás en la bio de Instagram, la mandás por WhatsApp, donde quieras.

## Características

- **Fuente de datos en vivo**: el HTML consulta el Google Sheet cada vez que alguien entra, con cache de 30 segundos.
- **Mensaje WhatsApp inteligente**: cada botón "Consultar" genera un mensaje con marca, producto, precio y un link directo al perfume en el catálogo. El vendedor ve exactamente de qué producto le preguntan.
- **Deep links**: cuando abrís `catalogo.com/#p=5` la página scrollea al producto 5 y lo resalta.
- **Mobile-first**: diseño pensado primero para celular (la mayoría de consultas van a venir de Instagram).
- **Fallback offline**: trae datos embebidos por si el sheet falla — el catálogo nunca queda vacío.
- **Fotos de perfumes**: URL configurable por producto (por defecto usa la CDN pública de Fragrantica).

## Stack

HTML + Vanilla JS + PapaParse (para leer el CSV). Sin frameworks, sin backend, sin build step.

## Personalizar después

Cosas que podés cambiar editando `index.html`:

- **Paleta**: variables CSS `--azul`, `--dorado`, etc. al inicio del `<style>`.
- **Tipografías**: el `<link>` de Google Fonts.
- **Mensaje WhatsApp**: `CONFIG.whatsappIntro`.
- **Número WhatsApp**: `CONFIG.whatsappNumber`.
- **Nombre marca**: buscar "Salvador Perfumería" y reemplazar.
- **Instagram**: buscar `@salvadorperfumeria`.
