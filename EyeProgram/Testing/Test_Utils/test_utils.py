import shutil
import os
import filecmp


def remove_tree(input_dir):
    """
    Repeatedly tries to delete the directory until it is successful or 
    it has been attempted 1000 times. This isto get around Windows file
    locks.
    """

    deleted_successfully = False

    for i in range(0, 1000):
        if os.path.exists(input_dir) and os.path.isdir(input_dir):
            shutil.rmtree(input_dir, ignore_errors=True)
        else:
            deleted_successfully = True
            break

    if not deleted_successfully and os.path.exists(input_dir) and os.path.isdir(input_dir):
            shutil.rmtree(input_dir)


def overwrite_expected_results_dir(test_data_dir):
    """
    Utility function that baseline the result in the output
    file with the one in the temp folder. This changes the
    expected result of the test.
    """
    print('WARNING - BASELINING TOOL ON')
    output_path = os.path.join(test_data_dir, "Outputs")
    temp_path = os.path.join(test_data_dir, "Temp")
    if os.path.exists(output_path) and os.path.isdir(output_path):
        remove_tree(output_path)

    if os.path.exists(temp_path) and os.path.isdir(temp_path):
        shutil.copytree(temp_path, output_path)
    else:
        raise IOError("Error - Directory Not Found: " + temp_path)


def are_dir_trees_equal(dir1, dir2):
    """
    Compare two directories recursively. Files in each directory are
    assumed to be equal if their names and contents are equal.

    @param dir1: First directory path
    @param dir2: Second directory path

    @return: True if the directory trees are the same, 
        all files are binary identical and there were 
        no errors while accessing the directories or files. 
        False otherwise.
   """
    dir_exist = True
    error_message = ''

    if not os.path.isdir(dir1):
        error_message += 'First directory given does not exist. \n'
        dir_exist = False

    if not os.path.isdir(dir2):
        error_message += 'Second directory given does not exist. \n'
        dir_exist = False

    if not dir_exist:
        return False, error_message

    dirs_cmp = filecmp.dircmp(dir1, dir2)

    # Check if any files/ sub directories were found in one folder but
    # not the other.
    sub_folders_equal = True
    if len(dirs_cmp.left_only) > 0:
        error_message += 'Left directory uniquely contains: \n' + str(dirs_cmp.left_only) + '\n'
        sub_folders_equal = False

    if len(dirs_cmp.right_only) > 0:
        error_message += 'Right directory uniquely contains: \n' + str(dirs_cmp.left_only) + '\n'
        sub_folders_equal = False
       
    if len(dirs_cmp.funny_files) > 0:
        error_message += ' Files could not be compared: \n' + str(dirs_cmp.funny_files) + '\n'
        sub_folders_equal = False

    if not sub_folders_equal:
        return False, error_message

    (_, mismatch, errors) = filecmp.cmpfiles(
        dir1, dir2, dirs_cmp.common_files, shallow=False)

    # Check if files in this directory are binary identical.
    files_equal = True

    if len(mismatch) > 0:
        error_message += 'Files do not match: \n' + str(mismatch) + '\n'
        files_equal = False
   
    if len(errors) > 0:
        error_message += 'Files do not exist in both directories: \n' + str(errors) + '\n'
        files_equal = False
        
    if not files_equal:
        return False, error_message

    for common_dir in dirs_cmp.common_dirs:
        new_dir1 = os.path.join(dir1, common_dir)
        new_dir2 = os.path.join(dir2, common_dir)
        sub_tree_equal, error_message = are_dir_trees_equal(new_dir1, new_dir2)
        if not sub_tree_equal:
            return False, error_message

    # All checks passed return True.
    return True, 'True'


def clear_temp(test_data_dir):
    """
    This function clears the Temp sub directory in this directory.
    If this errors it tries again. Note that it doesn't care if the
    the temp directory is already deleted.
    """
    temp_path = os.path.join(test_data_dir, "Temp")
    remove_tree(temp_path)
