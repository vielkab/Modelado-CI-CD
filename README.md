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

Arquitectura del Sistema
El proyecto está estructurado bajo una arquitectura de software limpia y desacoplada:

Backend: Construido con FastAPI (Python), encargado de centralizar las reglas de negocio, validar los rangos de edad, controlar los cupos en memoria y procesar los descuentos de forma segura.

Frontend: Una interfaz nativa, ligera y responsiva (HTML5, CSS3, JavaScript Modular) que consume la API en caliente y actualiza el inventario visual de cupos en tiempo real sin recargar la página.

🚀 Instrucciones de Ejecución (Entorno Local)
Sigue estos pasos para poner a correr el ecosistema completo en tu máquina:

1. Inicializar el Backend (API)
Asegúrate de tener Python instalado. Abre una terminal en la ruta del backend y ejecuta los siguientes comandos:

Bash
# 1. Navegar a la carpeta del servidor (si estás en la raíz)
cd Backend

# 2. Instalar las dependencias requeridas (FastAPI y Uvicorn)
pip install fastapi uvicorn pydantic

# 3. Inicializar el servidor con recarga automática en caliente
py -m uvicorn main:app --reload
🔌 Explicación Teórica de los Métodos HTTP Utilizados
Para que el equipo y el docente comprendan cómo fluye la información en este proyecto, es fundamental dominar los métodos del protocolo HTTP que permiten conectar nuestro Frontend con el Backend:

1. El Método GET (Consultar Información)
¿Qué es en el mundo real?: Es el equivalente a ir a una cartelera de anuncios a leer la información. Consumes los datos, los miras, pero no alteras nada de lo que está escrito ahí.

¿Cómo se aplica en nuestro proyecto?: Lo usamos para solicitar y traer el estado actual de los cupos generales desde el servidor hacia la tabla informativa. Adicionalmente, se emplea un GET específico mediante la cédula para consultar y extraer la ficha detallada de un alumno inscrito con sus respectivos desgloses financieros.

Regla clave: Este método es totalmente seguro y pasivo; no importa cuántas veces se consulte, los datos no van a cambiar ni a disminuir solo por mirar.

2. El Método POST (Enviar y Procesar Acciones)
¿Qué es en el mundo real?: Es el equivalente a llenar un formulario de matrícula en papel y entregarlo en la ventanilla de recepción. Estás enviando información nueva que la institución debe procesar, validar y registrar.

¿Cómo se aplica en nuestro proyecto?: Lo usamos en el momento exacto en que el representante hace clic en el botón "Proceder con la Pre-Inscripción". El Frontend empaqueta todos los datos del formulario y los envía al Backend para validar la edad, aplicar descuentos y restar un cupo en la memoria del servidor.

Regla clave: A diferencia del GET, este método sí altera el estado del servidor al crear un nuevo registro.

3. El Método PUT (Actualización Completa)
¿Qué es en el mundo real?: Es como reemplazar una carpeta de matrícula vieja por una completamente nueva que tiene todos los campos corregidos de golpe.

¿Cómo se aplica en nuestro proyecto?: Se ejecuta mediante la opción "Actualizar Ficha Completa", donde se sobrescriben todos los campos modificables del alumno registrado (como el nombre del representante, el nombre del niño y el teléfono) bajo su misma cédula.

4. El Método PATCH (Actualización Parcial)
¿Qué es en el mundo real?: Es el equivalente a usar corrector líquido sobre un único renglón específico de la ficha (como el número de teléfono) sin alterar el resto del documento original.

¿Cómo se aplica en nuestro proyecto?: Lo mapeamos en la función "Cambiar Teléfono". Permite modificar únicamente este dato de contacto de manera ligera y directa en el servidor sin necesidad de reenviar toda la información del alumno.

5. El Método DELETE (Eliminación de Recursos)
¿Qué es en el mundo real?: Es retirar la ficha de inscripción del archivador para dar de baja al alumno del curso vacacional.

¿Cómo se aplica en nuestro proyecto?: Se activa con la acción "Dar de Baja Alumno". Al enviar la cédula, el Backend borra al estudiante de la lista de inscritos y ejecuta la lógica inversa de negocio: devuelve y suma (+1) el cupo liberado en la tabla de los meses correspondientes.

🔄 El Flujo de Cooperación entre Métodos
Lo más interesante del proyecto es cómo estos métodos trabajan en equipo de forma consecutiva para lograr una experiencia reactiva:

Lectura Inicial (GET): El usuario entra a la web, el sistema lee los cupos y los dibuja en la tabla.

Procesamiento (POST/PUT/PATCH/DELETE): El usuario realiza una acción en la gestión de alumnos, el Frontend se comunica con el Backend, y este procesa los cambios alterando los datos en caliente.

Actualización Reactiva (GET de nuevo): En cuanto el Frontend recibe la confirmación exitosa (Status 200 OK) de cualquier operación de escritura, el código de JavaScript vuelve a ordenar inmediatamente un método GET en segundo plano. Esto hace que la tabla se vuelva a leer y se actualice frente a los ojos del usuario al instante, sin necesidad de refrescar manualmente toda la página web.