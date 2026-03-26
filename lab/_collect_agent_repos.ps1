$ErrorActionPreference = 'Stop'
$queries = @(
  '"ai agent" (language:Python OR language:TypeScript) pushed:>2026-02-01 stars:>50',
  '"llm agent" language:Python pushed:>2026-02-01 stars:>50',
  '"rag agent" (language:Python OR language:TypeScript) pushed:>2026-02-01 stars:>20',
  'topic:ai-agents pushed:>2026-02-01 stars:>50',
  'topic:llm-agents pushed:>2026-02-01 stars:>20',
  'topic:rag pushed:>2026-02-01 stars:>100',
  '"multi-agent" language:Python pushed:>2026-02-01 stars:>50',
  '"knowledge base" "agent" language:Python pushed:>2026-02-01 stars:>20'
)
$all = @()
foreach($q in $queries){
  $enc = [uri]::EscapeDataString($q)
  $url = "https://api.github.com/search/repositories?q=$enc&sort=updated&order=desc&per_page=20"
  try {
    $resp = Invoke-RestMethod -Headers @{'User-Agent'='copilot-agent';'Accept'='application/vnd.github+json'} -Uri $url -Method Get
    foreach($it in $resp.items){
      $all += [pscustomobject]@{
        query = $q
        full_name = $it.full_name
        html_url = $it.html_url
        description = $it.description
        language = $it.language
        stars = [int]$it.stargazers_count
        forks = [int]$it.forks_count
        pushed_at = $it.pushed_at
        created_at = $it.created_at
        updated_at = $it.updated_at
        topics = ($it.topics -join ',')
        license = if($it.license){$it.license.spdx_id}else{'NONE'}
        archived = [bool]$it.archived
      }
    }
  } catch {
    Write-Host "query_failed: $q"
  }
  Start-Sleep -Milliseconds 500
}
$dedup = $all | Group-Object full_name | ForEach-Object { $_.Group | Sort-Object stars -Descending | Select-Object -First 1 }
$cut = (Get-Date).AddDays(-30)
$scored = $dedup | Where-Object { -not $_.archived } | ForEach-Object {
  $ageDays = [math]::Max(1, ((Get-Date) - ([datetime]$_.created_at)).TotalDays)
  $recentBoost = if(([datetime]$_.pushed_at) -ge $cut){1.2}else{1.0}
  $licenseBoost = if($_.license -ne 'NONE' -and $_.license -ne 'NOASSERTION'){1.05}else{0.95}
  $trend = [math]::Round((($_.stars / [math]::Sqrt($ageDays)) * $recentBoost * $licenseBoost), 2)
  $_ | Add-Member -NotePropertyName trend_score -NotePropertyValue $trend -PassThru
}
$top = $scored | Sort-Object trend_score -Descending | Select-Object -First 10
$top | ConvertTo-Json -Depth 4 | Out-File -FilePath 'lab/top10_agent_apps_raw.json' -Encoding utf8
$scored | Sort-Object trend_score -Descending | Select-Object -First 50 | Export-Csv -NoTypeInformation -Path 'lab/top50_agent_apps_scored.csv' -Encoding utf8
Write-Host "candidates=$($dedup.Count)"
Write-Host 'top_saved=lab/top10_agent_apps_raw.json'
Write-Host 'scored_saved=lab/top50_agent_apps_scored.csv'
$top | Select-Object full_name,stars,language,pushed_at,trend_score | Format-Table -AutoSize | Out-String -Width 240 | Write-Host
