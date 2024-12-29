from django.core.management.base import BaseCommand
from app_modules.weather_app.models import City

class Command(BaseCommand):
    help = 'Add a list of Indian cities into the database'

    def handle(self, *args, **kwargs):
        indian_cities = [
            "Mumbai", "Delhi", "Bangalore", "Kolkata", "Chennai", "Ahmedabad", "Hyderabad", "Pune", 
            "Surat", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", 
            "Pimpri-Chinchwad", "Patna", "Vadodara", "Ghaziabad", "Ludhiana", "Agra", "Madurai", "Nashik", 
            "Faridabad", "Meerut", "Rajkot", "Kochi", "Coimbatore", "Jabalpur", "Howrah", "Chandigarh", 
            "Dhanbad", "Amritsar", "Chennai", "Noida", "Aurangabad", "Mysuru", "Kota", "Gwalior", "Bhubaneswar", 
            "Ranchi", "Solapur", "Dehradun", "Navi Mumbai", "Chittorgarh", "Bikaner", "Ajmer", "Udaipur"
        ]

        added_cities = 0

        # Loop through the cities and add them to the database
        for city_name in indian_cities:
            city, created = City.objects.get_or_create(name=city_name)
            if created:
                added_cities += 1
                self.stdout.write(self.style.SUCCESS(f'Added city: {city_name}'))

        if added_cities > 0:
            self.stdout.write(self.style.SUCCESS(f'Successfully added {added_cities} cities to the database.'))
        else:
            self.stdout.write(self.style.WARNING('No new cities added.'))
