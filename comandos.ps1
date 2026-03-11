
param(
    [string]$palabra
)


switch ($palabra) {
    "activar" { .\backend\Scripts\Activate.ps1 }
    "cerrar" { deactivate }
    "ejecutar" { python -m flask --app .\src\app.py run }
    default { Write-Output "opcion no valida" }
}