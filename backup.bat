@echo off

for /f "tokens=1-4 delims=/ " %%i in ("%date%") do (
	set day=%%i
	set month=%%j
	set year=%%k
	
	echo %day%
	echo %month%
	echo %year%
	)

set datestr=%year%_%month%_%day%

set BACKUP_FILE=d:\reportaton_%datestr%.backup
SET PGPASSWORD=<password>

echo on
"D:\Program Files\PostgreSQL\11\bin\pg_dump.exe" -U webapp -C -b -f %BACKUP_FILE% reportatron

COPY %BACKUP_FILE% "\\somedisk\somefolder\"