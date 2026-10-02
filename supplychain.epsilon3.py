import gurobipy as gp
from gurobipy import GRB

model = gp.Model("supply_chain_optimization")

#Sets Tanımlanması

S = ['S1', 'S2']                # Tedarikçiler
T = [1, 2]                      # Zaman Periyotları
R = ['R1', 'R2', 'R3']          # Hammaddeler
P = ['P1', 'P2', 'P3']          # Ürünler
M = ['M1', 'M2']                # Üretim yöntemleri
J = ['DC1']                     # Dağıtım merkezi
K = ['K1', 'K2', 'K3']          # Perakendeciler

#Binary Değişkenler

Nst = model.addVars(S, T, vtype=GRB.BINARY, name="Nst")
Vpkt = model.addVars(P, K, T, vtype=GRB.BINARY, name="Vpkt")
Usm = model.addVars(M, vtype=GRB.BINARY, name="Usm")

#Sürekli Değişkenler

MPmpt = model.addVars(M, P, T, lb=0, vtype=GRB.CONTINUOUS, name="MPmpt")
QXrst = model.addVars(R, S, T, lb=0, vtype=GRB.CONTINUOUS, name="QXrst")
Xpjt = model.addVars(P, J, T, lb=0, vtype=GRB.CONTINUOUS, name="Xpjt")
Ypkt = model.addVars(P, K, T, lb=0, vtype=GRB.CONTINUOUS, name="Ypkt")
Zpjkt = model.addVars(P, J, K, T, lb=0, vtype=GRB.CONTINUOUS, name="Zpjkt")
ipt = model.addVars(P, T, lb=0, vtype=GRB.CONTINUOUS, name="ipt")
irrt = model.addVars(R, T, lb=0, vtype=GRB.CONTINUOUS, name="irrt")
SURpkt = model.addVars(P, K, T, lb=0, vtype=GRB.CONTINUOUS, name="SURpkt")
Bpkt = model.addVars(P, K, T, lb=0, vtype=GRB.CONTINUOUS, name="Bpkt")

#modeli lineer yapmak için gerekli tanımlamalar

BigM = 20000
Xmpt = model.addVars(M, P, T, lb=0, vtype=GRB.CONTINUOUS, name="Xmpt")

#Model güncellenir -değişkenlerin sisteme işlenmesi için-
model.update()

#Maliyet Parametreleri
slcs = {(s,t): 5 for s in S for t in T}
Pcpt = {(p, t): 7 for p in P for t in T}
Cpjt = {(p, j, t): 5 for p in P for j in J for t in T}
Cpkt = {(p, k, t): 5 for p in P for k in K for t in T}
Cpjkt = {(p, j, k, t): 15 for p in P for j in J for k in K for t in T}
Hpjt = {(p, j, t): 5 for p in P for j in J for t in T}
Hpkt = {(p, k, t): 5 for p in P for k in K for t in T}
Hpt = {(p, t): 5 for p in P for t in T}
Hrt = {(r, t): 5 for r in R for t in T}
CBpkt = {(p, k, t): 500 for p in P for k in K for t in T}
Cmpt = {(m, p, t): (20 if m == "M1" else 5) for m in M for p in P for t in T}
cost_changm = {"M1": 100, "M2": 50}

#talep parametreleri
Dpkt = {(p, k, t): 50 for p in P for k in K for t in T}

#kapasite parametreleri
UBQXrst = {(r, s, t): 200 for r in R for s in S for t in T}
Capt = {t: 600 for t in T}
Capjt = {(j, t): 300 for j in J for t in T}
Capkt = {(k, t): 300 for k in K for t in T}
Qrt = {(r, t): 1 for r in R for t in T}
Qpjt = {(p, j, t): 150 for p in P for j in J for t in T}
Qpt = {(p, t): 150 for p in P for t in T}

#diğer parametreler

# Brrp[r, p] sözlüğünü manuel doldurma
Brrp = {
    # Ürün P1 için hammadde ihtiyaçları
    ('R1', 'P1'): 0.5,  # R1 hammaddesinden 0.5 birim
    ('R2', 'P1'): 0.3,
    ('R3', 'P1'): 0.2,

    # Ürün P2 için hammadde ihtiyaçları
    ('R1', 'P2'): 0.4,
    ('R2', 'P2'): 0.4,
    ('R3', 'P2'): 0.2,

    # Ürün P3 için hammadde ihtiyaçları
    ('R1', 'P3'): 0.3,
    ('R2', 'P3'): 0.3,
    ('R3', 'P3'): 0.4,
}
AmPt = {(m, p, t): 0.90 for m in M for p in P for t in T}          # %90 başarıyla teslimat
SURmax_pkt = {(p, k, t): 50 for p in P for k in K for t in T}      # Stok sınırı
Bmax_pkt = {(p, k, t): 30 for p in P for k in K for t in T}        # Eksik stok sınırı

#enerji, atık ve çevresel üst sınır
Empt = {(m, p, t): (100 if m == "M1" else 30) for m in M for p in P for t in T}
Rmpt = {(m, p, t): (50 if m == "M1" else 10) for m in M for p in P for t in T}
Emax = 25000
Rmax = 10000
Cmax = 5000

#kapasite düşüşü parametresi
deltam = {"M1": 0.0, "M2": 0.20}

#sonradan eklenen parametre listesinde olmayan parametre
Cxrst = {(r, s, t): 5 for r in R for s in S for t in T}

#Kısıt 23: Eğer yöntem m seçilmediyse (Usm=0), Xmpt'nin 0 olmak zorunda olduğunu gösteriyor.
for m in M:
    for p in P:
        for t in T:
            model.addConstr(Xmpt[m, p, t] <= Usm[m] * BigM, name=f"C23_{m}_{p}_{t}")

#Kısıt 24: Xmpt değeri gerçek üretim miktarını aşamaz.
for m in M:
    for p in P:
        for t in T:
            model.addConstr(Xmpt[m, p, t] <= MPmpt[m, p, t], name=f"C24_{m}_{p}_{t}")

# Kısıt 25: Eğer yöntem m seçildiyse (Usm=1), Xmpt en az MPmpt kadar olmalı.
for m in M:
    for p in P:
        for t in T:
            model.addConstr(Xmpt[m, p, t] >= MPmpt[m, p, t] - (1 - Usm[m]) * BigM, name=f"C25_{m}_{p}_{t}")

# Kısıt 4: Hammadde Dönüşüm Kısıtı
# (4) Hammadde Tedarik ve Üretim Dengesi
for r in R:
    for t in T:
        model.addConstr(
            gp.quicksum(QXrst[r, s, t] for s in S) >=
            gp.quicksum(Brrp[r, p] * MPmpt[m, p, t] for p in P for m in M),
            name=f"Material_Balance_r{r}_t{t}"
        )
#KISIT 5: Toplam üretim toplam kapasiteyi aşmamalı.
for t in T:
    for m in M:
        model.addConstr(
            gp.quicksum(MPmpt[m, p, t] for p in P) <= Capt[t] * (1 - deltam[m] * Usm[m]),
            name=f"Cap_t{t}_m{m}"
        )
# (6) Üretilen miktar sevkiyat toplamından büyük/eşit olmalı
for t in T:
    for p in P:
        for m in M:
            model.addConstr(
                gp.quicksum(Xpjt[p, j, t] for j in J) +
                gp.quicksum(Ypkt[p, k, t] for k in K) <= MPmpt[m, p, t],
                name=f"Flow_t{t}_p{p}_m{m}"
            )

# Kısıt 7: Üreticiden DC'ye giden ile Perakendeciye giden dengesinin kurulması.
for p in P:
    for t in T:
        model.addConstr(
            gp.quicksum(Xpjt[p, j, t] for j in J) -
            gp.quicksum(Ypkt[p, k, t] for k in K) == 0,
            name=f"Producer_Exit_Balance_p{p}_t{t}"
        )

# Kısıt 8: DC Depolama Kapasitesi: DC'de kalan miktar kapasiteyi aşmasın.
for t in T:
    for p in P:
        for j in J:
            model.addConstr(
                Xpjt[p, j, t] - gp.quicksum(Zpjkt[p, j, k, t] for k in K) <= Qpjt[p, j, t],
                name=f"DC_Storage_Capacity_t{t}_p{p}_j{j}"
            )

#Kısıt 9: DC Çıkış Kısıtı: DC'den çıkan miktar, gelen miktardan fazla olamaz
for t in T:
    for p in P:
        for j in J:
            model.addConstr(
                Xpjt[p, j, t] >= gp.quicksum(Zpjkt[p, j, k, t] for k in K),
                name=f"DC_Exit_Flow_t{t}_p{p}_j{j}"
            )

# Kısıt 10: DC Alım Kapasitesi
for t in T:
    for j in J:
        model.addConstr(
            gp.quicksum(Xpjt[p, j, t] for p in P) <= Capjt[j, t],
            name=f"DC_Cap_t{t}_j{j}"
        )

# Kısıt 11: Perakendeci Alım Kapasitesi
for t in T:
    for k in K:
        model.addConstr(
            gp.quicksum(Ypkt[p, k, t] for p in P) +
            gp.quicksum(Zpjkt[p, j, k, t] for j in J for p in P) <= Capkt[k, t],
            name=f"Retailer_Cap_t{t}_k{k}"
        )

# Kısıt 12: Envanter Denge Kısıtı (Stok, Talep, Eksiklik ve Fazlalık)
for t in T:
    for p in P:
        for k in K:
            # t=1 durumu için (t-1) değerleri 0 kabul edildi
            prev_B = Bpkt[p, k, t - 1] if t > T[0] else 0
            prev_SUR = SURpkt[p, k, t - 1] if t > T[0] else 0

            model.addConstr(
                Ypkt[p, k, t] + gp.quicksum(Zpjkt[p, j, k, t] for j in J) + Bpkt[p, k, t] - prev_B ==
                SURpkt[p, k, t] - prev_SUR + Dpkt[p, k, t],
                name=f"Inventory_Balance_t{t}_p{p}_k{k}"
            )

# Kısıt 13: Maksimum Fazla Stok Sınırı
for t in T:
    for p in P:
        for k in K:
            model.addConstr(
                SURpkt[p, k, t] <= SURmax_pkt[p, k, t] * Vpkt[p, k, t],
                name=f"Max_Surplus_t{t}_p{p}_k{k}"
            )

# Kısıt 14: Maksimum Stoksuzluk Sınırı (Binary Vpkt'nin tersiyle bağlı)
for t in T:
    for p in P:
        for k in K:
            model.addConstr(
                Bpkt[p, k, t] <= Bmax_pkt[p, k, t] * (1 - Vpkt[p, k, t]),
                name=f"Max_Shortage_t{t}_p{p}_k{k}"
            )

# Kısıt 15: Tedarikçi Ham Madde Alım Sınırı
for r in R:
    for s in S:
        for t in T:
            model.addConstr(
                QXrst[r, s, t] <= UBQXrst[r, s, t],
                name=f"Supplier_Limit_r{r}_s{s}_t{t}"
            )

# Kısıt 16 ve 17: Depolama Kapasitesi Eşitsizlikleri
for r in R:
    for t in T:
        model.addConstr(irrt[r, t] <= Qrt[r, t], name=f"Raw_Inv_Cap_t{t}_r{r}")

for p in P:
    for t in T:
        model.addConstr(ipt[p, t] <= Qpt[p, t], name=f"Prod_Inv_Cap_t{t}_p{p}")

# Kısıt 18, 19 ve 20: Çevresel Sınırlar (Enerji, Atık, Çevresel Maliyet)
for m in M:
    for t in T:
        model.addConstr(gp.quicksum(Empt[m, p, t] * Xmpt[m, p, t] for p in P) <= Emax, name=f"Energy_m{m}_t{t}")
        model.addConstr(gp.quicksum(Rmpt[m, p, t] * Xmpt[m, p, t] for p in P) <= Rmax, name=f"Waste_m{m}_t{t}")
        model.addConstr(gp.quicksum(Cmpt[m, p, t] * Xmpt[m, p, t] for p in P) <= Cmax, name=f"Env_Cost_m{m}_t{t}")

# Kısıt 21: Tek Yöntem Seçimi: Her periyotta sadece tek bir yöntem kullanılabilir
model.addConstr(gp.quicksum(Usm[m] for m in M) == 1, name="Single_Method_Selection")

## Amaç Fonksiyonu: Z3'ü Minimize Et

obj_z3 = gp.quicksum((Cmpt[m, p, t] + Empt[m, p, t] + Rmpt[m, p, t]) * Xmpt[m, p, t]
                     for m in M for p in P for t in T) + \
         gp.quicksum(cost_changm[m] * Usm[m] for m in M)

model.setObjective(obj_z3, GRB.MINIMIZE)
model.optimize()

if model.status == GRB.OPTIMAL:
    min_z3_degeri = model.objVal
    print(f"\nUlaşılabilecek Minimum Çevresel Etki (Z3 Alt Sınırı): {min_z3_degeri}")
    for m in M:
        if Usm[m].X > 0.5:
            print(f"Çevresel etkiyi minimize etmek için seçilen yöntem: {m}")