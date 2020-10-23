$file_content = Get-Content $args[0]
$sums = [Array[]]::new($file_content[0].Split([char]9).Length)
$sums = ,0 * $sums.Length

for($i=0;$i -lt $file_content.Length; $i++){
    $row = $file_content[$i].Split([char]9)
    for ($j = 0; $j -lt $row.Length; $j++) {
        $double = $row[$j] -as [double]
        if ($null -ne $double) { $sums[$j] = $sums[$j] + $double }
        else { $sums[$j] = "NaN" }
    }
}
Write-Output $sums