import { NextRequest, NextResponse } from 'next/server';
import { connection } from '../../../database/db';
import bcrypt from 'bcrypt';
import type { NextApiRequest, NextApiResponse } from 'next';
import { ResultSetHeader } from 'mysql2';

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

    // Insert the new user into the database
    await connection.query(
      'INSERT INTO customer (customer_name, email, password) VALUES (?, ?, ?)',
      [name, email, hashedPassword]
    );

    return NextResponse.json({ message: 'User created successfully' }, { status: 201 });
  } catch (err) {
    console.error(err);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}



export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    if (req.method === 'POST') {
      const { email, password, name } = req.body;
      const generatedKey = Math.random().toString(36).substr(2, 8); // Generate an 8-character random key
  
      try {
        const [result] = await connection.execute<ResultSetHeader>(
          'INSERT INTO customer (email, password, name, generated_key) VALUES (?, ?, ?, ?)',
          [email, password, name, generatedKey]
        );
  
        if (result.affectedRows > 0) {
          res.status(201).json({ message: 'User created successfully' });
        } else {
          res.status(400).json({ error: 'Failed to create user' });
        }
      } catch (error) {
        res.status(500).json({ error: 'Database error' });
      }
    } else {
      res.status(405).json({ error: 'Method not allowed' });
    }
  }
