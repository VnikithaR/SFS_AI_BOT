// backend/server.js
const express = require('express');
const connectDB = require('./db');  // Import the connectDB function
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const app = express();
const port = 5000;

app.use(express.json());  // Middleware to parse JSON requests

// Connect to MongoDB before starting the server
connectDB().then(db => {
    // Handle user signup
    app.post('/api/signup', async (req, res) => {
        const { username, password } = req.body;
        
        if (!username || !password) {
            return res.status(400).json({ error: 'Username and password are required' });
        }

        try {
            const usersCollection = db.collection('users');  // Access users collection

            // Check if the user already exists
            const existingUser = await usersCollection.findOne({ username });
            if (existingUser) {
                return res.status(400).json({ error: 'User already exists' });
            }

            // Hash the password before saving to the database
            const hashedPassword = await bcrypt.hash(password, 10);

            const newUser = {
                username,
                password: hashedPassword,
            };

            // Insert the new user into the collection
            await usersCollection.insertOne(newUser);

            // Respond with success message
            res.status(201).json({ success: 'User created successfully' });
        } catch (err) {
            console.error('Error signing up user:', err);
            res.status(500).json({ error: 'Server error' });
        }
    });

    // Handle user login
    app.post('/api/login', async (req, res) => {
        const { username, password } = req.body;

        if (!username || !password) {
            return res.status(400).json({ error: 'Username and password are required' });
        }

        try {
            const usersCollection = db.collection('users');  // Access users collection

            // Find user by username
            const user = await usersCollection.findOne({ username });
            if (!user) {
                return res.status(400).json({ error: 'Invalid username or password' });
            }

            // Compare the password with the hashed password in the database
            const isMatch = await bcrypt.compare(password, user.password);
            if (!isMatch) {
                return res.status(400).json({ error: 'Invalid username or password' });
            }

            // Generate JWT token
            const token = jwt.sign({ userId: user._id }, 'your_jwt_secret', { expiresIn: '1h' });

            // Respond with the JWT token
            res.json({ success: 'Login successful', token });
        } catch (err) {
            console.error('Error logging in user:', err);
            res.status(500).json({ error: 'Server error' });
        }
    });

    // Start the server after database connection
    app.listen(port, () => {
        console.log(`Server is running on http://localhost:${port}`);
    });
}).catch(err => {
    console.error('Error connecting to the database:', err);
    process.exit(1);
});
