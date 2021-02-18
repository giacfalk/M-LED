$match = "PrElGen" 
$replacement = Read-Host "MLED"

$files = Get-ChildItem $(get-location) -filter *PrElGen* -Recurse

$files |
    Sort-Object -Descending -Property { $_.FullName } |
    Rename-Item -newname { $_.name -replace $match, $replacement } -force



$files = Get-ChildItem $(get-location) -include *.cs, *.csproj, *.sln -Recurse 

foreach($file in $files) 
{ 
    ((Get-Content $file.fullname) -creplace $match, $replacement) | set-content $file.fullname 
}

read-host -prompt "Done! Press any key to close."