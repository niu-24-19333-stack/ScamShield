// ===========================================
// MongoDB Initialization Script
// ===========================================

// Create the scamshield database and user
db = db.getSiblingDB('scamshield');

// Create application user
db.createUser({
  user: 'scamshield_app',
  pwd: 'scamshield_password',
  roles: [
    { role: 'readWrite', db: 'scamshield' }
  ]
});

// Create indexes for better performance
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "created_at": -1 });

db.scans.createIndex({ "user_id": 1 });
db.scans.createIndex({ "created_at": -1 });
db.scans.createIndex({ "is_scam": 1 });

db.threats.createIndex({ "threat_type": 1 });
db.threats.createIndex({ "created_at": -1 });
db.threats.createIndex({ "severity": 1 });

db.sessions.createIndex({ "user_id": 1 });
db.sessions.createIndex({ "expires_at": 1 }, { expireAfterSeconds: 0 });

db.api_keys.createIndex({ "user_id": 1 });
db.api_keys.createIndex({ "key_hash": 1 }, { unique: true });
db.api_keys.createIndex({ "created_at": -1 });

// Create collections with validation
db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["email", "password_hash", "created_at"],
      properties: {
        email: { bsonType: "string" },
        password_hash: { bsonType: "string" },
        full_name: { bsonType: "string" },
        is_active: { bsonType: "bool" },
        is_verified: { bsonType: "bool" },
        created_at: { bsonType: "date" },
        updated_at: { bsonType: "date" }
      }
    }
  }
});

print('MongoDB initialization completed successfully!');
