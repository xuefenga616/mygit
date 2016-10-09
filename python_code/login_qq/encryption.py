#coding:utf-8
from hashlib import md5 as md5_
from ctypes import c_int32 as c32
import random
import rsa

def getEncryption(password, salt, vcode):
    vcode = vcode or ''
    salt = uin2hex(salt)
    password = password or ''
    h1 = md5(password.encode())
    s2 = md5(bytes.fromhex(h1 + salt))
    rsaH1 = rsa_(h1)
    rsaH1Len = format(len(rsaH1) // 2, '0>4x')
    hexVcode = s2b(vcode)
    vcodeLen = '000{}'.format(len(vcode), 'x')
    saltPwd = rsaH1Len+rsaH1+salt+vcodeLen+hexVcode
    initkey(s2)
    saltPwd = b64(saltPwd)
    initkey('')
    return saltPwd.translate(str.maketrans('/+=','-*_'))


def md5(byte):
    return md5_(byte).hexdigest().upper()

def uin2hex(s):
    maxlength = 16;
    salt = format(int(s), '0>%dx' % maxlength)
    return salt

def s2b(s):
    result = ''
    temp = map(ord, s)
    for e in temp:
        result += format(e,'0>2x')
    return result

def rsa_(s):
    n = 'F20CE00BAE5361F8FA3AE9CEFA495362FF7DA1BA628F64A347F0A8C012BF0B254A30CD92ABFFE7A6EE0DC424CB6166F8819EFA5BCCB20EDFB4AD02E412CCF579B1CA711D55B8B0B3AEB60153D5E0693A2A86F3167D7847A0CB8B00004716A9095D9BADC977CBB804DBDCBA6029A9710869A453F27DFDDF83C016D928B3CBF4C7'
    e = 3
    pui_key = rsa.PublicKey(int(n, 16), e)
    result = rsa.encrypt(bytes.fromhex(s), pui_key)
    return bytes.hex(result)

def b64(D, C=None):
    
    B = n(D, C) 
    A = h(B) 
    y = ''
    for z in A:
        y += chr(z)
    return d.encode(y)

def h(A): 

    global g, w, x, t, m, a, l
    g = bytearray(8)
    w = bytearray(8)    
    x = t = 0
    m = True
    a = 0

    y = len(A)
    B = 0
    a = (y + 10) % 8 
    if a != 0:
        a = 8 - a
    l = bytearray(y + a + 10)
    g[0] = ((e() & 248) | a) & 255
    for z in range(1,a+1):
        g[z] = e() & 255
    a += 1
    for z in range(8):
        w[z] = 0
    B = 1
    while B <= 2:
        if a < 8:
            g[a] = e() & 255
            a += 1
            B += 1
        if a == 8:
            o()
    z = 0
    while y > 0:
        if a < 8:
            g[a] = A[z]
            a += 1
            z += 1
            y -= 1
        if a == 8:
            o()
    B = 1
    while B <= 7:
        if a < 8:
            g[a] = 0
            a += 1
            B += 1
        if a == 8:
            o()
    return l


def n(C, B=None): 
    A = bytearray()
    if B:
        for z in range(len(C)):
            A.append(C[z] & 255)
    else:
        for z in range(0, len(C), 2):
            A.append(int(C[z:z+2], 16))
    return A

def o(): 
    global t, x, a, m, g, l, w 
    for y in range(8):
        if m:
            g[y] = c32(g[y] ^ w[y]).value
        else:
            g[y] = c32(g[y] ^ l[t + y]).value
    z = j(g)
    for y in range(8):
        l[x + y] = c32(z[y] ^ w[y]).value
        w[y] = g[y]    

    t = x
    x += 8
    a = 0
    m = False

def j(A): 
    B = 16
    G = i(A, 0, 4)
    F = i(A, 4, 4)
    I = i(r, 0, 4)
    H = i(r, 4, 4)
    E = i(r, 8, 4)
    D = i(r, 12, 4)
    C = 0
    J = 2654435769 >> 0
    while B > 0:
        C += J
        C = (C & 4294967295) >> 0
        G += c32((c32(F << 4).value + I) ^ (F + C) ^ ((F >> 5) + H)).value
        G = (G & 4294967295) >> 0
        F += c32((c32(G << 4).value + E) ^ (G + C) ^ ((G >> 5) + D)).value
        F = (F & 4294967295) >> 0
        B -= 1
    K = bytearray(8)
    b(K, 0, G)
    b(K, 4, F)
    return K

def b(z, A, y):
    z[A + 3] = (y >> 0) & 255
    z[A + 2] = (y >> 8) & 255
    z[A + 1] = (y >> 16) & 255
    z[A + 0] = (y >> 24) & 255


def i(B, C, y):
    if not y or y > 4: 
        y = 4
    z = 0
    for A in range(C, C + y):
        z = c32(z << 8).value
        z = z | B[A]

    return (z & 4294967295) >> 0




def e(): 
    return round(random.random() * 4294967295)
class d:
    PADCHAR = '='
    ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    def getbyte(A, z):
        y = ord(A[z])
        if y > 255:
            print('INVALID_CHARACTER_ERR: in d.getbyte')
        return y
    
    def encode(C):
        z = d.PADCHAR
        E = d.ALPHA
        D = d.getbyte
        y = []
        C = '' + C
        A = len(C) - len(C) % 3
        if len(C) == 0:
            return C

        for B in range(0, A, 3):
            F =c32((c32(D(C, B) << 16).value) | (c32(D(C, B+1) << 8).value) | D(C, B+2)).value
            y.append(E[F >> 18])
            y.append(E[(F >> 12) & 63])
            y.append(E[(F >> 6) & 63])
            y.append(E[F & 63])
        B += 3
        if len(C) - A == 1:
            F = c32(D(C, B) << 16).value
            y.append(E[F >> 18] + E[(F >> 12) & 63] + z + z)
        elif len(C) - A == 2:
            F = c32((c32(D(C, B) << 16).value) | (c32(D(C, B + 1) << 8).value)).value
            y.append(E[F >> 18] + E[(F >> 12) & 63] + E[(F >> 6) & 63] + z)

        return ''.join(y)

def initkey(y, z=None):
    global r
    r = n(y, z)
    
if __name__ == '__main__':
    password = 'zhangjie'
    r = getEncryption('qq密码', 'qq账号', '验证码')
    print(r)
