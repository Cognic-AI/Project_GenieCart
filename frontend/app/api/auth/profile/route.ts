import type { NextApiRequest, NextApiResponse } from 'next';
import { connection } from '../../../database/db';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    const { email } = req.body;

    try {
      const [rows] = await connection.execute(
        'SELECT generated_key FROM customer WHERE email = ?',
        [email]
      );

      if (rows.length > 0) {
        res.status(200).json({ generatedKey: rows[0].generated_key });
      } else {
        res.status(404).json({ error: 'User not found' });
      }
    } catch (error) {
      res.status(500).json({ error: 'Database error' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
