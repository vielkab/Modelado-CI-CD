from fastapi import FastAPI, HTTPException 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel 
from typing import List

app = FastAPI(
    title="Api Vacacional de futbol El Niño Moi",
    description="Una API para la gestion de cupos e inscripciones",
    version="1.0.0"
)

# Configuración de CORS para permitir peticiones desde tu Frontend local o la nube
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Modelo de validación de datos para las inscripciones entrantes
class Inscripcion(BaseModel):
    nombre_representante: str
    nombre_nino: str
    edad: int
    telefono: str
    meses_seleccionados: List[str]

# Base de datos simulada en memoria (Llaves corregidas para emparejar con el Frontend)
base_cupos = [
    {"mes": "Febrero", "c6_8": 0, "c9_11": 2, "c12_14": 6},
    {"mes": "Marzo", "c6_8": 30, "c9_11": 30, "c12_14": 30},
    {"mes": "Abril", "c6_8": 30, "c9_11": 30, "c12_14": 30},
    {"mes": "Mayo", "c6_8": 30, "c9_11": 30, "c12_14": 30},
]

lista_inscritos = []

@app.get("/")
def inicio():
    # Corregido: Llaves simples para evitar errores de sintaxis en Python
    return {"status": "online", "mensaje": "Servidor de El Niño Moi corriendo con control numérico de cupos."}

@app.get("/api/cupos")
def obtener_cupos():
    """Devuelve la cantidad de cupos disponibles para cada categoría en cada mes."""
    return base_cupos

@app.post("/api/inscribir")
def registrar_inscripcion(datos: Inscripcion):
    # 1. Validaciones iniciales de reglas de negocio
    if not datos.meses_seleccionados:
        raise HTTPException(status_code=400, detail="Debes seleccionar al menos un mes.")
    
    if datos.edad < 6 or datos.edad > 14:
        raise HTTPException(status_code=400, detail="La edad del niño debe estar estrictamente entre 6 y 14 años.")

    # 2. Determinar el nombre de la llave de la categoría según la edad
    categoria = ""
    edad = int(datos.edad) 

    if 6 <= edad <= 8:
        categoria = "c6_8"
    elif 9 <= edad <= 11:
        categoria = "c9_11"
    elif 12 <= edad <= 14:
        categoria = "c12_14"
    else:
        raise HTTPException(status_code=400, detail="Edad fuera del rango de las categorías disponibles.")

    # 3. FASE DE VALIDACIÓN: Asegurar que TODOS los meses elegidos tengan cupo disponible
    for mes_cliente in datos.meses_seleccionados:
        mes_encontrado = False
        
        for item in base_cupos:
            if item["mes"].lower() == mes_cliente.lower():
                mes_encontrado = True
                cupos_actuales = item.get(categoria)

                # Si por algún motivo la llave no existe en el diccionario
                if cupos_actuales is None:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error interno: La categoría '{categoria}' no se encuentra configurada en el servidor."
                    )

                # Si el mes no tiene espacio para esa edad
                if cupos_actuales <= 0:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Ya no quedan cupos disponibles para la categoría de edad seleccionada en el mes de {item['mes']}."
                    ) 
                break
                
        if not mes_encontrado:
            raise HTTPException(status_code=404, detail=f"El mes '{mes_cliente}' no es válido en el sistema.")

    # 4. FASE DE TRANSACCIÓN: Restar el cupo una vez que sabemos que todo está en orden
    for mes_cliente in datos.meses_seleccionados:
        for item in base_cupos:
            if item["mes"].lower() == mes_cliente.lower():
                item[categoria] -= 1  # Resta el cupo de forma controlada en caliente
                break

    # 5. LÓGICA FINANCIERA: Cálculo de costos y descuentos escalonados
    PRECIO_MES_BASE = 40.0
    cantidad_meses = len(datos.meses_seleccionados)
    subtotal = cantidad_meses * PRECIO_MES_BASE
    
    porcentaje_descuento = 0
    if cantidad_meses == 2:
        porcentaje_descuento = 10
    elif cantidad_meses == 3:
        porcentaje_descuento = 15
    elif cantidad_meses == 4:
        porcentaje_descuento = 20

    descuento_calculado = subtotal * (porcentaje_descuento / 100)
    total_a_pagar = subtotal - descuento_calculado

    # 6. Almacenamiento del registro de auditoría interna
    nueva_inscripcion = datos.dict()
    nueva_inscripcion["categoria_asignada"] = categoria
    nueva_inscripcion["financiero"] = {
        "subtotal": subtotal,
        "descuento_aplicado": f"{porcentaje_descuento}%",
        "total_final": total_a_pagar
    }
    lista_inscritos.append(nueva_inscripcion)
    
    # 7. Respuesta exitosa estructurada para el Frontend
    meses_texto = ", ".join(datos.meses_seleccionados)
    return {
        "status": "success",
        "mensaje": f"¡Pre-inscripción exitosa de {datos.nombre_nino} ({datos.edad} años) para los meses de: {meses_texto}! Total calculado: ${total_a_pagar:.2f}.",
        "detalles_cupos_restantes": base_cupos
    }

@app.get("/api/inscritos")
def ver_inscritos():
    """Endpoint de auditoría para verificar los alumnos registrados."""
    return {"total_registros": len(lista_inscritos), "alumnos": lista_inscritos}