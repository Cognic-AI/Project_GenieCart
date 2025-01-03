import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import AuthProvider from '@/components/AuthProvider'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'GenieCart',
  description: 'Your AI Shopping Assistant',
  icons: {
    icon: '/favicon.ico',
    // Optional: Add additional icon sizes
    // apple: '/apple-icon.png',
    // shortcut: '/favicon-16x16.png',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full">
      <body className={`${inter.className} min-h-screen flex flex-col bg-gray-100`}>
        <AuthProvider>
          <main className="flex-grow flex items-center justify-center">
            {children}
          </main>
        </AuthProvider>
      </body>
    </html>
  )
}

