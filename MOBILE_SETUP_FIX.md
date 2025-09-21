# 📱 Mobile App Setup & Login Fix Guide

## 🔧 Issues Fixed

### ✅ 1. Android SDK Error (SOLVED)
- **Issue**: Android SDK path not found
- **Solution**: Use Expo Go app on your phone or web browser instead of Android emulator
- **Action**: No Android SDK needed for development

### ✅ 2. Package Version Mismatch (SOLVED)
- **Issue**: expo-secure-store and react-native version conflicts
- **Solution**: Updated to compatible versions
- **Action**: Packages updated automatically

### ✅ 3. API Connection Issues (FIXED)
- **Issue**: Mobile app can't connect to Django backend
- **Solution**: Updated API configuration with proper error handling

## 🚀 How to Start the Project (Updated)

### Step 1: Start Django Backend
```powershell
# Option A: Use the batch file (recommended)
.\start_backend.bat

# Option B: Manual start
cd backend
python manage.py runserver 0.0.0.0:8000
```

### Step 2: Find Your IP Address (For Mobile Testing)
```powershell
# Run this to find your computer's IP
.\get_ip.bat
```

### Step 3: Update Mobile App Configuration
Edit `KonsultabotMobileNew\app.config.js` and replace `localhost` with your IP:
```javascript
extra: {
  apiUrl: "http://YOUR_IP_ADDRESS:8000/api"  // Replace YOUR_IP_ADDRESS
}
```

### Step 4: Start Mobile App
```powershell
cd KonsultabotMobileNew
npm start
```

## 📱 Testing Options

### Option 1: Web Browser (Easiest)
1. Start the mobile app with `npm start`
2. Press `w` to open in web browser
3. Test login/registration at `http://localhost:19006`

### Option 2: Expo Go App (Recommended)
1. Install Expo Go app on your phone
2. Start mobile app with `npm start`
3. Scan QR code with Expo Go app
4. Make sure your phone and computer are on same WiFi

### Option 3: Android Emulator (Optional)
1. Install Android Studio
2. Set up Android emulator
3. Press `a` in Expo CLI to open in emulator

## 🔍 Debugging Login Issues

### Check These First:
1. **Backend Running**: Ensure Django is running on `http://localhost:8000`
2. **API Endpoints**: Visit `http://localhost:8000/api/` to verify backend
3. **Network Connection**: Phone and computer on same WiFi
4. **Console Logs**: Check Expo dev tools for API error messages

### Test API Manually:
```bash
# Test registration endpoint
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@evsu.edu.ph","password":"testpass123","first_name":"Test","last_name":"User","student_id":"2021-12345"}'

# Test login endpoint  
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@evsu.edu.ph","password":"testpass123"}'
```

## 🛠️ Common Solutions

### If Login Still Fails:
1. **Check Django Admin**: Visit `http://localhost:8000/admin/` (admin@evsu.edu.ph / admin123)
2. **Verify User Creation**: Check if users are being created in admin panel
3. **Check API Logs**: Look at Django console for error messages
4. **Network Issues**: Try web version first to isolate mobile-specific issues

### If Registration Fails:
1. **Email Format**: Must use @evsu.edu.ph email
2. **Password Requirements**: Check Django password validation
3. **Student ID Format**: Ensure proper format (e.g., 2021-12345)
4. **Duplicate Users**: Check if email already exists

## 📋 Verification Checklist

- [ ] Django backend running on port 8000
- [ ] Can access `http://localhost:8000/admin/`
- [ ] Mobile app starts without errors
- [ ] API URL configured correctly
- [ ] Phone and computer on same network
- [ ] Expo Go app installed (for mobile testing)

## 🆘 Still Having Issues?

1. **Try Web Version First**: Use browser to test if backend works
2. **Check Network**: Ensure firewall isn't blocking connections
3. **Restart Services**: Stop and restart both Django and Expo
4. **Check Logs**: Look at both Django console and Expo dev tools

Your mobile app should now work properly with improved error handling and debugging information!
