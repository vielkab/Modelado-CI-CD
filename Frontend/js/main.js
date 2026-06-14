// CONFIGURACIÓN: URL del Backend en AWS Elastic Beanstalk
const API_URL = "http://desplieguecontinuomodelado-env.eba-fihm92pm.us-east-1.elasticbeanstalk.com";
//const API_URL = "http://127.0.0.1:8000";
document.addEventListener("DOMContentLoaded", () => {
    cargarCuposTabla();
    configurarFormulario();
});

// TAREA 1: CARGAR CUPOS DESDE LA API (GET)
async function cargarCuposTabla() {
    try {
        const response = await fetch(`${API_URL}/api/cupos`);
        if (!response.ok) throw new Error("Error al obtener los cupos del servidor.");
        
        const cupos = await response.json();
        
        cupos.forEach(item => {
            const mesMinuscula = item.mes.toLowerCase();
            
            const celda6_8 = document.getElementById(`cupo-${mesMinuscula}-6-8`);
            const celda9_11 = document.getElementById(`cupo-${mesMinuscula}-9-11`);
            const celda12_14 = document.getElementById(`cupo-${mesMinuscula}-12-14`);
            
            if (celda6_8) celda6_8.innerText = item.c6_8 <= 0 ? "Agotado" : item.c6_8;
            if (celda9_11) celda9_11.innerText = item.c9_11 <= 0 ? "Agotado" : item.c9_11;
            if (celda12_14) celda12_14.innerText = item.c12_14 <= 0 ? "Agotado" : item.c12_14;
            
            if (item.c6_8 <= 0 && item.c9_11 <= 0 && item.c12_14 <= 0) {
                const checkbox = document.getElementById(`check-${mesMinuscula}`);
                if (checkbox) {
                    checkbox.disabled = true;
                    const label = checkbox.parentElement;
                    if (label) label.style.color = "gray";
                }
            }
        });
    } catch (error) {
        console.error("Error en la petición GET:", error);
    }
}

// TAREA 2: ENVIAR FORMULARIO A LA API (POST)
function configurarFormulario() {
    const formulario = document.getElementById("form-inscripcion");
    if (!formulario) return;

    formulario.addEventListener("submit", async (event) => {
        event.preventDefault();

        // CAPTURA DE CAMPOS (Asegúrate de agregar el input 'txt-cedula' en tu HTML)
        const cedula = document.getElementById("txt-cedula").value.trim();
        const nombre_representante = document.getElementById("txt-representante").value.trim();
        const nombre_nino = document.getElementById("txt-nino").value.trim();
        const edad = parseInt(document.getElementById("txt-edad").value, 10);
        const telefono = document.getElementById("txt-telefono").value.trim();

        const meses_seleccionados = [];
        const checkboxesMarcados = document.querySelectorAll(".clase-mes:checked");
        checkboxesMarcados.forEach(cb => {
            meses_seleccionados.push(cb.value);
        });

        // Payload con la llave primaria (Cédula)
        const payload = {
            cedula,
            nombre_representante,
            nombre_nino,
            edad,
            telefono,
            meses_seleccionados
        };

        try {
            const response = await fetch(`${API_URL}/api/inscribir`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            });

            const resultado = await response.json();

            if (response.ok && resultado.status === "success") {
                mostrarAlerta(resultado.mensaje, "success");
                formulario.reset(); 
                cargarCuposTabla(); // Reactividad en caliente
            } else {
                mostrarAlerta(resultado.detail || "Error en la inscripción.", "error");
            }
        } catch (error) {
            console.error("Error en la petición POST:", error);
            mostrarAlerta("No se pudo conectar con el servidor de la API.", "error");
        }
    });
}

// --- NUEVA TAREA 3: ELIMINAR MATRÍCULA (DELETE) ---
async function ejecutarEliminarInscripcion(cedulaInput) {
    const cedulaTarget = cedulaInput || prompt("Ingrese la Cédula del niño que desea dar de BAJA:");
    if (!cedulaTarget) return;

    if (!confirm(`¿Está seguro de eliminar al alumno con Cédula ${cedulaTarget}? Esto devolverá los cupos.`)) return;

    try {
        const response = await fetch(`${API_URL}/api/inscribir/${cedulaTarget}`, {
            method: "DELETE"
        });
        const resultado = await response.json();

        if (response.ok) {
            mostrarAlerta(resultado.mensaje, "success");
            cargarCuposTabla(); // <--- Devuelve el cupo a la tabla visual inmediatamente sin recargar
        } else {
            mostrarAlerta(resultado.detail || "Error al eliminar.", "error");
        }
    } catch (error) {
        console.error("Error en la petición DELETE:", error);
    }
}

// --- NUEVA TAREA 4: ACTUALIZAR TELÉFONO (PATCH) ---
async function ejecutarModificarTelefono(cedulaInput) {
    const cedulaTarget = cedulaInput || prompt("Ingrese la Cédula del niño para cambiar el teléfono:");
    if (!cedulaTarget) return;

    const nuevoFono = prompt("Ingrese el nuevo número telefónico de contacto:");
    if (!nuevoFono) return;

    try {
        const response = await fetch(`${API_URL}/api/inscribir/${cedulaTarget}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ telefono: nuevoFono })
        });
        const resultado = await response.json();

        if (response.ok) {
            mostrarAlerta(resultado.mensaje, "success");
        } else {
            mostrarAlerta(resultado.detail || "Error al actualizar.", "error");
        }
    } catch (error) {
        console.error("Error en PATCH:", error);
    }
}

// --- NUEVA TAREA 5: MODIFICAR FICHA COMPLETA (PUT) ---
async function ejecutarModificarFichaCompleta(cedulaInput) {
    const cedulaTarget = cedulaInput || prompt("Ingrese la Cédula del alumno a modificar:");
    if (!cedulaTarget) return;

    const nuevoRepresentante = prompt("Nombre del Nuevo Representante:");
    const nuevoNino = prompt("Nombre Completo del Niño Corregido:");
    const nuevoTelefono = prompt("Nuevo Teléfono:");

    if (!nuevoRepresentante || !nuevoNino || !nuevoTelefono) {
        alert("Todos los campos son obligatorios para actualizar por PUT.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/api/inscribir/${cedulaTarget}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                nombre_representante: nuevoRepresentante,
                nombre_nino: nuevoNino,
                telefono: nuevoTelefono
            })
        });
        const resultado = await response.json();

        if (response.ok) {
            mostrarAlerta(resultado.mensaje, "success");
        } else {
            mostrarAlerta(resultado.detail || "Error al actualizar por PUT.", "error");
        }
    } catch (error) {
        console.error("Error en PUT:", error);
    }
}

function mostrarAlerta(mensaje, tipo) {
    const contenedorMensaje = document.getElementById("contenedor-alerta");
    if (!contenedorMensaje) {
        alert(mensaje);
        return;
    }
    contenedorMensaje.innerText = mensaje;
    contenedorMensaje.className = `alerta-${tipo}`;
    contenedorMensaje.style.display = "block";
}
// --- NUEVA TAREA 6: BUSCAR Y MOSTRAR DATOS DE UN ALUMNO 
window.ejecutarBuscarInscrito = async function() {
    const cedulaTarget = prompt("Ingrese la Cédula del alumno que desea consultar:");
    if (!cedulaTarget) return;

    try {
        const response = await fetch(`${API_URL}/api/inscribir/${cedulaTarget}`);
        const resultado = await response.json();

        if (response.ok && resultado.status === "success") {
            const alumno = resultado.datos;
            
            // Construimos un mensaje limpio con saltos de línea para mostrar los detalles
            const detalleAlumno = `
ICHFA DE MATRÍCULA ENCONTRADA

🔹 Datos del Alumno:
• Cédula: ${alumno.cedula}
• Niño: ${alumno.nombre_nino}
• Edad: ${alumno.edad} años (Categoría: ${alumno.categoria_asignada})

🔹 Contacto:
• Representante: ${alumno.nombre_representante}
• Teléfono: ${alumno.telefono}

🔹 Detalle del Curso:
• Meses Reservados: ${alumno.meses_seleccionados.join(", ")}

Información Financiera:
• Subtotal: $${alumno.financiero.subtotal.toFixed(2)}
• Descuento: ${alumno.financiero.descuento_aplicado}
• Total a Pagar: $${alumno.financiero.total_final.toFixed(2)}
            `;
            
            alert(detalleAlumno);
        } else {
            mostrarAlerta(resultado.detail || "No se pudo encontrar al estudiante.", "error");
        }
    } catch (error) {
        console.error("Error en GET individual:", error);
        mostrarAlerta("No se pudo conectar con el servidor para realizar la búsqueda.", "error");
    }
}