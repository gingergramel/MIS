# Deployment Guide für Neon PostgreSQL + Azure Web App

## 1. GitHub Secrets konfigurieren

Gehe auf dein GitHub Repository und konfiguriere diese Secrets:
**Settings → Secrets and variables → Actions → New repository secret**

### Erforderliche Secrets:

#### `DATABASE_URL`
Deine Neon PostgreSQL Connection URL:
```
postgresql://user:password@host/dbname
```
**Wo findet man das?**
- Gehe auf https://console.neon.tech
- Wähle dein Projekt aus
- Kopiere die Connection URL unter "Connection string"
- Format: `postgresql://[user]:[password]@[host]/[dbname]?sslmode=require`

#### `AZURE_WEBAPP_PUBLISH_PROFILE`
Die Publish-Konfigurationsdatei von Azure:
1. Gehe auf https://portal.azure.com
2. Navigiere zu deiner Web App (2526djangoapp-mk)
3. Klicke auf **Get publish profile** (rechts oben)
4. Speichere die XML-Datei
5. Öffne die Datei und kopiere den kompletten Inhalt in diesen Secret

## 2. Azure Web App konfigurieren

Logge dich in Azure ein und setze folgende **App Settings**:

```
DATABASE_URL = postgresql://...  (von Neon)
DEBUG = False
ALLOWED_HOSTS = 2526djangoapp-mk.azurewebsites.net
DJANGO_SETTINGS_MODULE = mysite.settings
```

## 3. Git Push für Deployment

Wenn du einen Push auf `main` machst, läuft automatisch:
1. ✅ Docker Image wird gebaut
2. ✅ Image wird zu GitHub Container Registry gepusht
3. ✅ Django Migrations werden ausgeführt
4. ✅ App wird zu Azure Web App deployed

```bash
git add .
git commit -m "Deploy to production"
git push origin main
```

Überprüfe den Status auf GitHub unter **Actions**

## 4. Local Development mit Neon

Erstelle eine `.env` Datei:
```
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
DEBUG=True
```

Starte die App:
```bash
python manage.py migrate
python manage.py runserver
```

## 5. Docker lokal testen

```bash
docker build -t patientenportal .
docker run -e DATABASE_URL="postgresql://..." -p 8000:8000 patientenportal
```

## Troubleshooting

**App startet nicht?**
- Überprüfe die `DATABASE_URL` auf Azure
- Schau die Logs: Azure Portal → Deployment Center → Logs

**Migrationen fehlgeschlagen?**
- SSH in Azure Web App
- Führe aus: `python manage.py migrate --noinput`

**Datenbankverbindung funktioniert nicht?**
- Prüfe Firewall-Regeln in Neon Console
- Stelle sicher, dass SSL/TLS aktiviert ist
