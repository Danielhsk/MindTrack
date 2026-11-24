"""Añade al Informe APA7 existente la comparación en test y notas de protocolo (sin regenerar el documento)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from docx import Document
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "Informe final MindTrack.docx"
TEST_CSV = ROOT / "reports" / "comparison_test.csv"
MARKER = "ADDENDUM_COMPARACION_TEST_2026"


def insert_paragraph_after(paragraph: Paragraph, text: str = "") -> Paragraph:
    new_p = OxmlElement("w:p")
    paragraph._p.addnext(new_p)
    new_para = Paragraph(new_p, paragraph._parent)
    if text:
        new_para.add_run(text)
    return new_para


def body_after(anchor: Paragraph, text: str) -> Paragraph:
    p = insert_paragraph_after(anchor, text)
    p.paragraph_format.first_line_indent = anchor.paragraph_format.first_line_indent
    return p


def main() -> None:
    if not OUT.exists():
        raise FileNotFoundError(f"No existe {OUT}")
    doc = Document(OUT)
    if any(MARKER in p.text for p in doc.paragraphs):
        print("Addendum ya presente; no se modifica el informe.")
        return

    anchor_idx = None
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip() == "Discusión":
            anchor_idx = i
            break
    if anchor_idx is None:
        raise RuntimeError("No se encontró el encabezado 'Discusión' para insertar el addendum.")

    anchor = doc.paragraphs[anchor_idx - 1]  # párrafo anterior a Discusión

    blocks = [
        (MARKER, False),
        (
            "Actualización metodológica (comparación simétrica en prueba). "
            "Complemento al informe: los umbrales se calibran únicamente en validación "
            "(recall clase 1 ≥ 0,85); el conjunto de prueba se reserva para comparar los tres "
            "modelos con el mismo τ, sin re-ajuste. Esta corrección alinea el Laboratorio "
            "(Arena de modelos: bloques «Validación» y «Test · los tres modelos») con los "
            "artefactos comparison_validation.csv y comparison_test.csv.",
            True,
        ),
        (
            "En validación, Logistic Regression lideró F1 (0,819) y registró menos falsas "
            "alarmas (FP=31). En prueba, los tres candidatos cumplieron recall ≥0,85; al "
            "ordenar por F1, PR-AUC, precisión, menor FP y menor FN, XGBoost quedó primero "
            "(F1=0,824; PR-AUC=0,933; FN=16; FP=35). Random Forest alcanzó el menor FN en "
            "prueba (12) pero con mayor FP (46). La producción adopta XGBoost por desempeño "
            "agregado en prueba, no por una única celda en validación.",
            True,
        ),
    ]

    cursor = anchor
    for text, is_body in blocks:
        if is_body:
            cursor = body_after(cursor, text)
        else:
            cursor = insert_paragraph_after(cursor, text)

    if TEST_CSV.exists():
        df = pd.read_csv(TEST_CSV)
        cols = [
            "Modelo",
            "Recall (C1)",
            "Precision (C1)",
            "F1-Score (C1)",
            "PR-AUC",
            "FN",
            "FP",
        ]
        df = df[[c for c in cols if c in df.columns]]
        for c in df.select_dtypes(include="float").columns:
            df[c] = df[c].map(lambda x: f"{x:.3f}")
        rows = [df.columns.tolist()] + df.astype(str).values.tolist()
        title = "13\nComparación de modelos en prueba (umbrales fijados en validación)"
        cap = insert_paragraph_after(cursor, "")
        cap.add_run(title).bold = True
        table = doc.add_table(rows=len(rows), cols=len(rows[0]))
        table.style = "Table Grid"
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                table.rows[i].cells[j].text = val
        tbl = table._tbl
        cap._p.addnext(tbl)
        cursor = insert_paragraph_after(cap, "")

        cursor = body_after(
            cursor,
            "Despliegue reproducible: además de Streamlit local y Streamlit Cloud, el repositorio "
            "incluye Dockerfile y docker compose up para ejecutar la aplicación con modelos y "
            "reportes versionados (documentación en docs/DOCKER.md).",
        )

    for i, p in enumerate(doc.paragraphs):
        if p.text.strip().startswith("Apéndice B: Comandos de reproducibilidad"):
            # siguiente párrafo con comandos
            if i + 1 < len(doc.paragraphs):
                cmd_para = doc.paragraphs[i + 1]
                body_after(
                    cmd_para,
                    "Docker (demo): docker compose up --build; acceso en http://localhost:8501.",
                )
            break

    doc.save(OUT)
    print(f"Addendum insertado en {OUT}")


if __name__ == "__main__":
    main()