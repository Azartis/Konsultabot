from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from chat.models import KnowledgeBase, CampusInfo
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Set up Konsultabot with initial data and admin user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--admin-email',
            type=str,
            default='admin@evsu.edu.ph',
            help='Admin email address'
        )
        parser.add_argument(
            '--admin-password',
            type=str,
            default='admin123',
            help='Admin password'
        )

    def handle(self, *args, **options):
        self.stdout.write('Setting up Konsultabot...')
        
        # Create admin user
        admin_email = options['admin_email']
        admin_password = options['admin_password']
        
        if not User.objects.filter(email=admin_email).exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email=admin_email,
                password=admin_password,
                student_id='ADMIN001'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created admin user: {admin_email}')
            )
        else:
            self.stdout.write('Admin user already exists')

        # Populate knowledge base
        knowledge_data = [
            {
                'question': 'What is EVSU?',
                'answer': 'Eastern Visayas State University (EVSU) is a state university in the Philippines with multiple campuses across Eastern Visayas region.',
                'category': 'general',
                'language': 'en'
            },
            {
                'question': 'Unsa ang EVSU?',
                'answer': 'Ang Eastern Visayas State University (EVSU) usa ka state university sa Pilipinas nga adunay daghang campus sa Eastern Visayas region.',
                'category': 'general',
                'language': 'ceb'
            },
            {
                'question': 'Ano an EVSU?',
                'answer': 'An Eastern Visayas State University (EVSU) usa nga state university ha Pilipinas nga may kadamo nga campus ha Eastern Visayas region.',
                'category': 'general',
                'language': 'war'
            },
            {
                'question': 'Where is EVSU Dulag campus located?',
                'answer': 'EVSU Dulag campus is located in Dulag, Leyte, Philippines. It offers various undergraduate and graduate programs.',
                'category': 'campus',
                'language': 'en'
            },
            {
                'question': 'What courses are offered at EVSU Dulag?',
                'answer': 'EVSU Dulag offers programs in Education, Engineering, Agriculture, Business, and other fields. For specific programs, please contact the admissions office.',
                'category': 'academics',
                'language': 'en'
            },
            {
                'question': 'How to enroll at EVSU?',
                'answer': 'To enroll at EVSU, you need to: 1) Submit application form, 2) Pass entrance exam, 3) Submit required documents, 4) Pay enrollment fees.',
                'category': 'enrollment',
                'language': 'en'
            },
            {
                'question': 'What are the library hours?',
                'answer': 'The EVSU library is typically open Monday to Friday, 8:00 AM to 5:00 PM. Hours may vary during holidays and special events.',
                'category': 'facilities',
                'language': 'en'
            },
            {
                'question': 'How to contact EVSU Dulag?',
                'answer': 'You can contact EVSU Dulag through their main office, email, or visit their official website for contact information.',
                'category': 'contact',
                'language': 'en'
            }
        ]

        for kb_data in knowledge_data:
            kb, created = KnowledgeBase.objects.get_or_create(
                question=kb_data['question'],
                defaults=kb_data
            )
            if created:
                self.stdout.write(f'Added: {kb_data["question"]}')

        # Populate campus info
        campus_data = [
            {
                'category': 'facilities',
                'title': 'EVSU Dulag Campus',
                'content': 'Main campus in Dulag, Leyte offering various undergraduate and graduate programs. Located in Dulag, Leyte, Philippines. Contact: Phone: (053) XXX-XXXX, Email: dulag@evsu.edu.ph. Facilities include Library, Computer Labs, Science Labs, Gymnasium, Cafeteria. Programs: Education, Engineering, Agriculture, Business Administration, Information Technology',
                'language': 'english',
                'tags': 'campus, main, dulag, leyte, programs, facilities'
            },
            {
                'category': 'services',
                'title': 'Registrar Office',
                'content': 'Handles student records, enrollment, and academic documents. Located at Administration Building, Ground Floor. Contact: registrar@evsu.edu.ph. Services include Student Records and Transcript Processing.',
                'language': 'english',
                'tags': 'registrar, enrollment, records, transcripts, services'
            },
            {
                'category': 'facilities',
                'title': 'Library',
                'content': 'Academic library with books, journals, and digital resources. Located at Library Building. Contact: library@evsu.edu.ph. Facilities include Reading Areas, Computer Stations, and Study Rooms. Provides Research Support and Study Materials.',
                'language': 'english',
                'tags': 'library, books, research, study, resources'
            }
        ]

        for campus_data_item in campus_data:
            campus, created = CampusInfo.objects.get_or_create(
                title=campus_data_item['title'],
                defaults=campus_data_item
            )
            if created:
                self.stdout.write(f'Added campus info: {campus_data_item["title"]}')

        self.stdout.write(
            self.style.SUCCESS('Successfully set up Konsultabot!')
        )
        self.stdout.write(f'Admin login: {admin_email} / {admin_password}')
        self.stdout.write('Visit http://127.0.0.1:8000/admin/ to access admin panel')
