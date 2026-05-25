$serviceRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path "$serviceRoot\..\.."

$env:PYTHONPATH = "$projectRoot\shared\python;$serviceRoot"

uvicorn src.main:app --host 0.0.0.0 --port 8101 --reload