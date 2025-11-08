@echo off
REM === Script pour fusionner le commit courant (HEAD détaché ou autre) dans master ===

echo.
echo === Début de la fusion dans master ===
echo.

REM Vérifie que tu es dans un dépôt Git
git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
    echo ❌ Ce dossier n'est pas un dépôt Git !
    pause
    exit /b
)

REM Récupère le commit actuel (HEAD)
for /f %%i in ('git rev-parse --short HEAD') do set COMMIT=%%i
echo Commit courant : %COMMIT%

REM Crée une branche temporaire à partir du commit actuel
git switch -c temp_merge_%COMMIT%

REM Sauvegarde de l'ancien master au cas où
git branch backup_master

REM Bascule sur master
git checkout master

REM Fusionne la branche temporaire
echo.
echo === Fusion en cours... ===
git merge temp_merge_%COMMIT%

if errorlevel 1 (
    echo ⚠️ Il y a des conflits de fusion. Résous-les manuellement.
    echo Branche temporaire : temp_merge_%COMMIT%
    echo Sauvegarde du master : backup_master
    pause
    exit /b
)

REM Si la fusion réussit, supprime la branche temporaire
git branch -d temp_merge_%COMMIT%

echo.
echo ✅ Fusion réussie !
echo 🔹 Le master contient maintenant le commit %COMMIT%.
echo 🔹 Une sauvegarde de l'ancien master est disponible sous le nom : backup_master
echo.

pause
