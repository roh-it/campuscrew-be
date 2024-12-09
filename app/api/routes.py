from flask import Blueprint, request, jsonify
from app.models import Users, Services, Bookings
import uuid
from datetime import datetime

api = Blueprint('api', __name__)

@api.route('/createUser', methods=['POST'])
def create_user():
    data = request.get_json()
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    email = data.get('email')
    password = data.get('password')
    isPfw = data.get("isPfw")
    if not password or not email:
        return jsonify({'error': 'E-Mail and password are required'}), 400
    
    existing_user = Users.find_by_email(email)
    if existing_user:
        return jsonify({'error': 'Email is already in use'}), 400

    user_id = str(uuid.uuid1())
    new_user, error = Users.create_user(email, password, firstName, lastName, user_id, is_pfw= isPfw)
    if error:
        return jsonify({'error': error}), 500

    return jsonify({'message': 'User created successfully', 'user_id': user_id, 'first_name': firstName, 'lastName': lastName, 'email':email, 'isPfw': isPfw}), 201


@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'E-Mail and password are required'}), 400

    user = Users.find_by_email(email)
    
    if user is None:
        return jsonify({'error': 'User not found'}), 400
    
    if user and Users.check_password(user, password):
        return jsonify({'message': 'Login successful', 'user_id': user["user_id"],  'first_name': user["first_name"], 'lastName': user["last_name"], 'email': user["email"],  'is_pfw': user["is_pfw"]}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 400

@api.route("/createService", methods=["POST"])
def create_service():
    try:
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        rate = data.get("rate")
        category_id = data.get("category_id")
        user_id = data.get("user_id")
        image_urls = data.get("image_urls", [])
        availability = data.get("availability", [])  # List of slots with timestamps

        if not all([name, description, rate, category_id, user_id]):
            return jsonify({"error": "Missing required fields"}), 400

        service_id, error = Services.create_service(name, description, rate, category_id, user_id)
        if error:
            return jsonify({"error": error}), 500

        if image_urls:
            images, error = Services.add_service_images(service_id, image_urls)
            if error:
                return jsonify({"error": error}), 500

        if availability:
            for slot in availability:
                if 'max_hrs' not in slot or 'avail_slots' not in slot:
                    return jsonify({"error": "Each availability slot must have 'max_hrs' and 'avail_slots'"}), 400
                if not all(isinstance(ts, str) for ts in slot['avail_slots']):
                    return jsonify({"error": "'avail_slots' must be a list of timestamps in string format"}), 400
                try:
                    for ts in slot['avail_slots']:
                        datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    return jsonify({"error": "Invalid timestamp format in 'avail_slots'. Expected format: YYYY-MM-DD HH:MM:SS"}), 400

            availability_data, error = Services.add_availability_slots(service_id, availability)
            if error:
                return jsonify({"error": error}), 500

        return jsonify({
            "message": "Service created successfully",
            "service_id": service_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api.route("/fetchService", methods=["GET"])
def get_services():
    try:
        category_id = request.args.get('category_id')
        user_id = request.args.get('user_id')
        if category_id:
            services, error = Services.get_services_by_category(category_id)
            if error:
                return jsonify({"error": error}), 500
            return jsonify({
                "message": "Services fetched successfully",
                "services": services,
                "filter": "category",
                "category_id": category_id
            }), 200
            
        elif user_id:
            services, error = Services.get_services_by_user(user_id)
            if error:
                return jsonify({"error": error}), 500
            return jsonify({
                "message": "Services fetched successfully",
                "services": services,
                "filter": "user",
                "user_id": user_id
            }), 200
            
        else:
            services, error = Services.get_all_services()
            if error:
                return jsonify({"error": error}), 500
            return jsonify({
                "message": "Services fetched successfully",
                "services": services,
                "filter": "none"
            }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/editService/<service_id>', methods=['PUT'])
def edit_service(service_id):
    try:
        data = request.get_json()
        updates = {}

        if 'name' in data:
            updates['name'] = data['name']
        if 'description' in data:
            updates['description'] = data['description']
        if 'rate' in data:
            updates['rate'] = data['rate']
        if 'category_id' in data:
            updates['category_id'] = data['category_id']

        if not updates:
            return jsonify({"error": "No valid fields to update"}), 400

        response = Services.update_service(service_id, updates)

        if not response.data:
            return jsonify({"error": "Failed to update service"}), 500

        return jsonify({"message": "Service updated successfully", "updated_service": response.data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/editSlot/<availability_id>', methods=['PUT'])
def edit_slot(availability_id):
    try:
        data = request.get_json()
        updates = {}
        if 'avail_slots' in data:
            if not all(isinstance(ts, str) for ts in data['avail_slots']):
                return jsonify({"error": "'avail_slots' must be a list of timestamps in string format"}), 400
            try:
                ts = data['avail_slots']
                datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return jsonify({"error": "Invalid timestamp format in 'avail_slots'. Expected format: YYYY-MM-DD HH:MM:SS"}), 400
            updates['avail_slots'] = data['avail_slots']
        
        if 'max_hrs' in data:
            updates['max_hrs'] = data['max_hrs']

        if not updates:
            return jsonify({"error": "No valid fields to update"}), 400

        response = Services.update_availability(availability_id, updates)

        if not response.data:
            return jsonify({"error": "Failed to update slot"}), 500

        return jsonify({"message": "Slot updated successfully", "updated_slot": response.data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@api.route("/createBooking", methods=["POST"])
def create_booking():
    try:
        data = request.get_json()
        service_id = data.get("service_id")
        user_id = data.get("user_id")
        availability_id = data.get("availability_id")

        if not all([service_id, user_id, availability_id]):
            return jsonify({"error": "Missing required fields"}), 400

        booking, error = Bookings.create_booking(service_id, user_id, availability_id)
        
        if error:
            return jsonify({"error": error}), 400

        return jsonify({
            "message": "Booking created successfully",
            "booking": {
                "booking_id": booking["booking_id"],
                "service_id": booking["service_id"],
                "booked_by": booking["booked_by"],
                "booking_time": booking["booking_time"],
                "availability_id": booking["availability_id"]
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/bookings/<user_id>", methods=["GET"])
def get_user_bookings(user_id):
    try:
        bookings, error = Bookings.get_user_bookings(user_id)
        if error:
            return jsonify({"error": error}), 500

        return jsonify({
            "message": "Bookings fetched successfully",
            "bookings": bookings
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route("/booking/<booking_id>", methods=["GET"])
def get_booking_details(booking_id):
    try:
        booking, error = Bookings.get_booking_details(booking_id)
        if error:
            return jsonify({"error": error}), 500

        return jsonify({
            "message": "Booking fetched successfully",
            "booking": booking
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/deleteSlotTiming/<slot_id>', methods=['DELETE'])
def delete_slot_timing(slot_id):
    try:
        delete_booking_response = Services.delete_booking_with_slot_id(slot_id)
        
        if not delete_booking_response.data:
            return jsonify({"error": "Failed to delete slot bookings"}), 500

        slot_response = Services.delete_slots(slot_id)

        if not slot_response.data:
            return jsonify({"error": "Failed to delete slot timing"}), 500

        return jsonify({"message": "Slot timing and associated bookings deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/deleteBooking/<booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    try:
        # Get the availability_id associated with the booking to mark it as not booked
        booking_response = Services.get_avail_id_of_booking(booking_id)
        
        if not booking_response.data:
            return jsonify({"error": "Booking not found"}), 404
        
        availability_id = booking_response.data['availability_id']

        # Delete the booking
        delete_response = Services.delete_booking_with_booking_id(booking_id)

        if not delete_response.data:
            return jsonify({"error": "Failed to delete booking"}), 500

        # Update availability slot to mark it as not booked
        delete = Services.update_book_status_false(availability_id)

        return jsonify({"message": "Booking deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/deleteService/<service_id>', methods=['DELETE'])
def delete_service(service_id):
    try:
        # Step 1: Check for and delete related bookings
        booking_response = Services.get_bookings_from_service_id(service_id)
        
        if booking_response.data:
            booking_ids = [booking['booking_id'] for booking in booking_response.data]
            delete_bookings_response = Services.delete_multiple_bookings(booking_ids)

            if not delete_bookings_response.data:
                return jsonify({"error": "Failed to delete service bookings"}), 500

        # Step 2: Delete related availability slots
        availability_response = Services.delete_slots_with_service_id(service_id)

        if not availability_response.data:
            return jsonify({"error": "Failed to delete availability slots"}), 500

        # Step 3: Delete related images
        image_response = Services.delete_service_images(service_id)

        if not image_response.data:
            return jsonify({"error": "Failed to delete service images"}), 500

        # Step 4: Delete the service itself
        service_response = Services.delete_service(service_id)

        if not service_response.data:
            return jsonify({"error": "Failed to delete service"}), 500

        return jsonify({"message": "Service, bookings, availability slots, and images deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
