import math

class KokenCEM43ClinicalToolkit:
    """
    KOKEN CEM43 Clinical Decision Support Toolkit (v2.0.0)
    Authors: Sevval Emine Koken (Gazi University Faculty of Medicine), Omer Hakan Koken
    Model: Sapareto-Dewey Cumulative Equivalent Minutes at 43°C with Tissue-Specific Thresholds
    """

    # Klinik doku hassasiyet eşikleri (CEM43 dakika cinsinden geri dönüşümsüz hasar sınırları)
    TISSUE_THRESHOLDS = {
        "brain": {"limit": 20.0, "name": "Beyin Dokusu (Merkezi Sinir Sistemi)"},
        "muscle": {"limit": 80.0, "name": "İskelet Kası Dokusu"},
        "skin": {"limit": 120.0, "name": "Deri ve Subkutan Doku"},
        "tumor_target": {"limit": 60.0, "name": "Hedef Tümör Dokusu (Terapötik Eşik)"}
    }

    def __init__(self, patient_id, tissue_type="tumor_target"):
        self.patient_id = patient_id
        self.tissue_type = tissue_type if tissue_type in self.TISSUE_THRESHOLDS else "tumor_target"
        self.total_cem43 = 0.0
        self.log = []

    def calculate_interval_dose(self, temp_celsius, duration_minutes):
        """Belirli bir sıcaklık ve süre aralığı için Sapareto-Dewey CEM43 dozunu hesaplar."""
        if temp_celsius < 39.0:
            r_value = 0.0
        elif 39.0 <= temp_celsius < 43.0:
            r_value = 0.25
        else:
            r_value = 0.50

        cem43 = duration_minutes * (r_value ** (43.0 - temp_celsius))
        self.total_cem43 += cem43
        self.log.append((temp_celsius, duration_minutes, round(cem43, 2)))
        return cem43

    def generate_clinical_report(self):
        """Klinik güvenlik sınırlarına göre karar destek raporu üretir."""
        tissue_info = self.TISSUE_THRESHOLDS[self.tissue_type]
        limit = tissue_info["limit"]
        dose = round(self.total_cem43, 2)

        report = [
            f"=== KOKEN CEM43 KLİNİK HİPERTERMİ RAPORU (v2.0) ===",
            f"Vaka Kodu: {self.patient_id}",
            f"Analiz Edilen Doku: {tissue_info['name']}",
            f"Kümülatif Termal Doz: {dose} CEM43 dakika",
            f"Referans Klinik Eşik: {limit} CEM43 dakika",
            "-" * 50
        ]

        if self.tissue_type == "tumor_target":
            if dose >= limit:
                status = "BAŞARILI: Terapötik sitotoksik doz eşiğine ulaşıldı."
            else:
                status = "UYARI: Yetersiz termal doz. Tedavi süresi veya sıcaklığı artırılmalı."
        else:
            if dose >= limit:
                status = "KRİTİK ALARM: Sağlıklı dokuda termal nekroz riski aşıldı! Soğutma başlatın."
            elif dose >= limit * 0.8:
                status = "DİKKAT: Sağlıklı doku hasar sınırının %80'ine yaklaşıldı."
            else:
                status = "GÜVENLİ: Sağlıklı doku termal tolerans sınırları içinde."

        report.append(f"KLİNİK KARAR: {status}")
        report.append("=" * 50)
        return "\n".join(report)

if __name__ == "__main__":
    # Örnek Klinik Simülasyon: Beyin tümörü hipertermi tedavisi sırasında çevre beyin dokusu takibi
    patient_sim = KokenCEM43ClinicalToolkit(patient_id="GAZI-ONC-2026-01", tissue_type="brain")
    patient_sim.calculate_interval_dose(temp_celsius=41.5, duration_minutes=15)
    patient_sim.calculate_interval_dose(temp_celsius=42.8, duration_minutes=10)
    patient_sim.calculate_interval_dose(temp_celsius=43.5, duration_minutes=5)
    print(patient_sim.generate_clinical_report())
