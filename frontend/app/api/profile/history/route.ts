import { NextResponse } from 'next/server';
import { connection } from '../../../database/db'

export async function POST(req: Request) {
  const { key } = await req.json();
  const [rows]: any = await connection.query(
    'SELECT * FROM history INNER JOIN item ON item.item_id = history.item_id WHERE customer_id = ?',
    [key]
  );
  return NextResponse.json(rows);
}