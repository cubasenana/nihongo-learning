param(
  [Parameter(Mandatory = $true)]
  [int]$Lesson,
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

function Add-Issue {
  param(
    [string]$Level,
    [string]$File,
    [int]$Line,
    [string]$Message
  )
  $script:Issues += [pscustomobject]@{
    Level = $Level
    File = $File
    Line = $Line
    Message = $Message
  }
}

$Issues = @()
$lessonName = "lesson-{0:D2}.md" -f $Lesson
$syllabusDir = Join-Path $Root "md/syllabus"
$lessonPath = Join-Path $syllabusDir $lessonName
$unlockPath = Join-Path $syllabusDir "grammar-unlock.md"

if (-not (Test-Path -LiteralPath $lessonPath)) {
  Add-Issue "P0" $lessonPath 0 "Lesson file is missing."
}

if (-not (Test-Path -LiteralPath $unlockPath)) {
  Add-Issue "P0" $unlockPath 0 "grammar-unlock.md is missing."
}

if (Test-Path -LiteralPath $lessonPath) {
  $lines = Get-Content -LiteralPath $lessonPath
  $text = $lines -join "`n"

  $requiredHeadings = @(
    "## 语法点",
    "## 课文",
    "## 生词表",
    "## 表达要点",
    "## 练习框架"
  )

  foreach ($heading in $requiredHeadings) {
    if ($text -notmatch [regex]::Escape($heading)) {
      Add-Issue "P0" $lessonPath 0 "Missing required heading: $heading"
    }
  }

  for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i].Contains([char]0xfffd)) {
      Add-Issue "P0" $lessonPath ($i + 1) "Replacement character U+FFFD found."
    }
  }

  if ($text -notmatch "\*\*语法覆盖\*\*") {
    Add-Issue "P0" $lessonPath 0 "Grammar coverage line is missing."
  }

  if ($text -notmatch "📖") {
    Add-Issue "P0" $lessonPath 0 "No 📖 marker found in lesson file."
  }

  $expectedColumns = $null
  $tableStart = 0
  for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    if ($line -match "^\|") {
      $columns = ([regex]::Matches($line, "\|")).Count - 1
      if ($null -eq $expectedColumns) {
        $expectedColumns = $columns
        $tableStart = $i + 1
      } elseif ($columns -ne $expectedColumns) {
        Add-Issue "P0" $lessonPath ($i + 1) "Markdown table column mismatch. Expected $expectedColumns columns from line $tableStart, got $columns."
      }
    } else {
      $expectedColumns = $null
      $tableStart = 0
    }
  }
}

Write-Output "# Gate Mechanical Precheck"
Write-Output ""
Write-Output "- Lesson: L$('{0:D2}' -f $Lesson)"
Write-Output "- File: $lessonPath"
Write-Output ""

if ($Issues.Count -eq 0) {
  Write-Output "Result: OK"
  exit 0
}

Write-Output "Result: Issues found"
Write-Output ""
Write-Output "| Level | File | Line | Message |"
Write-Output "|-------|------|------|---------|"
foreach ($issue in $Issues) {
  Write-Output ("| {0} | {1} | {2} | {3} |" -f $issue.Level, $issue.File, $issue.Line, $issue.Message)
}

if ($Issues | Where-Object { $_.Level -eq "P0" }) {
  exit 1
}

exit 0
