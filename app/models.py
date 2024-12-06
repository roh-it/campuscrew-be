from werkzeug.security import generate_password_hash, check_password_hash
from .config import Config
from supabase import create_client
import uuid
from datetime import datetime

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

class Users:
    @staticmethod
    def create_user(email, password, first_name, last_name, user_id, is_pfw):
        hashed_password = generate_password_hash(password)
        response = supabase.table("users").insert({
            "email": email,
            "password": hashed_password,
            "first_name": first_name,
            "last_name": last_name,
            "user_id": user_id,
            "is_pfw": is_pfw
        }).execute()
        print(response)
        if not response.data:
            return None, f"Failed to create user: {response.data}"
        return response.data, None

    @staticmethod
    def find_by_email(email):
        response = supabase.table("users").select("*").eq("email", email).execute()
        if not response or len(response.data) == 0:
            return None
        return response.data[0]

    @staticmethod
    def check_password(user, password):
        return check_password_hash(user["password"], password)

class Services:
    @staticmethod
    def create_service(name, description, rate, category_id, user_id):
        service_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        response = supabase.table("services").insert({
            "service_id": service_id,
            "name": name,
            "description": description,
            "rate": rate,
            "user_id": user_id,
            "category_id": category_id,
            "created_at": created_at
        }).execute()

        if not response.data:
            return None, f"Failed to create service: {response.error.message if response.error else 'Unknown error'}"
        return service_id, None

    @staticmethod
    def add_service_images(service_id, image_urls):
        image_records = [{"service_id": service_id, "image_url": url} for url in image_urls]
        response = supabase.table("serviceimages").insert(image_records).execute()

        if not response.data:
            return None, f"Failed to add service images: {response.error.message if response.error else 'Unknown error'}"
        return response.data, None

    @staticmethod
    def add_availability_slots(service_id, availability):
        slot_records = [
            {
                "service_id": service_id,
                "max_hrs": slot["max_hrs"],
                "avail_slots": slot["avail_slots"]
            }
            for slot in availability
        ]
        response = supabase.table("serviceavailability").insert(slot_records).execute()

        if not response.data:
            return None, f"Failed to add service availability: {response.error.message if response.error else 'Unknown error'}"
        return response.data, None
    
    @staticmethod
    def get_all_services():
        try:
            response = supabase.table("services") \
                .select("*, serviceimages(image_url), serviceavailability(max_hrs,avail_slots), users!inner(first_name, last_name, email)") \
                .execute()
            
            if not response.data:
                return [], None
            
            return response.data, None
        except Exception as e:
            return None, f"Error fetching services: {str(e)}"
        

    @staticmethod
    def get_services_by_category(category_id):
        try:
            response = supabase.table("services") \
                .select("*, serviceimages(image_url), serviceavailability(max_hrs, avail_slots), users!inner(first_name, last_name, email)") \
                .eq("category_id", category_id) \
                .execute()
            
            if not response.data:
                return [], None
                
            return response.data, None
        except Exception as e:
            return None, f"Error fetching services by category: {str(e)}"
        
    @staticmethod
    def get_services_by_user(user_id):
        try:
            response = supabase.table("services") \
                .select("*, serviceimages(image_url), serviceavailability(max_hrs,avail_slots), users!inner(first_name, last_name, email)") \
                .eq("user_id", user_id) \
                .execute()
            
            if not response.data:
                return [], None
                
            return response.data, None
        except Exception as e:
            return None, f"Error fetching services by user: {str(e)}"