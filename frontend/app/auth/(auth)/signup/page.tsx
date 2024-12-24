'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function SignUpPage(): React.JSX.Element {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [name, setName] = useState<string>('');
  const [error, setError] = useState<string>('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch('/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      });

      const data = await response.json();

      if (response.ok) {
        router.push('/auth/signin');
      } else {
        setError(data.error || 'Signup failed');
      }
    } catch (err) {
      console.log(err);
      setError('An error occurred during signup');
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen w-full" style={{ backgroundColor: '#121212' }}>
      <div className="w-full max-w-md p-8 space-y-8 rounded-xl shadow-2xl" style={{ backgroundColor: '#1e1e1e' }}>
        <h2 className="text-3xl font-extrabold text-center" style={{ color: '#00cec9' }}>
          Sign Up
        </h2>
        
        {error && (
          <div className="bg-red-500 text-white p-3 rounded-md text-center text-sm">
            {error}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="mt-8 space-y-6">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-300">
              Name
            </label>
            <input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 border text-gray-200 rounded-md focus:outline-none focus:ring-cyan-500 focus:border-cyan-500 sm:text-sm"
              style={{ backgroundColor: '#2a2a2a', borderColor: '#444444' }}
            />
          </div>
          
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-300">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 border text-gray-200 rounded-md focus:outline-none focus:ring-cyan-500 focus:border-cyan-500 sm:text-sm"
              style={{ backgroundColor: '#2a2a2a', borderColor: '#444444' }}
            />
          </div>
          
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-300">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 border text-gray-200 rounded-md focus:outline-none focus:ring-cyan-500 focus:border-cyan-500 sm:text-sm"
              style={{ backgroundColor: '#2a2a2a', borderColor: '#444444' }}
            />
          </div>
          
          <button
            type="submit"
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cyan-500 transition duration-150 ease-in-out"
            style={{ backgroundColor: '#00cec9' }}
          >
            Sign Up
          </button>
        </form>
        
        <div className="text-center">
          <Link
            href="/auth/signin"
            className="font-medium hover:text-cyan-300 transition duration-150 ease-in-out"
            style={{ color: '#00cec9', textDecoration: 'none', fontSize: '0.9rem' }}
          >
            Already have an account? Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}

