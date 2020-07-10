if exist ..\studio cd shared_code
Echo:
Echo MAKE SURE YOU ARE NOT CURRENTLY ON THE BRANCH YOU ARE TRYING TO DELETE!
Echo:
Set /P branch= "Name of branch to be deleted: "
git branch -d %branch%
git push origin --delete %branch%

if not exist ..\studio cd ..
git branch -d %branch%
git push origin --delete %branch%

echo BRANCH DELETED
echo ___________________________________________________________________
echo:
echo -~-~-Removed %branch%-~-~-
set /p end = "~   ENTER TO CONTINUE   ~"