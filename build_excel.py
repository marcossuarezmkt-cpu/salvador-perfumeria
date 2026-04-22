"""Genera catalogo.xlsx — seed para importar a Google Sheets.

El Excel es solo el punto de partida: lo importás a Google Sheets UNA VEZ,
después el vendedor edita online y el catálogo web se actualiza solo.
"""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

wb = Workbook()
ws = wb.active
ws.title = "Catalogo"

AZUL = "0B3D91"
AZUL_CLARO = "E8F0FE"
BLANCO = "FFFFFF"
GRIS = "6B7280"

headers = [
    "ID", "Marca", "Nombre", "Genero", "Tamaño (ml)",
    "Notas / Descripcion", "Precio (UYU)", "Precio antes (UYU)",
    "Stock", "Promocion", "Imagen URL"
]

# URLs de Fragrantica CDN (fimgs.net) — imágenes oficiales de los perfumes
# Patrón: https://fimgs.net/mdimg/perfume/375x500.{fragrantica_id}.jpg
IMG = lambda fid: f"https://fimgs.net/mdimg/perfume/375x500.{fid}.jpg"

# Top 10 perfumes benchmark Uruguay — con imágenes
data = [
    (1,  "Dior",              "Sauvage EDT",           "Hombre", 100, "Bergamota, pimienta de Sichuán, ambroxan. Fresco y especiado.",     10600, None, "SI", "NO", IMG(31861)),
    (2,  "Paco Rabanne",      "One Million EDT",       "Hombre", 100, "Cuero, canela, pomelo sangriento. Dulce y magnético.",               4590, 5100, "SI", "SI", IMG(3747)),
    (3,  "Carolina Herrera",  "212 VIP Men NYC EDT",   "Hombre", 100, "Gin tónic, menta, cuero vegetal. Fresco, nocturno.",                 5800, None, "SI", "NO", IMG(12865)),
    (4,  "Giorgio Armani",    "Acqua di Giò EDT",      "Hombre", 100, "Marino, bergamota, pachulí. Fresco acuático icónico.",               7500, None, "SI", "NO", IMG(410)),
    (5,  "Paco Rabanne",      "Invictus EDT",          "Hombre", 100, "Pomelo, laurel marino, ambergris. Deportivo y magnético.",           5200, None, "SI", "NO", IMG(18471)),
    (6,  "Carolina Herrera",  "Good Girl EDP",         "Mujer",   80, "Jazmín, almendra, cacao, tonka. Floral dulce elegante.",             6800, None, "SI", "NO", IMG(39681)),
    (7,  "Lancôme",           "La Vie Est Belle EDP",  "Mujer",  100, "Iris, pera, pachulí, vainilla. Gourmand luminoso.",                  8200, None, "SI", "NO", IMG(14982)),
    (8,  "Chanel",            "Coco Mademoiselle EDP", "Mujer",  100, "Rosa, jazmín, pachulí, vetiver. Oriental chic atemporal.",          10500, None, "SI", "NO", IMG(611)),
    (9,  "Yves Saint Laurent","Libre EDP",             "Mujer",   90, "Lavanda, azahar, vainilla madagascar. Floral sensual moderno.",      9200, None, "SI", "NO", IMG(56077)),
    (10, "Carolina Herrera",  "212 VIP Rosé EDP",      "Mujer",   80, "Champagne rosé, frutos rojos, musgo blanco. Festivo y femenino.",    5850, 6500, "SI", "SI", IMG(22857)),
]

ws.append(headers)
for col_idx, _ in enumerate(headers, 1):
    c = ws.cell(row=1, column=col_idx)
    c.font = Font(name="Arial", bold=True, color=BLANCO, size=11)
    c.fill = PatternFill("solid", start_color=AZUL)
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = Border(bottom=Side(style="medium", color=AZUL))

for row in data:
    ws.append(row)

thin = Side(style="thin", color="D1D5DB")
for row_idx in range(2, 2 + len(data)):
    fill = BLANCO if row_idx % 2 == 0 else AZUL_CLARO
    for col_idx in range(1, len(headers) + 1):
        c = ws.cell(row=row_idx, column=col_idx)
        c.font = Font(name="Arial", size=10)
        c.fill = PatternFill("solid", start_color=fill)
        c.border = Border(left=thin, right=thin, top=thin, bottom=thin)
        c.alignment = Alignment(vertical="center", wrap_text=True)
    ws.cell(row=row_idx, column=7).number_format = '"$"#,##0'
    ws.cell(row=row_idx, column=7).alignment = Alignment(horizontal="right", vertical="center")
    ws.cell(row=row_idx, column=8).number_format = '"$"#,##0;;-'
    ws.cell(row=row_idx, column=8).alignment = Alignment(horizontal="right", vertical="center")
    ws.cell(row=row_idx, column=1).alignment = Alignment(horizontal="center", vertical="center")
    for c_idx in (4, 5, 9, 10):
        ws.cell(row=row_idx, column=c_idx).alignment = Alignment(horizontal="center", vertical="center")
    if ws.cell(row=row_idx, column=10).value == "SI":
        for col_idx in range(1, len(headers) + 1):
            ws.cell(row=row_idx, column=col_idx).fill = PatternFill("solid", start_color="FDF4E0")

widths = {"A": 6, "B": 20, "C": 28, "D": 10, "E": 10, "F": 55,
          "G": 14, "H": 16, "I": 10, "J": 12, "K": 55}
for col, w in widths.items():
    ws.column_dimensions[col].width = w

ws.row_dimensions[1].height = 30
for r in range(2, 2 + len(data)):
    ws.row_dimensions[r].height = 40

dv_si_no = DataValidation(type="list", formula1='"SI,NO"', allow_blank=False)
ws.add_data_validation(dv_si_no)
dv_si_no.add("I2:I1000")
dv_promo = DataValidation(type="list", formula1='"SI,NO"', allow_blank=True)
ws.add_data_validation(dv_promo)
dv_promo.add("J2:J1000")
dv_gen = DataValidation(type="list", formula1='"Hombre,Mujer,Unisex"', allow_blank=False)
ws.add_data_validation(dv_gen)
dv_gen.add("D2:D1000")

ws.freeze_panes = "A2"

# Hoja instrucciones
ws2 = wb.create_sheet("LEEME")
inst = [
    ("Cómo usar este catálogo", ""),
    ("", ""),
    ("1. Importá este archivo a Google Sheets:", "Drive → Nuevo → Subir archivo → abrir con Google Sheets"),
    ("2. Publicá el sheet como CSV:", "Archivo → Compartir → Publicar en la web → formato CSV → copiar link"),
    ("3. Pegá ese link en index.html (línea 'CONFIG.sheetCsvUrl').", ""),
    ("4. Subí el proyecto a GitHub y conectalo a Vercel.", ""),
    ("", ""),
    ("De ahí en adelante:", ""),
    ("  • El vendedor edita el Google Sheet desde la computadora o celular.", ""),
    ("  • Los cambios aparecen en el catálogo web en ~30 segundos-5 minutos.", ""),
    ("  • No hay que correr ningún script ni redesplegar nada.", ""),
    ("", ""),
    ("Columnas (NO renombrar ni mover):", ""),
    ("  Stock = SI/NO (si está en stock se ve, si NO se oculta)", ""),
    ("  Promocion = SI/NO (si SI se muestra en la pestaña Promociones con badge dorado)", ""),
    ("  Precio antes (UYU) = solo si está en promo, el precio original tachado", ""),
    ("  Imagen URL = link público a la imagen del frasco", ""),
]
for row in inst:
    ws2.append(row)
ws2["A1"].font = Font(name="Arial", bold=True, color=BLANCO, size=14)
ws2["A1"].fill = PatternFill("solid", start_color=AZUL)
ws2.merge_cells("A1:B1")
ws2["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws2.row_dimensions[1].height = 28
for r in range(3, len(inst) + 1):
    ws2.cell(row=r, column=1).font = Font(name="Arial", size=10, bold=True, color=AZUL)
    ws2.cell(row=r, column=2).font = Font(name="Arial", size=10, color=GRIS)
    ws2.cell(row=r, column=1).alignment = Alignment(vertical="center", wrap_text=True)
    ws2.cell(row=r, column=2).alignment = Alignment(vertical="center", wrap_text=True)
ws2.column_dimensions["A"].width = 55
ws2.column_dimensions["B"].width = 75

import os
out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "catalogo.xlsx")
wb.save(out_path)
print(f"Saved: {out_path}")
