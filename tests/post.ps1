$url = "http://localhost:5000/shorten"

$body = @{
    long_url = "http://example.com"
}

$response = Invoke-RestMethod -Uri $url -Method Post -ContentType "application/json" -Body ($body | ConvertTo-Json)

$response | Format-Table -AutoSize

# If you get an error about the execution policy, you may need to change the PowerShell execution policy to allow scripts to run.
# You can do this with the command:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser