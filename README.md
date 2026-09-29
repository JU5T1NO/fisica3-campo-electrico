# Laboratorio de Física III – Programas de Campo Eléctrico

Universidad Nacional Mayor de San Marcos

Programa en Python que resuelve el cuestionario 3:

1. Líneas de campo eléctrico (método Δx = (Eₓ/E)Δs) para dos y cuatro cargas.
2. Potencial eléctrico de q₁ = −1.2 nC en (0,0) y q₂ = 2.5 nC en (0,0.5 m), y superficies equipotenciales de 5 V y 3 V.
3. Cálculo de E = |ΔV/Δs| y comparación con la ley de Coulomb.

## Cómo ejecutarlo

```bash
pip install -r requirements.txt
python3 cuestionario3.py
```

Para el modo interactivo del problema 2 (se ingresa `x y` y se muestra V):

```bash
python3 cuestionario3.py --interactivo
```

## Resultados esperados

- Se generan `2cargas.png`, `4cargas.png`, `equipotencial_5V.png`, `equipotencial_3V.png` y `problema3_superficies.png`.
- `V(1, 0) = 9.3117 V` (comprobable a mano: k·q₁/1 + k·q₂/√1.25).
- Superficie de 5 V en x = 0: y ≈ 0.171 m y y ≈ 3.176 m.
- Problema 3: E = ΔV/Δs ≈ 3.283 V/m frente a Coulomb ≈ 3.309 N/C (diferencia ≈ 0.76 %).

## Autor

Nombre y código del estudiante
