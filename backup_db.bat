@echo off

set BACKUP_DIR=C:\Backups

if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%

set DATE=%date:~10,4%-%date:~4,2%-%date:~7,2%
set TIME=%time:~0,2%-%time:~3,2%

sqlcmd -S localhost -E -Q "BACKUP DATABASE AssetManagement TO DISK='%BACKUP_DIR%\backup_%DATE%_%TIME%.bak' WITH INIT, COMPRESSION"

echo Backup done