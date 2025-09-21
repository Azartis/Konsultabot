"""
Management command to add more comprehensive technical knowledge
"""
from django.core.management.base import BaseCommand
from chat.models import KnowledgeBase

class Command(BaseCommand):
    help = 'Add more comprehensive technical knowledge base'

    def handle(self, *args, **options):
        additional_knowledge = [
            # Hardware Problems
            {
                'question': 'Computer won\'t turn on',
                'answer': 'Computer startup troubleshooting:\n1. Check power cable connections\n2. Try different power outlet\n3. For laptops: check battery charge\n4. Hold power button 10 seconds, then try starting\n5. Remove external devices and try again\n6. Check for hardware error beeps/lights\n7. Contact IT support if no response',
                'keywords': 'computer, laptop, won\'t turn on, power, startup, boot, dead',
                'category': 'hardware_support',
                'language': 'english',
                'confidence_score': 0.95
            },
            {
                'question': 'Blue screen of death error',
                'answer': 'Blue Screen (BSOD) troubleshooting:\n1. Note the error code if visible\n2. Restart computer\n3. Boot in safe mode if it happens again\n4. Check for recent hardware/software changes\n5. Run memory diagnostic\n6. Update drivers\n7. Contact IT with error code if persistent',
                'keywords': 'blue screen, BSOD, crash, error, windows, system crash',
                'category': 'hardware_support',
                'language': 'english',
                'confidence_score': 0.95
            },
            
            # Network Problems
            {
                'question': 'Internet is very slow',
                'answer': 'Slow internet troubleshooting:\n1. Run speed test (speedtest.net)\n2. Move closer to router\n3. Disconnect unused devices\n4. Restart router and device\n5. Check for background downloads/updates\n6. Switch to 5GHz band if available\n7. Contact ISP if speeds are much lower than plan',
                'keywords': 'internet, slow, speed, network, bandwidth, lag',
                'category': 'network_support',
                'language': 'english',
                'confidence_score': 0.9
            },
            {
                'question': 'Can\'t connect to WiFi network',
                'answer': 'WiFi connection troubleshooting:\n1. Check WiFi password is correct\n2. Restart WiFi on your device\n3. Forget network and reconnect\n4. Check if network is hidden (enter manually)\n5. Restart router\n6. Check if MAC filtering is enabled\n7. Reset network settings if needed',
                'keywords': 'wifi, can\'t connect, password, network, authentication',
                'category': 'network_support',
                'language': 'english',
                'confidence_score': 0.9
            },
            
            # Printer Specific Issues
            {
                'question': 'Printer paper jam problem',
                'answer': 'Paper jam removal steps:\n1. Turn off printer and unplug it\n2. Open all printer doors and trays\n3. Gently remove visible paper (pull in direction of paper path)\n4. Check for small torn pieces\n5. Close all doors and trays\n6. Plug in and turn on printer\n7. Run a test print',
                'keywords': 'printer, paper jam, stuck paper, feeding problem',
                'category': 'printer_support',
                'language': 'english',
                'confidence_score': 0.95
            },
            {
                'question': 'Poor print quality issues',
                'answer': 'Print quality improvement:\n1. Check ink/toner levels\n2. Run printer head cleaning utility\n3. Print alignment page and adjust if needed\n4. Use correct paper type settings\n5. Replace ink/toner cartridges if low\n6. Clean printer heads manually if needed',
                'keywords': 'print quality, blurry, faded, streaky, poor printing',
                'category': 'printer_support',
                'language': 'english',
                'confidence_score': 0.9
            },
            
            # Software Issues
            {
                'question': 'Program keeps crashing',
                'answer': 'Program crash troubleshooting:\n1. Restart the program\n2. Restart your computer\n3. Run program as administrator\n4. Check for program updates\n5. Reinstall the program\n6. Check system requirements\n7. Contact software support',
                'keywords': 'program, software, crash, application, keeps closing, error',
                'category': 'software_support',
                'language': 'english',
                'confidence_score': 0.9
            },
            
            # Campus Specific
            {
                'question': 'EVSU campus WiFi problems',
                'answer': 'EVSU Campus WiFi troubleshooting:\n1. Connect to "EVSU-Student" network\n2. Use your student credentials to login\n3. Clear browser cache if login page won\'t load\n4. Try different locations on campus\n5. Contact IT Help Desk at Library for assistance\n6. Check if your device is registered',
                'keywords': 'EVSU, campus wifi, student network, login, credentials',
                'category': 'campus_support',
                'language': 'english',
                'confidence_score': 0.95
            },
            {
                'question': 'Computer lab issues',
                'answer': 'Computer Lab troubleshooting:\n1. Try a different computer if available\n2. Check if you\'re logged in with correct credentials\n3. Save work frequently to avoid data loss\n4. Report hardware issues to lab assistant\n5. For software problems, restart the computer\n6. Contact IT if persistent issues',
                'keywords': 'computer lab, lab computer, login, save work, hardware',
                'category': 'campus_support',
                'language': 'english',
                'confidence_score': 0.9
            }
        ]

        created_count = 0
        for item in additional_knowledge:
            knowledge, created = KnowledgeBase.objects.get_or_create(
                question=item['question'],
                defaults=item
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created: {item['question']}")
            else:
                self.stdout.write(f"Already exists: {item['question']}")

        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {created_count} additional technical knowledge entries')
        )
