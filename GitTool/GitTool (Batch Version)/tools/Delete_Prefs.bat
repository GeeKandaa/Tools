echo:
echo In order for ALL preferences to be deleted please type in your user name as it appears on the appropriate folder in "C:\Users".
Set /P username="Username:"
rm -rf C:/Users/%username%/AppData/Roaming/com.aspexsoftware.Silhouette_Studio/
rm -rf C:/ProgramData/com.aspexsoftware.Silhouette_Studio.8/
echo USER PREFERENCES DELETED