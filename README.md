# Proyecto Integrado - SAFA Restaurant

## Descripción del Proyecto

El objetivo de este proyecto es desarrollar una aplicación web para la gestión de un restaurante, integrando los conocimientos adquiridos en todas las asignaturas del CFGS en Desarrollo de Aplicaciones Web (DAW). Cada grupo de alumnos deberá elegir la temática de su restaurante (pizzería, comida rápida, sushi, etc.) y construir un sistema que permita administrar sus operaciones diarias. La aplicación se desarrollará utilizando **Python con Django, una base de datos relacional y tecnologías web para el frontend**.

La plataforma gestionará los distintos roles del restaurante: clientes, camareros, cocineros y administradores. Los clientes podrán consultar la carta y realizar pedidos, los camareros asignarán mesas y atenderán órdenes, los cocineros gestionarán los platos en preparación y los administradores controlarán el negocio. Además, se implementarán funciones como el seguimiento del estado de los pedidos, la solicitud de cuenta y la administración de empleados y productos del menú. Este proyecto integrará aspectos técnicos, organizativos y de sostenibilidad, permitiendo a los alumnos aplicar sus conocimientos en un entorno práctico y colaborativo.

## Requisitos Funcionales

### Gestión de Usuarios
- Registro con correo/usuario y contraseña.
- Inicio de sesión seguro con recuperación de contraseña.
- Perfiles personalizables con foto y datos de usuario.
- Gestión de roles: Administrador, Cliente, Camarero, Cocinero.

### Gestión del Restaurante
- CRUD de la carta (añadir, modificar, eliminar platos y bebidas).
- Gestión de mesas: asignación, disponibilidad y estado.
- Configuración del horario de apertura y cierre.

### Gestión de Pedidos
- Tomar pedidos de clientes (presenciales y online).
- Actualizar el estado del pedido (en preparación, servido, pagado).
- Historial de pedidos por cliente y por mesa.

### Roles y Funcionalidades
#### Cliente:
- Consultar la carta y realizar pedidos.
- Solicitar la cuenta desde la aplicación.

#### Camarero:
- Asignar mesas y gestionar pedidos de clientes.
- Solicitar cobro y marcar mesas como disponibles.

#### Cocinero:
- Ver pedidos pendientes y cambiar su estado a preparado por producto.
- Visualizar recetas y tiempos estimados.

#### Administrador:
- Gestión de empleados y asignación de roles.
- Gestión de la carta y configuración del restaurante.
- Generación de reportes sobre ventas y pedidos.

### Facturación y Pagos
- Generación de facturas con desglose de productos y precios.

## Requisitos No Funcionales

### Rendimiento
- Operaciones comunes en menos de 2 segundos.
- Capacidad para manejar 1000 usuarios concurrentes.

### Seguridad
- Contraseñas cifradas (bcrypt).
- Protección contra ataques como SQL Injection, XSS y CSRF.

### Escalabilidad
- Preparado para la expansión a más usuarios.
- Escalabilidad horizontal para backend y base de datos.

### Compatibilidad
- Compatible con navegadores modernos (Chrome, Firefox, Edge, Safari).

### Usabilidad
- Interfaz intuitiva con diseño centrado en el usuario.
- Sistema de ayuda para guiar a nuevos usuarios.

## Plan de Desarrollo del Proyecto
1. **Definir la Temática del Restaurante**
2. **Modelado de la Base de Datos**
3. **Desarrollo del Backend**
4. **Desarrollo del Frontend**
5. **Documentación**

## Relación del Proyecto con las Asignaturas

| Módulo               | Contribución al Proyecto                                                                 |
|----------------------|------------------------------------------------------------------------------------------|
| **BD**               | Creación de BBDD Oracle, tablas, relaciones, históricos de sesiones, funciones y procedimientos. |
| **LMSGI**            | Diseño de mockups, interfaz responsive, validación de formularios, carrito de compras, modo claro/oscuro. |
| **Programación**     | Desarrollo del backend con Django, lógica de negocio, gestión de sesiones y autenticación. |
| **Digitalización**   | Análisis del impacto de la digitalización en la restauración, esquema de procesos y propuestas de mejora. |
| **Sistemas Informáticos** | Definición e instalación de redes, diseño de diagrama lógico de red. |

