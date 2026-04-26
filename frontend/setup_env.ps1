# Setup .env for React/Vite Frontend
$envContent = @"
VITE_FIREBASE_API_KEY=AIzaSyDdIJ4LHtQLnGNZXNeHmMeWg03lmtaZWmo
VITE_FIREBASE_AUTH_DOMAIN=ipt-master.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=ipt-master
VITE_FIREBASE_STORAGE_BUCKET=ipt-master.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=869160643502
VITE_FIREBASE_APP_ID=1:869160643502:web:d31677698848432338b63f
VITE_FIREBASE_MEASUREMENT_ID=G-Z3LE9LGJED
"@

$envContent | Out-File -FilePath .env -Encoding utf8
Write-Host "✅ Created frontend/.env with Firebase credentials." -ForegroundColor Green
Write-Host "⚠️  Reminder: Do NOT commit the .env file to GitHub." -ForegroundColor Red
