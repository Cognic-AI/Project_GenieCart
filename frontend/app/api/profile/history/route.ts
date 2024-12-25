import { NextResponse } from 'next/server';
import { connection } from '../../../database/db'

export async function POST(req: Request) {
  const { key } = await req.json();
  const [rows]: any = await connection.query(
    'SELECT * FROM (search_result INNER JOIN search_item ON search_result.search_id = search_item.search_id) INNER JOIN item ON item.item_id = search_item.item_id WHERE customer_id = ?',
    [key]
  );
  return NextResponse.json(rows);
}