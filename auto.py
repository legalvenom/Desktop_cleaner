from os import scandir, rename, makedirs
from os.path import splitext, exists, join
from shutil import move
from time import sleep
import zipfile
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ! FILL IN BELOW
# ? folder to track e.g. Windows: "C:\\Users\\UserName\\Downloads"
source_dir = "C:/Users/roshi/Downloads"
dest_dir_zip = "C:/Users/roshi/Desktop/downloaded_zip"
dest_dir_video = "C:/Users/roshi/Desktop/downloaded_video"
dest_dir_image = "C:/Users/roshi/Desktop/downloaded_image"
dest_dir_documents = "C:/Users/roshi/Desktop/downloaded_document"
extracted_dir = "C:/Users/roshi/Desktop/extracted_files"

# ? supported image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
# ? supported Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
# ? supported Document types
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]
# ? supported ZIP types
zip_extensions = [".zip"]

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)

def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    logging.info(f"Extracted zip file: {zip_path} to {extract_to}")

class MoverHandler(FileSystemEventHandler):
    # ? THIS FUNCTION WILL RUN WHENEVER THERE IS A CHANGE IN "source_dir"
    # ? .upper is for not missing out on files with uppercase extensions
    def on_modified(self, event):
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_zip_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)

    def check_zip_files(self, entry, name):  # * Checks all ZIP Files
        for zip_extension in zip_extensions:
            if name.endswith(zip_extension) or name.endswith(zip_extension.upper()):
                move_file(dest_dir_zip, entry, name)
                logging.info(f"Moved zip file: {name}")
                extracted_path = join(extracted_dir, splitext(name)[0])
                makedirs(extracted_path, exist_ok=True)
                extract_zip(join(dest_dir_zip, name), extracted_path)

    def check_video_files(self, entry, name):  # * Checks all Video Files
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):  # * Checks all Image Files
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):  # * Checks all Document Files
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Moved document file: {name}")


# ! NO NEED TO CHANGE BELOW CODE
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
