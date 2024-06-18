$url = "http://localhost:5000/shorten"

$body = @{
    long_url = "http://example.com"
}

$response = Invoke-RestMethod -Uri $url -Method Post -ContentType "application/json" -Body ($body | ConvertTo-Json)

$response | Format-Table -AutoSize
