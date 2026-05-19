# NimbusNotes

NimbusNotes, Docker ile container haline getirilmiş ve Google Kubernetes Engine üzerinde çalıştırılan basit bir bulut not alma uygulamasıdır.

## Kullanılan Teknolojiler

- Python Flask
- Docker
- Google Cloud Build
- Artifact Registry
- Google Kubernetes Engine
- Kubernetes Deployment
- Kubernetes Service
- Persistent Volume Claim
- NetworkPolicy

## Uygulama Mimarisi

Kullanıcı, LoadBalancer Service üzerinden NimbusNotes uygulamasına erişir. Uygulama Flask ile çalışır ve notları `/data` dizinine kaydeder. Bu dizin Kubernetes PVC ile kalıcı diske bağlanmıştır.

## Kubernetes Bileşenleri

- Deployment: NimbusNotes pod’unu yönetir.
- Service: Uygulamaya dış IP ile erişim sağlar.
- PVC: Not verilerinin kalıcı tutulmasını sağlar.
- NetworkPolicy: Pod trafiği için ağ politikası tanımlar.

## CI/CD Akışı

Cloud Build, uygulama kodundan Docker image oluşturur ve Artifact Registry’ye gönderir.

## Temel Komutlar

```bash
kubectl get pods
kubectl get service
kubectl rollout history deployment/nimbusnotes-deployment
kubectl scale deployment nimbusnotes-deployment --replicas=1
```