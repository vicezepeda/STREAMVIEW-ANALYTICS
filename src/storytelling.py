"""Guion breve basado en las métricas comunes, sin inferir crecimiento."""
from analisis import resumen

if __name__=='__main__':
    values=resumen();k=values['catalogo'];f=values['finanzas']
    print(f"El catálogo tiene {k['total']:,} títulos únicos.")
    print('La distribución por año de estreno es casi uniforme; no prueba crecimiento real.')
    print('Dirección explora el dashboard Python. Contenidos y Adquisición explora Power BI.')
    print(f"Finanzas considera {f['n']:,} películas, cobertura {f['cobertura_pct']:.2f}% y ROI agregado {f['roi_agregado_pct']:.2f}%.")
    print('El ROI no representa la rentabilidad de la plataforma. La prioridad es completar datos.')
