@echo off
rem http://this.is.thoughtcrime.org.nz/elliptic-curve-ca-guide

set Days=730
set EC=prime256v1
set RSAKeySize=4096
set CADate=%date:~0,4%%date:~5,2%%date:~8,2%
set BatPath=%~dp0
echo Data: [%CADate%]

echo =================================================================

if [%1]==[] (
	echo.
	echo GenCertEC -all
	echo GenCertEC -regenca
	echo GenCertEC -regenssl
	goto end
)

if [%1]==[-all] (
	Set /a GenCA=1
	Set /a GenSSL=1
) else if [%1]==[-regenca] (
	Set /a GenCA=1
	Set /a GenSSL=0
) else if [%1]==[-regenssl] (
	Set /a GenCA=0
	Set /a GenSSL=1
) else (
	echo.
	echo GenCertEC -all
	echo GenCertEC -regenca
	echo GenCertEC -regenssl
	goto end
)

if %GenCA% EQU 1 (
	rem Genertate EC CA cert
	%BatPath%openssl ecparam -out uPttCA.key -name %EC% -genkey
	%BatPath%openssl req -x509 -new -sha256 -key uPttCA.key -out uPttCA.crt -subj "/C=TW/CN=uPtt CA %CADate%/O=uPtt/OU=uPtt" -outform PEM -days %Days% -extensions req_ext_ca -config %BatPath%\openssl.cnf
)

if %GenSSL% EQU 1 (
	rem Generate EC SSL cert
	%BatPath%openssl ecparam -out uPttSSL.key -name %EC% -genkey
	%BatPath%openssl req -new -sha256 -nodes -key uPttSSL.key -outform pem -out uPttSSL.csr -subj "/C=TW/CN=localhost/O=uPtt/OU=uPtt" -reqexts req_ext -config %BatPath%\openssl.cnf
)

rem Sign the EC SSL cert by CA cert
%BatPath%openssl x509 -req -sha256 -CA uPttCA.crt -CAkey uPttCA.key -days %Days% -in uPttSSL.csr -CAcreateserial -extensions req_ext -extfile %BatPath%\openssl.cnf -out uPttSSL.crt

del .\uPttSSL.pem

for /f "tokens=*" %%a in (.\uPttSSL.crt) do (
	echo %%a>> .\uPttSSL.pem
)

for /f "tokens=*" %%a in (.\uPttSSL.key) do (
	echo %%a>> .\uPttSSL.pem
)

:end

echo generate Cert finish