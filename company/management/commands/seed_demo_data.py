from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from company.models import CompanyProfile, Statistic, ChatFAQ
from services.models import Service
from projects.models import Project


SERVICES = [
    ("Engineering Consultancy", "Engineering consultancy for construction and fabrication projects."),
    ("Structural Engineering", "Structural design and engineering solutions in Pokhara, Nepal."),
    ("Building Construction", "Engineering and construction services for buildings."),
    ("Infrastructure Development", "Infrastructure engineering and construction services in Nepal."),
    ("Project Management", "Project management and coordination for engineering and construction work."),
    ("Quantity Surveying & Estimation", "Quantity surveying and cost estimation services."),
    ("Metal Fabrication", "Metal fabrication company in Pokhara, Nepal — structural and custom metal fabrication."),
    ("Steel Fabrication", "Steel fabrication services for construction and industrial projects."),
    ("Custom Metal Works", "Custom metal works fabricated to drawings and specifications."),
    ("Renovation & Retrofitting", "Renovation and retrofitting services for existing structures."),
    ("Maintenance Services", "Maintenance services for buildings and fabricated structures."),
]

STARTER_FAQS = [
    ('What services do you offer?', 'services, service, offer, what do you do, work, सेवा',
     'We offer engineering consultancy, structural engineering, building construction, infrastructure development, '
     'project management, quantity surveying and estimation, metal and steel fabrication, custom metal works, '
     'renovation and retrofitting, and maintenance services.', 'View our services', '/services/'),
    ('Do you do metal fabrication?', 'metal, fabrication, steel, gate, gates, railing, railings, staircase, welding, फलाम',
     'Yes. Metal fabrication is a major part of our work: custom and structural steel fabrication, steel frames, '
     'gates, railings, staircases and industrial fabrication, built to drawings and specifications.',
     'Metal fabrication', '/services/metal-fabrication/'),
    ('How can I get a quote?', 'quote, quotation, price, cost, estimate, rate, मूल्य',
     'You can send us your project details with our quote form and our team will contact you. '
     'For urgent questions, call or message us on WhatsApp.', 'Get a Quote', '/get-a-quote/'),
    ('Where are you located?', 'location, located, address, where, office, map, ठेगाना, कहाँ',
     'Our office is at Pokhara-14, BP Marg, Pokhara, Nepal 33700.', 'Contact us', '/contact-us/'),
    ('How can I contact you?', 'contact, phone, call, number, email, mail, संपर्क',
     'You can call us on 9856082231 or email info.highnoon2019@gmail.com. You can also use the WhatsApp button '
     'or the contact form.', 'Contact page', '/contact-us/'),
    ('Are you hiring?', 'job, jobs, career, careers, hiring, vacancy, work with you, cv, apply, जागिर',
     'Open positions are listed on our Careers page, where you can apply and upload your CV.',
     'See careers', '/careers/'),
    ('Which projects have you done?', 'project, projects, portfolio, previous work, built',
     'You can see a selection of our work on the Projects page.', 'View projects', '/projects/'),
]

DEMO_PROJECTS = [
    ("Demo Residential Building", "residential", "completed", "Pokhara, Nepal"),
    ("Demo Commercial Complex", "commercial", "ongoing", "Pokhara, Nepal"),
    ("Demo Steel Structure Fabrication", "metal_fabrication", "completed", "Pokhara, Nepal"),
    ("Demo Infrastructure Project", "infrastructure", "upcoming", "Kaski, Nepal"),
]


class Command(BaseCommand):
    help = 'Seeds initial CompanyProfile, Statistics, Services and demo (placeholder) Projects.'

    def add_arguments(self, parser):
        parser.add_argument('--with-demo', action='store_true',
                            help='Also create placeholder demo projects (not needed - real projects are added).')

    def handle(self, *args, **options):
        profile, created = CompanyProfile.objects.get_or_create(
            id=1,
            defaults=dict(
                company_name='Highnoon Engineering Solutions Pvt. Ltd.',
                short_name='HES',
            ),
        )
        self.stdout.write(self.style.SUCCESS(
            f"CompanyProfile {'created' if created else 'already exists'}."
        ))

        for order, (title, desc) in enumerate([
            ('Service Categories', str(len(SERVICES))),
            ('Focus Area', 'Metal Fabrication'),
            ('Based In', 'Pokhara, Nepal'),
        ]):
            Statistic.objects.get_or_create(
                title=title, defaults={'value': desc, 'display_order': order}
            )

        # Starter chatbot answers (only facts already on the site). The client should review them in
        # Admin -> Chatbot questions. Created only when the table is empty so deleted ones don't return.
        if not ChatFAQ.objects.exists():
            for order, (q, kw, a, ltxt, lurl) in enumerate(STARTER_FAQS):
                ChatFAQ.objects.create(
                    question=q, keywords=kw, answer=a, link_text=ltxt, link_url=lurl, display_order=order,
                )

        for order, (name, short_desc) in enumerate(SERVICES):
            slug = slugify(name)
            Service.objects.get_or_create(
                slug=slug,
                defaults=dict(
                    name=name,
                    short_description=short_desc,
                    description=short_desc,
                    display_order=order,
                    active=True,
                ),
            )
        self.stdout.write(self.style.SUCCESS(f'Seeded {len(SERVICES)} services.'))

        if options.get('with_demo'):
            for name, category, status, location in DEMO_PROJECTS:
                Project.objects.get_or_create(
                    slug=slugify(name),
                    defaults=dict(
                        name=name, category=category, status=status, location=location,
                        description='This is placeholder/demo project data for development purposes only.',
                        is_demo=True, featured=True,
                    ),
                )
            self.stdout.write(self.style.WARNING('Demo projects created (is_demo=True). Delete before going live.'))

        # The company's own project photos (real, non-demo).
        call_command('add_my_projects')
        self.stdout.write(self.style.SUCCESS('Seed complete.'))
