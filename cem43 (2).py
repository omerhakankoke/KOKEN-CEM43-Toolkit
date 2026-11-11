# KOKEN CEM43 TOOLKIT v1
# Hipertermi doz hesabi (Sapareto & Dewey, 1984)
# CEM43 = sum( dt * R^(43-T) ); T<43 icin R=0.5, T>=43 icin R=0.25
import sys, csv

def cem43_parcasi(sure_sn, sicaklik_c):
    R = 0.5 if sicaklik_c < 43.0 else 0.25
    dakika = sure_sn / 60.0
    return dakika * (R ** (43.0 - sicaklik_c))

def seri_hesapla(parcalar):
    return round(sum(cem43_parcasi(s, t) for s, t in parcalar), 2)

if __name__ == "__main__":
    nabiz = [(300, 42.0)] * 4
    print("DEMO: 4 nabiz x (42C, 300sn) =", seri_hesapla(nabiz), "dk CEM43")
    print("Tek nabiz (42C,300sn) =", cem43_parcasi(300, 42.0), "dk")