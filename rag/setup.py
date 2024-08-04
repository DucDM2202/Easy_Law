import os
import shutil
import subprocess


def copy_env():
    if not os.path.exists(".env"):
        shutil.copy("env.example", ".env")
        print("Copied env.example to .env")
    else:
        print("File .env exists")


def install_requirements():
    if os.path.exists("requirements.txt"):
        subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
        print("Installed requirements from requirements.txt")
    else:
        print("File requirements.txt does not exist")


def download_data():
    from dotenv import load_dotenv

    load_dotenv()
    import gdown

    DRIVE_LINK = os.environ["DRIVE_LINK"]
    if not os.path.exists("data"):
        os.makedirs("data")
    gdown.download_folder(DRIVE_LINK, output="data", quiet=False)


if __name__ == "__main__":
    copy_env()
    install_requirements()
    # download_data()
