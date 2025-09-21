from django.core.management.base import BaseCommand
from chat.models import KnowledgeBase, CampusInfo

class Command(BaseCommand):
    help = 'Populate knowledge base with initial EVSU Dulag data'

    def handle(self, *args, **options):
        self.stdout.write('Populating knowledge base...')
        
        # Clear existing data
        KnowledgeBase.objects.all().delete()
        CampusInfo.objects.all().delete()
        
        # Knowledge base data
        knowledge_data = [
            # Greetings
            {
                'category': 'greeting',
                'question': 'Hello',
                'answer': "Hello! I'm Konsultabot, your AI assistant for EVSU Dulag campus. I can help with enrollment, academics, facilities, and campus life.",
                'language': 'english',
                'keywords': 'hello,hi,greetings,good morning,good afternoon',
                'confidence_score': 1.0
            },
            {
                'category': 'greeting',
                'question': 'Kumusta',
                'answer': "Kumusta! Ako si Konsultabot, inyong AI assistant sa EVSU Dulag. Makatabang ko sa enrollment, academics, ug campus life.",
                'language': 'bisaya',
                'keywords': 'kumusta,hello,greetings,maayong buntag',
                'confidence_score': 1.0
            },
            {
                'category': 'greeting',
                'question': 'Maupay',
                'answer': "Maupay nga adlaw! Ako si Konsultabot, inyong AI assistant ha EVSU Dulag. Matabang ako ha enrollment, academics, ngan campus life.",
                'language': 'waray',
                'keywords': 'maupay,hello,greetings,maupay nga aga',
                'confidence_score': 1.0
            },
            
            # Enrollment & Admission
            {
                'category': 'enrollment',
                'question': 'How to enroll at EVSU Dulag',
                'answer': "To enroll: 1) Visit Registrar's office 2) Submit Form 138, NSO Birth Certificate, Good Moral Certificate, 2x2 photos 3) Pay fees at Accounting 4) Get class schedule. Enrollment is typically before semester starts.",
                'language': 'english',
                'keywords': 'enrollment,enroll,admission,requirements,how to enroll',
                'confidence_score': 0.95
            },
            {
                'category': 'enrollment',
                'question': 'Enrollment requirements',
                'answer': "Required documents: Form 138 (Report Card), NSO Birth Certificate, Good Moral Certificate from previous school, 2x2 ID photos, Medical Certificate, Certificate of Transfer Credentials (for transferees).",
                'language': 'english',
                'keywords': 'requirements,documents,form 138,birth certificate',
                'confidence_score': 0.9
            },
            
            # Academic Programs
            {
                'category': 'academics',
                'question': 'What courses are offered',
                'answer': "EVSU Dulag offers: Bachelor of Elementary Education (BEED), Bachelor of Secondary Education (BSED), Bachelor of Science in Business Administration (BSBA), Bachelor of Science in Computer Science (BSCS), and other specialized programs.",
                'language': 'english',
                'keywords': 'courses,programs,degrees,beed,bsed,bsba,bscs',
                'confidence_score': 0.95
            },
            {
                'category': 'academics',
                'question': 'Computer Science program',
                'answer': "BSCS program covers programming, software development, database systems, networking, web development, and IT fundamentals. 4-year degree with practicum and thesis requirements.",
                'language': 'english',
                'keywords': 'computer science,bscs,programming,software,IT',
                'confidence_score': 0.9
            },
            
            # Facilities
            {
                'category': 'facilities',
                'question': 'Library services',
                'answer': "Library features: study areas, computer/internet access, book lending, research assistance, printing services, group study rooms. Open during campus hours, extended during exams.",
                'language': 'english',
                'keywords': 'library,books,study,research,computer,internet',
                'confidence_score': 0.9
            },
            {
                'category': 'facilities',
                'question': 'Computer lab',
                'answer': "Computer labs available with internet access, software for programming and office work. Schedule with IT department or use during free periods. Available for student projects.",
                'language': 'english',
                'keywords': 'computer,lab,internet,software,programming,IT',
                'confidence_score': 0.9
            },
        ]
        
        # Campus info data
        campus_data = [
            {
                'category': 'academics',
                'title': 'About EVSU Dulag',
                'content': "Eastern Visayas State University - Dulag Campus is a satellite campus offering quality education in the region.",
                'language': 'english',
                'tags': 'evsu,dulag,campus,university'
            },
            {
                'category': 'academics',
                'title': 'Courses Offered',
                'content': "EVSU Dulag offers various undergraduate programs including Education, Business, and Computer Science.",
                'language': 'english',
                'tags': 'courses,programs,education,business,computer science'
            },
            {
                'category': 'facilities',
                'title': 'Library Services',
                'content': "The campus library provides study areas, computer access, and research materials for students.",
                'language': 'english',
                'tags': 'library,study,research,books'
            },
            {
                'category': 'services',
                'title': 'Registrar Office',
                'content': "The Registrar handles enrollment, grades, transcripts, and academic records.",
                'language': 'english',
                'tags': 'registrar,enrollment,grades,transcripts'
            },
        ]
        
        # Create knowledge base entries
        for data in knowledge_data:
            KnowledgeBase.objects.create(**data)
        
        # Create campus info entries
        for data in campus_data:
            CampusInfo.objects.create(**data)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated {len(knowledge_data)} knowledge base entries and {len(campus_data)} campus info entries'
            )
        )
