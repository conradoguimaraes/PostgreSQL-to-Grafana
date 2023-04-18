$randomName = -join ((65..90) + (97..122) | Get-Random -Count 10 | % {[char]$_})

$destinationFolder = "C:\Users\Podengos\AppData\Local\Temp\sphinxBuild_"+$randomName
$destinationFolder

Get-Item –Path build | Move-Item -Destination $destinationFolder

echo "End of Program."