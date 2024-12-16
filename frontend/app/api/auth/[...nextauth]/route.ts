import NextAuth from "next-auth/next";
import CredentialsProvider from "next-auth/providers/credentials";
import { PrismaClient } from "@prisma/client";
import bcrypt from "bcrypt";

const prisma = new PrismaClient();

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

        const user = await prisma.customer.findUnique({
          where: { email: credentials.email }
        });

        if (!user) return null;

        const passwordMatch = await bcrypt.compare(
          credentials.password, 
          user.password
        );

        if (!passwordMatch) return null;

        return {
          id: user.customer_id.toString(),
          email: user.email,
          name: user.customer_name
        };
      }
    })
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.name = user.name;
      }
      return token;
    },
    async session({ session, token }) {
      session.user.id = token.id as string;
      session.user.name = token.name as string;
      return session;
    }
  },
  pages: {
    signIn: '/auth/signin'
  }
});

export { handler as GET, handler as POST };