## Web Yazılım Geliştiricisi Teknik Case

### Açıklama  

Proje **Django REST framework** ve **Vue.js** (Vue, bootstrap veya hazır template vb.) kullanılarak yapılmalıdır.  
Arayüzün tasarımına çok önem verilmesine gerek yoktur. Özelliklerin çalışması yeterlidir.  

Verilen proje süresinden önce teslim edilebilir.  
Zorunlu olmayan görevlerin yapılması artı olarak değerlendirilecektir.  

Geliştirme süreciyle ilgili görüşme yapılacaktır.  

Proje Github üzerinden gizli (private) repo olarak paylaşılmalı ve <https://github.com/noviteam> hesabına erişim izni gönderilmelidir.  

**Teslim Süresi:** 5 gün  
  
---
  
### Adımlar  

#### 1. Aşama: Üye giriş ve kayıt modülü
- **dj-rest-auth** kullanılacak (API + Front End)  

#### 2. Aşama: Kuruluş CRUD modülü (API)
**Model alanları:**  
- Kuruluş adı (kısa metin)  
- Kuruluş logo (görsel)  
- Kuruluş türü (Şahıs, Büyük işletme, KOBİ, STK)  
- Ülke (Tüm ülkelerden seçim)  
- Kuruluş tarihi  
- Çalışan sayısı (Sayı)  

#### 3. Aşama: Kuruluş filtreleme (API + Front End)
Filtreleme alanları:  
- Kuruluş adı  
- Kuruluş türü (çoklu seçim)  
- Ülke  
- Kuruluş tarihi (tam tarih aralığı)  
- Çalışan sayısı (aralık)  

**Örnek:** Türkiye’de bulunan çalışan sayısı 10’nun altında olan KOBİ ve STK kuruluşları.  

#### 4. Aşama (opsiyonel):  
- Kullanıcının kuruluşları takip etmesi  
- Takip ettiği kuruluşları listelemesi (API)  

#### 5. Aşama:
- API dokümanı hazırlanması (Swagger)  
- Proje kurulum dokümanı hazırlanması (README)  
- Kurulum sırasında örnek verilerin otomatik eklenmesi (users, kuruluşlar — fixtures/commands)  
- Birim testlerin yazılması (opsiyonel)  

#### 6. Aşama:
- **Docker compose** ile kurulum yapılması (Django app, PostgreSQL, Vue.js)  
- **AWS (Free Tier) EC2** ile canlıya alınması (opsiyonel)  

---  

### Tavsiye Paketler & Kaynaklar (zorunlu değil)

- [DRF API Documentation](https://www.django-rest-framework.org/topics/documenting-your-api/#documenting-your-api)  
- <https://djangopackages.org/grids/>  
- [dj-rest-auth](https://github.com/iMerica/dj-rest-auth)  
- [drf-yasg (Swagger)](https://github.com/axnsan12/drf-yasg)  
- [django-environ](https://github.com/joke2k/django-environ)  
- [django-countries](https://github.com/SmileyChris/django-countries/)  

