# Reporte de Integración Continua (CI)

Este documento detalla la configuración y el estado del pipeline de Integración Continua para el proyecto.

## 1. Estado del Pipeline

[![Estado del Workflow de CI/CD](https://github.com/USUARIO/REPOSITORIO/actions/workflows/ci.yml/badge.svg)](https://github.com/USUARIO/REPOSITORIO/actions/workflows/ci.yml)

**Nota:** Reemplaza `USUARIO` y `REPOSITORIO` con tu nombre de usuario y el nombre del repositorio de GitHub para activar el badge de estado.

## 2. Descripción del Workflow

El pipeline de CI/CD está definido en el archivo `.github/workflows/ci.yml` y se ejecuta en cada `push` y `pull_request` a la rama `main`.

### Jobs del Pipeline

#### 2.1. `build`

Este job se encarga de verificar la integridad y calidad del código.

-   **`configurar python`**: Configura el entorno de ejecución con Python 3.11.
-   **`Instalar dependencias`**: Instala las librerías necesarias desde `requirements.txt`.
-   **`ejecutar pruebas con unittest`**: Ejecuta la suite de pruebas unitarias.
-   **`generar reporte de cobertura`**: Crea un reporte de cobertura en formatos `html` y `xml`.
-   **`Subir artefacto de cobertura`**: Sube el reporte de cobertura HTML como un artefacto de la ejecución, que puede ser descargado.
-   **`SonarCloud Scan`**: Envía el reporte de análisis de código y cobertura a SonarCloud.

#### 2.2. `deploy`

Este job se ejecuta solo en los `push` a la rama `main` y después de que el job `build` haya sido exitoso.

-   **`Desplegar a Render`**: Utiliza un *deploy hook* para solicitar a Render que despliegue la última versión de la aplicación desde la rama `main`.

## 3. Calidad del Código y Cobertura

### Cobertura de Pruebas

El pipeline genera un reporte de cobertura de pruebas. El reporte HTML se puede descargar desde los artefactos de la ejecución del workflow en GitHub Actions para un análisis detallado.

### Análisis Estático

Utilizamos **SonarCloud** para el análisis estático del código, que ayuda a identificar bugs, vulnerabilidades y "code smells". Los resultados detallados están disponibles en el dashboard de SonarCloud del proyecto.
