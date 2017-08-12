from time import time

class StopWatch:
    
    def __init__(self, action):
        self.start_time = 0
        self.elapsed_time = 0
        self.action = action

    def start(self):
        self.start_time = time()
        print("Start stopwatch for '" + self.action + "' ...")

    def stop(self):
        self.elapsed_time = time() - self.start_time
        print("Stopping stopwatch for '" + self.action + "' ...")
        print(self.__convert_seconds(self.elapsed_time))

    def __convert_seconds(self, seconds):
        seconds = int(seconds)
        minutes = int(seconds / 60)
        seconds = seconds % 60
        hours = int(minutes / 60)
        minutes = minutes % 60

        if(hours == 0):
            if(minutes == 0):
                body = str(seconds) + " seconds"
            else:
                body = str(minutes) + " minutes " + str(seconds) + " seconds"
        else:
            body = str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds"

        return "Total elapsed time is " + body + "."