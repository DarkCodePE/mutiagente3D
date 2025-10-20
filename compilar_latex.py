"""
COMPILADOR DE DOCUMENTO LATEX
Compila el documento RobotsMonstruicidas.tex y genera el PDF
"""

import subprocess
import os
import sys

def compilar_latex():
    """Compila el documento LaTeX"""
    archivo_tex = "RobotsMonstruicidas.tex"
    
    if not os.path.exists(archivo_tex):
        print(f"❌ Error: No se encontró el archivo {archivo_tex}")
        return False
    
    print("Compilando documento LaTeX...")
    
    try:
        # Primera compilación
        print("Primera compilación...")
        result1 = subprocess.run(['pdflatex', '-interaction=nonstopmode', archivo_tex], 
                               capture_output=True, text=True)
        
        if result1.returncode != 0:
            print("❌ Error en primera compilación:")
            print(result1.stderr)
            return False
        
        # Segunda compilación (para referencias)
        print("Segunda compilación...")
        result2 = subprocess.run(['pdflatex', '-interaction=nonstopmode', archivo_tex], 
                               capture_output=True, text=True)
        
        if result2.returncode != 0:
            print("❌ Error en segunda compilación:")
            print(result2.stderr)
            return False
        
        # Verificar que se generó el PDF
        archivo_pdf = "RobotsMonstruicidas.pdf"
        if os.path.exists(archivo_pdf):
            print(f"✅ Documento compilado exitosamente: {archivo_pdf}")
            return True
        else:
            print("❌ Error: No se generó el archivo PDF")
            return False
            
    except FileNotFoundError:
        print("❌ Error: pdflatex no está instalado o no está en el PATH")
        print("Instale LaTeX (MiKTeX, TeX Live, etc.)")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def limpiar_archivos_auxiliares():
    """Limpia archivos auxiliares de LaTeX"""
    archivos_auxiliares = [
        "RobotsMonstruicidas.aux",
        "RobotsMonstruicidas.log", 
        "RobotsMonstruicidas.out",
        "RobotsMonstruicidas.toc",
        "RobotsMonstruicidas.fls",
        "RobotsMonstruicidas.fdb_latexmk",
        "RobotsMonstruicidas.synctex.gz"
    ]
    
    for archivo in archivos_auxiliares:
        if os.path.exists(archivo):
            try:
                os.remove(archivo)
                print(f"✓ Limpiado: {archivo}")
            except:
                pass

def verificar_dependencias():
    """Verifica que las dependencias estén disponibles"""
    print("Verificando dependencias...")
    
    # Verificar pdflatex
    try:
        result = subprocess.run(['pdflatex', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ pdflatex disponible")
        else:
            print("❌ pdflatex no disponible")
            return False
    except FileNotFoundError:
        print("❌ pdflatex no instalado")
        return False
    
    # Verificar archivos necesarios
    archivos_requeridos = [
        "RobotsMonstruicidas.tex",
        "grafica_rendimiento.png",
        "datos_latex.txt"
    ]
    
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} no encontrado")
            return False
    
    return True

def main():
    """Función principal"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║   COMPILADOR DE DOCUMENTO LATEX                               ║
    ║   Robots Monstruicidas - MIA-103                             ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Verificar dependencias
    if not verificar_dependencias():
        print("\n❌ Faltan dependencias. Instale LaTeX y genere los datos primero.")
        return False
    
    # Compilar documento
    if compilar_latex():
        print("\n🎉 ¡Documento compilado exitosamente!")
        print("📄 Archivo generado: RobotsMonstruicidas.pdf")
        
        # Limpiar archivos auxiliares
        print("\nLimpiando archivos auxiliares...")
        limpiar_archivos_auxiliares()
        
        return True
    else:
        print("\n❌ Error en la compilación")
        return False

if __name__ == "__main__":
    exito = main()
    sys.exit(0 if exito else 1)
