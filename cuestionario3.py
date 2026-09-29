#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratorio de Física III - Programas de Campo Eléctrico (UNMSM)
Solución del cuestionario3.tex

Uso:
    python3 cuestionario3.py            -> resuelve todo y guarda las figuras (PNG)
    python3 cuestionario3.py --interactivo
                                        -> además abre el modo "ingrese (x, y) y
                                           se muestra V" del problema 2
Requiere: numpy, matplotlib
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

K = 8.9875517923e9  # N m^2 / C^2


# ---------------------------------------------------------------------------
# Funciones generales (cargas puntuales en el plano xy)
# cargas = lista de tuplas (q, x, y)
# ---------------------------------------------------------------------------
def campo(cargas, x, y):
    """Devuelve Ex, Ey en el punto (x, y)."""
    Ex = Ey = 0.0
    for q, xq, yq in cargas:
        dx, dy = x - xq, y - yq
        r3 = (dx * dx + dy * dy) ** 1.5
        Ex += K * q * dx / r3
        Ey += K * q * dy / r3
    return Ex, Ey


def potencial(cargas, x, y):
    """V en (x, y), con V = 0 en el infinito."""
    V = 0.0
    for q, xq, yq in cargas:
        r = np.hypot(x - xq, y - yq)
        if r == 0:
            raise ZeroDivisionError("el punto coincide con una carga")
        V += K * q / r
    return V


# ---------------------------------------------------------------------------
# PROBLEMA 1: líneas de campo con el método de pasos  dx = (Ex/E) ds
# ---------------------------------------------------------------------------
def linea_de_campo(cargas, x0, y0, ds=0.02, sentido=+1, nmax=4000, rmin=0.05,
                   lim=4.0):
    """Sigue la línea de campo desde (x0,y0).
    sentido=+1 sigue E (sale de las cargas +), -1 va contra E."""
    xs, ys = [x0], [y0]
    x, y = x0, y0
    for _ in range(nmax):
        Ex, Ey = campo(cargas, x, y)
        E = np.hypot(Ex, Ey)
        if E == 0:
            break
        x += sentido * (Ex / E) * ds     # Δx = (Ex/E) Δs
        y += sentido * (Ey / E) * ds     # Δy = (Ey/E) Δs
        xs.append(x)
        ys.append(y)
        # se detiene al llegar a una carga o al salir de la ventana
        if any(np.hypot(x - xq, y - yq) < rmin for _, xq, yq in cargas):
            break
        if abs(x) > lim or abs(y) > lim:
            break
    return np.array(xs), np.array(ys)


def graficar_lineas(cargas, titulo, archivo, n_lineas=16, lim=3.0):
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    r0 = 0.1
    for q, xq, yq in cargas:
        if q > 0:  # las líneas nacen alrededor de las cargas positivas
            for t in np.linspace(0, 2 * np.pi, n_lineas, endpoint=False):
                xs, ys = linea_de_campo(cargas, xq + r0 * np.cos(t),
                                        yq + r0 * np.sin(t), lim=lim)
                ax.plot(xs, ys, color="tab:blue", lw=1)
    # vectores de campo (normalizados) sobre una malla
    g = np.linspace(-lim, lim, 15)
    X, Y = np.meshgrid(g, g)
    EX = np.zeros_like(X)
    EY = np.zeros_like(Y)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            if min(np.hypot(X[i, j] - xq, Y[i, j] - yq)
                   for _, xq, yq in cargas) < 0.25:
                continue
            EX[i, j], EY[i, j] = campo(cargas, X[i, j], Y[i, j])
    M = np.hypot(EX, EY)
    M[M == 0] = np.nan
    ax.quiver(X, Y, EX / M, EY / M, color="gray", alpha=0.45, scale=30,
              width=0.003)
    for q, xq, yq in cargas:
        ax.plot(xq, yq, "o", ms=13, color="red" if q > 0 else "black")
        ax.text(xq, yq, "+" if q > 0 else "−", color="white", ha="center",
                va="center", fontsize=11, fontweight="bold")
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(titulo)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(archivo, dpi=150)
    plt.close(fig)
    print(f"  figura guardada: {archivo}")


def problema1():
    print("\n=== PROBLEMA 1: líneas de campo ===")
    # (a) demostración de un paso del método en un punto
    dos = [(+1e-9, -1.0, 0.0), (-1e-9, 1.0, 0.0)]
    x, y, ds = 0.0, 0.5, 0.05
    Ex, Ey = campo(dos, x, y)
    E = np.hypot(Ex, Ey)
    print(f"  Punto (0, 0.5): Ex={Ex:.3f} N/C, Ey={Ey:.3f} N/C, |E|={E:.3f} N/C")
    print(f"  Siguiente punto (ds={ds}): ({x + Ex / E * ds:.4f}, {y + Ey / E * ds:.4f})")
    # (b) dos cargas
    graficar_lineas(dos, "Dos cargas: + en (−1,0), − en (1,0)", "2cargas.png",
                    n_lineas=14, lim=3.0)
    # (c) cuatro cargas
    cuatro = [(+1e-9, -1, -1), (+1e-9, 1, 1), (-1e-9, 1, -1), (-1e-9, -1, 1)]
    graficar_lineas(cuatro, "Cuatro cargas: + en (−1,−1),(1,1); − en (1,−1),(−1,1)",
                    "4cargas.png", n_lineas=12, lim=3.0)


# ---------------------------------------------------------------------------
# PROBLEMA 2: potencial de q1 (origen) y q2 (0, 0.5 m)
# ---------------------------------------------------------------------------
Q_PROB2 = [(-1.2e-9, 0.0, 0.0), (2.5e-9, 0.0, 0.5)]


def V2(x, y):
    return potencial(Q_PROB2, x, y)


def modo_interactivo():
    """El usuario da (x, y) y se muestra V; se repite hasta escribir 'q'."""
    print("\n--- Potencial de q1=-1.2 nC (0,0) y q2=2.5 nC (0,0.5) ---")
    print("Escriba 'x y' (en metros) o 'q' para salir.")
    while True:
        s = input("x y > ").strip()
        if s.lower() in ("q", "s", "salir"):
            break
        try:
            x, y = map(float, s.replace(",", " ").split())
            print(f"  V({x}, {y}) = {V2(x, y):.4f} V")
        except ZeroDivisionError:
            print("  Ese punto coincide con una carga (V infinito).")
        except Exception:
            print("  Entrada no válida. Ejemplo: 1.5 0.3")


def raices_en_y(x, V0, ymin=-5.0, ymax=5.0, n=4001, tol=0.004):
    """Todos los y tales que V(x,y)=V0 (búsqueda de cambio de signo + bisección
    hasta que los dos puntos que encuadran difieran en menos de tol < 0.005 m).
    Se evitan las posiciones de las cargas."""
    ys = np.linspace(ymin, ymax, n)
    f = []
    for y in ys:
        try:
            f.append(V2(x, y) - V0)
        except ZeroDivisionError:
            f.append(np.nan)
    f = np.array(f)
    sol = []
    for i in range(len(ys) - 1):
        a, b = ys[i], ys[i + 1]
        fa, fb = f[i], f[i + 1]
        if np.isnan(fa) or np.isnan(fb) or fa * fb > 0:
            continue
        # el cambio de signo por una asíntota (carga) NO es una raíz: se descarta
        if abs(fa) > 1e3 or abs(fb) > 1e3:
            continue
        while b - a > tol:
            m = 0.5 * (a + b)
            fm = V2(x, m) - V0
            if fa * fm <= 0:
                b, fb = m, fm
            else:
                a, fa = m, fm
        sol.append(0.5 * (a + b))  # promedio de los dos puntos que encuadran
    return sol


def superficie_equipotencial(V0, dx=0.25, xmax=5.0):
    """Para x = 0, 0.25, 0.5 ... busca los y con V=V0. Por simetría respecto a
    x=0 se reflejan los puntos a x negativo."""
    pts = []
    x = 0.0
    while x <= xmax + 1e-9:
        ys = raices_en_y(x, V0)
        for y in ys:
            pts.append((x, y))
            if x > 0:
                pts.append((-x, y))
        x += dx
    return np.array(pts)


def graficar_equipotencial_puntos(V0, archivo):
    pts = superficie_equipotencial(V0)
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    ax.plot(pts[:, 0], pts[:, 1], "k.", ms=5, label=f"puntos con V={V0} V")
    # curva "exacta" (contorno) para comparar
    g = np.linspace(-5, 5, 801)
    X, Y = np.meshgrid(g, g)
    with np.errstate(divide="ignore", invalid="ignore"):
        Z = sum(K * q / np.hypot(X - xq, Y - yq) for q, xq, yq in Q_PROB2)
    ax.contour(X, Y, Z, levels=[V0], colors="tab:blue", linewidths=1)
    ax.plot([], [], color="tab:blue", label="contorno exacto")
    ax.plot(0, 0, "ko", ms=10)
    ax.text(0.15, -0.35, "q₁ (−)")
    ax.plot(0, 0.5, "ro", ms=10)
    ax.text(0.15, 0.6, "q₂ (+)")
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect("equal")
    ax.set_xticks(range(-5, 6))
    ax.set_yticks(range(-5, 6))
    ax.grid(alpha=0.4)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title(f"Superficie equipotencial de {V0} V")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(archivo, dpi=150)
    plt.close(fig)
    print(f"  figura guardada: {archivo}")
    return pts


def problema2():
    print("\n=== PROBLEMA 2: potencial y superficies equipotenciales ===")
    print(f"  V(1, 0)     = {V2(1, 0):.4f} V")
    print(f"  V(0, 1)     = {V2(0, 1):.4f} V")
    print(f"  V(2, 2)     = {V2(2, 2):.4f} V")
    # (a) 5 V: punto con x=0
    print("\n  (a) Superficie de 5 V")
    print("  Puntos sobre x=0 (y donde V=5 V):",
          [round(y, 4) for y in raices_en_y(0.0, 5.0)])
    pts5 = graficar_equipotencial_puntos(5.0, "equipotencial_5V.png")
    print("  Tabla (x, y) de la superficie de 5 V, x >= 0:")
    for x, y in pts5[pts5[:, 0] >= 0]:
        print(f"    x = {x:5.2f}   y = {y:8.4f}")
    # (b) 3 V
    print("\n  (b) Superficie de 3 V (puede haber 4 puntos para un mismo x)")
    pts3 = graficar_equipotencial_puntos(3.0, "equipotencial_3V.png")
    for x in (0.0, 0.5, 1.0, 1.5, 2.0):
        print(f"    x = {x:4.2f}: y = {[round(y, 4) for y in raices_en_y(x, 3.0)]}")


# ---------------------------------------------------------------------------
# PROBLEMA 3: E = |ΔV/Δs| comparado con Coulomb
# ---------------------------------------------------------------------------
def raices_en_x(y, V0, xmin=0.01, xmax=6.0, n=6000, tol=1e-5):
    xs = np.linspace(xmin, xmax, n)
    f = np.array([V2(x, y) - V0 for x in xs])
    sol = []
    for i in range(len(xs) - 1):
        if f[i] * f[i + 1] <= 0:
            a, b = xs[i], xs[i + 1]
            while b - a > tol:
                m = 0.5 * (a + b)
                if (V2(a, y) - V0) * (V2(m, y) - V0) <= 0:
                    b = m
                else:
                    a = m
            sol.append(0.5 * (a + b))
    return sol


def problema3():
    print("\n=== PROBLEMA 3: E = |ΔV/Δs| vs ley de Coulomb ===")
    # Superficies que encierran V=6 V con ΔV = 1 V: 5.5 V y 6.5 V
    Va, Vb = 6.5, 5.5
    print(f"  Superficies de {Vb} V y {Va} V (ΔV = 1 V, centradas en 6 V)")
    # curvas cerca del eje x positivo
    fig, ax = plt.subplots(figsize=(6.5, 6))
    for V0, c in ((Va, "tab:red"), (6.0, "gray"), (Vb, "tab:blue")):
        ys = np.linspace(-0.3, 0.3, 61)
        xs_ = []
        yy = []
        for y in ys:
            r = raices_en_x(y, V0, xmin=0.5)
            # nos quedamos con la raíz del eje x positivo más cercana a la zona
            if r:
                xs_.append(r[-1] if len(r) == 1 else r[-1])
                yy.append(y)
        ax.plot(xs_, yy, color=c, label=f"{V0} V")
    # valores de x sobre el eje (y=0)
    xa = raices_en_x(0.0, Va, xmin=0.5)[-1]
    xb = raices_en_x(0.0, Vb, xmin=0.5)[-1]
    # también con y = ±0.1 como sugiere el enunciado
    for yv in (-0.1, 0.1):
        ra = raices_en_x(yv, Va, xmin=0.5)[-1]
        rb = raices_en_x(yv, Vb, xmin=0.5)[-1]
        print(f"  y = {yv:+.1f}: x({Va} V) = {ra:.4f} m,  x({Vb} V) = {rb:.4f} m")
    # Punto medio sobre el eje x: el que tiene V = 6 V
    xm = raices_en_x(0.0, 6.0, xmin=0.5)[-1]
    Ex, Ey = campo(Q_PROB2, xm, 0.0)
    E_C = np.hypot(Ex, Ey)
    nx, ny = Ex / E_C, Ey / E_C   # E es perpendicular a las equipotenciales

    def t_en_normal(V0):
        """Distancia t (con signo) sobre la recta normal por (xm,0) donde V=V0."""
        f = lambda t: V2(xm + t * nx, t * ny) - V0
        lo, hi = -0.6, 0.6
        for _ in range(60):          # bisección
            mid = 0.5 * (lo + hi)
            if f(lo) * f(mid) <= 0:
                hi = mid
            else:
                lo = mid
        return 0.5 * (lo + hi)

    ta, tb = t_en_normal(Va), t_en_normal(Vb)
    ds = abs(ta - tb)                   # Δs medido sobre la perpendicular
    ds_x = abs(xb - xa)                 # (solo referencia: medido sobre el eje x)
    E_dV = 1.0 / ds
    print(f"  En y=0: x({Va} V) = {xa:.4f} m,  x({Vb} V) = {xb:.4f} m"
          f"  (separación en x = {ds_x:.4f} m, NO es perpendicular)")
    print(f"  Punto medio (V=6 V) en el eje x: x = {xm:.4f} m")
    print(f"  Dirección de E en ese punto: ({nx:.3f}, {ny:.3f})")
    print(f"  Δs medido sobre la perpendicular = {ds:.4f} m")
    print(f"  E = |ΔV/Δs|          = {E_dV:.4f} V/m")
    print(f"  E (ley de Coulomb)   = {E_C:.4f} N/C   (Ex={Ex:.4f}, Ey={Ey:.4f})")
    print(f"  Diferencia relativa  = {abs(E_dV - E_C) / E_C * 100:.3f} %")
    ax.plot([xm + tb * nx, xm + ta * nx], [tb * ny, ta * ny], "k-", lw=2,
            label="Δs (perpendicular)")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title("Superficies equipotenciales cerca del eje x positivo")
    ax.legend()
    ax.grid(alpha=0.3)
    ax.set_aspect("equal")
    fig.tight_layout()
    fig.savefig("problema3_superficies.png", dpi=150)
    plt.close(fig)
    print("  figura guardada: problema3_superficies.png")


if __name__ == "__main__":
    problema1()
    problema2()
    problema3()
    if "--interactivo" in sys.argv:
        modo_interactivo()
