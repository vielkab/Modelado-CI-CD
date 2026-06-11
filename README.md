# ⚽ API Vacacional de Fútbol "El Niño Moi"

Este proyecto es una plataforma web desacoplada diseñada para gestionar de forma automática las pre-inscripciones y el control numérico de cupos para los cursos vacacionales de fútbol. El sistema calcula de manera dinámica las categorías de los niños según su edad y aplica descuentos escalonados si se seleccionan múltiples meses.

## 📂 Estructura del Proyecto

El repositorio se organiza de la siguiente manera para mantener un desarrollo limpio, modular y listo para la contenerización:

```text
├── Backend/
│   ├── main.py              # Código principal de FastAPI (Rutas, validaciones y reglas de negocio)
│   ├── Dockerfile           # Configuración de Docker para desplegar el Backend en Cloud Run
│   └── requirements.txt     # Dependencias del servidor (fastapi, uvicorn, pydantic)
│
├── Frontend/
│   ├── js/
│   │   └── main.js          # Lógica modular en JS (Peticiones fetch GET/POST y actualización de DOM)
│   ├── css/
│   │   └── estilos.css      # Estilos visuales de la interfaz de usuario
│   ├── index.html           # Formulario de inscripción y tabla de cupos dinámica
│   └── Dockerfile           # Configuración de Docker opcional para el despliegue del Frontend
│
└── README.md                # Documentación técnica del proyecto

## 🛠️ Arquitectura del Sistema

El proyecto está estructurado bajo una arquitectura de software limpia y desacoplada:
* **Backend:** Construido con **FastAPI** (Python), encargado de centralizar las reglas de negocio, validar los rangos de edad, controlar los cupos en memoria y procesar los descuentos de forma segura.
* **Frontend:** Una interfaz nativa, ligera y responsiva (**HTML5, CSS3, JavaScript Modular**) que consume la API en caliente y actualiza el inventario visual de cupos en tiempo real sin recargar la página.

---

## 🚀 Instrucciones de Ejecución (Entorno Local)

Sigue estos pasos para poner a correr el ecosistema completo en tu máquina:

### 1. Inicializar el Backend (API)

Asegúrate de tener Python instalado. Abre una terminal en la ruta del backend y ejecuta los siguientes comandos:

```bash
# 1. Navegar a la carpeta del servidor (si estás en la raíz)
cd Backend

# 2. Instalar las dependencias requeridas (FastAPI y Uvicorn)
pip install fastapi uvicorn pydantic

# 3. Inicializar el servidor con recarga automática en caliente
python -m uvicorn main:app --reload

## 🔌 Explicación Teórica de los Métodos HTTP Utilizados

Para que el equipo y el docente comprendan cómo fluye la información en este proyecto, es fundamental dominar los dos métodos del protocolo HTTP que permiten conectar nuestro Frontend con el Backend:

### 1. El Método GET (Consultar Información)
* **¿Qué es en el mundo real?:** Es el equivalente a ir a una cartelera de anuncios a leer la información. Consumes los datos, los miras, pero no alteras nada de lo que está escrito ahí.
* **¿Cómo se aplica en nuestro proyecto?:** Lo usamos exclusivamente para **solicitar y traer** el estado actual de los cupos desde el servidor. Cuando un usuario entra a la página web, el sistema ejecuta un "GET" hacia la ruta del servidor de forma invisible. El servidor responde enviando la lista de los meses con sus respectivos cupos disponibles, y nuestra interfaz toma esos números y los dibuja en la tabla. 
* **Regla clave:** Este método es totalmente seguro y pasivo; no importa cuántas veces se consulte, los cupos no van a cambiar ni a disminuir solo por mirar la tabla.

### 2. El Método POST (Enviar y Procesar Acciones)
* **¿Qué es en el mundo real?:** Es el equivalente a llenar un formulario de matrícula en papel y entregarlo en la ventanilla de recepción. Estás enviando información nueva y específica que la institución debe procesar, validar y registrar, provocando un cambio real en sus carpetas internas.
* **¿Cómo se aplica en nuestro proyecto?:** Lo usamos en el momento exacto en que el representante hace clic en el botón "Inscribir". En ese instante, el Frontend empaqueta todos los datos escritos (el nombre del niño, su edad, el teléfono y los meses que seleccionó) y los envía hacia el Backend mediante un "POST". 
* **Regla clave:** A diferencia del GET, este método **sí altera el estado del servidor**. Cuando el Backend recibe este "POST", activa las reglas de negocio en la memoria: calcula si la edad corresponde a la categoría correcta, aplica los descuentos financieros por cantidad de meses y, si todo está en orden, **resta un cupo** en el inventario del servidor.

### 🔄 El Flujo de Cooperación entre Ambos Métodos

Lo más interesante del proyecto es cómo estos dos métodos trabajan en equipo de forma consecutiva durante una inscripción exitosa:

1. **Lectura Inicial (GET):** El usuario entra a la web, el sistema hace un GET y muestra cuántos cupos quedan.
2. **Procesamiento (POST):** El usuario envía el formulario, se dispara un POST, el servidor procesa los datos y descuenta el cupo internamente.
3. **Actualización Reactiva (GET de nuevo):** En cuanto el Frontend recibe la confirmación de que el POST fue exitoso, el código de JavaScript vuelve a ordenar inmediatamente un método GET en segundo plano. Esto hace que la tabla se vuelva a leer y se actualice con los nuevos cupos reducidos frente a los ojos del usuario al instante, logrando una experiencia fluida sin necesidad de reiniciar o refrescar manualmente toda la página web.