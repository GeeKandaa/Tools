if not exist ..\studio cd ..
"C:\git-repo\s2g\src\submodules\srt-tool\source\Builds - srt-tool\Windows\srt-tool\srt-tool.exe" --cmd=dechaff -w --project=studio.xojo_project
echo FIRST RUN COMPLETED
"C:\git-repo\s2g\src\submodules\srt-tool\source\Builds - srt-tool\Windows\srt-tool\srt-tool.exe" --cmd=dechaff -w --project=studio.xojo_project
echo SECOND RUN COMPLETED
echo CHAFF REMOVAL COMPLETED