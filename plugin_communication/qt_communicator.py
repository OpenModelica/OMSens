import sys


class QTCommunicator:

    def __init__(self, total_progress_messages):
        self.messages_completed = 1
        self.total_progress_messages = total_progress_messages

        # Message of initialization
        self._send_first_message(self.messages_completed)

    def set_total_progress_messages(self, cant):
        self.total_progress_messages = cant
        self.messages_completed = 1

        self._send_update(1)

    def update_completed(self, new_messages=1):

        self.messages_completed += new_messages
        if self.total_progress_messages > 0:
            percentage_completed = int(self.messages_completed / self.total_progress_messages * 100)
            if percentage_completed > 100:
                percentage_completed = 100
            # Send update
            self._send_update(percentage_completed)

    def _send_first_message(self, percentage_completed):
        print(str(percentage_completed), end="")
        sys.stdout.flush()

    def _send_update(self, percentage_completed):
        # Communication through stdout
        print("," + str(percentage_completed), end="")
        sys.stdout.flush()
