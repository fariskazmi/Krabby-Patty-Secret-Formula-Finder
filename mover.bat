@echo off
setlocal enabledelayedexpansion
set max=0
set past_max=0
:loop
echo im working...
timeout /t 2 /nobreak
for %%x in (*.bmp) do (
  set "FN=%%~nx"
  if !FN! GTR !max! (
    set max=!FN!
  )
)
if !max! GTR !past_max! (
    set past_max=!max!
    echo highest version: %max%.bmp
    ren C:\out\%max%.bmp food.bmp 
    echo renamed to food
    move C:\out\food.bmp C:\actualpic  
    echo food moved successfully
    echo.
  ) else (
         echo no new pic found 
         echo.)
goto loop

