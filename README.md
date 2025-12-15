# Evaluacion2_Django-TailWindCSS

# Sistema de Gestión de Ventas

Sistema web desarrollado con Django y Tailwind CSS para la gestión de ventas, clientes y productos. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre ventas, clientes y productos, así como el seguimiento de detalles de ventas.

## Características

- ✨ Interfaz moderna con Tailwind CSS
- 📦 Gestión completa de productos
- 👥 Administración de clientes
- 💰 Registro y seguimiento de ventas
- 📊 Detalles de ventas con cálculos automáticos
- 🔒 Sistema de autenticación Django

## Requisitos

- Python 3.9+
- Django 4.2+
- Base de datos SQLite (incluida)

## Instalación

1. Clonar el repositorio:
```powershell
git clone <https://github.com/Dania2701/Evaluacion2_Django-TailWindCSS.git>
Set-Location ventas_project_new
```

2. Crear y activar entorno virtual:
```powershell
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```
> Si aparece el error “running scripts is disabled…”, ejecuta (como administrador):
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```
> Luego vuelve a activar:
> ```powershell
> .\venv\Scripts\Activate.ps1
> ```

3. Instalar dependencias:
```powershell
pip install django
```

4. Aplicar migraciones:
```powershell
python manage.py makemigrations
python manage.py migrate
```

5. Crear superusuario (opcional):
```powershell
python manage.py createsuperuser
```

6. Iniciar servidor de desarrollo:
```powershell
python manage.py runserver
```

El sistema estará disponible en: http://127.0.0.1:8000/ventas/

## Estructura del Proyecto

```
ventas_project_new/
├── manage.py
├── ventas/                 # Aplicación principal
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Lógica de vistas
│   ├── forms.py           # Formularios
│   ├── urls.py            # URLs de la aplicación
│   └── templates/         # Plantillas HTML
│       └── ventas/        # Templates específicos
├── ventas_project_new/    # Configuración del proyecto
│   ├── settings.py        # Configuración general
│   ├── urls.py           # URLs del proyecto
│   └── wsgi.py           # Configuración WSGI
└── static/               # Archivos estáticos
```

## Modelos

### Cliente
- Nombre
- Email (único)
- RUT (único)
- Fecha de creación/modificación

### Producto
- Nombre
- Categoría
- Precio
- Fecha de creación/modificación

### Venta
- Cliente (ForeignKey)
- Fecha
- Total (calculado automáticamente)
- Fecha de creación/modificación

### DetalleVenta
- Venta (ForeignKey)
- Producto (ForeignKey)
- Cantidad
- Precio
- Descuento
- Fecha de creación/modificación

## Funcionalidades Principales

### Gestión de Clientes
- Crear nuevo cliente
- Listar todos los clientes
- Editar información de cliente
- Eliminar cliente

### Gestión de Productos
- Agregar nuevo producto
- Listar productos disponibles
- Actualizar información de producto
- Eliminar producto

### Gestión de Ventas
- Crear nueva venta
- Ver lista de ventas
- Ver detalles de venta específica
- Eliminar venta

## Uso

1. Acceder al sistema:
   - Abrir http://127.0.0.1:8000/. (En caso de no funcionar, probar el siguiente link http://127.0.0.1.8000/ventas/)
   - Iniciar sesión si es necesario

2. Gestión de Clientes:
   - Ir a /clientes/
   - Usar el botón "Crear Nuevo Cliente"
   - Completar formulario con datos del cliente

3. Gestión de Productos:
   - Ir a /productos/
   - Usar "Crear Nuevo Producto"
   - Ingresar detalles del producto

4. Registro de Ventas:
   - Ir a /ventas/
   - Clic en "Nueva Venta"
   - Seleccionar cliente y productos
   - El total se calcula automáticamente

## Características Técnicas

- Cálculo automático de totales de venta
- Validación de formularios
- Manejo de errores y excepciones
- Interfaz responsiva con Tailwind CSS
- URLs amigables y navegación intuitiva

## Desarrollo

Para contribuir al proyecto:

1. Crear rama feature:
```powershell
git checkout -b feature/nombre-caracteristica
```

2. Realizar cambios y commits:
```powershell
git add .
git commit -m "Descripción del cambio"
```

3. Subir cambios:
```powershell
git push origin feature/nombre-caracteristica
```

## Contacto

Para dudas o sugerencias, contactar a:
- GitHub: [Dania2701](https://github.com/Dania2701)