$file_content = Get-Content $args[0]

for($i=0; $i -lt $file_content.Length; $i++){
    $row = $file_content[$i].Split([char]9)
    for($k = 1; $k -lt $args.Length; $k++){
        if($row -contains $args[$k]){
            Write-Host $row
            $k = $args.Length
        }
    }
}
