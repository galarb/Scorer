import serial
import threading
import queue

class RpiUart:
    def __init__(self, port='/dev/ttyAMA0', baudrate=115200, timeout=1):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        self.queue = queue.Queue()
        self.running = False
        self.thread = None

    def _listen(self):
        while self.running:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                if line:
                    self.queue.put(line)
            except Exception as e:
                print(f"[UART Error] {e}")

    def start(self):
        """Start listening in a background thread"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._listen, daemon=True)
            self.thread.start()

    def stop(self):
        """Stop listening and close serial"""
        self.running = False
        if self.thread:
            self.thread.join()
        self.ser.close()

    def get_message(self):
        """Retrieve the next message if available, else None"""
        try:
            return self.queue.get_nowait()
        except queue.Empty:
            return None

    def send(self, message):
        """Send a string to UART"""
        if not message.endswith("\n"):
            message += "\n"
        self.ser.write(message.encode('utf-8'))

