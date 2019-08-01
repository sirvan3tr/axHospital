'''
 Author: Sirvan Almasi @ Imperial College London
 August 2019
 Dissertation Project

 This code represents a trusted organisation with the knowledge
 of p and q, factors of n, thus enabling them to create secret 
 keys for everyone using the same n.
'''

from functions import *
import os
import hmac, hashlib, random, csv


class TrustedHub:

    def __init__(self, I, p, q, k):
        #16 bit primes, generated using openssl
        #not to be used for production
        self.p = p #56999 # Secret
        self.q = q #58403 # Secret
        self.n = self.p*self.q

        self.k = k # number of keys

        self.idRaw = I
        self.jIndices = [] # indices for our supposed pseudorandom functino
        self.publicKeys = [] # the final public keys
        self.secretKeys = [] # secret keys generated

    '''
    CREATE THE IDENTITY
    '''
    def createID(self):
        # Generate k keys
        kMax = 0
        while(kMax < self.k):
            j, v = self.genPubKey(self.idRaw)
            if (j):
                self.jIndices.append(j)
                self.publicKeys.append(v)
                kMax += 1

        for v in self.publicKeys:
            self.secretKeys.append(self.genSecretKey(v, self.p, self.q, self.n))

        os.system('color a')
        print ("##Printing public Keys:")
        print (self.publicKeys)

        print ("##Printing Secret Keys:")
        print (self.secretKeys)

        print ("##Printing j indices:")
        print (self.jIndices)

        print ("##Printing n:")
        print (self.n)

        print ("##Printing I:")
        print (self.idRaw)

        return self.publicKeys, self.secretKeys, self.jIndices, self.n, self.idRaw


    '''
    GENERATE PUB KEY
    '''
    def genPubKey(self, idRaw):
        # this bit of the code has to be reviewed
        randInt = random.randint(0, self.n)
        digest_maker = hmac.new(
            bytes(str(randInt), 'latin-1'),
            bytes(str(idRaw), 'latin-1'),
            hashlib.sha256).hexdigest()
        pubHatInt = int(digest_maker, 16) % self.n
        pubKey = egcd(pubHatInt, self.n)[1] % self.n
        try:
            # Check for sqrt modulus
            c1 = tonelli(pubHatInt,self.p)
            c2 = tonelli(pubHatInt,self.q)
            return randInt, pubKey
        except:
            return False, False

    '''
    GENERATE SECRET KEY
        v = public key
        p and q = secret factors of n
        n = modulus, product of p & q
    '''
    def genSecretKey(self, v, p, q, n):
        v = egcd(v, n)[1] % n
        b1 = tonelli(v % p, p)
        b2 = tonelli(v % q, q) 

        # Square root signs
        a = [b1, b2, b1, b2*-1, b1*-1, b2*-1, b1*-1, b2]
        j = 0
        smallest = -1
        for i in range(0,4):
            n = [p, q]
            c = [a[j], a[j+1]]
            cr = chinese_remainder(n, c)
            if (smallest<0):
                smallest = cr
            elif(cr < smallest):
                smallest = cr
            j +=2

        return smallest