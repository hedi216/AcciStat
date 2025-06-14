@echo off
REM Supprimer tous les fichiers et sous-dossiers du dossier "archive"

set "target=C:\Users\guessMeWho\Desktop\accient_analys\archive"

IF EXIST "%target%" (
    echo Suppression du contenu du dossier %target% ...
    rmdir /s /q "%target%"
    mkdir "%target%"
    echo Le contenu du dossier %target% a été supprimé.
) ELSE (
    echo Le dossier %target% n'existe pas.
)

pause

