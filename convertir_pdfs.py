import os
import fitz  # PyMuPDF

# Configuración de directorios
INPUT_DIR = "."
OUTPUT_DIR = "."
OUTPUT_EXTENSION = ".md"  # Puedes cambiarlo a ".txt" si lo prefieres

def extraer_texto_de_pdf(ruta_pdf):
    """Extrae todo el texto de un PDF página por página."""
    texto_completo = []
    
    try:
        # Abre el PDF en modo solo lectura (por defecto)
        documento = fitz.open(ruta_pdf)
        
        for numero_pagina in range(len(documento)):
            pagina = documento[numero_pagina]
            texto = pagina.get_text()
            
            # Añadimos un separador de página para que la IA entienda la estructura
            texto_completo.append(f"\n--- Página {numero_pagina + 1} ---\n")
            texto_completo.append(texto)
            
        documento.close()
        return "".join(texto_completo)
    
    except Exception as e:
        return f"[ERROR al leer el PDF: {e}]"

def main():
    # 1. Verificar y crear el directorio de salida si no existe
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"✅ Carpeta '{OUTPUT_DIR}/' creada exitosamente.")

    # 2. Verificar que exista la carpeta de entrada
    if not os.path.exists(INPUT_DIR):
        print(f"❌ Error: La carpeta '{INPUT_DIR}/' no existe. Créala y añade tus PDFs.")
        return

    # 3. Procesar cada archivo en la carpeta de entrada
    archivos_procesados = 0
    for nombre_archivo in os.listdir(INPUT_DIR):
        if nombre_archivo.lower().endswith(".pdf"):
            ruta_entrada = os.path.join(INPUT_DIR, nombre_archivo)
            
            # Crear el nombre del archivo de salida (ej: documento.pdf -> documento.md)
            nombre_base = os.path.splitext(nombre_archivo)[0]
            ruta_salida = os.path.join(OUTPUT_DIR, f"{nombre_base}{OUTPUT_EXTENSION}")
            
            print(f"⏳ Procesando: {nombre_archivo}...")
            
            # Extraer texto
            texto_extraido = extraer_texto_de_pdf(ruta_entrada)
            
            # Validar si se extrajo texto (para detectar PDFs escaneados)
            if len(texto_extraido.strip()) < 50:
                print(f"  ⚠️  Advertencia: Se extrajo muy poco texto de '{nombre_archivo}'.")
                print(f"     Es posible que sea un PDF escaneado (imagen) y requiera OCR.")
            
            # Guardar en el nuevo archivo (Sobrescribe si ya existe, pero NUNCA toca el original)
            with open(ruta_salida, "w", encoding="utf-8") as archivo_salida:
                archivo_salida.write(texto_extraido)
                
            print(f"  ✅ Guardado en: {ruta_salida}")
            archivos_procesados += 1

    print(f"\n🎉 ¡Proceso completado! Se procesaron {archivos_procesados} archivos PDF.")

if __name__ == "__main__":
    main()