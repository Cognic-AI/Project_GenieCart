'use client'

import { useSession, signOut } from 'next-auth/react';
import { redirect } from 'next/navigation';

export default function ProfilePage() {
  const { data: session, status } = useSession({
    required: true,
    onUnauthenticated() {
      redirect('/auth/signin');
    }
  });

  if (status === 'loading') {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-96">
        <h1 className="text-2xl font-bold mb-4 text-center">User Profile</h1>
        
        <div className="text-center">
          <p className="mb-2">
            <strong>Name:</strong> {session?.user?.name}
          </p>
          <p className="mb-4">
            <strong>Email:</strong> {session?.user?.email}
          </p>
          
          <button 
            onClick={() => signOut({ callbackUrl: '/auth/signin' })}
            className="w-full bg-red-500 text-white py-2 rounded-md hover:bg-red-600"
          >
            Sign Out
          </button>
        </div>
      </div>
    </div>
  );
}