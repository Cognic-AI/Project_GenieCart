import { NextRequest, NextResponse } from 'next/server';
import { connection } from '../../../database/db';
import bcrypt from 'bcrypt';

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

    if (existingUser && existingUser.length > 0) {
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
