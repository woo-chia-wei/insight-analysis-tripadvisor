from time import time

def stop_watch(f):
    def convert_seconds(seconds):
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

    def stop_watch_decoractor(self):
        print("Start stopwatch for '" + f.__name__ + "' ...")
        start_time = time()
        f(self)
        print("Stopping stopwatch for '" + f.__name__+ "' ...")
        print(convert_seconds(time() - start_time))

    return stop_watch_decoractor
