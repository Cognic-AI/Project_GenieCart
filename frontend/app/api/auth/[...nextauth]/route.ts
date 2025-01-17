
import NextAuth from "next-auth/next";
import CredentialsProvider from "next-auth/providers/credentials";
import { createHash } from 'crypto';
import { connection } from '../../../database/db';

// Function to verify a password
async function verifyPassword(storedPassword: string, inputPassword: string): Promise<boolean> {
  const [salt, storedHash] = storedPassword.split(':');

  // Recompute the hash using the input password and the stored salt
  const inputHash = createHash('sha256')
    .update(inputPassword + salt)
    .digest('hex');

  return storedHash === inputHash;
}


const handler = NextAuth({
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null;
        }
        try {
          const [users] = await connection.query(
            'SELECT * FROM customer WHERE email = ?',
            [credentials.email]
          );
          const user = users[0];
          if (!user) return null;
          const passwordMatch = await verifyPassword(
            user.password,
            credentials.password
          );
          if (!passwordMatch) return null;
          return {
            id: user.customer_id.toString(),
          };
        } catch (error) {
          console.error('Error during authentication:', error);
          return null;
        }
      }
    })
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
      }
      return session;
    }
  },
  pages: {
    signIn: '/auth/signin'
  }
});



export { handler as GET, handler as POST };