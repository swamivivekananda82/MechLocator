from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from mechanics.models import Mechanic, UserProfile
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Populate database with sample mechanic shops and users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mechanics',
            type=int,
            default=20,
            help='Number of mechanic shops to create (default: 20)'
        )
        parser.add_argument(
            '--users',
            type=int,
            default=5,
            help='Number of sample users to create (default: 5)'
        )

    def handle(self, *args, **options):
        num_mechanics = options['mechanics']
        num_users = options['users']

        self.stdout.write(
            self.style.SUCCESS(f'Creating {num_mechanics} mechanic shops and {num_users} users...')
        )

        # Create sample users
        self.create_sample_users(num_users)

        # Create sample mechanics
        self.create_sample_mechanics(num_mechanics)

        self.stdout.write(
            self.style.SUCCESS('Sample data creation completed successfully!')
        )

    def create_sample_users(self, num_users):
        """Create sample user accounts with profiles."""
        sample_users = [
            {'username': 'john_doe', 'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com'},
            {'username': 'jane_smith', 'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane@example.com'},
            {'username': 'mike_wilson', 'first_name': 'Mike', 'last_name': 'Wilson', 'email': 'mike@example.com'},
            {'username': 'sarah_jones', 'first_name': 'Sarah', 'last_name': 'Jones', 'email': 'sarah@example.com'},
            {'username': 'david_brown', 'first_name': 'David', 'last_name': 'Brown', 'email': 'david@example.com'},
        ]

        for i, user_data in enumerate(sample_users[:num_users]):
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password='password123',
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )
                
                # Create user profile
                UserProfile.objects.create(
                    user=user,
                    phone=f'+1-555-{1000 + i:04d}',
                    address=f'{100 + i} Main Street, City, State {10000 + i}'
                )
                
                self.stdout.write(f'Created user: {user.username}')

    def create_sample_mechanics(self, num_mechanics):
        """Create sample mechanic shops with realistic data."""
        mechanic_data = [
            {
                'name': 'ABC Auto Repair',
                'address': '123 Main Street, Downtown, City, State 12345',
                'contact': '+1-555-0101',
                'working_hours': 'Monday-Friday: 8:00 AM - 6:00 PM\nSaturday: 9:00 AM - 4:00 PM\nSunday: Closed',
                'rating': 4.8
            },
            {
                'name': 'City Auto Service',
                'address': '456 Oak Avenue, Midtown, City, State 12345',
                'contact': '+1-555-0102',
                'working_hours': 'Monday-Friday: 7:30 AM - 7:00 PM\nSaturday: 8:00 AM - 5:00 PM\nSunday: 10:00 AM - 2:00 PM',
                'rating': 4.6
            },
            {
                'name': 'Express Car Care',
                'address': '789 Pine Street, Uptown, City, State 12345',
                'contact': '+1-555-0103',
                'working_hours': 'Monday-Saturday: 8:00 AM - 6:00 PM\nSunday: Closed',
                'rating': 4.4
            },
            {
                'name': 'Pro Auto Solutions',
                'address': '321 Elm Street, Westside, City, State 12345',
                'contact': '+1-555-0104',
                'working_hours': 'Monday-Friday: 8:00 AM - 6:00 PM\nSaturday: 9:00 AM - 3:00 PM\nSunday: Closed',
                'rating': 4.9
            },
            {
                'name': 'Quick Fix Garage',
                'address': '654 Maple Drive, Eastside, City, State 12345',
                'contact': '+1-555-0105',
                'working_hours': 'Monday-Friday: 7:00 AM - 8:00 PM\nSaturday: 8:00 AM - 6:00 PM\nSunday: 9:00 AM - 4:00 PM',
                'rating': 4.3
            },
            {
                'name': 'Reliable Auto Repair',
                'address': '987 Cedar Lane, Northside, City, State 12345',
                'contact': '+1-555-0106',
                'working_hours': 'Monday-Friday: 8:00 AM - 6:00 PM\nSaturday: 9:00 AM - 4:00 PM\nSunday: Closed',
                'rating': 4.7
            },
            {
                'name': 'Speedy Auto Service',
                'address': '147 Birch Road, Southside, City, State 12345',
                'contact': '+1-555-0107',
                'working_hours': 'Monday-Saturday: 7:00 AM - 7:00 PM\nSunday: 10:00 AM - 3:00 PM',
                'rating': 4.5
            },
            {
                'name': 'Trusted Car Care',
                'address': '258 Willow Way, Central, City, State 12345',
                'contact': '+1-555-0108',
                'working_hours': 'Monday-Friday: 8:00 AM - 6:00 PM\nSaturday: 9:00 AM - 4:00 PM\nSunday: Closed',
                'rating': 4.8
            },
            {
                'name': 'VIP Auto Repair',
                'address': '369 Spruce Street, Heights, City, State 12345',
                'contact': '+1-555-0109',
                'working_hours': 'Monday-Friday: 8:00 AM - 7:00 PM\nSaturday: 9:00 AM - 5:00 PM\nSunday: Closed',
                'rating': 4.6
            },
            {
                'name': '24/7 Auto Service',
                'address': '741 Poplar Avenue, Valley, City, State 12345',
                'contact': '+1-555-0110',
                'working_hours': '24/7 Emergency Service Available',
                'rating': 4.2
            },
            {
                'name': 'Classic Car Specialists',
                'address': '852 Ash Street, Historic, City, State 12345',
                'contact': '+1-555-0111',
                'working_hours': 'Monday-Friday: 9:00 AM - 5:00 PM\nSaturday: 10:00 AM - 3:00 PM\nSunday: Closed',
                'rating': 4.9
            },
            {
                'name': 'Hybrid Auto Experts',
                'address': '963 Chestnut Drive, Modern, City, State 12345',
                'contact': '+1-555-0112',
                'working_hours': 'Monday-Friday: 8:00 AM - 6:00 PM\nSaturday: 9:00 AM - 4:00 PM\nSunday: Closed',
                'rating': 4.7
            },
            {
                'name': 'Luxury Auto Service',
                'address': '159 Magnolia Lane, Upscale, City, State 12345',
                'contact': '+1-555-0113',
                'working_hours': 'Monday-Friday: 9:00 AM - 6:00 PM\nSaturday: 10:00 AM - 4:00 PM\nSunday: Closed',
                'rating': 4.8
            },
            {
                'name': 'Budget Auto Repair',
                'address': '357 Sycamore Road, Budget, City, State 12345',
                'contact': '+1-555-0114',
                'working_hours': 'Monday-Friday: 7:00 AM - 6:00 PM\nSaturday: 8:00 AM - 4:00 PM\nSunday: Closed',
                'rating': 4.1
            },
            {
                'name': 'Family Auto Care',
                'address': '486 Acacia Street, Family, City, State 12345',
                'contact': '+1-555-0115',
                'working_hours': 'Monday-Friday: 8:00 AM - 6:00 PM\nSaturday: 9:00 AM - 4:00 PM\nSunday: Closed',
                'rating': 4.6
            },
            {
                'name': 'Mobile Auto Service',
                'address': '597 Juniper Way, Mobile, City, State 12345',
                'contact': '+1-555-0116',
                'working_hours': 'Mobile Service - Call for Appointment',
                'rating': 4.4
            },
            {
                'name': 'Truck & SUV Specialists',
                'address': '618 Cypress Drive, Industrial, City, State 12345',
                'contact': '+1-555-0117',
                'working_hours': 'Monday-Friday: 7:00 AM - 7:00 PM\nSaturday: 8:00 AM - 5:00 PM\nSunday: Closed',
                'rating': 4.5
            },
            {
                'name': 'European Auto Service',
                'address': '739 Redwood Lane, European, City, State 12345',
                'contact': '+1-555-0118',
                'working_hours': 'Monday-Friday: 8:00 AM - 6:00 PM\nSaturday: 9:00 AM - 4:00 PM\nSunday: Closed',
                'rating': 4.8
            },
            {
                'name': 'Asian Auto Repair',
                'address': '864 Sequoia Street, Asian, City, State 12345',
                'contact': '+1-555-0119',
                'working_hours': 'Monday-Friday: 8:00 AM - 6:00 PM\nSaturday: 9:00 AM - 4:00 PM\nSunday: Closed',
                'rating': 4.6
            },
            {
                'name': 'Performance Auto Tuning',
                'address': '975 Fir Avenue, Performance, City, State 12345',
                'contact': '+1-555-0120',
                'working_hours': 'Monday-Friday: 9:00 AM - 6:00 PM\nSaturday: 10:00 AM - 4:00 PM\nSunday: Closed',
                'rating': 4.7
            }
        ]

        # City center coordinates (example: New York City)
        base_lat = 40.7128
        base_lng = -74.0060

        for i, data in enumerate(mechanic_data[:num_mechanics]):
            if not Mechanic.objects.filter(name=data['name']).exists():
                # Generate random coordinates within city area (±0.1 degrees)
                lat = base_lat + (random.uniform(-0.1, 0.1))
                lng = base_lng + (random.uniform(-0.1, 0.1))
                
                # Add some random variation to ratings
                rating = data['rating'] + random.uniform(-0.2, 0.2)
                rating = max(0.0, min(5.0, rating))  # Clamp between 0 and 5
                
                mechanic = Mechanic.objects.create(
                    name=data['name'],
                    latitude=Decimal(str(lat)),
                    longitude=Decimal(str(lng)),
                    address=data['address'],
                    contact=data['contact'],
                    rating=Decimal(str(round(rating, 1))),
                    working_hours=data['working_hours'],
                    is_active=True
                )
                
                self.stdout.write(f'Created mechanic: {mechanic.name} at {mechanic.latitude}, {mechanic.longitude}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {min(num_mechanics, len(mechanic_data))} mechanic shops')
        )
