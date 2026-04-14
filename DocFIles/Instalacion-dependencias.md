# Instalación de dependencias para el proyecto

Este proyecto usa Python y requiere instalar las librerías externas en el mismo intérprete que se usa para ejecutar el código.

## Pasos recomendados

1. Abre PowerShell o la terminal en la carpeta del proyecto:
   ```powershell
   cd "c:\Users\julia\OneDrive\Documentos\IO methods"
   ```

2. Activa el entorno virtual si existe:
   ```powershell
   .venv\Scripts\activate
   ```

3. Instala las dependencias con el archivo `requirements.txt`:
   ```powershell
   pip install -r requirements.txt
   ```

4. Si necesitas actualizar `pip`:
   ```powershell
   python -m pip install --upgrade pip
   ```

## Qué hace cada paso

- `activate`: asegura que Python use el entorno virtual del proyecto.
- `pip install -r requirements.txt`: instala las librerías necesarias.
- `requirements.txt` contiene dependencias como `PySide6` y `numpy`.

## Qué hacer si aparece un error

- Si falta `PySide6`, revisa que estés usando el intérprete correcto.
- Si se usa un Python distinto al del entorno virtual, aparecerá:
  - `ModuleNotFoundError: No module named 'PySide6'`

## Recomendación

Siempre usa el mismo entorno virtual para instalar dependencias y ejecutar el proyecto. Esto evita que Python busque paquetes en otro intérprete.
