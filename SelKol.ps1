$file_content = Get-Content $args[0]
$numOfArgs = $args.Length

for($i=0;$i -lt $file_content.Length; $i++){
    for($j=1; $j -lt $numOfArgs; $j++){
        Write-Host $file_content[$i].Split([char]9)[$args[$j]] $([char]9) -NoNewLine
    }
    Write-Host
}