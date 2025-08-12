import time, sys

print("Welcome to Procrastidoro! Press enter to check on time elapsed.")

class Timer:
    def __init__(self, thistimername):
        self.name = thistimername
        self.sumtime = 0
        self.running = False
        self.starttime = 0

    def start(self):
        # TODO: already running?
        self.running = True
        self.starttime = time.time()

    def stop(self):
        # TODO: already stopped?
        self.running = False
        self.sumtime = time.time() - self.starttime + self.sumtime

    def look(self):
        if self.running:
            return time.time() - self.starttime + self.sumtime
        else:
            return self.sumtime

    def look_pretty(self):
        if self.running:
            seconds = time.time() - self.starttime + self.sumtime
        else:
            seconds = self.sumtime
        hr_part = int(int(seconds / 60 ) /60)
        min_part = int(seconds / 60) - int(int(seconds / 60 ) /60) * 60
        sec_part = int(seconds - min_part*60)
        hr_str = str(hr_part) if hr_part > 9 else "0" + str(hr_part)
        min_str = str(min_part) if min_part > 9 else "0" + str(min_part)
        sec_str = str(sec_part) if sec_part > 9 else "0" + str(sec_part)
        return hr_str + ":" + min_str + ":" + sec_str
        

t1 = Timer("Productivity Time")
t2 = Timer("Leisure Time")

while True:
    print("Timer " + t1.name + ": " + t1.look_pretty())
    print("Timer " + t2.name + ": " + t2.look_pretty())
    command = input("What do you want to do next? ")
    #if command == "look timer 1" or command == "l1":
     #   print(t1.look())
    #TODO: despaghettify
    if command == "start timer 1" or command == "s1":
        t1.start()
        print(t1.name + " started")
    if command == "start timer 2" or command == "s2":
        t2.start()
        print(t2.name + " started")
    if command == "stop timer 1" or command == "x1":
        t1.stop()
        print(t1.name + " stopped")
    if command == "stop timer 2" or command == "x2":
        t2.stop()
        print(t2.name + " stopped")    
    if command == "exit" or command == "Exit":
        sys.exit()
