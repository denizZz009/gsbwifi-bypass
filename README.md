# GSBWIFI Auto-Auth & Bypass 

<img width="812" height="523" alt="image" src="https://github.com/user-attachments/assets/e9ffb4a3-dc01-4035-8090-dbd102543598" />

GSBWIFI ağlarında yaşanan "captive portal" erişim krizlerine ve DPI (Deep Packet Inspection) tabanlı hız kısıtlamalarına (QoS) kesin çözüm sağlayan Python tabanlı otomasyon ve bypass aracı.

## 💡 Proje Hakkında

Tarayıcının hantal UI render ve SSL handshake süreçlerini aradan çıkaran bu script, doğrudan `j_spring_security_check` endpoint'ine **fail-fast** prensibiyle agresif POST istekleri atarak Auth sunucusundaki ilk boşlukta yetkilendirmeyi tamamlar. Ağa bağlanıldığı an otomatik devreye giren entegre **Cloudflare WARP (warp-cli)** modülü ise tüm ağ trafiğinizi şifreli tünele sokarak paket denetimi filtrelerini bypass eder ve altyapının izin verdiği maksimum bant genişliğine ulaşmanızı sağlar.

##  Özellikler
- **Hızlı Doğrulama (Auto-Auth):** "Timeout" yiyen sayfaları beklemez, saniyeler içinde ağa yetkilendirme sağlar.
- **Hız Kısıtı Aşma (DPI Bypass):** Cloudflare WARP entegrasyonu ile trafik şekillendirme (Traffic Shaping) filtrelerini atlar.
- **Güvenli Kimlik Yönetimi:** Şifreleriniz kod içine gömülmez, lokal `config.ini` dosyanızda güvenle saklanır.
- **Otomatik Bağımlılık Kurulumu:** Sistemde WARP yüklü değilse, Windows Paket Yöneticisi (winget) üzerinden otomatik kurulum imkanı sunar.

##  Kurulum

1. Repoyu bilgisayarınıza klonlayın:
   ```bash
   git clone [https://github.com/KULLANICI_ADIN/gsbwifi-bypass-tool.git](https://github.com/KULLANICI_ADIN/gsbwifi-bypass-tool.git)
   cd gsbwifi-bypass-tool
2. Gerekli kütüphaneyi yükleyin:
   ```bash
   pip install -r requirements.txt
3. Kullanım
   ```bash
   python main.py
   
- İlk Çalıştırma: Script, ilk açılışta bulunduğunuz dizine bir config.ini dosyası oluşturacaktır. Aracı kapatın, bu dosyanın içine GSBWIFI (TC Kimlik ve Şifre) bilgilerinizi girin ve aracı tekrar başlatın.
- Menü Kullanımı: Karşınıza çıkan yeşil terminal ekranından sadece ağa bağlanmayı veya bağlanıp doğrudan WARP tünelini açmayı seçebilirsiniz.


## ⚠️ Yasal Uyarı
Bu araç, ağ sorunlarını kişisel kullanım düzeyinde çözmek ve teknik bir konsepti (PoC) kanıtlamak amacıyla eğitim amaçlı yazılmıştır. Ağ altyapılarına kasıtlı zarar verecek DDoS veya flood amaçlı kullanılamaz. Sorumluluk son kullanıcıya aittir.

## Geliştirici: 
- Deniz Egemen Emare
- Linkedin: in/degemen
