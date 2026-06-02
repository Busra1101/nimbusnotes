# NimbusNotes

NimbusNotes, Docker ile container hâline getirilmiş ve Google Kubernetes Engine üzerinde çalıştırılmış bulut tabanlı bir not yönetim uygulamasıdır. Uygulama, kullanıcıdan aldığı notları kalıcı olarak saklar ve Kubernetes bileşenleri üzerinden yönetilir.

## 1. Uygulama Mimarisi

NimbusNotes basit bir Flask web uygulamasıdır.

- Kullanıcı web arayüzünden not ekler veya siler.
- Flask uygulaması gelen istekleri işler.
- Notlar `/data/notes.txt` dosyasına yazılır.
- `/data` dizini Kubernetes PVC ile kalıcı diske bağlanır.
- Böylece pod silinse veya yeniden oluşsa bile notlar korunur.

## 2. Sistem Mimarisi

Kullanıcı → LoadBalancer Service → Kubernetes Deployment → Flask Container → Persistent Volume Claim → Persistent Volume

## 3. Kubernetes Mimarisi

Projede kullanılan Kubernetes bileşenleri:

- Deployment: Uygulama pod’unu yönetir ve yeni sürümlerin dağıtılmasını sağlar.
- Service: LoadBalancer tipiyle uygulamaya dış IP üzerinden erişim sağlar.
- PersistentVolumeClaim: Uygulama verilerinin kalıcı tutulmasını sağlar.
- NetworkPolicy: Pod trafiği için ağ politikası tanımlar.

## 4. Kullanılan Teknolojiler

- Python Flask
- Docker
- Google Cloud Build
- Artifact Registry
- Google Kubernetes Engine
- Kubernetes Deployment
- Kubernetes Service
- Persistent Volume Claim
- NetworkPolicy
- GitHub

## 5. Docker ve Container Süreci

Uygulama Dockerfile ile container hâline getirilmiştir. Docker image, Artifact Registry üzerinde saklanmıştır.

Image adresi:

`europe-west1-docker.pkg.dev/nimbusnotes-busra-2026/nimbusnotes-repo/nimbusnotes:v10`

## 6. CI/CD Pipeline Akışı

Projede CI/CD yapılandırması için `cloudbuild.yaml` kullanılmıştır.

Cloud Build akışı:

Kaynak kod → Cloud Build → Docker image build → Artifact Registry push

Cloud Build ile uygulamanın Docker image'ı otomatik olarak oluşturulmuş ve Artifact Registry'ye gönderilmiştir. Kubernetes deployment güncellemesi ise `kubectl set image` komutu ile uygulanmıştır.

## 7. Deployment ve Service Kullanımı

Deployment, NimbusNotes uygulamasının pod olarak çalışmasını sağlar.

Service ise uygulamanın dış dünyadan erişilebilir olmasını sağlar. Bu projede Service tipi `LoadBalancer` olarak tanımlanmıştır.

## 8. PV/PVC Kullanımı

Uygulamadaki notlar container içinde geçici olarak tutulmamaktadır. Bunun yerine `/data` dizini PVC ile kalıcı diske bağlanmıştır.

Bu sayede:

- Pod silinse bile veri kaybolmaz.
- Yeni pod aynı veriye erişebilir.
- Uygulama daha güvenilir hâle gelir.

## 9. NetworkPolicy Kullanımı

Projede `network-policy.yaml` dosyası ile NetworkPolicy tanımlanmıştır. Bu dosya, NimbusNotes podları için ingress ağ politikası oluşturur.

Demo ortamında LoadBalancer üzerinden uygulamaya erişimin kesilmemesi için ingress trafiğine izin verilmiştir. Böylece NetworkPolicy bileşeninin Kubernetes ortamında nasıl tanımlandığı gösterilmiştir.

## 10. Rolling Update

Yeni uygulama sürümleri Kubernetes rolling update ile canlı ortama alınmıştır.

Örnek komut:

`kubectl set image deployment/nimbusnotes-deployment nimbusnotes=europe-west1-docker.pkg.dev/nimbusnotes-busra-2026/nimbusnotes-repo/nimbusnotes:v10`

Rolling update sayesinde Kubernetes eski pod’u kapatıp yeni image ile pod oluşturur.

## 11. Rollback

Kubernetes rollout geçmişi üzerinden eski sürümlere geri dönülebilir.

Örnek komut:

`kubectl rollout undo deployment/nimbusnotes-deployment`

Bu özellik, hatalı bir sürüm yayınlandığında önceki çalışan sürüme dönmeyi sağlar.

## 12. Ölçekleme

Deployment replica sayısı değiştirilerek uygulama ölçeklenebilir.

Örnek komut:

`kubectl scale deployment nimbusnotes-deployment --replicas=2`

Bu projede PVC `ReadWriteOnce` yapıda olduğu için kalıcı disk aynı anda birden fazla pod tarafından kullanılamaz. Bu nedenle uygulama final durumda 1 replica ile çalıştırılmıştır. Scaling komutu test edilmiştir ve PVC kullanılan uygulamalarda storage stratejisinin önemli olduğu görülmüştür.

## 13. Temel Komutlar

- `kubectl get pods`
- `kubectl get service`
- `kubectl get pvc`
- `kubectl get deployment`
- `kubectl rollout history deployment/nimbusnotes-deployment`
- `kubectl rollout status deployment/nimbusnotes-deployment`

## 14. Proje Dosya Yapısı

- `app/app.py`
- `app/Dockerfile`
- `app/requirements.txt`
- `app/static/clouds.jpg`
- `k8s/deployment.yaml`
- `k8s/service.yaml`
- `k8s/pvc.yaml`
- `k8s/network-policy.yaml`
- `cloudbuild.yaml`
- `README.md`

## 15. Canlı Uygulama

`http://104.155.89.172`

## 16. GitHub Repository

`https://github.com/Busra1101/nimbusnotes`


## 17. Kubernetes Test ve Kontrol Komutları

### Pod, Service, PVC ve Deployment Kontrolü

```bash
kubectl get pods
kubectl get svc
kubectl get pvc
kubectl get deployment
```

### Scaling Testi

Deployment replica sayısı değiştirilerek scaling testi yapılmıştır.

```bash
kubectl scale deployment nimbusnotes-deployment --replicas=2
kubectl get pods
```

PVC `ReadWriteOnce` kullandığı için final çalışan sürümde replica sayısı tekrar 1 yapılmıştır.

```bash
kubectl scale deployment nimbusnotes-deployment --replicas=1
```

### Rolling Update Testi

Yeni image sürümü deployment üzerine uygulanmıştır.

```bash
kubectl set image deployment/nimbusnotes-deployment nimbusnotes=europe-west1-docker.pkg.dev/nimbusnotes-busra-2026/nimbusnotes-repo/nimbusnotes:v10
kubectl rollout status deployment/nimbusnotes-deployment
```

### Rollback Testi

Hatalı veya istenmeyen bir güncelleme durumunda önceki sürüme dönüş test edilmiştir.

```bash
kubectl rollout undo deployment/nimbusnotes-deployment
kubectl rollout status deployment/nimbusnotes-deployment
```

### PVC Üzerindeki Notları Kontrol Etme

Uygulamanın kullandığı gerçek veri dosyası pod içindeki `/data/notes.txt` yolundadır.

```bash
kubectl get pods
kubectl exec -it POD_ADI -- cat /data/notes.txt
```