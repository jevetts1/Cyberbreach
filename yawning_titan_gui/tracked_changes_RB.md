# networks.html
* Added new `upload` button

# item_manager.js
* Added functionality to the `upload` button
* Created `upload-dialogue .submit` functionality to allow file upload 
* Added `send_files` for file upload
    * Added `contentType: false` to allow files to be sent
    * Added `processData: false` to ensure files and processed into strings

# el_dialogue_center.html
* Added in a row to allow an upload file field 

# views.py 
* Added in new `upload-dialogue` entry in `NetworksView`
* Added the field `show_file_input`
* In the class `GameModeConfigView`, in `db_manager`, added `upload_network` function to be able to process files

# Troubleshooting
* I found that if something was not working as expected during testing, clearing the browser's cache helped
