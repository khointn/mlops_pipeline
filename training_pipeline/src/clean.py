import os
import shutil
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def clean(remove_tmp = True):
    rm_folders = ['./tmp', './src/__pycache__', './__pycache__', 'catboost_info']
    rm_files = ['logs.log']

    if not remove_tmp:
        rm_folders = rm_folders[1:].copy()
    else:
        pass

    # Remove folders
    for folder in rm_folders:
        if os.path.isdir(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
            
            if folder != './tmp': # Delete cache folders
                os.rmdir(folder)
    
    # Remove files
    for file_path in rm_files:
        if os.path.isfile(file_path):
            os.remove(file_path)

    print('Delete temporary files successfully')
    
if __name__ == '__main__':
    clean(remove_tmp=False)