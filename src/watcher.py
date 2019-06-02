
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
  DIRECTORY_TO_WATCH = "C:\watcher_directory"

  def __init__(self):
    print('Running watcher script')
    self.observer = Observer()

  def run(self):
    event_handler = Handler()
    self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
    self.observer.start()
    try:
      while True:
          time.sleep(5)
    except:
      self.observer.stop()
      print("Error")

    self.observer.join()


class Handler(FileSystemEventHandler):
  @staticmethod
  def on_any_event(event):
    if event.is_directory:
      return None

    elif event.event_type == 'created':
      # Take any action here when a file is first created.
      print("Received created event - %s." % event.src_path)
      filepath = event.src_path.split(os.sep)
      print(filepath[len(filepath) - 1])

      filename = filepath[len(filepath) - 1]

      filepath.pop(len(filepath) - 1)

      filepath = os.sep.join(filepath)
      print(filepath)

      os.system(f"..\detection_scripts\ShapeRecognition.exe {filepath} {filename}")

if __name__ == "__main__":
    w = Watcher()
    w.run()
    