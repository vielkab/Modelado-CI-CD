// CONFIGURACIÓN: URL del Backend (provisional)
const API_URL = "http://desplieguecontinuomodelado-env.eba-fihm92pm.us-east-1.elasticbeanstalk.com/docs";

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
            
            // Actualizar los números de la tabla dinámicamente en caliente
            const celda6_8 = document.getElementById(`cupo-${mesMinuscula}-6-8`);
            const celda9_11 = document.getElementById(`cupo-${mesMinuscula}-9-11`);
            const celda12_14 = document.getElementById(`cupo-${mesMinuscula}-12-14`);
            
            if (celda6_8) celda6_8.innerText = item.c6_8 <= 0 ? "Agotado" : item.c6_8;
            if (celda9_11) celda9_11.innerText = item.c9_11 <= 0 ? "Agotado" : item.c9_11;
            if (celda12_14) celda12_14.innerText = item.c12_14 <= 0 ? "Agotado" : item.c12_14;
            
            // Si todo el mes se queda sin cupos en general, deshabilitamos el checkbox
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
        event.preventDefault(); // Evita que la página se recargue

        const nombre_representante = document.getElementById("txt-representante").value.trim();
        const nombre_nino = document.getElementById("txt-nino").value.trim();
        const edad = parseInt(document.getElementById("txt-edad").value, 10);
        const telefono = document.getElementById("txt-telefono").value.trim();

        const meses_seleccionados = [];
        const checkboxesMarcados = document.querySelectorAll(".clase-mes:checked");
        checkboxesMarcados.forEach(cb => {
            meses_seleccionados.push(cb.value);
        });

        const payload = {
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
                cargarCuposTabla(); // Recarga la tabla en vivo con los cupos actualizados
            } else {
                mostrarAlerta(resultado.detail || "Error en la inscripción.", "error");
            }
        } catch (error) {
            console.error("Error en la petición POST:", error);
            mostrarAlerta("No se pudo conectar con el servidor de la API.", "error");
        }
    });
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