'''class MinecraftDog():
    def __init__(self, name):
        self.name = name
        self.color = "brown"
        self.food = "steak"
        self.health = 20

    def getHurt(self):
        self.health -= 1
        print(self.health)
    def die(self):
        self.health = 0
        print(self.health)
        print(self.name + " has died")

Robby = MinecraftDog("Robby")
print(Robby.health)
Robby.getHurt()
Robby.die()'''




import math
import time

num = int(input("pick a number nurd: "))
startTime = time.time()
factors = []

def faster():
    i=1
    while i <= math.sqrt(num):
        if num%i == 0:
            factors.append(i)
            i+=1
        for n in range(0,len(factors)):
            factors.append(int(num/factors[n]))
def slower():
    i = 1
    while i <= num:
        if num%i == 0:
            factors.append(i)
        i+=1


faster()
print(time.time() - startTime)
print(factors)
