# SETUP — Configuración paso a paso

Tiempo total: ~15-20 minutos. Lo hacés una sola vez.

---

## PARTE 1 — Google Sheets como base de datos

### 1.1. Subir el Excel a Google Drive
1. Andá a https://drive.google.com (logueate con tu cuenta Google).
2. Clic en **+ Nuevo** → **Subir archivo** → elegí `data/catalogo.xlsx`.
3. Cuando termine de subir, doble clic en el archivo.
4. Arriba te va a aparecer "Archivo ▸ Abrir con Google Sheets" o un botón "Abrir con". Abrí con Google Sheets.
5. Guardá como Google Sheets (File → Save as Google Sheets). Ahora tenés una versión editable online.

### 1.2. Publicar el sheet como CSV
1. Con el sheet abierto: **Archivo** → **Compartir** → **Publicar en la Web**.
2. En "Vincular", elegí la hoja **"Catalogo"** (NO "Todo el documento", NO "LEEME").
3. En formato, elegí **"Valores separados por comas (.csv)"**.
4. Clic **Publicar**. Confirmá si te pregunta.
5. Copiá la URL larga que te muestra (algo como `https://docs.google.com/spreadsheets/d/e/2PACX-XXX.../pub?output=csv`).

### 1.3. Pegar esa URL en el catálogo
1. Abrí `index.html` en cualquier editor de texto.
2. Buscá el bloque `CONFIG` (está a mitad del archivo, es fácil de encontrar).
3. Pegá tu URL entre las comillas de `sheetCsvUrl`:

```js
const CONFIG = {
  sheetCsvUrl: 'https://docs.google.com/spreadsheets/d/e/2PACX-XXX.../pub?output=csv',
  whatsappNumber: '59898240357',
  ...
};
```

4. Guardá el archivo.

### 1.4. Probar que funcione
1. Abrí `index.html` con doble clic o sirviéndolo desde un server local.
2. Cambiá algo en el Google Sheet (ej: el precio de un perfume).
3. Esperá ~30-60 segundos, recargá el catálogo.
4. Deberías ver el nuevo valor.

> **⚠️ Importante**: Google Sheets publicado cachea ~5 minutos. Si los cambios tardan, esperá un poco o forzá refresh con Ctrl+Shift+R.

---

## PARTE 2 — Desplegar en Vercel con GitHub

### 2.1. Crear el repositorio en GitHub
1. Crear cuenta gratis en https://github.com si no tenés.
2. Arriba a la derecha: **+** → **New repository**.
3. Nombre: `salvador-perfumeria` (o lo que quieras).
4. Dejá en **Public** (necesario para Vercel free).
5. NO marques "Initialize with README" (vamos a subir los nuestros).
6. **Create repository**.

### 2.2. Subir los archivos al repo
Opción fácil (sin terminal):
1. En la página del repo recién creado, clic **"uploading an existing file"**.
2. Arrastrá TODOS los archivos de la carpeta `fede/` (menos `node_modules/`, `.vercel`, `preview_*.png`).
3. Abajo escribí un mensaje de commit (ej: "Primera versión") y clic **Commit changes**.

Opción con terminal (si tenés git instalado):
```bash
cd fede/
git init
git add .
git commit -m "Primera versión"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/salvador-perfumeria.git
git push -u origin main
```

### 2.3. Conectar Vercel
1. Crear cuenta en https://vercel.com con tu GitHub (Login with GitHub).
2. **Add New...** → **Project**.
3. Elegí el repo `salvador-perfumeria`.
4. Framework Preset: **Other** (detección automática).
5. Root Directory: dejá en **./**.
6. Clic **Deploy**.
7. En 30 segundos tenés una URL tipo `salvador-perfumeria-XXX.vercel.app`.

### 2.4. Pegar esa URL en el catálogo (para los links de WhatsApp)
1. Abrí `index.html` de nuevo.
2. En `CONFIG`, completá:

```js
catalogUrl: 'https://salvador-perfumeria-XXX.vercel.app',
```

3. Guardá.
4. Volvé a subir el archivo al repo (o `git push` si usás terminal).
5. Vercel re-despliega solo en ~30 segundos.

> Esto hace que los mensajes de WhatsApp incluyan el link directo al perfume consultado.

### 2.5. (Opcional) Poner un nombre más lindo al dominio Vercel
1. En el dashboard de Vercel → proyecto → **Settings** → **Domains**.
2. Podés renombrar el subdominio de .vercel.app a lo que quieras (si está disponible).
3. Ej: `salvador-perfumeria.vercel.app`.

---

## Flujo a partir de acá

### El vendedor (día a día):
1. Abre el Google Sheet.
2. Edita precios, marca SI/NO stock, agrega perfumes, marca promos.
3. Cierra la pestaña. Listo.

### Vos (ajustes puntuales):
- Ajustes al diseño, nuevos filtros, cambios de texto: editás `index.html` → commit a GitHub → Vercel redesplega solo.
- Nada que hacer para actualizaciones del catálogo (eso lo maneja el vendedor directo en el sheet).

---

## Troubleshooting

**"El sheet lo cambié hace rato y no se actualiza en el catálogo"**
- Google cachea la publicación CSV ~5 minutos. Esperá.
- Asegurate de haber pulsado "Publicar" después de editar (en algunos casos hay que republicar).
- Ctrl+Shift+R para forzar recarga.

**"Las imágenes de los perfumes no cargan"**
- Las URLs pueden caducar o bloquearse por el sitio origen.
- En el sheet, en la columna **Imagen URL**, podés reemplazar por otra URL pública.
- O buscá la foto en Google Images, clic derecho "Copiar dirección de imagen", pegala ahí.

**"Quiero cambiar el número de WhatsApp"**
- Editá `CONFIG.whatsappNumber` en `index.html`, commitealo.

**"Quiero agregar una promo con porcentaje de descuento"**
- Completá `Precio (UYU)` con el precio promocional, `Precio antes (UYU)` con el precio normal, y `Promocion` = SI. El HTML calcula y muestra ambos.

---

## Siguientes pasos sugeridos

- Ir cargando más perfumes en el sheet (agregar filas, mantener ID único).
- Cuando tengan fotos propias de los frascos, subir las imágenes a Google Drive (con permiso de lectura pública) o Imgur, y pegar el link en `Imagen URL`.
- Customizar el texto de bienvenida del WhatsApp si el vendedor quiere otra cosa (ej: "Hola! Vi tu catálogo y me interesa...").
- Si crece mucho: considerar agregar categorías (Árabes, Minis, Body splash), filtros por rango de precio, orden por precio, etc.
