@echo off
setlocal

:: Check if an argument was provided
if "%~1"=="" (
    echo Usage: %~nx0 input_video.mp4
    exit /b 1
)

:: Get the input video file and base name
set "input_file=%~1"
for %%f in ("%input_file%") do set "base_name=%%~nf"

:: Create the folder named after the base name
if not exist "%base_name%" (
    mkdir "%base_name%"
)

:: Run FFmpeg command to extract frames and save them in the created folder
ffmpeg -i "%input_file%" -vf "fps=1,scale=640:480" "%base_name%\output_%%04d.png"

endlocal
