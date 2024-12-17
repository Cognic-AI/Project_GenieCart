'use client';

import React, { useState } from 'react';
import { signIn } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function SignInPage(): React.JSX.Element {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<string>('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');

    try {
      const result = await signIn('credentials', {
        redirect: false,
        email,
        password,
      });

      if (result?.error) {
        setError('Invalid email or password');
      } else {
        router.push('/profile');
      }
    } catch (err) {
      setError('An error occurred during login');
    }
  };

  return (
    <div
      className="flex items-center justify-center min-h-screen"
      style={{
        backgroundColor: '#121212',
        color: '#ffffff',
        height: '100vh', // Ensure full viewport height
      }}
    >
      <div
        className="p-6 rounded-lg shadow-lg"
        style={{
          backgroundColor: '#1e1e1e',
          maxWidth: '90%',
          width: '400px', // Responsively adjusts
          boxShadow: '0 4px 10px rgba(0, 0, 0, 0.3)',
        }}
      >
        <h1
          className="text-2xl font-bold mb-6 text-center"
          style={{ color: '#00cec9' }}
        >
          Sign In
        </h1>

        {error && (
          <div
            className="p-3 rounded mb-4"
            style={{
              backgroundColor: '#e74c3c',
              color: '#ffffff',
              textAlign: 'center',
              fontSize: '0.9rem',
            }}
          >
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="email"
              className="block text-sm"
              style={{ color: '#bbbbbb' }}
            >
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full p-3 rounded"
              style={{
                border: '1px solid #444444',
                backgroundColor: '#2a2a2a',
                color: '#ffffff',
              }}
            />
          </div>

          <div>
            <label
              htmlFor="password"
              className="block text-sm"
              style={{ color: '#bbbbbb' }}
            >
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full p-3 rounded"
              style={{
                border: '1px solid #444444',
                backgroundColor: '#2a2a2a',
                color: '#ffffff',
              }}
            />
          </div>

          <button
            type="submit"
            className="w-full p-3 rounded text-lg font-semibold"
            style={{
              backgroundColor: '#00cec9',
              color: '#ffffff',
              border: 'none',
              cursor: 'pointer',
              transition: 'background-color 0.3s',
            }}
            onMouseOver={(e) =>
              (e.currentTarget.style.backgroundColor = '#00b4a6')
            }
            onMouseOut={(e) =>
              (e.currentTarget.style.backgroundColor = '#00cec9')
            }
          >
            Sign In
          </button>
        </form>

        <div className="mt-4 text-center">
          <Link
            href="/auth/signup"
            style={{
              color: '#00cec9',
              textDecoration: 'none',
              fontSize: '0.9rem',
            }}
          >
            Don&apos;t have an account? Sign Up
          </Link>
        </div>
      </div>
    </div>
  );
}
