import random
from math import gcd as bltin_gcd
import sympy

class Blum_Blum_Shub:

    seed = 0
    p = 0 
    q = 0
    n = 0 
    generatedValues = []
    
    def __init__(self, p, q, seed = 0):
        print("initialized Blum_Blum_Shub")
        self.setP(p)
        self.setQ(q)
        if(self.p > 0 and self.q > 0):
            self.__setN()
            if seed <= 0:
                self.__setSeed()

    def setP(self, p):
        
        if (not sympy.isprime(p)):
            return False
        
        self.p = p
        return True

    def setQ(self, q):
        if (not sympy.isprime(q)):
            return False
        
        self.q = q        
        return True  

    def __setN(self):
        self.n = self.p * self.q

    def __setSeed(self):
        while(not self.__is_coprime(self.n, self.seed) and self.seed < 1):
            self.seed = random.randint(0, self.n - 1)

    def __is_coprime(self, p, q):
        return bltin_gcd(p, q) == 1

    def __next_usable_prime(x):
        p = sympy.nextprime(x)
        while (p % 4 != 3):
            p = sympy.nextprime(p)

    def rotateP(self):
        p = self.__next_usable_prime(p)
        return p

    def rotateQ(self):
        q = self.__next_usable_prime(q)
        return q


    def __generate_value(self):
        if len(self.generatedValues) == 0:
            return pow(self.seed, 2) % self.n
        
        return pow(self.generatedValues[-1], 2) % self.n 
               

    def generate_bits(self, amount):
        if(self.p == self.q):
            print('p should be different than q')
            return False

        if (self.n == 0):
            print('N is equal 0')
            return False

        else:
            result = []
            for i in range(amount):
                temp = 0
                for j in range(8):
                    
                    generatedValue = self.__generate_value()
                    self.generatedValues.append(generatedValue)
                
                    temp = temp << 1 | generatedValue % 2
                
                result.append(temp)
            return result