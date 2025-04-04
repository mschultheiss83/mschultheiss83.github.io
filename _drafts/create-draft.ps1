<#
.SYNOPSIS
  Erstellt eine Entwurfsdatei (Markdown) basierend auf Benutzereingaben fùr ID, Kategorie, URLs und Inhalt.
  Der Inhalt kann direkt eingegeben oder aus einer Datei geladen werden.

.DESCRIPTION
  Dieses Skript fùhrt den Benutzer durch die Eingabe einer eindeutigen Draft-ID (nur Kleinbuchstaben und Bindestriche),
  einer Kategorie, einer Liste von URLs und einem mehrzeiligen Text fùr Thema/Beschreibung/Inhalt.
  Der Benutzer kann wùhlen, ob der Inhalt direkt im Skript eingegeben oder aus einer Textdatei geladen werden soll.
  Anschlieùend wird im aktuellen Verzeichnis eine Markdown-Datei im Format 'JJJJ-MM-TT_draft-id.md' erstellt,
  die die gesammelten Informationen strukturiert enthùlt.

.NOTES
  Version:      0.4
  Author:       Martin Schultheiss / Gemini 2.5 pro AI Assistant
  Erstellt am:  2025-04-04
  Angepasst am:  2025-04-04 (Verbesserte Benutzerfreundlichkeit bei der Inhaltsauswahl)

.EXAMPLE
  .\create-draft.ps1
  # Folgt den Anweisungen zur Eingabe der Daten und wùhlt die Inhaltsquelle.
#>

# --- Konfiguration ---
$script:endMarker = "###END###" # Schlùsselwort, um die mehrzeilige Eingabe zu beenden

# --- Hilfsfunktion fùr die Draft-ID Validierung ---
function Test-ValidDraftId {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Id
    )
    # Muss Kleinbuchstaben oder Bindestriche enthalten, nicht leer sein,
    # nicht mit Bindestrich anfangen/enden, keine doppelten Bindestriche haben.
    if ([string]::IsNullOrWhiteSpace($Id)) { return $false }
    if ($Id -match '^[a-z-]+$' -and $Id -notmatch '^-|-$|--') {
        return $true
    } else {
        return $false
    }
}

# --- Anfang der Benutzereingaben ---

Write-Host "Willkommen beim Draft Creator!"
Write-Host "------------------------------------"

# Draft-ID abfragen und validieren
do {
    $draftId = Read-Host "Bitte geben Sie eine eindeutige Draft-ID ein (nur Kleinbuchstaben und Bindestriche)"
    if (-not (Test-ValidDraftId $draftId)) {
        Write-Warning "Ungùltige Draft-ID. Bitte nur Kleinbuchstaben und Bindestriche verwenden (keine doppelten, Anfùnge oder Enden)."
    }
} until (Test-ValidDraftId $draftId)

# Kategorie abfragen
$category = Read-Host "Bitte geben Sie die Kategorie ein"

# URLs abfragen
Write-Host "Bitte geben Sie die URLs ein. Beenden Sie die Eingabe mit einer leeren Zeile."
$urls = @()
while ($true) {
    $url = Read-Host
    if ([string]::IsNullOrWhiteSpace($url)) {
        break
    }
    $urls += $url
}

# Auswahl der Inhaltsquelle mit Wiederholung bei Fehler
Write-Host "------------------------------------"
do {
    $contentSourceRaw = Read-Host "Wie mùchten Sie den Inhalt eingeben? (Direkt/Datei) [D/F]"
    $contentSource = $contentSourceRaw.Trim()
    $mainContent = ""
    $invalidInput = $false

    if ($contentSource -ceq "D" -or $contentSource -ceq "Direkt" -or $contentSource -ceq "d" -or $contentSource -ceq "direkt") {
        Write-Host "Bitte geben Sie den Inhalt ein. Beenden Sie die Eingabe mit '$script:endMarker' in einer neuen Zeile."
        $mainContentLines = @()
        while ($true) {
            $line = Read-Host
            if ($line -ceq $script:endMarker) {
                break
            }
            $mainContentLines += $line
        }
        $mainContent = $mainContentLines -join "`n"
    } elseif ($contentSource -ceq "F" -or $contentSource -ceq "Datei" -or $contentSource -ceq "f" -or $contentSource -ceq "datei") {
        $filePath = Read-Host "Bitte geben Sie den Pfad zur Textdatei ein"
        if (Test-Path -Path $filePath -PathType Leaf) {
            try {
                $mainContent = Get-Content -Path $filePath -Raw
            } catch {
                Write-Error "Fehler beim Lesen der Datei: $($_.Exception.Message)"
                exit 1
            }
        } else {
            Write-Error "Die angegebene Datei wurde nicht gefunden."
            exit 1
        }
    } else {
        Write-Warning "Ungùltige Auswahl. Bitte 'D' fùr Direkt oder 'F' fùr Datei eingeben."
        $invalidInput = $true
    }
} until (-not $invalidInput)

# --- Dateiinhalt generieren ---

# Dateiname: JJJJ-MM-TT_draft-id.md
$currentDate = Get-Date -Format 'yyyy-MM-dd'
$fileName = "$($currentDate)_$($draftId).md"
$filePath = Join-Path -Path $PWD -ChildPath $fileName # Im aktuellen Verzeichnis

# Dateiinhalt (Markdown Format)
$fileBody = @"
---
# Draft: $draftId
title: [generate an appropriate title based on the reference and subject]
date: $currentDate
categories: [$($category), determine two appropriate alternative categories]
tags: [determine appropriate tags, comma-separated]
ai: [instert your ai model, $currentDate]
---
## URLs
$($urls | ForEach-Object { "- $_" } | Out-String)

## Thema / Beschreibung / Inhalt

$($mainContent)

"@ # Das '@' muss am Anfang der Zeile stehen

# --- Dateierstellung ---

Write-Host "------------------------------------"
Write-Host "Erstelle Datei: $fileName"

try {
    # Erstellt die Datei (oder ùberschreibt sie) mit UTF8-Kodierung
    Set-Content -Path $filePath -Value $fileBody -Encoding UTF8 -ErrorAction Stop

    # Erfolgsmeldung
    Write-Host "Datei erfolgreich erstellt:" -ForegroundColor Green
    Write-Host $filePath

} catch {
    # Fehlermeldung, falls etwas schiefgeht
    Write-Host "Fehler beim Erstellen der Datei '$filePath'." -ForegroundColor Red
    Write-Host "Fehlermeldung: $($_.Exception.Message)" -ForegroundColor Red
}

# --- Ende der Dateierstellung ---

Write-Host "------------------------------------"
Write-Host "Skript beendet."