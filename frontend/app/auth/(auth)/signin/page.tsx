'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { signIn } from "../../../api/auth.js";


export default function SignInPage(): React.JSX.Element {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<string>('');
  const router = useRouter();

  // const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
  //   e.preventDefault();
  //   setError('');

  //   try {
  //     const result = await signIn('credentials', {
  //       redirect: false,
  //       email,
  //       password,
  //     });

  //     if (result?.error) {
  //       setError('Invalid email or password');
  //     } else {
  //       router.push('/profile');
  //     }
  //   } catch (err) {
  //     console.log(err);
  //     setError('An error occurred during login');
  //   }
  // };
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');

    try {
      const uid = await signIn(email,password);
      console.log(uid);
      sessionStorage.setItem(
        'uid',uid
      );
        router.push('/profile');
      
    } catch (err) {
      console.log(err);
      setError('An error occurred during login');
    }
  };
  return (
    <div
  className="flex items-center min-h-screen w-full bg-[url('sign.png')]"
  style={{
    backgroundColor: '#5479f7',
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    justifyContent: 'flex-end', // Aligns the box to the right
  }}
>
  <div
    className="w-full max-w-md p-8 space-y-8 rounded-xl shadow-2xl"
    style={{
      backgroundColor: 'white',
      marginRight: '15%', // Adds spacing from the right edge
    }}
  >
    <h2
      className="mt-6 text-center text-3xl font-extrabold"
      style={{ color: '#5479f7' }}
    >
      Sign In
        </h2>
        {error && (
          <div className="bg-red-500 text-white p-3 rounded-md text-center text-sm">
            {error}
          </div>
        )}
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="email" className="sr-only">
                Email address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="appearance-none rounded-t-md relative block w-full px-3 py-2 border text-gray-200 placeholder-grey-200 rounded-t-md focus:outline-none focus:ring-cyan-500 focus:border-cyan-500 focus:z-10 sm:text-sm"
                style={{ color: '#5479f7', borderColor: '#101D6B', borderWidth:2,backgroundColor:'white' }}
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <label htmlFor="password" className="sr-only">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                className="appearance-none rounded-b-md relative block w-full px-3 py-2 border text-gray-200 placeholder-grey-200 rounded-b-md focus:outline-none focus:ring-cyan-500 focus:border-cyan-500 focus:z-10 sm:text-sm"
                style={{ color: '#5479f7', borderColor: '#101D6B', borderWidth:2 , backgroundColor:'white'}}
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cyan-500 transition duration-150 ease-in-out"
              style={{ backgroundColor: '#5479f7',color:"white" ,fontWeight:'bold', fontSize:20}}
            >
              Sign In
            </button>
          </div>
        </form>
        <div className="text-center">
          <Link
            href="/auth/signup"
            className="font-medium hover:text-cyan-300 transition duration-150 ease-in-out"
            style={{ color: '#5479f7', textDecoration: 'none', fontSize: '0.9rem' }}
          >
            Don&apos;t have an account? Sign Up
          </Link>
        </div>
      </div>
    </div>
  );
}

