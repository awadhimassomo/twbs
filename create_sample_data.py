import os
import django
import random
from django.utils.text import slugify
from django.core.files.base import ContentFile

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twebs.settings')
django.setup()

from website.models import (
    SiteSettings, HomePageSection, ServiceCard, ProductCategory, 
    Product, Page, Testimonial
)

def create_site_settings():
    """Create basic site settings"""
    try:
        site_settings = SiteSettings.objects.first()
        if not site_settings:
            print("Creating site settings...")
            site_settings = SiteSettings.objects.create(
                site_title="Twebs Laboratory Equipment",
                site_description="Quality Laboratory Equipment and Scientific Instrumentation in Tanzania",
                phone="+255 123 456 789",
                email="info@twebs.co.tz",
                address="P.O.Box 15968\nUsa River, Arusha\nTanzania",
                facebook_url="https://facebook.com/twebs",
                twitter_url="https://twitter.com/twebs",
                instagram_url="https://instagram.com/twebs",
                linkedin_url="https://linkedin.com/company/twebs",
            )
            print("Site settings created")
        else:
            print("Site settings already exist")
        return site_settings
    except Exception as e:
        print(f"Error creating site settings: {e}")
        return None

def create_home_sections():
    """Create homepage sections"""
    try:
        # Clear existing sections
        if HomePageSection.objects.count() > 0:
            print("Homepage sections already exist")
            return
        
        print("Creating homepage sections...")
        # Hero section
        hero = HomePageSection.objects.create(
            section_type="hero",
            title="Advanced Laboratory Equipment for Precision Research",
            subtitle="Supporting scientific innovation and excellence across Tanzania",
            active=True
        )
        
        # Services section
        services = HomePageSection.objects.create(
            section_type="services",
            title="Our Services",
            subtitle="Comprehensive Laboratory Solutions",
            active=True
        )
        
        # Why us section
        why_us = HomePageSection.objects.create(
            section_type="why_us",
            title="Why Choose Twebs",
            subtitle="Your Trusted Partner in Laboratory Excellence",
            active=True
        )
        
        print("Created homepage sections")
    except Exception as e:
        print(f"Error creating homepage sections: {e}")

def create_service_cards():
    """Create service cards"""
    try:
        # Clear existing cards
        if ServiceCard.objects.count() > 0:
            print("Service cards already exist")
            return
        
        print("Creating service cards...")
        services = [
            {
                "title": "Equipment Supply",
                "description": "We provide a wide range of high-quality laboratory equipment from trusted global manufacturers.",
                "icon_name": "beaker",
                "order": 1
            },
            {
                "title": "Installation & Setup",
                "description": "Our technical team handles professional installation and configuration of all equipment.",
                "icon_name": "tools",
                "order": 2
            },
            {
                "title": "Training & Support",
                "description": "We offer comprehensive training and ongoing technical support for all our products.",
                "icon_name": "education",
                "order": 3
            },
            {
                "title": "Maintenance & Calibration",
                "description": "Regular maintenance and precise calibration services to ensure your equipment performs optimally.",
                "icon_name": "settings",
                "order": 4
            }
        ]
        
        for service in services:
            ServiceCard.objects.create(
                title=service["title"],
                description=service["description"],
                icon_name=service["icon_name"],
                active=True,
                order=service["order"]
            )
        
        print(f"Created {len(services)} service cards")
    except Exception as e:
        print(f"Error creating service cards: {e}")

def create_product_categories():
    """Create product categories"""
    try:
        # Clear existing categories
        if ProductCategory.objects.count() > 0:
            print("Product categories already exist")
            return ProductCategory.objects.all()
        
        print("Creating product categories...")
        categories = [
            {
                "name": "Air Filter Systems",
                "description": "Advanced air filtration systems for laboratory environments",
                "order": 1
            },
            {
                "name": "Mask Evaluation Systems",
                "description": "Equipment for testing and evaluating mask effectiveness",
                "order": 2
            },
            {
                "name": "Dust Sensor Systems",
                "description": "Precision sensors for dust detection and air quality monitoring",
                "order": 3
            },
            {
                "name": "Generators",
                "description": "Reliable power generators for laboratory use",
                "order": 4
            },
            {
                "name": "Air Quality Monitoring",
                "description": "Systems for monitoring and analyzing air quality parameters",
                "order": 5
            }
        ]
        
        created_categories = []
        for i, category in enumerate(categories):
            cat = ProductCategory.objects.create(
                name=category["name"],
                description=category["description"],
                order=category["order"]
            )
            created_categories.append(cat)
        
        print(f"Created {len(categories)} product categories")
        return created_categories
    except Exception as e:
        print(f"Error creating product categories: {e}")
        return []

def create_products(categories):
    """Create sample products"""
    try:
        if Product.objects.count() > 0:
            print("Products already exist")
            return
        
        print("Creating products...")
        
        category_dict = {category.name: category for category in categories}
        
        # Products for each category
        all_products = []
        
        # Air Filter Systems
        air_filter_products = [
            {
                "name": "AIR-1000 Advanced HEPA Filtration System",
                "description": "High-efficiency particulate air (HEPA) filtration system designed for laboratory environments requiring clean air conditions.",
                "features": """
                - 99.97% filtration efficiency for particles as small as 0.3 microns
                - Adjustable airflow settings from 200-800 CFM
                - Low noise operation (<60 dB)
                - Digital control panel with filter life indicator
                - Compact design for space-efficient installation
                """,
                "specifications": """
                Dimensions: 60cm x 50cm x 30cm
                Weight: 25kg
                Power: 110-240V, 50/60Hz
                Filter Types: Pre-filter, HEPA filter, Activated Carbon filter
                Filter Life: Up to 12 months (depending on use)
                Warranty: 2 years
                """
            },
            {
                "name": "AIR-2000 Clean Room Filtration Unit",
                "description": "Comprehensive filtration system for clean room applications in pharmaceutical, medical, and research facilities.",
                "features": """
                - ISO Class 5-8 clean room compatibility
                - Dual-stage HEPA and ULPA filtration
                - Continuous air quality monitoring
                - Automatic contamination detection and alerts
                - Remote monitoring capabilities via network connection
                """,
                "specifications": """
                Dimensions: 120cm x 70cm x 40cm
                Weight: 45kg
                Power: 220-240V, 50/60Hz
                Filter Types: Pre-filter, HEPA filter, ULPA filter
                Filter Life: Up to 24 months (depending on use)
                Warranty: 3 years
                """
            },
            {
                "name": "AIR-3000 Mobile Laboratory Air Purifier",
                "description": "Portable air filtration system for laboratories with changing air quality requirements or multiple zones.",
                "features": """
                - Wheeled design for easy mobility between laboratory spaces
                - Quick setup and operation
                - High-capacity air processing (up to 1000 CFM)
                - Multi-stage filtration including HEPA and chemical filtration
                - Battery backup for uninterrupted operation
                """,
                "specifications": """
                Dimensions: 75cm x 55cm x 35cm
                Weight: 30kg
                Power: 110-240V, 50/60Hz, optional battery operation
                Filter Types: Pre-filter, HEPA filter, Chemical filter
                Filter Life: 6-12 months
                Warranty: 2 years
                """
            }
        ]
        
        # Mask Evaluation Systems
        mask_evaluation_products = [
            {
                "name": "MASK-TEST 1000 Basic Filtration Efficiency Tester",
                "description": "Entry-level mask testing equipment for measuring basic filtration efficiency of face masks and respirators.",
                "features": """
                - Aerosol particle filtration efficiency testing
                - Breathing resistance measurement
                - Standard compliance testing for various mask types
                - User-friendly interface with guided testing procedures
                - Automated test reports generation
                """,
                "specifications": """
                Testing Capability: N95, KN95, surgical masks
                Test Parameters: Filtration efficiency, pressure drop
                Sample Size: Standard mask dimensions
                Power: 220V, 50Hz
                Dimensions: 50cm x 40cm x 30cm
                Weight: 15kg
                """
            },
            {
                "name": "MASK-TEST 2000 Advanced Respirator Testing System",
                "description": "Comprehensive testing system for advanced evaluation of respirator performance including fit testing and material analysis.",
                "features": """
                - Complete respirator evaluation capabilities
                - Simulated breathing patterns for real-world testing
                - Bacterial filtration efficiency testing
                - Mask fit testing capabilities
                - Material integrity and durability testing
                """,
                "specifications": """
                Testing Capability: All respirator types including N95, N99, FFP2, FFP3
                Test Parameters: Filtration efficiency, breathability, fit factor, bacterial filtration
                Sample Size: Various mask types and sizes
                Power: 220V, 50/60Hz
                Dimensions: 80cm x 60cm x 50cm
                Weight: 35kg
                """
            },
            {
                "name": "MASK-TEST 3000 Research-Grade Mask Evaluation Lab",
                "description": "Complete laboratory setup for comprehensive mask research and development, suitable for regulatory compliance testing and certification.",
                "features": """
                - Full-spectrum mask performance evaluation
                - Environmental conditioning capabilities
                - Simulation of various usage conditions
                - Compliance testing for international standards
                - Research and development capabilities for new mask designs
                """,
                "specifications": """
                Testing Capability: All mask types and respiratory protection devices
                Test Parameters: Comprehensive evaluation against all major international standards
                Environmental Control: Temperature, humidity, and airflow control
                Power: 220-240V, 50/60Hz, 3-phase
                Dimensions: 2m x 1.5m x 2m (full system)
                Weight: 120kg
                """
            }
        ]
        
        # Dust Sensor Systems
        dust_sensor_products = [
            {
                "name": "DUST-DETECT 100 Basic Particulate Monitor",
                "description": "Entry-level dust and particulate matter monitoring system for laboratory environments and industrial settings.",
                "features": """
                - Real-time PM2.5 and PM10 monitoring
                - Digital display with color-coded air quality indicators
                - Data logging capabilities
                - USB connectivity for data export
                - Compact wall-mountable design
                """,
                "specifications": """
                Sensor Type: Laser particle counter
                Detection Range: PM1.0, PM2.5, PM10
                Measurement Range: 0-999 μg/m³
                Accuracy: ±10% at 100μg/m³
                Display: 3.5" LCD
                Power: 12V DC adapter or battery operated
                Dimensions: 15cm x 10cm x 5cm
                """
            },
            {
                "name": "DUST-DETECT 200 Advanced Particulate Analysis System",
                "description": "Professional-grade dust monitoring system with advanced analytics and reporting features for research and compliance applications.",
                "features": """
                - High-precision laser diffraction technology
                - Particle size distribution analysis
                - Multiple sensor deployment capability
                - Cloud-based data management and reporting
                - Regulatory compliance reporting templates
                """,
                "specifications": """
                Sensor Type: Advanced laser diffraction
                Detection Range: PM0.5 to PM100
                Size Classification: 8 channels
                Measurement Range: 0-1000 μg/m³
                Accuracy: ±5% across measurement range
                Network: Wi-Fi, Ethernet, optional 4G
                Power: 110-240V AC
                Dimensions: 25cm x 20cm x 15cm
                """
            },
            {
                "name": "DUST-DETECT 300 Environmental Dust Monitoring Station",
                "description": "Comprehensive outdoor and indoor dust monitoring station with weather parameters correlation and long-term environmental assessment capabilities.",
                "features": """
                - Complete environmental monitoring package
                - Weather parameter integration (temp, humidity, pressure, wind)
                - Solar power option for remote deployment
                - GPS location tracking
                - Advanced data analytics and predictive modeling
                """,
                "specifications": """
                Sensor Types: Multiple - optical, gravimetric
                Parameters: PM0.5-PM100, weather conditions
                Environmental Protection: IP66 weatherproof enclosure
                Power: 110-240V AC, solar option available
                Communication: 4G/LTE, Satellite option
                Dimensions: 40cm x 30cm x 20cm (main unit)
                """
            }
        ]
        
        # Generators
        generator_products = [
            {
                "name": "GEN-100 Basic Laboratory Power Generator",
                "description": "Reliable backup power solution for essential laboratory equipment during power outages.",
                "features": """
                - Quick-start capability for emergency backup
                - Pure sine wave output for sensitive equipment
                - Automatic voltage regulation
                - Low noise operation suitable for laboratory environments
                - Compact design for efficient space utilization
                """,
                "specifications": """
                Power Output: 5kVA
                Voltage: 220-240V, 50Hz
                Engine: 4-stroke, air-cooled
                Fuel Type: Unleaded gasoline
                Tank Capacity: 15L
                Runtime: 8 hours at 75% load
                Noise Level: <70dB at 7m
                Dimensions: 70cm x 50cm x 55cm
                Weight: =60kg
                """
            },
            {
                "name": "GEN-200 Advanced Research Laboratory Generator",
                "description": "High-capacity power generation system for medium to large laboratories with critical equipment requirements.",
                "features": """
                - Automatic transfer switch integration
                - Remote monitoring and control capabilities
                - Precision power output for sensitive analytical equipment
                - Parallel operation capability for expanded power needs
                - Comprehensive safety features and alarms
                """,
                "specifications": """
                Power Output: 15kVA
                Voltage: 220-240V, 50/60Hz, single/three phase
                Engine: 4-cylinder, liquid-cooled
                Fuel Type: Diesel
                Tank Capacity: 50L
                Runtime: 12 hours at full load
                Noise Level: <65dB at 7m
                Dimensions: 120cm x 70cm x 90cm
                Weight: 180kg
                """
            },
            {
                "name": "GEN-300 Uninterruptible Laboratory Power System",
                "description": "Integrated power solution combining generator and UPS functionality for zero-downtime laboratory operations.",
                "features": """
                - True uninterrupted power transfer
                - Intelligent load management
                - Power conditioning and stabilization
                - Advanced battery management system
                - Scalable design for growing power requirements
                """,
                "specifications": """
                Power Output: 10kVA generator with 5kVA UPS
                Voltage: 220-240V, 50/60Hz
                Battery Backup: 30 minutes at full load
                Fuel Type: Diesel
                Tank Capacity: 30L
                Runtime: 10 hours at full load (generator)
                Communication: Ethernet, RS-485
                Dimensions: 150cm x 80cm x 100cm (complete system)
                Weight: 250kg
                """
            }
        ]
        
        # Air Quality Monitoring
        air_quality_products = [
            {
                "name": "AQM-100 Basic Air Quality Monitor",
                "description": "Entry-level indoor air quality monitoring system for basic laboratory environments.",
                "features": """
                - Monitors CO2, VOCs, temperature, and humidity
                - Real-time display with simple status indicators
                - Audible alerts for threshold violations
                - USB data export capability
                - Desktop or wall-mountable design
                """,
                "specifications": """
                Parameters: CO2, VOCs, Temperature, Humidity
                CO2 Range: 0-5000ppm
                VOC Detection: Qualitative (Low/Medium/High)
                Temperature Range: 0-50°C
                Humidity Range: 10-90% RH
                Power: USB or battery operated
                Dimensions: 12cm x 8cm x 3cm
                """
            },
            {
                "name": "AQM-200 Professional Multi-Parameter Air Quality System",
                "description": "Comprehensive air quality monitoring system for professional laboratory environments requiring precise atmospheric control.",
                "features": """
                - Multi-parameter monitoring (CO2, CO, O3, NO2, VOCs, PM)
                - Historical data tracking and trend analysis
                - Multiple sensor node capabilities
                - Smartphone app integration
                - Customizable alerts and notifications
                """,
                "specifications": """
                Parameters: CO2, CO, O3, NO2, VOCs, PM1/2.5/10, Temperature, Humidity
                Measurement Ranges: Lab-grade for all parameters
                Accuracy: ±2% of reading for gases, ±5% for PM
                Storage: 1 year of minute-by-minute data
                Connectivity: Wi-Fi, Bluetooth, Ethernet
                Power: 110-240V AC
                Dimensions: 20cm x 15cm x 10cm (main unit)
                """
            },
            {
                "name": "AQM-300 Research-Grade Environmental Monitoring Station",
                "description": "Complete research-grade air quality monitoring system for advanced environmental research and regulatory compliance.",
                "features": """
                - Reference-grade sensors with highest accuracy
                - Complete gas and particulate analysis
                - Full meteorological parameter integration
                - Advanced data analytics platform
                - Regulatory compliance reporting
                """,
                "specifications": """
                Parameters: All criteria pollutants + extensive VOC speciation
                Measurement Methods: EPA equivalent methods
                Data Resolution: 1-minute sampling
                Calibration: Automatic self-calibration routines
                Connectivity: Ethernet, 4G/LTE, optional satellite
                Power: 110-240V AC, optional solar
                Dimensions: 50cm x 40cm x 30cm (analyzer unit)
                """
            }
        ]
        
        # Create all products
        product_categories = {
            "Air Filter Systems": air_filter_products,
            "Mask Evaluation Systems": mask_evaluation_products,
            "Dust Sensor Systems": dust_sensor_products,
            "Generators": generator_products,
            "Air Quality Monitoring": air_quality_products
        }
        
        for category_name, products in product_categories.items():
            category = category_dict.get(category_name)
            if not category:
                print(f"Category {category_name} not found")
                continue
                
            for i, product_data in enumerate(products):
                product = Product.objects.create(
                    category=category,
                    name=product_data["name"],
                    description=product_data["description"],
                    features=product_data["features"],
                    specifications=product_data["specifications"],
                    order=i + 1,
                    active=True
                )
                all_products.append(product)
        
        print(f"Created {len(all_products)} products")
    except Exception as e:
        print(f"Error creating products: {e}")

def create_pages():
    """Create static pages"""
    try:
        if Page.objects.count() > 0:
            print("Pages already exist")
            return
        
        print("Creating pages...")
        
        # About page
        about_page = Page.objects.create(
            title="About Us",
            slug="about",
            content="""
            <h2>Our Story</h2>
            <p>Twebs is a leading supplier of laboratory and scientific instrumentation in Tanzania. Established with a mission to provide high-quality laboratory equipment to research institutions, universities, hospitals, and industries across Tanzania.</p>
            
            <p>Since our founding, we've been committed to delivering superior products, exceptional customer service, and technical expertise to our clients. Our team of specialists understands the unique challenges faced by laboratories in Tanzania and works closely with customers to provide tailored solutions.</p>
            
            <h2>Our Mission</h2>
            <p>To enhance scientific progress in Tanzania by providing reliable, high-quality laboratory equipment and technical support, enabling researchers and professionals to pursue excellence in their work.</p>
            
            <h2>Our Values</h2>
            <ul>
                <li><strong>Quality:</strong> We are committed to providing only the highest quality products that meet international standards.</li>
                <li><strong>Integrity:</strong> We conduct our business with honesty, transparency, and ethical practices.</li>
                <li><strong>Customer Focus:</strong> We prioritize understanding and meeting our customers' needs through personalized service.</li>
                <li><strong>Innovation:</strong> We continuously seek new technologies and solutions to address evolving laboratory needs.</li>
                <li><strong>Local Expertise:</strong> We combine global knowledge with local understanding to provide relevant solutions for Tanzania.</li>
            </ul>
            
            <h2>Our Team</h2>
            <p>Our team consists of experienced professionals with backgrounds in laboratory science, engineering, and customer service. We're dedicated to understanding the specific needs of our clients and providing solutions that help them achieve their research and analytical goals.</p>
            """,
            active=True
        )
        
        # Contact page
        contact_page = Page.objects.create(
            title="Contact Us",
            slug="contact",
            content="""
            <p>We're here to answer any questions you may have about our products and services. Reach out to our team and we'll respond as soon as possible.</p>
            
            <h3>Our Office Hours</h3>
            <p>Monday to Friday: 8:00 AM - 5:00 PM<br>
            Saturday: 9:00 AM - 1:00 PM<br>
            Sunday: Closed</p>
            
            <h3>How to Find Us</h3>
            <p>Our office is located in Usa River, Arusha, Tanzania. Please contact us to schedule a visit to our showroom.</p>
            """,
            active=True
        )
        
        print(f"Created pages")
    except Exception as e:
        print(f"Error creating pages: {e}")

def create_testimonials():
    """Create customer testimonials"""
    try:
        if Testimonial.objects.count() > 0:
            print("Testimonials already exist")
            return
        
        print("Creating testimonials...")
        
        testimonials = [
            {
                "name": "Dr. Sarah Kimani",
                "position": "Research Director",
                "company": "Tanzanian Institute of Medical Research",
                "quote": "Twebs has been instrumental in equipping our new microbiology lab. Their attention to detail and after-sales support have been exceptional. The team's knowledge about laboratory equipment made the procurement process seamless."
            },
            {
                "name": "Prof. John Mbwambo",
                "position": "Head of Chemistry Department",
                "company": "University of Dar es Salaam",
                "quote": "We've been working with Twebs for over three years, and they consistently deliver quality equipment with excellent technical support. Their team understands the unique challenges we face in our research environment."
            },
            {
                "name": "Dr. Alice Mwangi",
                "position": "Laboratory Director",
                "company": "Arusha Medical Research Center",
                "quote": "The quality of equipment and level of service provided by Twebs is outstanding. They don't just sell products - they provide complete solutions tailored to our specific needs."
            }
        ]
        
        for testimonial in testimonials:
            Testimonial.objects.create(
                name=testimonial["name"],
                position=testimonial["position"],
                company=testimonial["company"],
                quote=testimonial["quote"],
                active=True
            )
        
        print(f"Created {len(testimonials)} testimonials")
    except Exception as e:
        print(f"Error creating testimonials: {e}")

if __name__ == "__main__":
    print("Creating sample data for Twebs website...")
    site_settings = create_site_settings()
    create_home_sections()
    create_service_cards()
    categories = create_product_categories()
    create_products(categories)
    create_pages()
    create_testimonials()
    print("\nSample data creation complete! Log in to the admin panel to view and edit content.")
