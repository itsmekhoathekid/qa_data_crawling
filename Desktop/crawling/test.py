import os

def create_chapter_folders(folder_path, n1,n2):
    # Ensure the folder exists, create if it doesn't
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Directory created at: {folder_path}")
    
    # Create chap_n empty folders in the specified folder
    for i in range(n1, n2):
        folder_name = f"chap_{i}"
        folder_full_path = os.path.join(folder_path, folder_name)
        
        # Create the empty folder
        if not os.path.exists(folder_full_path):
            os.makedirs(folder_full_path)
            print(f"Folder created: {folder_full_path}")
        else:
            print(f"Folder already exists: {folder_full_path}")

# Example usage:
folder_path = r"C:\Users\VIET HOANG - VTS\Desktop\crawling\pictures\Physics"
create_chapter_folders(folder_path, 1, 8)
