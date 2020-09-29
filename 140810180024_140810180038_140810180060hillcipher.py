#Muhammad Razzaaq Fadilah
#140810180024
#Hill Cipher
import numpy as np

def error_handling(teks):
    error_counter = False

    for karakter in teks:
        if (ord(karakter) >= 91 and ord(karakter) <= 96) or (ord(karakter) < 65 or ord(karakter) > 122):
            print("input teks salah!")
            error_counter = True
            break

    return error_counter

def teks_ke_matriks(teks, ordo):
    total_matriks_huruf = len(teks) // int(ordo)
    matriks_teks = np.zeros((int(ordo), total_matriks_huruf))
    k = 0

    for i in range(total_matriks_huruf):
        for j in range(int(ordo)):
            matriks_teks[j][i] = ord(teks[k]) - 65
            k += 1

    return matriks_teks

def matriks_mod_26(matriks_hasil, total_matriks_huruf, ordo):
    matriks_hasil_mod = np.zeros((int(ordo), int(total_matriks_huruf)))
    
    for i in range(total_matriks_huruf):
        for j in range(int(ordo)):
            matriks_hasil_mod[j][i] = matriks_hasil[j][i] % 26
    
    return matriks_hasil_mod

def matriks_invers_mod_26(matriks_kunci, ordo):
    matriks_invers = np.linalg.inv(matriks_kunci)
    determinan = np.linalg.det(matriks_kunci)
    invers_mod = mod_inverse(round(determinan), 26)
    matriks_adjoint = matriks_invers * determinan
    
    for i in range(int(ordo)):
        for j in range(int(ordo)):
            matriks_adjoint[i][j] = matriks_adjoint[i][j] % 26

    return matriks_adjoint * invers_mod

def mod_inverse(a, m) : 
    a = a % m 
    for x in range(1, m) : 
        if ((a * x) % m == 1) : 
            return x 
    return 1

def cari_kunci(plaintext, ciphertext):
    error_handling(plaintext)
    error_handling(ciphertext)

    if len(plaintext) == 0 or len(ciphertext) == 0:
        return "Teks tidak boleh kosong"

    if len(plaintext) != len(ciphertext):
        return "Panjang plaintext dan ciphertext harus sama!"

    if len(plaintext) % 2 != 0 or len(ciphertext) % 2 != 0:
        return "Panjang plaintext dan ciphertext harus genap!"

    plaintext_temp = ""
    ciphertext_temp = ""

    for karakter in plaintext:
        if ord(karakter) >= 97 and ord(karakter) <= 122:
            plaintext_temp = plaintext_temp + chr(ord(karakter) - 32)
        
        else:
            plaintext_temp = plaintext_temp + karakter
        

    for karakter in ciphertext:
        if ord(karakter) >= 97 and ord(karakter) <= 122:
            ciphertext_temp = ciphertext_temp + chr(ord(karakter) - 32)
        
        else:
            ciphertext_temp = ciphertext_temp + karakter

    m = np.floor(np.sqrt(len(plaintext_temp)))
    stopKey = False
        
    for i in range(2, int(m)+1):
        stopKey = False
        pt_full = teks_ke_matriks(plaintext_temp, i)
        ct_full = teks_ke_matriks(ciphertext_temp, i)
        pt = teks_ke_matriks(plaintext_temp[0:(i**2)], i)
        ct = teks_ke_matriks(ciphertext_temp[0:(i**2)], i)
        total_matriks_huruf = len(plaintext_temp) // i

        pt_invers = matriks_invers_mod_26(pt, i)
        matriks_kunci = ct.dot(pt_invers)

        for x in range(i):
            for y in range(i):
                matriks_kunci[x][y] = matriks_kunci[x][y] % 26
        
        matriks_hasil_pt = matriks_kunci.dot(pt_full)
        matriks_hasil_mod_pt = matriks_mod_26(matriks_hasil_pt, total_matriks_huruf, i)
        
        for j in range(total_matriks_huruf):
            for k in range(i):
                if round(matriks_hasil_mod_pt[k][j]) != round(ct_full[k][j]):
                    stopKey = True

        if stopKey == False:
            break

    if stopKey:
            return "Matriks kunci tidak tersedia"

    else:
        return matriks_kunci

def hill_cipher(teks, matriks_kunci, ordo, mode):
    if len(teks) == 0:
        print("Teks tidak boleh kosong")
    
    teks_temp = ""
    i = 0

    for karakter in teks:
        if ord(karakter) >= 97 and ord(karakter) <= 122:
            teks_temp = teks_temp + chr(ord(karakter) - 32)
        
        else:
            teks_temp = teks_temp + karakter

    #Kasus dimana teks yang akan dienkripsi tidak sesuai jumlah barisnya dengan matriks kunci
    #Menambahkan satu karakter 'Z' di belakang teks
    if len(teks) % int(ordo) != 0:
        for i in range(len(teks) % int(ordo)):
            teks_temp = teks_temp + "Z"
    
    matriks_teks = teks_ke_matriks(teks_temp, ordo)
    total_matriks_huruf = len(teks_temp) // int(ordo)

    if int(mode) == 1:
        matriks_hasil = matriks_kunci.dot(matriks_teks)
        matriks_hasil_mod = matriks_mod_26(matriks_hasil, total_matriks_huruf, ordo)

        for i in range(total_matriks_huruf):
            for j in range(int(ordo)):
                karakter = chr(int(matriks_hasil_mod[j][i]) + 65)
                print(karakter, end = "")

    elif int(mode) == 2:
        matriks_kunci_invers = matriks_invers_mod_26(matriks_kunci, ordo)
        matriks_hasil = matriks_kunci_invers.dot(matriks_teks)
        matriks_hasil_mod = matriks_mod_26(matriks_hasil, total_matriks_huruf, ordo)
        
        for i in range(total_matriks_huruf):
            for j in range(int(ordo)):
                karakter = chr(int(matriks_hasil_mod[j][i]) + 65)
                print(karakter, end = "")

    print("\n")

def main():
    mode = input("Input mode (angka 1 untuk enkripsi, angka 2 untuk dekripsi, angka 3 untuk cari kunci): ")
    error_status = False
    
    try:
        int(mode)

    except ValueError:
        print("input mode harus berupa integer!")
        return

    if int(mode) < 1 or int(mode) > 3:
            print("input mode tidak tersedia!")
            return

    if int(mode) == 3:
        plaintext = input("Masukkan plaintext: ")
        ciphertext = input("Masukkan ciphertext: ")
        print(cari_kunci(plaintext, ciphertext))
        return
    
    ordo = input("Masukkan ordo matriks: ")

    try:
        int(ordo)

    except ValueError:
        print("input ordo harus berupa integer!")
        return

    if int(ordo) < 0:
        print("nilai ordo tidak boleh negatif!")
        return

    print("Masukkan elemen matriks: \n")
    
    matriks_kunci = np.zeros((int(ordo), int(ordo)))
    for i in range(int(ordo)):
        for j in range(int(ordo)):
            temp = input()
            
            try:
                int(temp)

            except ValueError:
                print("input elemen harus berupa integer!")
                return

            matriks_kunci[i][j] = temp

    try:
        np.linalg.inv(matriks_kunci)

    except np.linalg.LinAlgError:
        print("matriks kunci tidak memiliki invers!")
        return

    print("\n")
    teks = input("Masukkan teks: ")
    
    error_status = error_handling(teks)
    
    if error_status:
        return
    
    hill_cipher(teks, matriks_kunci, ordo, mode)

if __name__ == "__main__":
    main()