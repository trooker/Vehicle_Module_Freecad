import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"File modified: {event.src_path}")
        # Add your custom logic here
        
if __name__ == "__main__":
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    