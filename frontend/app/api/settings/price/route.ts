import { NextResponse } from 'next/server';
import { connection } from '../../../database/db';
export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { uid,price_level } = body;

    if (!uid && !price_level) {
      return NextResponse.json({ error: 'Uid is required' }, { status: 400 });
    }

    const [rows]: any = await connection.execute(
      'UPDATE customer SET price_level = ? WHERE customer_id = ?',
      [price_level,uid]
    );

    // Ensure response is returned after the database operation
    if (rows.affectedRows > 0) {
      return NextResponse.json({ message: 'Price updated successfully' }, { status: 200 });
    } else {
      return NextResponse.json({ error: 'No matching customer found' }, { status: 404 });
    }
  } catch (error) {
    console.error('Database error:', error);
    return NextResponse.json({ error: 'Database error' }, { status: 500 });
  }
}