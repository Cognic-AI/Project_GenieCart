import { NextResponse } from 'next/server';
import { connection } from '../../../database/db'

export async function POST(req: Request) {
  const { key } = await req.json();
  const [rows]: any = await connection.query(
    'SELECT customer_name,email,generated_key,image,country,price_level FROM customer WHERE customer_id = ?',
    [key]
  );
  return NextResponse.json(rows);
}