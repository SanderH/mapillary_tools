__author__ = 'Sander H'

import sys
import os
import time
import shutil

reload(sys)
sys.setdefaultencoding("utf-8")

if __name__ == '__main__':
    '''
    Use from command line as: python import_VIRB_folders.py sourcepath
	You need to set the environment variable MAPILLARY_IMPORT_PATH to 
	contain the import path.
	
	This script will move the photo's on your VIRB to the the import path 
	and rename the files uniquely by the following naming convention:
	<yyyy-MM-dd>_<VIRB folder number>_<original filename>
	
	After this, you can split up the photo's in sequences with time_split.py
    '''

    if len(sys.argv) <> 2:
        print("Usage: python import_VIRB_folders.py sourcepath")
        raise IOError("Bad input parameters.")
    sourcepath = sys.argv[1]

    try:
        MAPILLARY_IMPORT_PATH = os.environ['MAPILLARY_IMPORT_PATH']
    except KeyError:
        print("You are missing one of the environment variables MAPILLARY_IMPORT_PATH. This is required.")
        sys.exit()

    if sourcepath.lower().endswith(".jpg"):
        # single file
        print("sourcepath must be the folder containing your photo's. The DCIM folder on your VIRB should be OK.")

    else:
        # folder(s)
        recursive = False
        for root, sub_folders, files in os.walk(sourcepath):
            print root
            for file in files:
                # only take the photo's, leaving the video's on the device
                if not file.lower().endswith('.jpg'):
                    print 'Skipping: ' + os.path.join(root, file)
                    continue
                print 'Moving: ' + os.path.join(root, file)
                if root.endswith('_VIRB'):
                    #          <yyyy-MM-dd>_<VIRB folder number>_<original filename>
                    destfile = time.strftime('%Y-%m-%d', time.gmtime(os.path.getmtime(os.path.join(root, file)))) + '_' + root[:-5][-3:] + '_' + file
                    print 'To: ' + os.path.join(MAPILLARY_IMPORT_PATH, destfile)
                    shutil.move(os.path.join(root, file), os.path.join(MAPILLARY_IMPORT_PATH, destfile))

    raw_input("Press Enter to continue...")