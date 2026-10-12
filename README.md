# BİÇEB — Biodiversity Analysis / Biyoçeşitlilik Analizi

BİÇEB is a desktop application for alpha and beta diversity calculations. It reads CSV, XLS and XLSX abundance tables and exports results to XLSX. The interface can be switched between Turkish and English.

BİÇEB, alfa ve beta çeşitliliği hesaplayan bir masaüstü uygulamasıdır. CSV, XLS ve XLSX bolluk tablolarını okur; sonuçları XLSX olarak kaydeder. Arayüz dili Türkçe ve İngilizce arasında değiştirilebilir.

## Kolay kurulum / Easy installation

Kullanıcıların Python kurmasına gerek yoktur. [BİÇEB 0.2.1 indirme sayfasını](https://github.com/ecirkucuksille/Biceb/releases/tag/v0.2.1) açın ve işletim sisteminize uygun dosyayı indirin:

| Sistem | İndirilecek dosya | Kurulum |
| --- | --- | --- |
| Windows 10/11 (64 bit) | `BICEB-<sürüm>-windows-x64-setup.exe` | Dosyayı açın, kurulum sihirbazını izleyin. Yönetici yetkisi gerekmez. Başlat menüsünde BİÇEB görünür. |
| macOS Intel | `BICEB-<sürüm>-macos-x86_64.dmg` | DMG'yi açın, BICEB simgesini Applications klasörüne sürükleyin. |
| macOS Apple Silicon | `BICEB-<sürüm>-macos-arm64.dmg` | DMG'yi açın, BICEB simgesini Applications klasörüne sürükleyin. |
| Ubuntu ve Debian (64 bit) | `biceb_<sürüm>_amd64.deb` | Dosyayı yazılım yükleyiciyle açın ve **Kur** seçeneğine basın. Uygulama menüsünde BİÇEB görünür. |
| Diğer Linux dağıtımları (x86_64) | `BICEB-<sürüm>-linux-x86_64.AppImage` | Dosyaya çalıştırma izni verin ve açın. Kurulum gerekmez. |

No Python installation is needed. Open the [BİÇEB 0.2.1 download page](https://github.com/ecirkucuksille/Biceb/releases/tag/v0.2.1) and download the file for your operating system. Run the Windows setup, drag the macOS app to Applications, or install the Linux DEB. On other Linux distributions, mark the AppImage executable and open it.

**Dağıtım durumu:** Linux paketleri yerel olarak üretildi ve sınandı. Windows ve macOS kurulum dosyaları `.github/workflows/build.yml` üzerinden ilgili işletim sistemlerinde üretilir. macOS uygulaması henüz Apple Developer sertifikasıyla imzalanıp noter onayından geçirilmedi; halka açık, uyarısız dağıtım için bu adım gereklidir. Windows'ta yayıncı imzası olmadan SmartScreen uyarısı görülebilir. Ayrıntılar için [dağıtım kılavuzuna](docs/distribution.md) bakın.

## Input format / Veri biçimi

The first column contains unique species names. Every other column represents a sample site and contains nonnegative numeric abundances, including decimals. Site names must be unique and no site may be entirely empty. Presence/absence analyses convert every positive abundance to `1` automatically. Chao1, both rarefaction methods, Brillouin, Simpson variance and Jackknife require whole individual counts; the app explains this when a fractional table is used with one of these methods.

İlk sütunda benzersiz tür adları bulunur. Diğer sütunlar örnek alanlardır ve ondalıklı değerler dahil negatif olmayan sayısal bollukları içerir. Örnek alan adları benzersiz olmalı; tamamen boş alan bulunmamalıdır. Var/yok analizleri pozitif bollukları otomatik olarak `1` değerine dönüştürür. Chao1, iki seyreltme yöntemi, Brillouin, Simpson varyansı ve Jackknife tam sayı birey sayıları gerektirir; ondalıklı veriyle seçildiklerinde uygulama bunu açıkça bildirir.

## Analysis selection / Analiz seçimi

Alpha diversity is grouped under **Species Richness Indices**, **Diversity Indices**, and **Species Abundance & Models**. Click an analysis and choose **Run Analysis** for its usual result window. For Margalef–Menhinick–DMM, select the metric beside **Chart** to plot the desired row. To export several alpha analyses at once, check their boxes in the left panel and choose **Export Selected Indices**. Each selected analysis is saved to a separate sheet in one XLSX file; no combined result window opens.

Alfa çeşitliliği **Tür Zenginliği İndisleri**, **Çeşitlilik İndisleri** ve **Tür Bolluğu ve Modeller** altında düzenlenmiştir. Tek analiz için ilgili satırı seçip **Analizi Çalıştır** düğmesine basın. Margalef–Menhinick–DMM sonucunda **Grafik** yanındaki ölçütü seçerek istediğiniz grafiği çizin. Birden çok alfa analizini almak için soldaki kutuları işaretleyip **Seçili İndisleri Dışa Aktar** düğmesine basın. Her analiz tek bir XLSX dosyasında ayrı çalışma sayfasına kaydedilir; birleşik sonuç ekranı açılmaz.

Example files are in `sampledata/`. The **Guide / Kılavuz** button opens a bilingual quick start and links to the historical Turkish PDF.

## Run from source / Kaynaktan çalıştırma

Use Python 3.11–3.13. Create a fresh environment; the old `venv/` folder is incomplete and should not be reused.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python -m biceb
```

On Windows PowerShell:

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -e .
.venv\Scripts\pythonw.exe -m biceb
```

The program's log file is stored in the operating system's application data directory under `BICEB/BİÇEB/logs/biceb.log`. It rotates automatically. Input data stays on your computer.

## Tests / Testler

```bash
.venv/bin/python -m pip install -e '.[dev]'
QT_QPA_PLATFORM=offscreen .venv/bin/python -m pytest -q
```

On Windows, omit `QT_QPA_PLATFORM=offscreen` when running tests in a desktop session.

## Installer builds / Kurulum paketlerinin üretimi

The GitHub Actions workflow builds an Inno Setup installer on Windows, two DMGs on macOS, and DEB and AppImage packages on Linux. The resulting packages include the Python runtime, Qt, calculation tables, logo and guide. Pushing a version tag adds the installers and checksums to its GitHub Release after all four builds pass. See [distribution instructions](docs/distribution.md) for local build commands and signing requirements.

Most numerical formulas are retained from the original project; rarefaction, Jackknife and lognormal lookup defects were corrected. Scientific validation against the guide and independent references remains an ongoing review task.

The original `Windows/` PyQt5 screens remain in the source archive for reference. The current launcher uses `biceb/` and does not import those screens.
