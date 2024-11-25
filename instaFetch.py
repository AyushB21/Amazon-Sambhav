import instaloader
import os
import shutil

def fetch_post(post_url):
    # Initialize Instaloader
    loader = instaloader.Instaloader()

    # Extract the post using the shortcode (POST_ID from URL)
    shortcode = post_url.split("/")[-2]
    post = instaloader.Post.from_shortcode(loader.context, shortcode)

    current_directory = os.getcwd()
    folder_path = f"static/images/{shortcode}"

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        #Delete the folder and its contents
        shutil.rmtree(folder_path)

    #Temporarily change directory to download the image
    os.chdir("static/images")
    # Download the image
    loader.download_post(post, target=shortcode)

    # Change back to the original directory
    os.chdir(current_directory)

    
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


    return shortcode, post.caption, len(os.listdir(folder_path))
