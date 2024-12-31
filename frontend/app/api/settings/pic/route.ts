import { NextResponse } from 'next/server';
import { connection } from '../../../database/db';
export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { uid, pic } = body;

    if (!uid && !pic) {
      return NextResponse.json({ error: 'Uid is required' }, { status: 400 });
    }

    const [rows]: any = await connection.execute(
      'UPDATE customer SET image = ? WHERE customer_id = ?',
      [pic,uid]
    );

    // Ensure response is returned after the database operation
    if (rows.affectedRows > 0) {
      return NextResponse.json({ message: 'Pic updated successfully' }, { status: 200 });
    } else {
      return NextResponse.json({ error: 'No matching customer found' }, { status: 404 });
    }

  } catch (error) {
    console.error('Database error:', error);
    return NextResponse.json({ error: 'Database error' }, { status: 500 });
  }
}