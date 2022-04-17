@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=source
set BUILDDIR=build

%SPHINXBUILD% -b rinoh %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:end
popd
