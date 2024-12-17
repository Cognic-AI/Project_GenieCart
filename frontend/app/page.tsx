import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-md text-center">
        <h1 className="text-3xl font-bold mb-6 text-gray-800">
          Welcome to Customer Management App
        </h1>
        
        <p className="text-gray-600 mb-8">
          Get started by creating an account or signing in to access your profile.
        </p>
        
        <div className="flex justify-center space-x-4">
          <Link 
            href="/auth/signup" 
            className="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 transition duration-300"
          >
            Sign Up
          </Link>
          
          <Link 
            href="/auth/signin" 
            className="bg-green-500 text-white px-6 py-2 rounded-md hover:bg-green-600 transition duration-300"
          >
            Sign In
          </Link>
        </div>
      </div>
    </div>
  )
}