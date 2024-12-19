'use client';

import { useSession, signOut } from 'next-auth/react';
import { useEffect, useState } from 'react';
import { redirect } from 'next/navigation';

export default function ProfilePage() {
  const { data: session, status } = useSession({
    required: true,
    onUnauthenticated() {
      redirect('/auth/signin');
    }
  });

  const [generatedKey, setGeneratedKey] = useState<string | null>(null);

  useEffect(() => {
    if (session?.user?.email) {
      fetch('/api/profile', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: session.user.email }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.generatedKey) {
            setGeneratedKey(data.generatedKey);
          }
        })
        .catch(() => {
          setGeneratedKey('Error retrieving key');
        });
    }
  }, [session?.user?.email]);

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
          <p className="mb-2">
            <strong>Email:</strong> {session?.user?.email}
          </p>
          <p className="mb-4">
            <strong>Generated Key:</strong> {generatedKey || 'Loading...'}
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
