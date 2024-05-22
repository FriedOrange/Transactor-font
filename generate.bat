@echo off

fontforge -script source\generate.py

rem Generate intermediate UFO sources
for %%f in (source\temp\Transactor*.sfd) do (
	sfd2ufo %%f source\%%~nf.ufo
)
