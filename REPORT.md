## import.py
In import.py, I have made it so that all loaded pieces of information are stored temporarily, and
then only committed to the database after all of them have been loaded correctly.
This makes sure that there are no errors in the CSV files, and if there are, these can be fixed
before running the import as a whole again.

This should help avoid problems if there are faulty CSV files used, but it does most likely cost
some speed. However, since this tool is not really meant to be run constantly, I think that this is
the better side of the trade off.

This function is extremely slow on the hardware I am using, but I have found the source of the
slowness to just be the `consumption.save()` function so I think I have no choice but to leave it
as it is. I have also added an optional commandline argument which allows one to only load a
fraction of all data for the purposes of being able to run the web application without waiting an
extremely long time.
