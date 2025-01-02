import { NextRequest, NextResponse } from 'next/server';
import { connection } from '../../../database/db';
import bcrypt from 'bcrypt';
import { ResultSetHeader } from 'mysql2';

// Generate a more robust key with letters and numbers
function generateKey(length: number = 12): string {
  const numbers = '0123456789';
  const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  const allChars = numbers + letters;
  
  // Ensure we start with at least one letter and one number
  let key = letters.charAt(Math.floor(Math.random() * letters.length)) +
            numbers.charAt(Math.floor(Math.random() * numbers.length));
  
  // Fill the rest with random characters
  for (let i = key.length; i < length; i++) {
    key += allChars.charAt(Math.floor(Math.random() * allChars.length));
  }
  
  return key;
}

export async function POST(req: NextRequest) {
  const { name, email, password } = await req.json();

  if (!name || !email || !password) {
    return NextResponse.json({ error: 'All fields are required' }, { status: 400 });
  }

  try {
    // Check if the user already exists
    const [existingUser] = await connection.query(
      'SELECT * FROM customer WHERE email = ?',
      [email]
    );

    if (existingUser.length > 0) {
      return NextResponse.json({ error: 'Email already in use' }, { status: 409 });
    }

    // Hash the password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Generate random key
    const generatedKey = generateKey();

    // Insert the new user into the database with the generated key
    const [result] = await connection.query<ResultSetHeader>(
      'INSERT INTO customer (customer_name, email, password, generated_key) VALUES (?, ?, ?, ?)',
      [name, email, hashedPassword, generatedKey]
    );

    if (result.affectedRows > 0) {
      return NextResponse.json({ message: 'User created successfully' }, { status: 201 });
    } else {
      return NextResponse.json({ error: 'Failed to create user' }, { status: 400 });
    }
  } catch (err) {
    console.error(err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}