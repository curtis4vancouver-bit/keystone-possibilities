import os
import glob

def main():
    user_data_dir = r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data"
    
    # Files to look for and delete
    lock_files = [
        os.path.join(user_data_dir, "lock"),
        os.path.join(user_data_dir, "SingletonLock"),
        os.path.join(user_data_dir, "Default", "SingletonLock"),
        os.path.join(user_data_dir, "Default", "lock"),
    ]
    
    deleted_any = False
    for filepath in lock_files:
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"Deleted lock file: {filepath}")
                deleted_any = True
            except Exception as e:
                print(f"Failed to delete lock file {filepath}: {e}")
                
    if not deleted_any:
        print("No lock files found or deleted.")

if __name__ == "__main__":
    main()
