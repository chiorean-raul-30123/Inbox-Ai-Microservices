$serviceRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path "$serviceRoot\..\.."

$env:PYTHONPATH = "$projectRoot\shared\python;$serviceRoot"
$env:CLAMAV_ENABLED="true"
$env:CLAMAV_HOST="localhost"
$env:CLAMAV_PORT="3310"

uvicorn src.main:app --host 0.0.0.0 --port 8102 --reload