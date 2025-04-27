// backend/db.js
const { MongoClient } = require('mongodb');

// MongoDB connection string (change if you're not using localhost)
const url = 'mongodb://localhost:27017';  // MongoDB URL (default for local MongoDB)
const dbName = 'sfs_infobot_db';  // Database name

let db;

// Function to connect to MongoDB
async function connectDB() {
    if (db) return db;  // Return the existing connection if already connected

    try {
        const client = new MongoClient(url, { useNewUrlParser: true, useUnifiedTopology: true });
        await client.connect();
        console.log('Connected to MongoDB');
        
        db = client.db(dbName);  // Select the database
        return db;
    } catch (err) {
        console.error('Error connecting to MongoDB:', err);
        process.exit(1);  // Exit the process if connection fails
    }
}

module.exports = connectDB;
