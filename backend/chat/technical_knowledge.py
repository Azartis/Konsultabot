"""
Technical Knowledge Base for IT Support
Handles printer, wifi, computer, and other technical problems
"""

TECHNICAL_PROBLEMS = {
    "printer_problems": {
        "paper_jam": {
            "keywords": ["paper jam", "paper stuck", "jammed", "papel na stuck", "paper feeding", "paper feed"],
            "problem": "Paper jam in printer",
            "solution": """Oh no, paper jams are so frustrating! 😤 Don't worry though - I've helped tons of people fix this, and we'll get your printer working again. Let's tackle this step by step:

🔧 **Let's fix this paper jam together:**

1. **First, let's be safe** - Turn off your printer and unplug the power cord (this prevents any accidents)
2. **Open everything up** - Open all the doors and access panels you can find
3. **Gentle removal** - Carefully pull out the jammed paper, following the direction it normally feeds (don't yank it!)
4. **Check for sneaky pieces** - Look for any torn bits hiding in there - they love to cause more jams later
5. **Clear the path** - Make sure nothing else is blocking the paper route
6. **Close it all up** - Shut all those doors and panels properly
7. **Power up** - Plug back in and turn on your printer
8. **Test it out** - Try a test print to make sure we got it!

**Still giving you trouble?** Sometimes the rollers get worn out or there's something else stuck in there. If it keeps jamming, let me know and we'll try some other tricks! 

Did this help get your printer back to behaving? 🤞""",
            "prevention": "Use proper paper size, don't overfill tray, keep printer clean"
        },
        "printer_offline": {
            "keywords": ["printer offline", "printer not found", "can't find printer", "printer disconnected", "printer not responding", "printer unavailable"],
            "problem": "Printer shows offline or not found",
            "solution": """I totally get how annoying it is when your printer just decides to go offline! 😠 It's like it has a mind of its own sometimes. Let's get this sorted out - I've seen this issue so many times, and we can definitely fix it:

🖨️ **Let's reconnect your printer step by step:**

1. **First, let's check the basics** (I know, I know, but these simple things often work!):
   • Make sure that USB cable is snug and secure
   • If it's a network printer, check WiFi/ethernet connection
   • Double-check the power cable is plugged in properly

2. **The classic "turn it off and on again"** (it really works!):
   • Turn your printer completely off, then back on
   • Restart your computer too
   • Give everything about 30 seconds to wake up properly

3. **Let's tell Windows to find your printer again:**
   • Go to Settings > Printers & Scanners
   • Remove your printer from the list
   • Add it back again (Windows will search for it)
   • Run the Windows printer troubleshooter - it's actually pretty good!
   • Set it as your default printer

4. **If it's still being stubborn, let's update the drivers:**
   • Download fresh drivers from the manufacturer's website
   • Uninstall the old ones first (they might be corrupted)
   • Install the new drivers and restart your computer

This usually does the trick! How's it looking now? Still giving you grief? 🤔""",
            "prevention": "Keep drivers updated, check connections regularly"
        },
        "printer_power": {
            "keywords": ["printer not turning on", "printer won't turn on", "printer no power", "printer dead", "printer not starting", "correctly plugged in", "power button not working"],
            "problem": "Printer not turning on despite being plugged in",
            "solution": """🔌 **Printer Power Troubleshooting:**

1. **Check Power Connection:**
   • Power cord firmly connected to printer
   • Power cord connected to wall outlet
   • Try different power outlet
   • Check power strip/surge protector

2. **Test Power Source:**
   • Test outlet with another device
   • Try different power cord if available
   • Check circuit breaker/fuse

3. **Printer Power Button:**
   • Press and hold for 3-5 seconds
   • Look for LED lights or display
   • Try multiple short presses
   • Check if button is stuck

4. **Hard Reset:**
   • Unplug for 60 seconds
   • Hold power button while unplugged (10 sec)
   • Plug back in and try turning on
   • Check for error lights/sounds

5. **Hardware Check:**
   • All doors/covers closed properly
   • Paper tray inserted correctly
   • Remove and reseat cartridges
   • Check for loose internal connections

**If still not working:** Internal power supply may be faulty - contact repair service.""",
            "prevention": "Use surge protectors, avoid power surges, regular maintenance"
        },
        "print_quality": {
            "keywords": ["blurry print", "faded print", "streaky print", "poor quality", "smudged", "lines on paper", "ghosting", "white gap", "white line", "white lines", "white gaps", "gap on paper", "line on paper", "printing gaps", "printing lines", "white space", "missing ink", "incomplete printing", "pixma", "g3730", "canon printer", "print head", "nozzle", "ink cartridge"],
            "problem": "Print quality issues - gaps, lines, or poor output",
            "solution": """🎨 **Print Quality Fix - White Gaps/Lines/Poor Output:**

**For White Gaps or Lines (like PIXMA G3730):**

1. **Print Head Issues (Most Common):**
   • Run Deep Cleaning cycle 2-3 times
   • Print nozzle check pattern
   • Clean print heads manually with cotton swab and distilled water
   • Let printer sit for 30 minutes, then try again

2. **Ink Supply Problems:**
   • Check ink levels in all cartridges
   • Look for air bubbles in ink tubes
   • Prime the ink system if available
   • Replace empty or low cartridges

3. **Clogged Nozzles:**
   • Use printer's cleaning utility repeatedly
   • Print test pages between cleanings
   • For stubborn clogs: Turn off printer overnight, try cleaning again
   • Consider using cleaning solution designed for your printer

4. **Paper and Settings:**
   • Ensure correct paper type selected in driver
   • Use high-quality paper appropriate for your printer
   • Check print quality settings (use "High" or "Best" quality)
   • Avoid draft mode for important documents

5. **Physical Cleaning:**
   • Clean paper path with lint-free cloth
   • Remove any paper dust or debris
   • Check for damaged or worn rollers
   • Ensure print heads move freely

6. **Advanced Solutions:**
   • Replace print head assembly if removable
   • Check for firmware updates
   • Reset printer to factory defaults
   • Contact Canon support for PIXMA-specific issues

**For PIXMA G3730 specifically:** This model is prone to print head clogging. Regular use and monthly cleaning cycles prevent most issues.""",
            "prevention": "Use quality paper, replace cartridges when low, regular maintenance"
        },
        "printer_slow": {
            "keywords": ["printer slow", "printing slowly", "takes long time", "slow printing"],
            "problem": "Printer printing very slowly",
            "solution": """⚡ **Speed Up Printing:**

1. **Check print settings:**
   • Change to "Fast" or "Draft" mode
   • Reduce print quality if acceptable
   • Print in grayscale instead of color

2. **Memory issues:**
   • Close other programs
   • Restart computer
   • Add more RAM to printer if possible

3. **Connection optimization:**
   • Use USB instead of network if possible
   • Check network speed for network printers
   • Update printer drivers

4. **Maintenance:**
   • Clean printer heads
   • Update firmware
   • Check for background processes""",
            "prevention": "Regular maintenance, optimal settings for job type"
        }
    },
    "wifi_problems": {
        "slow_internet": {
            "keywords": ["slow internet", "slow wifi", "internet slow", "bagal ng internet"],
            "problem": "Internet is very slow",
            "solution": """1. Restart your router (unplug 30 seconds, plug back)
2. Move closer to router
3. Check for interference (microwaves, other devices)
4. Run speed test to confirm issue
5. Contact ISP if speeds are much lower than expected
6. Consider upgrading internet plan""",
            "prevention": "Regular router restarts, optimal router placement"
        },
        "no_connection": {
            "keywords": ["no internet", "can't connect", "no wifi", "walang internet"],
            "problem": "Cannot connect to internet",
            "solution": """1. Check if WiFi is enabled on device
2. Restart device and router
3. Forget and reconnect to WiFi network
4. Check if other devices can connect
5. Reset network settings if needed
6. Contact ISP if widespread outage""",
            "prevention": "Keep network passwords secure, regular router maintenance"
        }
    },
    "computer_problems": {
        "wont_start": {
            "keywords": ["won't start", "won't turn on", "no power", "hindi nag-oopen", "computer dead", "pc not starting", "laptop won't boot"],
            "problem": "Computer won't start or turn on",
            "solution": """💻 **Computer Won't Start Fix:**

1. **Power supply check:**
   • Check power cable connections
   • Try different power outlet
   • Test power adapter (laptops)
   • Check power strip/surge protector

2. **Hardware basics:**
   • Press power button firmly (hold 3-5 sec)
   • Check if any lights/fans turn on
   • Listen for beeps or sounds
   • Remove battery and try AC only (laptops)

3. **Memory issues:**
   • Remove and reseat RAM sticks
   • Try one RAM stick at a time
   • Clean RAM contacts with eraser
   • Test in different slots

4. **Internal connections:**
   • Reseat all cables inside case
   • Check motherboard power connections
   • Ensure graphics card is seated properly
   • Check for loose components

5. **Minimal boot test:**
   • Disconnect all unnecessary devices
   • Remove extra RAM, drives
   • Try booting with essentials only

**If still not working:** Motherboard or power supply may be faulty.""",
            "prevention": "Regular cleaning, avoid power surges, proper shutdown"
        },
        "blue_screen": {
            "keywords": ["blue screen", "BSOD", "blue screen of death", "system crash", "stop error", "critical error"],
            "problem": "Blue Screen of Death (BSOD)",
            "solution": """🔵 **Blue Screen Fix:**

1. **Immediate steps:**
   • Note the STOP error code
   • Take photo of error screen
   • Restart computer
   • Boot in Safe Mode if needed

2. **Driver issues:**
   • Update all drivers (especially graphics)
   • Roll back recent driver updates
   • Use Device Manager to check conflicts
   • Download drivers from manufacturer sites

3. **System diagnostics:**
   • Run Windows Memory Diagnostic
   • Check hard drive with CHKDSK
   • Run System File Checker: sfc /scannow
   • Use Windows built-in troubleshooters

4. **Software conflicts:**
   • Uninstall recently installed programs
   • Disable startup programs
   • Run antivirus full scan
   • Check for Windows updates

5. **Hardware testing:**
   • Test RAM with MemTest86
   • Check hard drive health
   • Monitor CPU/GPU temperatures
   • Reseat all components

**Common STOP codes:**
• 0x0000007E: System thread exception
• 0x0000003B: System service exception
• 0x00000050: Page fault in nonpaged area""",
            "prevention": "Keep drivers updated, regular system maintenance, avoid overheating"
        },
        "slow_computer": {
            "keywords": ["computer slow", "pc slow", "laptop slow", "running slowly", "sluggish", "laggy", "bagal ng computer"],
            "problem": "Computer running very slowly",
            "solution": """🐌 **Speed Up Computer:**

1. **Immediate fixes:**
   • Restart computer
   • Close unnecessary programs
   • Check Task Manager for high CPU usage
   • End resource-heavy processes

2. **Storage cleanup:**
   • Run Disk Cleanup utility
   • Delete temporary files
   • Empty Recycle Bin
   • Uninstall unused programs
   • Move files to external storage

3. **Startup optimization:**
   • Disable unnecessary startup programs
   • Use Task Manager > Startup tab
   • Keep only essential programs
   • Delay non-critical startups

4. **System maintenance:**
   • Run antivirus full scan
   • Update Windows and drivers
   • Defragment hard drive (HDD only)
   • Check for malware with Malwarebytes

5. **Hardware upgrades:**
   • Add more RAM if possible
   • Replace HDD with SSD
   • Clean dust from fans/vents
   • Check hard drive health

**Performance monitoring:**
• Use Task Manager to identify bottlenecks
• Check CPU, Memory, Disk usage
• Monitor temperatures""",
            "prevention": "Regular maintenance, avoid installing unnecessary software, keep system updated"
        },
        "freezing": {
            "keywords": ["computer freezing", "pc freezes", "laptop freezes", "system hangs", "not responding", "frozen screen"],
            "problem": "Computer freezes or hangs frequently",
            "solution": """🧊 **Fix Computer Freezing:**

1. **Immediate response:**
   • Try Ctrl+Alt+Del
   • Wait 30 seconds for response
   • Force restart if completely frozen
   • Note what you were doing when it froze

2. **Temperature check:**
   • Check if computer feels hot
   • Clean dust from vents and fans
   • Ensure proper ventilation
   • Monitor CPU/GPU temperatures

3. **Software issues:**
   • Update all drivers
   • Run Windows Update
   • Scan for malware/viruses
   • Check for conflicting programs
   • Boot in Safe Mode to test

4. **Hardware diagnostics:**
   • Test RAM with Windows Memory Diagnostic
   • Check hard drive with CHKDSK
   • Reseat RAM and connections
   • Test with minimal hardware

5. **System optimization:**
   • Disable visual effects
   • Reduce startup programs
   • Increase virtual memory
   • Check power settings

**Pattern analysis:**
• Does it freeze during specific tasks?
• After how long does it freeze?
• Any error messages before freezing?""",
            "prevention": "Keep system cool, regular updates, avoid overloading system resources"
        },
        "no_internet": {
            "keywords": ["no internet", "can't connect internet", "internet not working", "no network", "wifi not working", "ethernet not working"],
            "problem": "Computer can't connect to internet",
            "solution": """🌐 **Internet Connection Fix:**

1. **Basic checks:**
   • Check if WiFi is enabled
   • Verify network password
   • Try ethernet cable if available
   • Restart modem and router

2. **Windows network troubleshooting:**
   • Run Network Troubleshooter
   • Reset network adapters
   • Flush DNS: ipconfig /flushdns
   • Reset TCP/IP: netsh int ip reset

3. **Driver issues:**
   • Update network adapter drivers
   • Uninstall and reinstall network drivers
   • Check Device Manager for errors
   • Download drivers from manufacturer

4. **Network settings:**
   • Forget and reconnect to WiFi
   • Check proxy settings
   • Disable VPN temporarily
   • Reset network settings

5. **Advanced fixes:**
   • Check firewall settings
   • Disable antivirus temporarily
   • Use different DNS servers (8.8.8.8)
   • Contact ISP if widespread issue

**Command line tools:**
• ipconfig /release
• ipconfig /renew
• ping google.com
• nslookup google.com""",
            "prevention": "Keep network drivers updated, avoid network setting changes"
        },
        "overheating": {
            "keywords": ["computer hot", "overheating", "laptop hot", "fan loud", "thermal shutdown", "too hot"],
            "problem": "Computer overheating issues",
            "solution": """🔥 **Overheating Fix:**

1. **Immediate cooling:**
   • Shut down computer immediately
   • Let it cool for 30+ minutes
   • Check if vents are blocked
   • Use in cooler environment

2. **Cleaning:**
   • Clean dust from vents with compressed air
   • Clean keyboard and screen vents
   • Remove dust from internal fans
   • Clean heat sinks if accessible

3. **Ventilation improvement:**
   • Use on hard, flat surfaces
   • Avoid beds, couches, carpets
   • Use laptop cooling pad
   • Ensure adequate room ventilation

4. **Software optimization:**
   • Close resource-heavy programs
   • Reduce screen brightness
   • Use power saving mode
   • Monitor CPU usage

5. **Hardware checks:**
   • Check if fans are working
   • Replace thermal paste (advanced)
   • Check for failing fans
   • Monitor temperatures with software

**Temperature monitoring tools:**
• HWMonitor
• Core Temp
• SpeedFan
• MSI Afterburner

**Safe temperatures:**
• CPU: Under 80°C
• GPU: Under 85°C""",
            "prevention": "Regular cleaning, proper ventilation, avoid blocking vents"
        }
    },
    "software_problems": {
        "program_not_opening": {
            "keywords": ["program not opening", "software won't start", "application not launching", "exe not working", "program crashed", "app won't open", "software crash", "program error"],
            "problem": "Program or software won't open",
            "solution": """💾 **Software Won't Start Fix:**

1. **Basic troubleshooting:**
   • Restart computer
   • Run as administrator (right-click > Run as admin)
   • Check if program is already running in Task Manager
   • Try running in compatibility mode

2. **File integrity:**
   • Reinstall the program
   • Run program's repair/modify option
   • Check for corrupted installation files
   • Download fresh installer from official site

3. **System requirements:**
   • Check if system meets minimum requirements
   • Update Windows to latest version
   • Install required redistributables (Visual C++, .NET)
   • Check available disk space

4. **Conflicts and dependencies:**
   • Disable antivirus temporarily
   • Close other programs
   • Update graphics drivers
   • Check Windows Event Viewer for errors

5. **Advanced fixes:**
   • Run System File Checker: sfc /scannow
   • Check registry for corruption
   • Create new user account to test
   • Boot in Safe Mode and try""",
            "prevention": "Keep software updated, regular system maintenance"
        },
        "browser_issues": {
            "keywords": ["browser slow", "browser crash", "browser not working", "chrome slow", "firefox crash", "edge problems", "browser freeze", "website not loading"],
            "problem": "Web browser problems and performance issues",
            "solution": """🌐 **Browser Issues Fix:**

1. **Basic browser fixes:**
   • Clear browser cache and cookies
   • Disable unnecessary extensions
   • Update browser to latest version
   • Restart browser completely

2. **Performance optimization:**
   • Close unused tabs
   • Clear browsing history
   • Disable hardware acceleration if causing issues
   • Reset browser settings to default

3. **Connection issues:**
   • Check internet connection
   • Flush DNS cache: ipconfig /flushdns
   • Try incognito/private mode
   • Disable VPN/proxy temporarily

4. **Extension problems:**
   • Disable all extensions
   • Enable one by one to find problematic extension
   • Remove suspicious or unused extensions
   • Update remaining extensions

5. **Advanced solutions:**
   • Create new browser profile
   • Reinstall browser completely
   • Check for malware/adware
   • Run browser's built-in cleanup tool""",
            "prevention": "Regular cache clearing, keep extensions minimal, update browser regularly"
        },
        "email_problems": {
            "keywords": ["email not working", "can't send email", "email not receiving", "outlook problems", "gmail issues", "email sync", "email password"],
            "problem": "Email client or service issues",
            "solution": """📧 **Email Problems Fix:**

1. **Basic email troubleshooting:**
   • Check internet connection
   • Verify email settings (SMTP, IMAP, POP3)
   • Check email password and username
   • Try accessing email via web browser

2. **Sending issues:**
   • Check SMTP server settings
   • Verify port numbers (usually 587 or 465)
   • Enable "Less secure app access" if needed
   • Check if email is in outbox/drafts

3. **Receiving issues:**
   • Check spam/junk folder
   • Verify IMAP/POP3 settings
   • Check storage quota
   • Test with different email client

4. **Outlook specific:**
   • Run Outlook in safe mode
   • Repair Outlook data files (.pst/.ost)
   • Create new Outlook profile
   • Update Outlook to latest version

5. **Mobile email issues:**
   • Remove and re-add email account
   • Check mobile data/WiFi connection
   • Update email app
   • Clear email app cache""",
            "prevention": "Keep email clients updated, regular password updates, backup important emails"
        },
        "file_recovery": {
            "keywords": ["deleted files", "recover files", "lost documents", "file recovery", "restore files", "accidental delete", "recycle bin"],
            "problem": "Accidentally deleted or lost files",
            "solution": """📁 **File Recovery Solutions:**

1. **Check Recycle Bin first:**
   • Open Recycle Bin on desktop
   • Look for deleted files
   • Right-click and "Restore" if found
   • Empty Recycle Bin only after confirming

2. **Recent file locations:**
   • Check "Recent" in File Explorer
   • Look in Documents, Downloads, Desktop
   • Check application's recent files list
   • Search by file name or type

3. **Windows File History:**
   • Go to Settings > Update & Security > Backup
   • Click "More options" under File History
   • Browse and restore from backup
   • Check previous versions in file properties

4. **System Restore:**
   • Type "Create a restore point" in Start menu
   • Click "System Restore"
   • Choose restore point before file loss
   • Follow wizard to restore system

5. **Third-party recovery:**
   • Use free tools like Recuva or PhotoRec
   • Stop using computer immediately after deletion
   • Run recovery software as administrator
   • Save recovered files to different drive""",
            "prevention": "Regular backups, enable File History, be careful with delete operations"
        },
        "virus_malware": {
            "keywords": ["virus", "malware", "infected", "suspicious activity", "pop-ups", "slow computer", "unwanted programs"],
            "problem": "Computer infected with virus or malware",
            "solution": """🦠 **Virus/Malware Removal:**

1. **Immediate isolation:**
   • Disconnect from internet
   • Don't enter passwords or personal info
   • Boot in Safe Mode if possible
   • Back up important files to external drive

2. **Scanning and removal:**
   • Run full antivirus scan
   • Use Malwarebytes Anti-Malware
   • Try Windows Defender Offline scan
   • Use multiple scanners for thorough check

3. **Manual cleanup:**
   • Check installed programs for suspicious software
   • Remove unknown browser extensions
   • Check startup programs
   • Clear browser cache and cookies

4. **System restoration:**
   • Use System Restore to previous clean state
   • Reset browser settings to default
   • Change all passwords after cleaning
   • Update all software and OS

5. **Prevention setup:**
   • Install reputable antivirus
   • Enable Windows Defender
   • Keep OS and software updated
   • Avoid suspicious downloads/emails

**Warning signs:**
• Slow performance
• Unexpected pop-ups
• Homepage changes
• Unknown programs installed""",
            "prevention": "Use antivirus, avoid suspicious links, keep software updated"
        },
        "windows_update": {
            "keywords": ["windows update", "update failed", "update stuck", "update error", "windows not updating"],
            "problem": "Windows Update issues",
            "solution": """🔄 **Windows Update Fix:**

1. **Basic troubleshooting:**
   • Restart computer and try again
   • Check internet connection
   • Free up disk space (need 10+ GB)
   • Run Windows Update Troubleshooter

2. **Reset Windows Update:**
   • Stop Windows Update service
   • Clear update cache folder
   • Restart Windows Update service
   • Use Windows Update Reset tool

3. **Manual methods:**
   • Download updates manually from Microsoft
   • Use Windows Update Catalog
   • Install updates one by one
   • Try updating in Safe Mode

4. **Advanced fixes:**
   • Run DISM tool: DISM /Online /Cleanup-Image /RestoreHealth
   • Use System File Checker: sfc /scannow
   • Reset Windows Update components
   • Check Windows Update log files

5. **Last resort:**
   • Use Windows Update Assistant
   • Perform in-place upgrade
   • Consider clean Windows installation
   • Contact Microsoft Support

**Common error codes:**
• 0x80070002: Files missing
• 0x8024402F: Connection issues
• 0x80240034: Update service problems""",
            "prevention": "Regular updates, maintain free disk space, stable internet"
        }
    },
    "mobile_problems": {
        "phone_slow": {
            "keywords": ["phone slow", "mobile slow", "android slow", "iphone slow", "smartphone laggy", "tablet slow"],
            "problem": "Mobile phone running slowly",
            "solution": """📱 **Speed Up Mobile Phone:**

1. **Immediate fixes:**
   • Restart phone
   • Close background apps
   • Clear recent apps
   • Check available storage

2. **Storage cleanup:**
   • Delete unused apps
   • Clear app cache and data
   • Move photos/videos to cloud
   • Delete old downloads and files

3. **App management:**
   • Update all apps
   • Uninstall unused apps
   • Disable bloatware
   • Limit background app refresh

4. **System optimization:**
   • Update operating system
   • Restart phone regularly
   • Disable visual effects/animations
   • Use lite versions of apps

5. **Hardware considerations:**
   • Check if phone is overheating
   • Consider factory reset as last resort
   • May need newer phone if very old
   • Check battery health""",
            "prevention": "Regular restarts, keep storage free, update apps"
        },
        "battery_drain": {
            "keywords": ["battery drain", "battery dies fast", "phone battery", "battery life", "charging issues", "won't charge", "charging slow"],
            "problem": "Mobile phone battery draining quickly",
            "solution": """🔋 **Fix Battery Drain:**

1. **Check battery usage:**
   • Go to Settings > Battery
   • Identify apps using most battery
   • Close or uninstall battery-hungry apps
   • Check screen time usage

2. **Optimize settings:**
   • Reduce screen brightness
   • Use dark mode if available
   • Turn off location services for unnecessary apps
   • Disable push notifications

3. **Connectivity management:**
   • Turn off WiFi/Bluetooth when not needed
   • Use airplane mode in low signal areas
   • Disable mobile data for unused apps
   • Turn off mobile hotspot

4. **App optimization:**
   • Close background apps
   • Disable auto-sync for apps
   • Use battery saver mode
   • Update all apps

5. **Hardware checks:**
   • Check charging cable and adapter
   • Clean charging port
   • Consider battery replacement if old
   • Avoid extreme temperatures""",
            "prevention": "Optimize settings, regular charging habits, avoid overheating"
        },
        "app_crashes": {
            "keywords": ["app crash", "app not working", "app keeps closing", "app freeze", "app error", "mobile app problem"],
            "problem": "Mobile apps crashing or not working properly",
            "solution": """📱 **Fix App Crashes:**

1. **Basic app fixes:**
   • Force close and restart app
   • Restart your phone
   • Check if app needs update
   • Clear app cache and data

2. **Storage and memory:**
   • Free up storage space
   • Close other running apps
   • Check available RAM
   • Move apps to SD card if possible

3. **App-specific solutions:**
   • Uninstall and reinstall app
   • Check app permissions
   • Log out and log back in
   • Check app's official support

4. **System-level fixes:**
   • Update operating system
   • Check for system app updates
   • Reset app preferences
   • Boot in safe mode to test

5. **Network-related:**
   • Check internet connection
   • Switch between WiFi and mobile data
   • Clear network settings
   • Disable VPN if using""",
            "prevention": "Keep apps updated, maintain free storage, regular phone restarts"
        }
    },
    "gaming_problems": {
        "game_lag": {
            "keywords": ["game lag", "fps drop", "game slow", "gaming performance", "game stuttering", "low fps"],
            "problem": "Gaming performance issues and lag",
            "solution": """🎮 **Fix Gaming Lag:**

1. **Graphics settings:**
   • Lower game graphics quality
   • Reduce resolution if needed
   • Disable unnecessary visual effects
   • Update graphics drivers

2. **System optimization:**
   • Close unnecessary programs
   • Disable background apps
   • Set game to high priority in Task Manager
   • Use Game Mode in Windows

3. **Hardware checks:**
   • Monitor CPU and GPU temperatures
   • Check available RAM
   • Ensure adequate power supply
   • Clean dust from computer fans

4. **Network optimization:**
   • Use wired connection instead of WiFi
   • Close bandwidth-heavy applications
   • Check ping and internet speed
   • Consider gaming VPN for better routing

5. **Advanced tweaks:**
   • Disable Windows updates during gaming
   • Adjust power settings to high performance
   • Update DirectX and Visual C++ redistributables
   • Consider hardware upgrades if needed""",
            "prevention": "Regular driver updates, maintain clean system, monitor temperatures"
        },
        "game_crashes": {
            "keywords": ["game crash", "game won't start", "game freezes", "game error", "steam problems", "epic games issues"],
            "problem": "Games crashing or failing to start",
            "solution": """🎮 **Fix Game Crashes:**

1. **Basic troubleshooting:**
   • Restart game and launcher
   • Run game as administrator
   • Verify game files integrity
   • Update game to latest version

2. **System requirements:**
   • Check minimum system requirements
   • Update graphics drivers
   • Install latest DirectX and Visual C++
   • Check available disk space

3. **Compatibility fixes:**
   • Run in compatibility mode
   • Disable fullscreen optimizations
   • Try windowed mode
   • Disable overlays (Steam, Discord, etc.)

4. **Hardware-related:**
   • Check for overheating
   • Test RAM with memory diagnostic
   • Monitor power supply stability
   • Reduce overclocking if any

5. **Software conflicts:**
   • Disable antivirus temporarily
   • Close RGB software and utilities
   • Update Windows to latest version
   • Clean boot to eliminate conflicts""",
            "prevention": "Keep drivers updated, maintain system health, avoid overclocking"
        }
    },
    "audio_video_problems": {
        "no_sound": {
            "keywords": ["no sound", "audio not working", "speakers not working", "microphone not working", "sound issues"],
            "problem": "Audio/sound not working properly",
            "solution": """🔊 **Fix Audio Problems:**

1. **Basic audio checks:**
   • Check volume levels and mute status
   • Test different audio sources
   • Try different speakers/headphones
   • Check audio cable connections

2. **Windows audio settings:**
   • Right-click sound icon > Open Sound settings
   • Check output device selection
   • Run Windows audio troubleshooter
   • Update audio drivers

3. **Device Manager fixes:**
   • Open Device Manager
   • Expand "Sound, video and game controllers"
   • Update or reinstall audio drivers
   • Check for disabled devices

4. **Advanced solutions:**
   • Restart Windows Audio service
   • Reset audio settings to default
   • Check for Windows updates
   • Disable audio enhancements

5. **Hardware troubleshooting:**
   • Test with different audio devices
   • Check for loose connections
   • Try different audio ports
   • Consider audio hardware failure""",
            "prevention": "Keep drivers updated, handle audio equipment carefully"
        },
        "video_playback": {
            "keywords": ["video not playing", "video lag", "video stuttering", "media player issues", "youtube problems"],
            "problem": "Video playback issues and media problems",
            "solution": """🎥 **Fix Video Playback:**

1. **Basic video fixes:**
   • Try different media player
   • Update current media player
   • Check video file isn't corrupted
   • Restart computer

2. **Codec and format issues:**
   • Install codec pack (K-Lite recommended)
   • Try converting video to different format
   • Use VLC player (plays most formats)
   • Check if video format is supported

3. **Performance optimization:**
   • Close other programs
   • Lower video quality/resolution
   • Update graphics drivers
   • Check available RAM and CPU usage

4. **Browser video issues:**
   • Clear browser cache
   • Disable browser extensions
   • Try different browser
   • Enable hardware acceleration

5. **Network streaming:**
   • Check internet connection speed
   • Try lower quality stream
   • Pause and let video buffer
   • Use wired connection if possible""",
            "prevention": "Keep media players updated, maintain good internet connection"
        }
    }
}

def get_technical_solution(message, language="english"):
    """Get technical solution based on the message"""
    message_lower = message.lower()
    
    # First check for vague problems that need clarification
    vague_problem_responses = {
        'printer problem': {
            'problem': 'Printer Issue - Need More Details',
            'solution': """I'd be happy to help with your printer problem! To give you the best solution, could you please tell me more specifically:

🖨️ **What exactly is happening?**
• Is the printer not turning on?
• Is it showing as offline?
• Are there paper jams?
• Is the print quality poor (faded, streaky, blurry)?
• Are there error messages? If so, what do they say?
• Is it not printing at all, or printing incorrectly?

Once you provide more details, I can give you step-by-step troubleshooting instructions!""",
            'prevention': 'Regular maintenance and proper paper loading can prevent most printer issues.',
            'confidence': 0.9
        },
        'computer problem': {
            'problem': 'Computer Issue - Need More Details',
            'solution': """I'm here to help with your computer problem! To provide the best solution, please tell me:

💻 **What specific issue are you experiencing?**
• Won't turn on or start up?
• Running very slowly?
• Freezing or crashing?
• Blue screen errors?
• Specific error messages?
• Software not working properly?
• Hardware issues (keyboard, mouse, screen)?

The more details you provide, the better I can help you fix it!""",
            'prevention': 'Regular updates, antivirus scans, and proper shutdown can prevent many computer issues.',
            'confidence': 0.9
        },
        'wifi problem': {
            'problem': 'WiFi/Internet Issue - Need More Details',
            'solution': """I can help you with your WiFi problem! Please let me know:

📶 **What exactly is the issue?**
• Can't connect to WiFi at all?
• Connected but no internet access?
• Very slow internet speed?
• Keeps disconnecting?
• Can't find your network?
• Wrong password errors?
• Specific to EVSU campus WiFi?

With more details, I can provide targeted troubleshooting steps!""",
            'prevention': 'Keep WiFi drivers updated and restart your router periodically for optimal performance.',
            'confidence': 0.9
        }
    }
    
    # Check for vague problems first
    for vague_key, response in vague_problem_responses.items():
        if vague_key in message_lower:
            return response
    
    # Then check for specific technical problems
    for category, problems in TECHNICAL_PROBLEMS.items():
        for problem_key, problem_data in problems.items():
            # Check if any keyword matches
            if any(keyword in message_lower for keyword in problem_data['keywords']):
                return {
                    'problem': problem_data['problem'],
                    'solution': problem_data['solution'],
                    'prevention': problem_data['prevention'],
                    'confidence': 0.8
                }
    
    return None

def get_adaptive_response(user_message, conversation_history=None):
    """
    Generate adaptive responses based on user patterns and history
    """
    # Check for technical problems first
    tech_solution = get_technical_solution(user_message)
    if tech_solution:
        return tech_solution
    
    # Default response for non-technical queries
    return None
