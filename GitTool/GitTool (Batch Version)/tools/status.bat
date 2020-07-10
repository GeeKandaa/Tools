echo:
echo STUDIO STATUS
if not exist ..\studio cd ..
git status
if exist ..\studio cd shared_code
echo ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~
echo:
echo SHARED_CODE STATUS
git status
echo ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~