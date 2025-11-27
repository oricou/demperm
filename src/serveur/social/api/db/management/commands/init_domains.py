"""
Django management command to initialize the 9 fixed political domains.
"""
from django.core.management.base import BaseCommand
from db.entities.domain_entity import Domain


class Command(BaseCommand):
    help = 'Initialize the 9 fixed political domains'
    
    # The 9 fixed domains as specified
    DOMAINS = [
        {
            'domain_name': 'Culture',
            'description': 'Discussions sur la culture locale, événements culturels, patrimoine',
            'icon_url': None,
        },
        {
            'domain_name': 'Sport',
            'description': 'Discussions sur le sport local, infrastructures sportives, événements',
            'icon_url': None,
        },
        {
            'domain_name': 'Environnement',
            'description': 'Discussions sur l\'environnement, écologie, développement durable',
            'icon_url': None,
        },
        {
            'domain_name': 'Transports',
            'description': 'Discussions sur les transports publics, mobilité, infrastructures',
            'icon_url': None,
        },
        {
            'domain_name': 'Sécurité',
            'description': 'Discussions sur la sécurité publique, prévention, police municipale',
            'icon_url': None,
        },
        {
            'domain_name': 'Santé',
            'description': 'Discussions sur la santé publique, hôpitaux, services de santé',
            'icon_url': None,
        },
        {
            'domain_name': 'Emploi',
            'description': 'Discussions sur l\'emploi local, formation, développement économique',
            'icon_url': None,
        },
        {
            'domain_name': 'Éducation',
            'description': 'Discussions sur l\'éducation, écoles, formation, jeunesse',
            'icon_url': None,
        },
        {
            'domain_name': 'Numérique',
            'description': 'Discussions sur le numérique, innovation, smart city, connectivité',
            'icon_url': None,
        },
    ]
    
    def handle(self, *args, **options):
        """Execute the command."""
        self.stdout.write(self.style.SUCCESS('Initializing political domains...'))
        
        created_count = 0
        existing_count = 0
        
        for domain_data in self.DOMAINS:
            domain_name = domain_data['domain_name']
            
            # Check if domain already exists
            if Domain.objects.filter(domain_name=domain_name).exists():
                self.stdout.write(
                    self.style.WARNING(f'Domain "{domain_name}" already exists, skipping...')
                )
                existing_count += 1
                continue
            
            # Create the domain
            Domain.objects.create(**domain_data)
            self.stdout.write(
                self.style.SUCCESS(f'Created domain: {domain_name}')
            )
            created_count += 1
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS(f'Domains created: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'Domains already existing: {existing_count}'))
        self.stdout.write(self.style.SUCCESS(f'Total domains: {Domain.objects.count()}'))
        self.stdout.write(self.style.SUCCESS('='*50))

