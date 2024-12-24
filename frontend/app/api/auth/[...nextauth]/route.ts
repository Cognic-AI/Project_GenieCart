
import NextAuth from "next-auth/next";
import CredentialsProvider from "next-auth/providers/credentials";
import bcrypt from "bcrypt";
import { connection } from '../../../database/db';
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
          const passwordMatch = await bcrypt.compare(
            credentials.password,
            user.password
          );
          if (!passwordMatch) return null;
          return {
            id: user.customer_id.toString(),
            email: user.email,
            name: user.customer_name,
            generated_key: user.generated_key,
            image: user.image
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
        token.name = user.name;
        token.generated_key = user.generated_key;
        token.image = user.image;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
        session.user.name = token.name as string;
        session.user.generated_key = token.generated_key as string;
        session.user.image = token.image as string;
      }
      return session;
    }
  },
  pages: {
    signIn: '/auth/signin'
  }
});

export { handler as GET, handler as POST };