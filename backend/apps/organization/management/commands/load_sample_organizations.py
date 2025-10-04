import os
import json

from django.core.management.base import BaseCommand
from django.conf import settings

from organization.models import Organization


class Command(BaseCommand):
    help = 'Load sample organization data using Django models'

    def handle(self, *args, **options):
        # Path to JSON file
        json_file_path = os.path.join(settings.BASE_DIR, 'sample_data', 'organizations.json')

        if not os.path.exists(json_file_path):
            self.stdout.write(
                self.style.ERROR(f'JSON file not found: {json_file_path}')
            )
            return

        # Read JSON file
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                organizations_data = json.load(file)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error reading JSON file: {str(e)}')
            )
            return

        success_count = 0
        exists_count = 0
        error_count = 0

        self.stdout.write(f'Loading {len(organizations_data)} organizations...')

        # Create organizations using Django model
        for org_data in organizations_data:
            try:
                # Convert string date to date object
                from datetime import datetime
                if isinstance(org_data['founding_date'], str):
                    org_data['founding_date'] = datetime.strptime(
                        org_data['founding_date'], '%Y-%m-%d'
                    ).date()

                # Use get_or_create to avoid duplicates
                org, created = Organization.objects.get_or_create(
                    name=org_data["name"],
                    defaults={
                        'org_type': org_data["org_type"],
                        'nation': org_data["nation"],
                        'founding_date': org_data["founding_date"],
                        'headcount': org_data["headcount"],
                    }
                )

                if created:
                    success_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created: {org_data["name"]}')
                    )
                else:
                    exists_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Already exists: {org_data["name"]}')
                    )

            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'✗ Error creating {org_data["name"]}: {str(e)}')
                )

        # Summary
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write('Summary:')
        self.stdout.write(f'✓ Successfully created: {success_count}')
        if exists_count > 0:
            self.stdout.write(f'⚠ Already existed: {exists_count}')
        if error_count > 0:
            self.stdout.write(f'✗ Errors: {error_count}')
        self.stdout.write(f'Total processed: {len(organizations_data)}')

        if success_count > 0:
            self.stdout.write(
                self.style.SUCCESS('\nSample data loaded successfully!')
            )
        elif exists_count > 0 and error_count == 0:
            self.stdout.write(
                self.style.SUCCESS('\nAll organizations already exist - database is ready!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('No organizations were processed successfully.')
            )
