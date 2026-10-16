"""Genera siete figuras estáticas del catálogo común en visualizaciones/."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import metrics as M
from src.prep import explode, load_clean

OUT = Path(__file__).resolve().parents[1] / "visualizaciones"
C_PEL, C_SER, GRIS = "#1f4e79", "#f28e2b", "#8c8c8c"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False})


def _save(fig, name):
    OUT.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=160)
    plt.close(fig)


def f1_evolucion(df):
    a = M.por_anio(df)
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.plot(a.anio, a["Película"], marker="o", color=C_PEL, label="Películas")
    ax.plot(a.anio, a["Serie"], marker="o", color=C_SER, label="Series")
    ax.set_ylim(0, a[["Película", "Serie"]].max().max() * 1.3)
    ax.set_title("Títulos por año de estreno y tipo (2010–2025)", loc="left", weight="bold")
    ax.set_xlabel("Año de estreno")
    ax.set_ylabel("Títulos")
    ax.legend(frameon=False)
    ax.text(2010, a[["Película", "Serie"]].max().max() * 1.12,
            "Nota: el número por año es casi constante; no permite inferir crecimiento real del catálogo.",
            fontsize=8, color=GRIS)
    _save(fig, "f1_evolucion_anual.png")


def f2_paises(df):
    p = M.top_paises(df).iloc[::-1]
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.barh(p.country, p.titulos, color=C_PEL)
    for i, v in enumerate(p.titulos):
        ax.text(v + 80, i, f"{v:,}", va="center", fontsize=8)
    ax.set_title("Top 10 países por número de títulos (películas y series)", loc="left", weight="bold")
    ax.set_xlabel("Títulos (un título puede tener varios países)")
    _save(fig, "f2_top_paises.png")


def f3_generos(df):
    g = M.top_generos(df).iloc[::-1]
    e = explode(df, "genres")
    piv = e[e.genres.isin(g.genres)].groupby(["genres", "tipo"]).size().unstack(fill_value=0).reindex(g.genres)
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    left = np.zeros(len(piv))
    for tipo, col in [("Película", C_PEL), ("Serie", C_SER)]:
        ax.barh(piv.index, piv[tipo], left=left, color=col, label=tipo + "s")
        left += piv[tipo].values
    ax.set_title("Top 10 géneros por volumen y tipo", loc="left", weight="bold")
    ax.set_xlabel("Títulos (un título puede tener varios géneros)")
    ax.legend(frameon=False, loc="lower right")
    _save(fig, "f3_generos.png")


def f4_idiomas(df):
    i = M.idiomas(df).iloc[::-1]
    fig, ax = plt.subplots(figsize=(7.5, 4.0))
    left = np.zeros(len(i))
    for tipo, col in [("Película", C_PEL), ("Serie", C_SER)]:
        ax.barh(i.idioma, i[tipo], left=left, color=col, label=tipo + "s")
        left += i[tipo].values
    ax.set_title("Idiomas principales del catálogo (código ISO)", loc="left", weight="bold")
    ax.set_xlabel("Títulos")
    ax.legend(frameon=False, loc="lower right")
    _save(fig, "f4_idiomas.png")


def f5_popularidad_calificacion(df):
    eligible = df[df.votos_suficientes & (df.popularidad > 0)]
    d = eligible.sample(n=min(6000, len(eligible)), random_state=42)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for tipo, col in [("Película", C_PEL), ("Serie", C_SER)]:
        s = d[d.tipo == tipo]
        ax.scatter(s.popularidad, s.calificacion, s=np.clip(s.votos / 200, 4, 120),
                   alpha=0.35, color=col, label=tipo + "s", edgecolor="none")
    ax.set_xscale("log")
    ax.set_xlabel("Popularidad (escala log; índice de la fuente)")
    ax.set_ylabel("Calificación promedio (0–10)")
    ax.set_title(f"Popularidad vs. calificación (muestra n={len(d):,})",
                 loc="left", weight="bold")
    ax.legend(frameon=False, markerscale=2, loc="lower right")
    _save(fig, "f5_popularidad_calificacion.png")


def f6_presupuesto_ingresos(df):
    f = df[df.tiene_finanzas]
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.scatter(f.presupuesto / 1e6, f.ingresos / 1e6, s=10, alpha=0.4, color=C_PEL, edgecolor="none")
    x = np.logspace(-0.5, 3, 50)
    ax.plot(x, x, color=GRIS, lw=1, ls="--")
    ax.plot(x, 3 * x, color=C_SER, lw=1, ls="--")
    ax.text(0.006, 0.9, "--- gris: ingresos = presupuesto (ROI 0 %)", transform=ax.transAxes, fontsize=8, color=GRIS)
    ax.text(0.006, 0.84, "--- naranja: ingresos = 3× presupuesto (ROI 200 %)", transform=ax.transAxes, fontsize=8, color=C_SER)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("Presupuesto (USD millones, log)")
    ax.set_ylabel("Ingresos (USD millones, log)")
    ax.set_title(f"Presupuesto vs. ingresos, películas con ambos datos (n={len(f):,})",
                 loc="left", weight="bold")
    _save(fig, "f6_presupuesto_ingresos.png")


def f7_paises_calificacion(df):
    p = M.paises_calificacion(df, min_titulos=30).head(10).iloc[::-1]
    fig, ax = plt.subplots(figsize=(7.5, 4.0))
    ax.barh(p.country, p.calificacion_prom, color=C_PEL)
    ax.set_xlim(0, 10)
    for i, v in enumerate(p.calificacion_prom):
        ax.text(v + 0.01, i, f"{v:.2f} (n={int(p.titulos.iloc[i])})", va="center", fontsize=8)
    ax.set_title("Calificación promedio por país (≥30 títulos con votos suficientes)",
                 loc="left", weight="bold")
    ax.set_xlabel("Calificación promedio (0 a 10)")
    _save(fig, "f7_paises_calificacion.png")


def main():
    df = load_clean()
    for fn in [f1_evolucion, f2_paises, f3_generos, f4_idiomas,
               f5_popularidad_calificacion, f6_presupuesto_ingresos, f7_paises_calificacion]:
        fn(df)
    print("figuras:", sorted(p.name for p in OUT.glob("*.png")))


if __name__ == "__main__":
    main()
