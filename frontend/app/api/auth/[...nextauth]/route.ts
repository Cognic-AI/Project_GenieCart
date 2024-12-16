import NextAuth from "next-auth/next";
import CredentialsProvider from "next-auth/providers/credentials";
import mysql from "mysql2/promise"; // MySQL import
import bcrypt from "bcrypt";

// Set up MySQL connection
const connection = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

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

        // Query user from MySQL
        const [rows] = await connection.query(
          'SELECT * FROM customers WHERE email = ?',
          [credentials.email]
        );

        if (rows.length === 0) return null;

        const user = rows[0];

        // Check if password matches
        const passwordMatch = await bcrypt.compare(credentials.password, user.password);
        if (!passwordMatch) return null;

        // Return user data if password matches
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
    if (session.user) {
      session.user.id = token.id as string;
      session.user.name = token.name as string;
    }
    return session;
  }

  },
  pages: {
    signIn: '/auth/signin' // Define the sign-in page
  }
});

export { handler as GET, handler as POST };
