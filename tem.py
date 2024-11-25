import os
folder_path = "static/images/C_hilbYS436"

#Delete all files that are not jpg
for filename in os.listdir(folder_path):
    if not filename.endswith(".jpg"):
        os.remove(os.path.join(folder_path, filename))
        
for i, filename in enumerate(os.listdir(folder_path)):
    if filename.endswith(".jpg"):
        old_file_path = os.path.join(folder_path, filename)
        new_file_name = f"{i+1}.jpg"  # Change the extension if needed
        new_file_path = os.path.join(folder_path, new_file_name)
        os.rename(old_file_path, new_file_path)
