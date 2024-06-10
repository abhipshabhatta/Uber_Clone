import redis
import pickle

# Create a Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Get all session keys
session_keys = redis_client.keys('session:*')

print("Session Keys:", session_keys)

# Get all session data
all_sessions = {}
for key in session_keys:
    session_data = redis_client.get(key)
    all_sessions[key] = session_data

print("All Sessions:", all_sessions)

# Deserialize session data
deserialized_sessions = {}
for key, session_data in all_sessions.items():
    try:
        deserialized_sessions[key] = pickle.loads(session_data.encode('latin1'))  # Ensure correct encoding
    except (pickle.UnpicklingError, AttributeError, EOFError, ImportError, IndexError) as e:
        print(f"Error deserializing session data for key {key}: {e}")
        deserialized_sessions[key] = None

print("Deserialized Sessions:", deserialized_sessions)
