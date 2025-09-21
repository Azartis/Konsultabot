"""
Management command to populate technical knowledge base
"""
from django.core.management.base import BaseCommand
from chat.models import KnowledgeBase

class Command(BaseCommand):
    help = 'Populate technical knowledge base with IT support information'

    def handle(self, *args, **options):
        tech_knowledge = [
            {
                'question': 'My printer is not working',
                'answer': 'Here are common printer troubleshooting steps:\n1. Check power and connections\n2. Restart the printer\n3. Check for paper jams\n4. Verify ink/toner levels\n5. Update printer drivers\n6. Set printer as default',
                'keywords': 'printer, printing, not working, offline, paper jam',
                'category': 'technical_support',
                'language': 'english',
                'confidence_score': 0.9
            },
            {
                'question': 'WiFi connection problems',
                'answer': 'To fix WiFi issues:\n1. Restart your router\n2. Check WiFi password\n3. Move closer to router\n4. Restart your device WiFi\n5. Forget and reconnect to network\n6. Contact IT if problem persists',
                'keywords': 'wifi, internet, connection, network, slow, disconnected',
                'category': 'technical_support',
                'language': 'english',
                'confidence_score': 0.9
            },
            {
                'question': 'Computer running very slowly',
                'answer': 'To speed up your computer:\n1. Restart your computer\n2. Close unnecessary programs\n3. Check available storage space\n4. Run disk cleanup\n5. Check for malware\n6. Update software and drivers',
                'keywords': 'computer, slow, performance, lag, freeze',
                'category': 'technical_support',
                'language': 'english',
                'confidence_score': 0.9
            },
            {
                'question': 'Email not working',
                'answer': 'Email troubleshooting steps:\n1. Check internet connection\n2. Verify email settings\n3. Check spam/junk folder\n4. Restart email application\n5. Try webmail access\n6. Contact IT for server settings',
                'keywords': 'email, outlook, gmail, send, receive, not working',
                'category': 'technical_support',
                'language': 'english',
                'confidence_score': 0.9
            },
            {
                'question': 'Software installation problems',
                'answer': 'Software installation help:\n1. Run installer as administrator\n2. Check available disk space\n3. Temporarily disable antivirus\n4. Check system requirements\n5. Download fresh installer\n6. Contact IT for corporate software',
                'keywords': 'software, install, installation, program, application, error',
                'category': 'technical_support',
                'language': 'english',
                'confidence_score': 0.9
            }
        ]

        created_count = 0
        for item in tech_knowledge:
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
            self.style.SUCCESS(f'Successfully added {created_count} technical knowledge entries')
        )
