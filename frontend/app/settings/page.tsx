'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Avatar } from "@/components/ui/avatar"
import {updatePriceLevel,updateName,updatePic, fetchProfile, updateKey} from '../api/firestore.js';
import { KeyIcon } from 'lucide-react'

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

export default function SettingsPage() {
  const [isEditing, setIsEditing] = useState(false)
  const [tempUserName, setTempUserName] = useState("")
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [secret, setSecretKey] = useState('');
  const [showPopup, setShowPopup] = useState(false); // To control popup visibility
  const [newAvatarLink, setNewAvatarLink] = useState("https://m.media-amazon.com/images/M/MV5BOGQ5YWFjYjItODE5OC00ZDQxLTk5ZmYtNzY0YzM4NjIyMWFlXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg"); // For the input link
  const [user_,setUser] = useState({
    customer_id:"",
    customer_name: '',
    email: '',
    image:'',
    generated_key:'',
    country:'',
    price_level:'Low',
  });

  const handleClosePopup = () => {
    setShowPopup(false); // Hide the popup
  };

  const handleAvatarChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      user_.image =  URL.createObjectURL(file)
    }
  };

  const handleEditClick = () => {
    setIsEditingProfile(true);
  };

  const handleSubmitClick = () => {
    user_.image = newAvatarLink; // Update avatarSrc with the new link
    setIsEditingProfile(false); // Exit edit mode
    handlePicSaving();
  };

  const handleEditToggle = () => {
    setIsEditing(!isEditing);
    setTempUserName(user_.customer_name);
  }

  // const handlePriceSaving = async () => {
  //   try {
  //     const response = await fetch('/api/settings/price', {
  //       method: 'POST',
  //       headers: { 'Content-Type': 'application/json' },
  //       body: JSON.stringify({ uid: user?.id,price_level:user_.price_level }),
  //     });

  //     if (!response.ok) {
  //       const errorData = await response.json(); // Parse the response body to get the error
  //       throw new Error(errorData.error || 'An unknown error occurred'); // Use the error message from the body
  //     }

  //     // Handle successful response (e.g., show success message or update state)
  //       console.log('Price level saved successfully.');

  //   } catch (error) {
  //   console.error('Error saving price level:', error.message);
  //   // Optionally, you could show the error to the user in the UI as well
  //   }
  // };

  const handlePriceSaving = async () => {
    try {
        await updatePriceLevel(sessionStorage.getItem('uid'),user_.price_level);

      // Handle successful response (e.g., show success message or update state)
        console.log('Price level saved successfully.');

    } catch (error) {
    console.error('Error saving price level:', error.message);
    // Optionally, you could show the error to the user in the UI as well
    }
  };

  // const handleNameSaving = async () => {
  //   user_.customer_name = tempUserName;
  //   try {
  //     const response = await fetch('/api/settings/name', {
  //       method: 'POST',
  //       headers: { 'Content-Type': 'application/json' },
  //       body: JSON.stringify({ uid: user?.id,name: tempUserName}),
  //     });

  //     if (!response.ok) {
  //       const errorData = await response.json(); // Parse the response body to get the error
  //       throw new Error(errorData.error || 'An unknown error occurred'); // Use the error message from the body
  //     }

  //     // Handle successful response (e.g., show success message or update state)
  //       console.log('Name saved successfully.');
  //       handleEditToggle();

  //   } catch (error) {
  //   console.error('Error saving name:', error.message);
  //   // Optionally, you could show the error to the user in the UI as well
  //   }
  // };

  const handleNameSaving = async () => {
    user_.customer_name = tempUserName;
    try {
      await updateName(sessionStorage.getItem('uid'),user_.customer_name);
      // Handle successful response (e.g., show success message or update state)
        console.log('Name saved successfully.');
        handleEditToggle();

    } catch (error) {
    console.error('Error saving name:', error.message);
    // Optionally, you could show the error to the user in the UI as well
    }
  };

  // const handlePicSaving = async () => {
  //   try {
  //     const response = await fetch('/api/settings/pic', {
  //       method: 'POST',
  //       headers: { 'Content-Type': 'application/json' },
  //       body: JSON.stringify({ uid: user?.id,pic:newAvatarLink }),
  //     });

  //     if (!response.ok) {
  //       const errorData = await response.json(); // Parse the response body to get the error
  //       throw new Error(errorData.error || 'An unknown error occurred'); // Use the error message from the body
  //     }

  //     // Handle successful response (e.g., show success message or update state)
  //       console.log('Pic saved successfully.');

  //   } catch (error) {
  //   console.error('Error saving pic:', error.message);
  //   // Optionally, you could show the error to the user in the UI as well
  //   }
  // };

  const handlePicSaving = async () => {
    try {
      await updatePic(sessionStorage.getItem('uid'),user_.image);
      // Handle successful response (e.g., show success message or update state)
        console.log('Pic saved successfully.');

    } catch (error) {
    console.error('Error saving pic:', error.message);
    // Optionally, you could show the error to the user in the UI as well
    }
  };
  const handleLoadingProfile = async () => {
    try {
      const profile = await fetchProfile("customer",sessionStorage.getItem("uid"));
      if (profile) {
        setUser({
          customer_id: sessionStorage.getItem("uid"),
          customer_name: profile.name, // Access the 'name' property from the fetched profile
          email: profile.email || "", // Handle undefined fields gracefully
          image: profile.image_link || "",
          price_level: profile.price_level || "",
          generated_key: profile.generated_key || "",
          country: profile.country || "",
        });}else{
          console.error("Profile not found!");
        }
    } catch (error) {
      console.error('Error fetching suggestions:', error);
    }
  };

  const handleGenerateKey = async() => {
    
      const secretKey = generateKey();
      setSecretKey(secretKey);
      await updateKey(sessionStorage.getItem('uid'),secretKey);
      setShowPopup(true);
    
  };

  useEffect(() => {
    if (sessionStorage.getItem('uid')) {
      handleLoadingProfile();
    }
  }, []);

  return (
    <div
  className="flex items-center min-h-screen w-full bg-[url('settings.png')]"
  style={{
    backgroundColor: '#5479f7',
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    justifyContent: 'flex-end', // Aligns the box to the right
  }}
>
<div className="container mx-auto p-4 flex justify-end">
  <Card className="max-w-2xl w-full md:w-1/2 lg:w-1/2">
    <CardHeader>
      <CardTitle className="text-2xl" style={{color:"#5479f7", textAlign:'center'}}>User Settings</CardTitle>
    </CardHeader>
    <CardContent className="space-y-6">
      {/* User Price Preference */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold" style={{color:"#5479f7"}}>Price Preference</h3>
        <RadioGroup value={user_.price_level} className="space-y-3">
          <div className="flex items-center space-x-3">
            <RadioGroupItem value="Low" id="Low" className='text-blue-500 border-blue-500 checked:bg-blue-500 checked:border-blue-500' onClick={() => {setUser((prevUser) => ({
                ...prevUser, // Spread the previous state
                price_level: "Low", // Update the price_level
              }));}}/>
            <Label htmlFor="Low" className="cursor-pointer">
              Low range prices
            </Label>
          </div>
          <div className="flex items-center space-x-3">
            <RadioGroupItem value="Middle" id="Middle" className='text-blue-500 border-blue-500 checked:bg-blue-500 checked:border-blue-500'onClick={() => {setUser((prevUser) => ({
                ...prevUser, // Spread the previous state
                price_level: "Middle", // Update the price_level
              }));}}/>
            <Label htmlFor="Middle" className="cursor-pointer">
              Middle range prices
            </Label>
          </div>
          <div className="flex items-center space-x-3">
            <RadioGroupItem value="High" id="High" className='text-blue-500 border-blue-500 checked:bg-blue-500 checked:border-blue-500'onClick={() => {setUser((prevUser) => ({
                ...prevUser, // Spread the previous state
                price_level: "High", // Update the price_level
              }));}}/>
            <Label htmlFor="High" className="cursor-pointer">
              High range prices
            </Label>
          </div>
        </RadioGroup>
        <Button onClick={handlePriceSaving} style={{ color: "white", background: "#5479f7", marginLeft: "10px" }}>
                Save
              </Button>
          </div>

          {/* User Name Change */}
          <div className="space-y-2">
            <h3 className="text-lg font-semibold"  style={{color:"#5479f7"}}>User Name</h3>
            <div className="flex items-center space-x-2">
              {isEditing ? (
                <div className='flex'>
                <Input 
                  value={tempUserName} 
                  onChange={(e) => setTempUserName(e.target.value)}
                />
                <Button onClick={handleNameSaving} style={{ color: "white", background: "#5479f7", marginLeft: "10px" }}>
                Save
              </Button>
                </div>
              ) : (
                <div>
                <span className="text-lg">{user_.customer_name}</span>
                <Button onClick={handleEditToggle} style={{ color: "white", background: "#5479f7", marginLeft: "10px" }}>
                Change
              </Button>
                </div>
              )}
            </div>
          </div>

          {/* User Profile Change */}
          <div className="space-y-2">
      <h3 className="text-lg font-semibold" style={{ color: "#5479f7" }}>Profile Picture</h3>
      <div className="flex items-center space-x-4">
      <Avatar className="h-24 w-24">
      <img src={user_.image || 'https://m.media-amazon.com/images/M/MV5BOGQ5YWFjYjItODE5OC00ZDQxLTk5ZmYtNzY0YzM4NjIyMWFlXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg'} alt="Profile" className="w-full h-40 object-cover mb-4" />  
        </Avatar>
        <div>
          {isEditingProfile ? (
            <div className="flex items-center space-x-2">
              <Input 
                type="text" 
                placeholder="Enter image URL" 
                value={newAvatarLink} 
                onChange={(e) => setNewAvatarLink(e.target.value)} 
                className="border p-2"
              />
              <Button onClick={handleSubmitClick} style={{ color: "white", background: "#5479f7" }}>
                Save
              </Button>
            </div>
          ) : (
            <>
              <Input 
                type="file" 
                accept="image/*" 
                onChange={handleAvatarChange}
                className="hidden"
                id="avatar-upload"
              />
              <Button onClick={handleEditClick} style={{ color: "white", background: "#5479f7", marginLeft: "10px" }}>
                Change
              </Button>
            </>
          )}
        </div>
      </div>
      <h3 className="text-lg font-semibold" style={{ color: "#5479f7" }}>Secret Key</h3>
      <Button variant="outline" className="flex items-center gap-2" style={{color:"#5479f7"}} onClick={handleGenerateKey}>
                <KeyIcon className="h-5 w-5" />
                Generate New Secret Key
            </Button>
    </div>
        </CardContent>
      </Card>
    </div>
    {/* Popup */}
    {showPopup?(
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white p-6 rounded shadow-lg">
            <h2 className="text-lg font-bold mb-4">Your Secret Key</h2>
            <p className="mb-4">
              Please save this key securely. It will only be shown once.
            </p>
            <p className="mb-6 p-2 bg-gray-200 rounded">{secret}</p>
            <button
              onClick={handleClosePopup}
              className="px-4 py-2 bg-blue-500 text-white rounded"
            >
              Close
            </button>
          </div>
        </div>
      ):<></>}
    </div>
  )
}

