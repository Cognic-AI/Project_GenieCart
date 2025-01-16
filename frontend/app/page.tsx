"use client"

import Link from 'next/link'
import CollapsibleCard from './components/CollapsibleCard';


export default function Home() {

  return (
    <div
  className="flex items-center min-h-screen w-full bg-[url('back.png')]"
  style={{
    backgroundColor: '#5479f7',
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    justifyContent: 'flex-start', // Aligns the box to the right
  }}
>
  <div
    className="w-full max-w-md p-8 space-y-8 rounded-xl shadow-2xl"
    style={{
      backgroundColor: 'white',
      marginLeft: '15%', // Adds spacing from the right edge
    }}
  >
      <h1
        className="text-3xl font-bold mb-6 text-gray-800"
        style={{ color: '#5479f7' }} 
      >
          Welcome to Customer Management App
        </h1>
        
        <p className="text-gray-600 mb-8">
          Get started by creating an account or signing in to access your profile.
        </p>
        
        <div className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-4">
          <Link 
            href="/auth/signup" 
            className="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 transition duration-300"style={{background:"#5479f7"}}
          >
            Sign Up
          </Link>
          
          <Link 
            href="/auth/signin" 
            className="bg-green-500 text-white px-6 py-2 rounded-md hover:bg-green-600 transition duration-300" style={{background:"#5479f7"}}
          >
            Sign In
          </Link>
        </div>
      </div>
      {/* Collapsible card */}
      <CollapsibleCard />
    </div>
  )
}

