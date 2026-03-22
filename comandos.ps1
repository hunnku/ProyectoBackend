
param(
    [string]$palabra
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$activateScript = Join-Path $scriptDir 'backend\Scripts\Activate.ps1'

switch ($palabra) {
    "activar" {
        . "$scriptDir\backend\Scripts\Activate.ps1"
    }
    "cerrar" {
        if (Get-Command deactivate -ErrorAction SilentlyContinue) {
            deactivate
        } else {
            Write-Warning "No hay comando 'deactivate' disponible."
        }
    }
    "ejecutar" {
        python -m flask --app "$scriptDir\src\app.py" run
    }
    "apidoc" {
        python -m flask --app "$scriptDir\src\apidoc.py" run
    }
    "test" {
        python -m unittest discover -s "$scriptDir\test"
    }
    default {
        Write-Output "opcion no valida"
    }
}