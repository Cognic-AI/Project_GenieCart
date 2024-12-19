import { NextResponse } from 'next/server';
import { connection } from '../../database/db';
export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { email } = body;

    if (!email) {
      return NextResponse.json({ error: 'Email is required' }, { status: 400 });
    }

    const [rows]: any = await connection.execute(
      'SELECT generated_key FROM customer WHERE email = ?',
      [email]
    );

    if (rows.length > 0) {
      return NextResponse.json({ generatedKey: rows[0].generated_key }, { status: 200 });
    } else {
      return NextResponse.json({ error: 'User not found' }, { status: 404 });
    }
  } catch (error) {
    console.error('Database error:', error);
    return NextResponse.json({ error: 'Database error' }, { status: 500 });
  }
}