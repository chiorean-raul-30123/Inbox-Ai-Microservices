$serviceRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path "$serviceRoot\..\.."

$env:PYTHONPATH = "$projectRoot\shared\python;$serviceRoot"

python -m src.main