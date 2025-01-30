# 🐼 My Panda  
**¡Un puente entre Django y Pandas para la limpieza de datos!**  

## 🎯 ¿Qué es My Panda?  
**My Panda** es una aplicación web sencilla y funcional que permite a los usuarios cargar archivos en formato `.csv`, realizar una limpieza básica de datos y visualizar tablas directamente en su navegador.

Este proyecto combina dos de mis grandes pasiones: **el desarrollo web** y **el análisis de datos**. Mi objetivo principal es ofrecer una herramienta intuitiva y práctica que refleje mi amor por Python y el potencial de Django y Pandas trabajando juntos.  

Aunque ya existen herramientas similares, este proyecto es mi humilde aporte para explorar y aprender más sobre estas tecnologías, mientras las integro de una forma accesible para cualquier usuario.  

---

## 💡 Funcionalidades Principales  
### ✅ Implementadas  
- **Subida de Archivos CSV**: Los usuarios pueden subir archivos para procesarlos de forma rápida y sencilla.  
- **Visualización de Tablas con Pandas**: El contenido del archivo se muestra como una tabla directamente en la página web.  
- **Estadísticas Básicas**:  
  - Número de filas y columnas.  
  - Detección de columnas con valores nulos.  
  - Identificación de valores duplicados.  
- **Filtrado y Ordenación de Datos**: Herramientas para interactuar con los datos y aplicar filtros o criterios de ordenación.  
- **Descarga de Archivos Limpios**: Exportación del archivo procesado en formato `.csv`.  
- **Visualización de Valores Nulos**: Gráfico que representa los valores faltantes en cada columna.  

### 🚀 Funcionalidades Futuras  
- **Conversión de formatos**: Permitir exportar los datos limpios en `.xlsx` o `.json`, con selección de columnas.  
- **Mayor interactividad**:
  - Filtrar por columnas específicas.  
  - Realizar búsquedas dentro del archivo.  
  - Ordenar los datos por diferentes criterios.  
- **Análisis con gráficos**:  
  - Histogramas para columnas numéricas.  
  - Gráficos de barras para columnas categóricas.  

---

## 🚀 Tecnologías Utilizadas  
- **Frontend:** HTML, CSS, Bootstrap  
- **Backend:** Django  
- **Análisis de Datos:** Pandas  
- **Gráficos y Visualización:** Matplotlib, Seaborn  
- **Base de Datos:** PostgreSQL  
- **Despliegue:** Gunicorn  

---

## 📚 Motivación del Proyecto  
Este proyecto nace de mi pasión por Python y mi interés por combinar el desarrollo web con el análisis de datos. Django y Pandas son herramientas poderosas que, al trabajar juntas, tienen un potencial increíble para resolver problemas reales.

Quise crear un proyecto que me permitiera seguir aprendiendo, enfrentándome a nuevos desafíos y compartiendo una solución útil con la comunidad.  

---

## 🛠️ Instalación y Configuración  
### Prerrequisitos  
- Python 3.x instalado en tu máquina.  
- Un entorno virtual para aislar las dependencias del proyecto.  

### Instalación  
```bash
# Clonar el repositorio
git clone https://github.com/Abednego7/my_panda.git
cd my_panda

# Crear entorno virtual e instalar dependencias
python -m venv env
source env/bin/activate  # En Windows usa: env\Scripts\activate
pip install -r requirements.txt

# Aplicar migraciones e iniciar el servidor
python manage.py migrate
python manage.py runserver
```

---

## 📦 Dependencias Principales  
```text
asgiref==3.8.1
dj-database-url==2.3.0
Django==5.1.3
gunicorn==23.0.0
matplotlib==3.10.0
numpy==2.1.3
pandas==2.2.3
psycopg2-binary==2.9.10
seaborn==0.13.2
sqlparse==0.5.2
tzdata==2024.2
```

---

## 📌 Contacto  
Si tienes alguna sugerencia o duda, no dudes en contactarme. ¡Estoy abierto a mejoras y contribuciones!  

---

## 📷 Preview (hasta ahora)
![Vista previa uno](https://github.com/Abednego7/my_panda/blob/b45995036030da9fe80186e2770f2964fb2441dc/preview/preview.png)
![Vista previa dos](https://github.com/Abednego7/my_panda/blob/b45995036030da9fe80186e2770f2964fb2441dc/preview/preview-two.png)
