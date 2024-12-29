import zipfile
import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from app_modules.weather_app.models import City

class Command(BaseCommand):
    help = 'Extract city names from cities15000.zip and save them to the database'

    def add_arguments(self, parser):
        # Define the command-line argument
        parser.add_argument(
            '--extract_dir',
            type=str,
            default='cities15000_data',  # Default extract directory
            help='Directory where the ZIP file will be extracted (defaults to cities15000_data)'
        )

    def handle(self, *args, **kwargs):
        # Get project directory dynamically
        project_dir = settings.BASE_DIR
        
        # Specify the ZIP file name as cities15000.zip
        zip_file_name = 'cities15000.zip'
        zip_file_path = os.path.join(project_dir, zip_file_name)
        
        # The default directory to extract the files
        extract_dir = os.path.join(project_dir, kwargs['extract_dir'])

        # Check if the ZIP file exists
        if not os.path.exists(zip_file_path):
            self.stderr.write(f"Error: ZIP file {zip_file_path} does not exist.")
            return

        # Ensure the extraction directory exists
        if not os.path.exists(extract_dir):
            os.makedirs(extract_dir)

        cities_file = None
        try:
            # Unzip the file
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            self.stdout.write(f"Files extracted to: {extract_dir}")

            # Set the cities file path after extraction
            cities_file = os.path.join(extract_dir, 'cities15000.txt')

            # Process the cities and save them to the database
            self.extract_and_save_city_names(cities_file)

        except zipfile.BadZipFile:
            self.stderr.write(f"Error: The file {zip_file_path} is not a valid ZIP file.")
        except Exception as e:
            self.stderr.write(f"Error: {str(e)}")

    def extract_and_save_city_names(self, cities_file):
        """
        Extracts city names from the cities15000.txt file and saves them to the database.
        """
        try:
            city_objects = []
            with open(cities_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter='\t')

                # Skip the header
                next(reader)

                # Extract city names and prepare for bulk creation
                for row in reader:
                    city_name = row[1]  
                    try:
                        city_name = city_name.split("_","-")[1]
                        print('\033[91m'+'city_name: ' + '\033[92m', city_name)
                    except:
                        pass
                   
                    if not City.objects.filter(name=city_name).exists():
                        city_objects.append(City(name=city_name))

                    # Optionally, print every 100th city processed
                    if len(city_objects) % 100 == 0:
                        self.stdout.write(f"Processed {len(city_objects)} cities")

                # Bulk create cities in the database
                if city_objects:
                    City.objects.bulk_create(city_objects)
                    self.stdout.write(f"Saved {len(city_objects)} cities to the database.")

        except FileNotFoundError:
            self.stderr.write(f"File {cities_file} not found!")
        except Exception as e:
            self.stderr.write(f"Error processing the cities data: {e}")
