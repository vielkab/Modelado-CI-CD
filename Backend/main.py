from fastapi import FastAPI, HTTPException 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel 
from typing import List

app = FastAPI(
    title="Api Vacacional de futbol El Niño Moi",
    description="Una API para la gestion de cupos e inscripciones con CRUD Completo",
    version="1.1.0"
)

FRONTEND_URL_PROD = "https://modelado-ci-cd-817979807762.europe-west1.run.app"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL_PROD,
        "http://localhost:5173",
        "http://localhost:4200",
        "http://127.0.0.1:5500", # Live Server local habitual
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"], # Permite explícitamente GET, POST, PUT, PATCH, DELETE
    allow_headers=["*"]
)

# Modelo de validación de datos actualizado con Cédula
class Inscripcion(BaseModel):
    cedula: str  
    nombre_representante: str
    nombre_nino: str
    edad: int
    telefono: str
    meses_seleccionados: List[str]

# Modelos auxiliares para modificaciones parciales/totales
class ActualizarTelefono(BaseModel):
    telefono: str

class ActualizarInscripcionCompleta(BaseModel):
    nombre_representante: str
    nombre_nino: str
    telefono: str

# Base de datos simulada en memoria
base_cupos = [
    {"mes": "Febrero", "c6_8": 0, "c9_11": 2, "c12_14": 6},
    {"mes": "Marzo", "c6_8": 30, "c9_11": 30, "c12_14": 30},
    {"mes": "Abril", "c6_8": 30, "c9_11": 30, "c12_14": 30},
    {"mes": "Mayo", "c6_8": 30, "c9_11": 30, "c12_14": 30},
]

lista_inscritos = []

@app.get("/")
def inicio():
    return {"status": "online", "mensaje": "Servidor de El Niño Moi corriendo."}

@app.get("/api/cupos")
def obtener_cupos():
    return base_cupos

# --- 1. MÉTODO POST: REGISTRAR ---
@app.post("/api/inscribir")
def registrar_inscripcion(datos: Inscripcion):
    # Validación: Evitar duplicados de cédula
    for alumno in lista_inscritos:
        if alumno["cedula"] == datos.cedula:
            raise HTTPException(status_code=400, detail=f"La cédula {datos.cedula} ya se encuentra registrada en el sistema.")

    if not datos.meses_seleccionados:
        raise HTTPException(status_code=400, detail="Debes seleccionar al menos un mes.")
    
    if datos.edad < 6 or datos.edad > 14:
        raise HTTPException(status_code=400, detail="La edad del niño debe estar estrictamente entre 6 y 14 años.")

    categoria = ""
    edad = int(datos.edad) 

    if 6 <= edad <= 8:
        categoria = "c6_8"
    elif 9 <= edad <= 11:
        categoria = "c9_11"
    elif 12 <= edad <= 14:
        categoria = "c12_14"

    # Validar cupos disponibles
    for mes_cliente in datos.meses_seleccionados:
        mes_encontrado = False
        for item in base_cupos:
            if item["mes"].lower() == mes_cliente.lower():
                mes_encontrado = True
                cupos_actuales = item.get(categoria)
                if cupos_actuales <= 0:
                    raise HTTPException(status_code=400, detail=f"Ya no quedan cupos en {item['mes']} para la categoría {categoria}.")
                break
        if not mes_encontrado:
            raise HTTPException(status_code=404, detail=f"El mes '{mes_cliente}' no es válido.")

    # Restar cupos
    for mes_cliente in datos.meses_seleccionados:
        for item in base_cupos:
            if item["mes"].lower() == mes_cliente.lower():
                item[categoria] -= 1
                break

    # Lógica financiera
    PRECIO_MES_BASE = 40.0
    cantidad_meses = len(datos.meses_seleccionados)
    subtotal = cantidad_meses * PRECIO_MES_BASE
    porcentaje_descuento = 0
    if cantidad_meses == 2: porcentaje_descuento = 10
    elif cantidad_meses == 3: porcentaje_descuento = 15
    elif cantidad_meses == 4: porcentaje_descuento = 20

    descuento_calculado = subtotal * (porcentaje_descuento / 100)
    total_a_pagar = subtotal - descuento_calculado

    nueva_inscripcion = datos.model_dump()
    nueva_inscripcion["categoria_asignada"] = categoria
    nueva_inscripcion["financiero"] = {
        "subtotal": subtotal,
        "descuento_aplicado": f"{porcentaje_descuento}%",
        "total_final": total_a_pagar
    }
    lista_inscritos.append(nueva_inscripcion)
    
    meses_texto = ", ".join(datos.meses_seleccionados)
    return {
        "status": "success",
        "mensaje": f"¡Pre-inscripción exitosa de {datos.nombre_nino} (CI: {datos.cedula})! Total: ${total_a_pagar:.2f}.",
        "detalles_cupos_restantes": base_cupos
    }

# --- 2. MÉTODO PUT: ACTUALIZACIÓN TOTAL (Nombres y Representante) ---
@app.put("/api/inscribir/{cedula}")
def actualizar_inscripcion_total(cedula: str, datos: ActualizarInscripcionCompleta):
    for alumno in lista_inscritos:
        if alumno["cedula"] == cedula:
            alumno["nombre_representante"] = datos.nombre_representante
            alumno["nombre_nino"] = datos.nombre_nino
            alumno["telefono"] = datos.telefono
            return {"status": "success", "mensaje": f"Ficha de matrícula (CI: {cedula}) actualizada por completo con éxito."}
    raise HTTPException(status_code=404, detail="No se encontró ningún estudiante con esa cédula.")

# --- 3. MÉTODO PATCH: ACTUALIZACIÓN PARCIAL (Solo el teléfono) ---
@app.patch("/api/inscribir/{cedula}")
def actualizar_telefono_parcial(cedula: str, datos: ActualizarTelefono):
    for alumno in lista_inscritos:
        if alumno["cedula"] == cedula:
            alumno["telefono"] = datos.telefono
            return {"status": "success", "mensaje": f"Teléfono asignado a la CI {cedula} modificado a: {datos.telefono}."}
    raise HTTPException(status_code=404, detail="Estudiante no registrado.")

# --- 4. MÉTODO DELETE: ELIMINAR Y DEVOLVER CUPO ---
@app.delete("/api/inscribir/{cedula}")
def eliminar_inscripcion(cedula: str):
    global lista_inscritos
    inscrito_encontrado = None
    
    for alumno in lista_inscritos:
        if alumno["cedula"] == cedula:
            inscrito_encontrado = alumno
            break
            
    if not inscrito_encontrado:
        raise HTTPException(status_code=404, detail="La cédula especificada no existe en la base de datos.")
    
    # Devolución automática de cupos (+1)
    meses = inscrito_encontrado["meses_seleccionados"]
    categoria = inscrito_encontrado["categoria_asignada"]
    
    for mes_cliente in meses:
        for item in base_cupos:
            if item["mes"].lower() == mes_cliente.lower():
                item[categoria] += 1
                break
                
    # Remover de la lista
    lista_inscritos = [a for a in lista_inscritos if a["cedula"] != cedula]
    return {"status": "success", "mensaje": f"Matrícula de {inscrito_encontrado['nombre_nino']} eliminada. Cupos liberados correctamente."}

@app.get("/api/inscritos")
def ver_inscritos():
    return {"total_registros": len(lista_inscritos), "alumnos": lista_inscritos}

# --- NUEVA RUTA: OBTENER UN ALUMNO POR CÉDULA (GET) ---
@app.get("/api/inscribir/{cedula}")
def obtener_inscrito_por_cedula(cedula: str):
    for alumno in lista_inscritos:
        if alumno["cedula"] == cedula:
            return {"status": "success", "datos": alumno}
    raise HTTPException(status_code=404, detail="No se encontró ningún estudiante registrado con esa cédula.")