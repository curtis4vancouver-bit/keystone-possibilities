# setup_kdp_workspace.ps1
# Programmatically sets up the Amazon KDP manuscript development workspace at C:\Users\Curtis\Keystone_Downloads

$targetDir = "C:\Users\Curtis\Keystone_Downloads"
$folders = @("Templates", "Output", "Source")

Write-Host "==============================================" -ForegroundColor Yellow
Write-Host "   KEYSTONE KDP WORKSPACE INITIALIZER v1.0   " -ForegroundColor Yellow
Write-Host "==============================================" -ForegroundColor Yellow
Write-Host ""

# Create base directories
if (-not (Test-Path $targetDir)) {
    try {
        New-Item -Path $targetDir -ItemType Directory -Force | Out-Null
        Write-Host "Successfully created base directory: $targetDir" -ForegroundColor Green
    } catch {
        Write-Error "Failed to create directory $targetDir : $_"
        exit
    }
} else {
    Write-Host "Base directory already exists: $targetDir" -ForegroundColor Cyan
}

foreach ($folder in $folders) {
    $fullPath = Join-Path $targetDir $folder
    if (-not (Test-Path $fullPath)) {
        New-Item -Path $fullPath -ItemType Directory -Force | Out-Null
        Write-Host "Successfully created sub-directory: $fullPath" -ForegroundColor Green
    } else {
        Write-Host "Sub-directory already exists: $fullPath" -ForegroundColor Cyan
    }
}

# Create a sample Manuscript Source Outline
$sourceOutlinePath = Join-Path $targetDir "Source\Manuscript_Raw.txt"
if (-not (Test-Path $sourceOutlinePath)) {
    $outlineContent = @"
# THE KEYSTONE PROTOCOL: METABOLIC SCIENCE & RECOMPOSITION MANUAL
Authored by: Wayne Stevenson
Published under: Keystone wellness Architecture

========================================================================
PART 1: THE FOUNDATIONAL MINDSET
========================================================================
- The High-Performance Tradesman: Cellular leverage under heavy load.
- Moving beyond traditional bodybuilding models into systemic biohacking.

========================================================================
PART 2: THE REBUILD PHASE (THE WOLVERINE STACK)
========================================================================
- BPC-157 (Body Protection Compound 157): Gastric stability, systemic inflammation, tendon-to-bone repair.
- TB-500 (Thymosin Beta-4): Cellular migration, tissue regeneration, rapid joint healing.
- CJC-1295 / Ipamorelin: Natural GH secretagogues for nightly restoration and deep sleep.
- Standard Safety Case Study: 5-month repair cycle and proper titration schedules.

========================================================================
PART 3: THE PEPTIDE GLP-1 CO-PROTOCOL
========================================================================
- Tirzepatide & Semaglutide: Mitigating high metabolic stress, insulin sensitivity, and visceral fat reduction.
- Preventing Ozempic Face, Hair Loss, & Muscle Wasting: 
  * The GHK-Cu topical peptide skin matrix.
  * Maintaining the 200g daily protein floor.
  * Essential mineral and hydration formulas.

========================================================================
PART 4: SYSTEM DESIGN & BLUEPRINTS
========================================================================
- High-concurrency focus sessions: Original Melodic House tracks for deep workflow.
- Standard daily wellness trackers and data-driven metabolic logs.
"@

    Set-Content -Path $sourceOutlinePath -Value $outlineContent -Force
    Write-Host "Successfully initialized raw manuscript draft: $sourceOutlinePath" -ForegroundColor Green
}

# Create a KDP Metadata JSON configuration
$metadataPath = Join-Path $targetDir "Source\KDP_Metadata.json"
if (-not (Test-Path $metadataPath)) {
    $metadataContent = @{
        Title = "The Keystone Protocol: Metabolic Science & Recomposition Manual"
        Subtitle = "Advanced Biohacking, Peptide Architecture, and Deep Restoration for High-Stress Executives & Trades"
        Author = "Wayne Stevenson"
        Publisher = "Keystone Wellness Architecture"
        Language = "English"
        TrimSize = "6.0 in x 9.0 in"
        BleedSetting = "No Bleed"
        Categories = @("Health & Fitness / Alternative Therapies", "Medical / Endocrinology", "Business & Economics / General")
        Keywords = @("Peptides", "BPC-157", "GLP-1", "Biohacking", "Metabolic Health", "Wolverine Stack", "Keystone Protocol")
        PWA_DirectDownloadAccess = $true
    } | ConvertTo-Json -Depth 4

    Set-Content -Path $metadataPath -Value $metadataContent -Force
    Write-Host "Successfully initialized KDP metadata file: $metadataPath" -ForegroundColor Green
}

Write-Host ""
Write-Host "==============================================" -ForegroundColor Yellow
Write-Host "   WORKSPACE READY - PROCEED TO COMPILING     " -ForegroundColor Yellow
Write-Host "==============================================" -ForegroundColor Yellow
