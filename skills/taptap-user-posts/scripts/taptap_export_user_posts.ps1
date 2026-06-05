param(
  [Parameter(Mandatory = $true)]
  [string]$UserId,

  [string]$OutDir = "",
  [string]$PythonPath = "",
  [int]$Limit = 10,
  [int]$RetryCount = 3,
  [int]$SleepMilliseconds = 250,
  [switch]$SkipFetch,
  [switch]$SkipDetails,
  [switch]$SkipTopicDetails,
  [switch]$OnlyFetchMissingTopicDetails
)

$ErrorActionPreference = "Stop"

if ($Limit -lt 1 -or $Limit -gt 10) {
  throw "TapTap by-user API currently supports Limit between 1 and 10."
}

$xua = "V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D102%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3D1f111717-ec6d-4fb8-b700-b42244fbc766%26OS%3DWindows%26OSV%3DNT%26DT%3DPC"
$base = "https://www.taptap.cn"
if (-not $OutDir) {
  $OutDir = Join-Path (Join-Path (Get-Location) "outputs") ("taptap_" + $UserId)
}
$outRoot = [System.IO.Path]::GetFullPath($OutDir)
$rawDir = Join-Path $outRoot "raw"
$feedDir = Join-Path $rawDir "user_feed_pages"
$detailsDir = Join-Path $rawDir "moment_details"
$topicDetailsDir = Join-Path $rawDir "topic_details"
$combinedPath = Join-Path $rawDir "user_feed_all_raw.json"
$processorPath = Join-Path $PSScriptRoot "taptap_process_posts.py"

New-Item -ItemType Directory -Force -Path $outRoot, $rawDir, $feedDir, $detailsDir, $topicDetailsDir | Out-Null

if (-not (Test-Path -LiteralPath $processorPath)) {
  throw "Missing processor script: $processorPath"
}

if (-not $PythonPath) {
  $bundled = "C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
  if (Test-Path -LiteralPath $bundled) {
    $PythonPath = $bundled
  } else {
    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if ($cmd) {
      $PythonPath = $cmd.Source
    }
  }
}
if (-not $PythonPath -or -not (Test-Path -LiteralPath $PythonPath)) {
  throw "Python not found. Pass -PythonPath C:\path\to\python.exe."
}

$headers = @{
  "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
  "Accept" = "application/json, text/plain, */*"
  "Accept-Language" = "zh-CN,zh;q=0.9"
}

function Invoke-TapTapJson {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Url
  )
  $content = $null
  for ($attempt = 1; $attempt -le $RetryCount; $attempt++) {
    try {
      $resp = Invoke-WebRequest -Uri $Url -Headers $headers -UseBasicParsing
      $content = $resp.Content
      break
    } catch {
      if ($attempt -eq $RetryCount) { throw }
      Start-Sleep -Seconds $attempt
    }
  }
  return $content
}

if (-not $SkipFetch) {
  $next = "/webapiv2/feed/v7/by-user?user_id=$UserId&limit=$Limit&__times=0"
  $all = New-Object System.Collections.Generic.List[object]
  $seen = @{}
  $page = 1

  while ($next) {
    if ($seen.ContainsKey($next)) {
      throw "Repeated next_page detected: $next"
    }
    $seen[$next] = $true

    $separator = If ($next.Contains("?")) { "&" } Else { "?" }
    $url = "$base$next$separator" + "X-UA=$xua"
    $pagePath = Join-Path $feedDir ("page_{0:D3}.json" -f $page)
    $content = Invoke-TapTapJson -Url $url
    $content | Set-Content -LiteralPath $pagePath -Encoding UTF8

    $json = $content | ConvertFrom-Json
    if (-not $json.success) {
      throw "TapTap API returned success=false on feed page $page"
    }
    foreach ($item in $json.data.list) {
      $all.Add($item) | Out-Null
    }

    Write-Host ("feed page={0} count={1} total_so_far={2} next={3}" -f $page, $json.data.list.Count, $all.Count, [bool]$json.data.next_page)
    $next = $json.data.next_page
    $page += 1
    Start-Sleep -Milliseconds $SleepMilliseconds
  }

  [pscustomobject]@{
    fetched_at = (Get-Date).ToString("s")
    source = "https://www.taptap.cn/user/$UserId"
    count = $all.Count
    items = $all
  } | ConvertTo-Json -Depth 100 | Set-Content -LiteralPath $combinedPath -Encoding UTF8
} elseif (-not (Test-Path -LiteralPath $combinedPath)) {
  throw "SkipFetch was set, but raw feed file does not exist: $combinedPath"
}

if (-not $SkipDetails) {
  $feedPayload = Get-Content -LiteralPath $combinedPath -Raw -Encoding UTF8 | ConvertFrom-Json
  if ($OnlyFetchMissingTopicDetails) {
    $ids = @(
      $feedPayload.items |
        Where-Object { $_.moment -and -not $_.moment.topic } |
        ForEach-Object { $_.moment.id_str }
    )
  } else {
    $ids = @(
      $feedPayload.items |
        Where-Object { $_.moment } |
        ForEach-Object { $_.moment.id_str }
    )
  }
  $i = 0
  foreach ($id in $ids) {
    $i += 1
    $path = Join-Path $detailsDir "$id.json"
    if (Test-Path -LiteralPath $path) {
      Write-Host ("detail skip {0}/{1} {2}" -f $i, $ids.Count, $id)
      continue
    }
    $url = "$base/webapiv2/moment/v3/detail?id=$id&X-UA=$xua"
    $content = Invoke-TapTapJson -Url $url
    $content | Set-Content -LiteralPath $path -Encoding UTF8
    Write-Host ("detail {0}/{1} {2}" -f $i, $ids.Count, $id)
    Start-Sleep -Milliseconds $SleepMilliseconds
  }
}

if (-not $SkipTopicDetails) {
  $feedPayload = Get-Content -LiteralPath $combinedPath -Raw -Encoding UTF8 | ConvertFrom-Json
  $topicPairs = New-Object System.Collections.Generic.List[object]
  $seenTopicIds = @{}
  foreach ($item in $feedPayload.items) {
    if ($item.moment -and $item.moment.topic -and $item.moment.topic.id_str) {
      $topicId = [string]$item.moment.topic.id_str
      if (-not $seenTopicIds.ContainsKey($topicId)) {
        $seenTopicIds[$topicId] = $true
        $topicPairs.Add([pscustomobject]@{ moment_id = [string]$item.moment.id_str; topic_id = $topicId }) | Out-Null
      }
    }
    if ($item.moment -and $item.moment.reposted_moment -and $item.moment.reposted_moment.topic -and $item.moment.reposted_moment.topic.id_str) {
      $topicId = [string]$item.moment.reposted_moment.topic.id_str
      if (-not $seenTopicIds.ContainsKey($topicId)) {
        $seenTopicIds[$topicId] = $true
        $topicPairs.Add([pscustomobject]@{ moment_id = [string]$item.moment.reposted_moment.id_str; topic_id = $topicId }) | Out-Null
      }
    }
  }
  $i = 0
  foreach ($pair in $topicPairs) {
    $i += 1
    $path = Join-Path $topicDetailsDir ("{0}__{1}.json" -f $pair.moment_id, $pair.topic_id)
    if (Test-Path -LiteralPath $path) {
      Write-Host ("topic skip {0}/{1} {2}" -f $i, $topicPairs.Count, $pair.topic_id)
      continue
    }
    $url = "$base/webapiv2/topic/v1/detail?id=$($pair.topic_id)&X-UA=$xua"
    $content = Invoke-TapTapJson -Url $url
    $content | Set-Content -LiteralPath $path -Encoding UTF8
    Write-Host ("topic {0}/{1} {2}" -f $i, $topicPairs.Count, $pair.topic_id)
    Start-Sleep -Milliseconds $SleepMilliseconds
  }
}

$prefix = "taptap_$UserId"
& $PythonPath $processorPath `
  --raw $combinedPath `
  --details-dir $detailsDir `
  --topic-details-dir $topicDetailsDir `
  --out-dir $outRoot `
  --user-id $UserId `
  --prefix $prefix

Write-Host ("DONE output_dir={0}" -f $outRoot)
