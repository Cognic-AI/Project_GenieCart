'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { COUNTRIES } from '../../../../lib/countries';
import CountrySelector from '../../../components/selector';
import { SelectMenuOption } from '@/lib/types';
import { signUp } from "../../../api/auth.js";
import { createAccount } from "../../../api/firestore.js";
import dynamic from 'next/dynamic';

function generateKey(length: number = 12): string {
  const numbers = '0123456789';
  const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  const allChars = numbers + letters;
  
  // Ensure we start with at least one letter and one number
  let key = letters.charAt(Math.floor(Math.random() * letters.length)) +
            numbers.charAt(Math.floor(Math.random() * numbers.length));
  
  // Fill the rest with random characters
  for (let i = key.length; i < length; i++) {
    key += allChars.charAt(Math.floor(Math.random() * allChars.length));
  }
  
  return key;
}

export default function SignUpPage(): React.JSX.Element {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [name, setName] = useState<string>('');
  const [location, setLocation] = useState(null);
   const [error, setError] = useState<string>('');
   const [showMap, setShowMap] = useState(false);
   const [generatedKey, setGeneratedKey] = useState(""); // To store the key for the popup
  const [showPopup, setShowPopup] = useState(false); // To control popup visibility
  const router = useRouter();

  const [isOpen, setIsOpen] = useState(false);
  // Default this to a country's code to preselect it
  const [country, setCountry] = useState('AF');


  // const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
  //   e.preventDefault();
  //   setError('');

  //   try {
  //     const response = await fetch('/api/auth/signup', {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json',
  //       },
  //       body: JSON.stringify({ email, password, name, country }),
  //     });

  //     const data = await response.json();

  //     if (response.ok) {
  //       router.push('/auth/signin');
  //     } else {
  //       setError(data.error || 'Signup failed');
  //     }
  //   } catch (err) {
  //     console.log(err);
  //     setError('An error occurred during signup');
  //   }
  // };

  // const sendEmail = async (email,generated_key,name)=>{
  //     // alert(JSON.stringify(submittedData));
  //     try {      
  //         // Create the request body
  //         const body = {
  //           email:email,
  //           name:name, 
  //           generated_key:generated_key,
  //         };
      
  //         // Make the POST request
  //         const response = await fetch("http://localhost:8000/api/sendSecret", {
  //           method: "POST",
  //           headers: {
  //             "Content-Type": "application/json",
  //           },
  //           body: JSON.stringify(body),
  //         });
      
  //         // Handle the response
  //         if (response.ok) {
  //           const data = await response.json();
  //           console.log(`Response: ${JSON.stringify(data)}`);
  //         } else {
  //           const error = await response.json();
  //           console.log(`Error: ${JSON.stringify(error)}`);
  //         }
  //       } catch (err) {
  //         console.log(`Error: ${err.message}`);
  //       }
    
  // };

  const MapPicker = dynamic(() => import("../../../components/MapPicker"), {
    ssr: false, // Disable server-side rendering for this component
  });
  

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');

    try {
      if(location==null){
        const err = "Location should be selected"
        console.log(err);
        setError(err);
        return;
      }
      const user = await signUp(email,password);
      const key  = generateKey();
      setGeneratedKey(key); // Store the key in state

      await createAccount("customer",{
        name:name,
        email:email,
        id:user.uid,
        country:country,
        generated_key:key,
        price_level:"LOW",
        image:"",
        latitude:location.lat,
        longitude:location.lng
      });
      // await sendEmail(email,key,name);
      //Instead of sending mail, just showing one time secretkey 
      // Show the popup with the key, and after closing it my manual close btn, popup will dissapear
      setShowPopup(true);
      console.log("User signed up:", user);

    } catch (err) {
      console.log(err);
      setError('An error occurred during signup');
    }
  };

  const handleClosePopup = () => {
    setShowPopup(false); // Hide the popup
      router.push('/auth/signin');
  };

  const handleMap = (loc) => {
    //open the map and let user to select the location
    //get location data 
    setLocation(loc);
    setShowMap(false);
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
    >Sign Up
        </h2>
        
        {error && (
          <div className="bg-red-500 text-white p-3 rounded-md text-center text-sm">
            {error}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="mt-8 space-y-6">
          <div>
            <label htmlFor="name" className="block text-sm font-medium" style={{ color: '#5479f7' }}>
              Name
            </label>
            <input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-cyan-500 focus:border-cyan-500 sm:text-sm"
              style={{ color: '#5479f7', borderColor: '#101D6B', borderWidth: 3, backgroundColor: 'white' }}
            />
          </div>
          
          <div>
            <label htmlFor="email" className="block text-sm font-medium" style={{ color: '#5479f7' }}>
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-cyan-500 focus:border-cyan-500 sm:text-sm"
              style={{ color: '#5479f7', borderColor: '#101D6B', borderWidth: 3, backgroundColor: 'white' }}
            />
          </div>
          
          <div>
            <label htmlFor="password" className="block text-sm font-medium" style={{ color: '#5479f7' }}>
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="mt-1 block w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-cyan-500 focus:border-cyan-500 sm:text-sm"
              style={{ color: '#5479f7', borderColor: '#101D6B', borderWidth: 3, backgroundColor: 'white' }}
            />
          </div>

          <div>
          <CountrySelector
              id={'countries'}
              open={isOpen}
              onToggle={() => setIsOpen(!isOpen)}
              onChange={val => setCountry(val)}
              // We use this type assertion because we are always sure this find will return a value but need to let TS know since it could technically return null
              selectedValue={COUNTRIES.find(option => option.value === country) as SelectMenuOption} 
            />
          </div>
          <div className='w-full'>
          {location ? `Lat:${location.lat}, Lng:${location.lng}` : ''}
          
        </div>
          <button
            type="button"
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cyan-500 transition duration-150 ease-in-out"
            style={{ backgroundColor: '#5479f7', color:'white', fontWeight:'bold', fontSize:20}}
            onClick={() => setShowMap(true)}
          >
            Set the location
          </button>
          
          <button
            type="submit"
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cyan-500 transition duration-150 ease-in-out"
            style={{ backgroundColor: '#5479f7', color:'white', fontWeight:'bold', fontSize:20}}
          >
            Sign Up
          </button>
        </form>
        
        <div className="text-center">
          <Link
            href="/auth/signin"
            className="font-medium hover:text-cyan-300 transition duration-150 ease-in-out"
            style={{ color: '#5479f7', textDecoration: 'none', fontSize: '0.9rem' }}
          >
            Already have an account? Sign In
          </Link>
        </div>
      </div>
      {/* Popup */}
      {showPopup?(
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white p-6 rounded shadow-lg">
            <h2 className="text-lg font-bold mb-4">Your Secret Key</h2>
            <p className="mb-4">
              Please save this key securely. It will only be shown once.
            </p>
            <p className="mb-6 p-2 bg-gray-200 rounded">{generatedKey}</p>
            <button
              onClick={handleClosePopup}
              className="px-4 py-2 bg-blue-500 text-white rounded"
            >
              Close
            </button>
          </div>
        </div>
      ):<></>}
      {showMap? (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0,0,0,0.5)',
          }}
        >
          <div
            style={{
              position: 'absolute',
              top: '0',
              left: '0',
              right: '0',
              bottom: '0',
              transform: 'none',
              backgroundColor: 'white',
              padding: '20px',
              borderRadius: '0', /* Remove border radius for full-screen effect */
              zIndex: '1000', /* Ensures it's on top of other elements */
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'center',
              alignItems: 'center',
              overflow: 'hidden', /* Prevents overflow in the modal */

            }}
          >
            <MapPicker onLocationSelect={handleMap} />
          </div>
        </div>
      ):<></>}
    </div>
  );
}

