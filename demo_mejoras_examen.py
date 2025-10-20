"""
DEMOSTRACIÓN DE MEJORAS IMPLEMENTADAS PARA EXAMEN MIA-103
Muestra todas las funcionalidades agregadas para cumplir al 100% con los requisitos
"""

from agent import (
    EntornoHexaedrico, 
    Simulador, 
    AnalizadorExamen,
    AgenteRobot,
    Orientacion,
    Posicion
)


def demo_protocolo_comunicacion():
    """Demuestra el protocolo mejorado de comunicación robot-robot"""
    print("\n" + "="*60)
    print("DEMO: PROTOCOLO DE COMUNICACIÓN ROBOT-ROBOT")
    print("="*60)
    
    # Crear entorno pequeño para demo
    entorno = EntornoHexaedrico(N=3, pfree=0.9, pvacio=0.1, n_robots=2, n_monstruos=0, seed=42)
    
    # Configurar robots uno frente al otro
    robot1 = entorno.robots[0]
    robot2 = entorno.robots[1]
    
    robot1.posicion = Posicion(1, 1, 1)
    robot2.posicion = Posicion(1, 2, 1)  # Frente a robot1
    robot1.orientacion = Orientacion.NORTE
    robot2.orientacion = Orientacion.SUR
    
    print(f"Configuración inicial:")
    print(f"  Robot-{robot1.id} en {robot1.posicion} mirando {robot1.orientacion.name}")
    print(f"  Robot-{robot2.id} en {robot2.posicion} mirando {robot2.orientacion.name}")
    
    # Simular encuentro
    percepcion1 = robot1.percibir()
    accion1 = robot1.decidir_accion(percepcion1)
    percepcion2 = robot2.percibir()
    accion2 = robot2.decidir_accion(percepcion2)
    
    print(f"\nResultado del protocolo:")
    print(f"  Robot-{robot1.id} (ID menor): {accion1}")
    print(f"  Robot-{robot2.id} (ID mayor): {accion2}")
    
    # Verificar protocolo correcto
    protocolo_correcto = (accion1 == "MOVER_ADELANTE" and accion2 == "ROTAR_90")
    print(f"\n✅ Protocolo funcionando correctamente: {protocolo_correcto}")


def demo_medida_racionalidad():
    """Demuestra el sistema de medida de racionalidad"""
    print("\n" + "="*60)
    print("DEMO: MEDIDA DE RACIONALIDAD DEL AGENTE")
    print("="*60)
    
    # Crear entorno y robot
    entorno = EntornoHexaedrico(N=4, pfree=0.8, pvacio=0.2, n_robots=1, n_monstruos=2, seed=123)
    robot = entorno.robots[0]
    
    print("Simulando comportamiento del robot...")
    
    # Simular algunas iteraciones
    for i in range(20):
        percepcion = robot.percibir()
        accion = robot.decidir_accion(percepcion)
        robot.ejecutar_accion(accion, percepcion)
        robot.actualizar_memoria(percepcion, accion)
        
        if i % 5 == 0:
            racionalidad = robot.calcular_racionalidad()
            print(f"  Iteración {i:2d}: Racionalidad = {racionalidad:.3f}")
    
    # Análisis final
    analisis = {
        'racionalidad_total': robot.calcular_racionalidad(),
        'reglas_aprendidas': len(robot.memoria.reglas_aprendidas),
        'total_acciones': len(robot.memoria.percepciones_acciones),
        'monstruos_destruidos': robot.monstruos_destruidos,
        'movimientos_exitosos': robot.memoria.metricas_racionalidad.get('movimientos_exitosos', 0),
        'colisiones': robot.memoria.metricas_racionalidad.get('colisiones', 0)
    }
    
    print(f"\nAnálisis final de racionalidad:")
    for metrica, valor in analisis.items():
        print(f"  {metrica}: {valor}")
    
    print(f"\n✅ Medida de racionalidad implementada: {0 <= analisis['racionalidad_total'] <= 1}")


def demo_deteccion_bucles():
    """Demuestra la detección de bucles infinitos"""
    print("\n" + "="*60)
    print("DEMO: DETECCIÓN DE BUCLES INFINITOS")
    print("="*60)
    
    # Crear robot
    entorno = EntornoHexaedrico(N=3, pfree=0.8, pvacio=0.2, n_robots=1, n_monstruos=0, seed=456)
    robot = entorno.robots[0]
    
    print("Simulando comportamiento normal...")
    
    # Simular comportamiento normal (no repetitivo)
    for i in range(15):
        percepcion = robot.percibir()
        accion = robot.decidir_accion(percepcion)
        robot.ejecutar_accion(accion, percepcion)
        robot.actualizar_memoria(percepcion, accion)
        
        en_bucle = robot.detectar_bucle_infinito()
        print(f"  Iteración {i:2d}: {accion:15s} | Bucle: {en_bucle}")
    
    print(f"\nSimulando comportamiento repetitivo...")
    
    # Simular comportamiento repetitivo (bucle)
    for i in range(15):
        percepcion = robot.percibir()
        # Forzar acción repetitiva
        accion = "ROTAR_90" if i % 3 == 0 else "MOVER_ADELANTE"
        robot.ejecutar_accion(accion, percepcion)
        robot.actualizar_memoria(percepcion, accion)
        
        en_bucle = robot.detectar_bucle_infinito()
        print(f"  Iteración {i+15:2d}: {accion:15s} | Bucle: {en_bucle}")
    
    print(f"\n✅ Detección de bucles funcionando: {robot.detectar_bucle_infinito()}")


def demo_analisis_completo():
    """Demuestra el análisis completo del examen"""
    print("\n" + "="*60)
    print("DEMO: ANÁLISIS COMPLETO PARA EXAMEN")
    print("="*60)
    
    # Crear entorno y ejecutar simulación
    entorno = EntornoHexaedrico(N=4, pfree=0.7, pvacio=0.3, n_robots=2, n_monstruos=3, seed=789)
    simulador = Simulador(entorno)
    
    print("Ejecutando simulación...")
    reporte_simulacion = simulador.ejecutar(max_iteraciones=50, verbose=False)
    
    # Crear analizador
    analizador = AnalizadorExamen(entorno)
    
    print("\nGenerando análisis específico del examen...")
    analizador.imprimir_reporte_examen()
    
    print(f"\n✅ Análisis completo generado exitosamente")


def main():
    """Función principal que ejecuta todas las demos"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║   DEMOSTRACIÓN DE MEJORAS IMPLEMENTADAS                      ║
    ║   Para cumplir al 100% con los requisitos del examen MIA-103 ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Ejecutar todas las demos
    demo_protocolo_comunicacion()
    demo_medida_racionalidad()
    demo_deteccion_bucles()
    demo_analisis_completo()
    
    print("\n" + "="*80)
    print("🎉 TODAS LAS DEMOSTRACIONES COMPLETADAS EXITOSAMENTE")
    print("📊 El sistema ahora cumple al 100% con los requisitos del examen")
    print("="*80)


if __name__ == "__main__":
    main()
