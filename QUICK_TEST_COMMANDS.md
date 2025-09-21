# 🚀 Konsultabot - Quick Test Commands

## 🔥 **Instant Testing Guide**

### **Start Both Servers (Run in separate terminals):**

**Terminal 1 - Django Backend:**
```bash
cd "c:\Users\Ace Ziegfred Culapas\CascadeProjects\Project"
.venv\Scripts\Activate.ps1
python backend\manage.py runserver 192.168.1.11:8000
```

**Terminal 2 - React Native Frontend:**
```bash
cd "c:\Users\Ace Ziegfred Culapas\CascadeProjects\Project\KonsultabotMobileNew"
npm start
```

## 🧪 **Test Scenarios**

### **1. Authentication Test:**
- **Login**: `admin@evsu.edu.ph` / `admin123`
- **Register**: `student@evsu.edu.ph` / `123456` / `2024001`

### **2. Technical Support Test:**
Try these voice or text queries:
- "My printer is not working"
- "WiFi is very slow"
- "Computer won't turn on"
- "Blue screen error"
- "EVSU campus WiFi problems"
- "Paper jam in printer"
- "Can't send emails"
- "Software won't install"

### **3. Voice Features Test:**
1. Tap microphone button 🎤
2. Say: "My printer has a paper jam"
3. Watch it convert to text and respond
4. Listen to spoken response

### **4. Adaptive Intelligence Test:**
1. Ask: "My printer is not working"
2. Wait for response
3. Ask the same question again
4. Should detect repetition and offer clarification

### **5. Campus Information Test:**
- "Tell me about EVSU"
- "Computer lab information"
- "Campus facilities"
- "Academic programs"

## 🎯 **Expected Results:**

### ✅ **Technical Queries Should Show:**
- 🔧 **Tech Support** mode indicator
- Comprehensive step-by-step solutions
- Prevention tips
- High confidence scores (90%+)

### ✅ **Voice Features Should:**
- Convert speech to text accurately
- Send message automatically
- Speak bot responses aloud
- Show microphone icons on voice messages

### ✅ **Adaptive Features Should:**
- Remember conversation history
- Detect repeated questions
- Offer clarification for similar queries
- Learn user patterns

## 📱 **Mobile Testing:**
1. Scan QR code with Expo Go app
2. Test all features on actual device
3. Voice recognition works better on real devices
4. Test microphone permissions

## 🌐 **Web Testing:**
1. Press 'w' in Metro bundler
2. Opens in browser
3. Test login and chat features
4. Voice may have limited support in browser

## 🔧 **Troubleshooting:**

### **If Backend Issues:**
```bash
# Check if Django is running
curl http://192.168.1.11:8000/

# Restart backend
python backend\manage.py runserver 192.168.1.11:8000
```

### **If Frontend Issues:**
```bash
# Clear Metro cache
npx expo start --clear

# Restart Metro bundler
npm start
```

### **If Voice Not Working:**
- Ensure microphone permissions granted
- Test on physical device (better than simulator)
- Check device volume settings
- Try different voice commands

## 🎉 **Success Indicators:**
- ✅ Login works without errors
- ✅ Messages send and receive properly
- ✅ Technical queries get 🔧 Tech Support responses
- ✅ Voice button records and converts speech
- ✅ Bot responses are spoken aloud
- ✅ Visual indicators show message types
- ✅ Confidence scores display
- ✅ Session continuity maintained

---
**🏆 Your Konsultabot is Production Ready! 🏆**
