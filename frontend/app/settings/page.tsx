'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Avatar } from "@/components/ui/avatar"
import {updatePriceLevel,updateName,updatePic, fetchProfile, updateKey, updateLocation} from '../api/firestore.js';
import { KeyIcon, MapPinIcon } from 'lucide-react'
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

export default function SettingsPage() {
  const [isEditing, setIsEditing] = useState(false)
  const [tempUserName, setTempUserName] = useState("")
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [secret, setSecretKey] = useState('');
  const [location, setLocation] = useState(null);
   const [showMap, setShowMap] = useState(false);
  const [showPopup, setShowPopup] = useState(false); // To control popup visibility
  const [showPriceSuccessPopup, setShowPriceSuccessPopup] = useState(false); // For price success popup
  const [newAvatarLink, setNewAvatarLink] = useState("https://lindamood.net/wp-content/uploads/2019/09/Blank-profile-image.jpg"); // For the input link
  const [user_,setUser] = useState({
    customer_id:"",
    customer_name: '',
    email: '',
    image:'',
    generated_key:'',
    country:'',
    price_level:'Low',
    latitude:'',
    longitude:'',
  });

  const MapPicker = dynamic(() => import("../components/MapPicker"), {
    ssr: false, // Disable server-side rendering for this component
  });

  const handleMap = (loc) => {
    //open the map and let user to select the location
    //get location data 
    setLocation(loc);
    setUser((prev)=>{
      return {...prev,latitude:loc.lat,longitude:loc.lng};
    });
    handleLocationSaving(loc.lat,loc.lng);
    setShowMap(false);
  };

  const handleLocationSaving = async (lat,lng) => {
    try {
      await updateLocation(sessionStorage.getItem('uid'),lat,lng);
      // Handle successful response (e.g., show success message or update state)
        console.log('Location saved successfully.');

    } catch (error) {
    console.error('Error saving location:', error.message);
    // Optionally, you could show the error to the user in the UI as well
    }
  };


  const handleClosePopup = () => {
    setShowPopup(false); // Hide the popup
  };

  const handleClosePriceSuccessPopup = () => {
    setShowPriceSuccessPopup(false);
  };

  const handleAvatarChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files[0]) {
      user_.image = URL.createObjectURL(files[0]);
    }
  };

  const handleEditClick = () => {
    setIsEditingProfile(true);
  };

  const handleSubmitClick = () => {
    setUser((prev)=>{
      return {...prev,image:newAvatarLink};
    });
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
        setShowPriceSuccessPopup(true); // Show success popup
        setTimeout(() => {
          setShowPriceSuccessPopup(false);
        }, 3000); // Hide after 3 seconds
    } catch (error) {
      if (error instanceof Error) {
        console.error('Error saving price level:', error.message);
      } else {
        console.error('Error saving price level:', error);
      }
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
    setUser((prev)=>{
      return {...prev,customer_name:tempUserName};
    });
    try {
      await updateName(sessionStorage.getItem('uid'),user_.customer_name);
      // Handle successful response (e.g., show success message or update state)
        console.log('Name saved successfully.');
        handleEditToggle();
    } catch (error) {
      if (error instanceof Error) {
        console.error('Error saving name:', error.message);
      } else {
        console.error('Error saving name:', error);
      }
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
      if (error instanceof Error) {
        console.error('Error saving pic:', error.message);
      } else {
        console.error('Error saving pic:', error);
      }
      // Optionally, you could show the error to the user in the UI as well
    }
  };
  const handleLoadingProfile = async () => {
    try {
      const profile = await fetchProfile("customer",sessionStorage.getItem("uid"));
      if (profile) {
        setUser({
          customer_id: sessionStorage.getItem("uid") || "",
          customer_name: profile.name, // Access the 'name' property from the fetched profile
          email: profile.email || "", // Handle undefined fields gracefully
          image: profile.image_link || "",
          price_level: profile.price_level || "",
          generated_key: profile.generated_key || "",
          country: profile.country || "",
          latitude:profile.latitude || "",
          longitude:profile.longitude || "",
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
    <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* Left Column (Price Preference, User Name, Profile Picture) */}
      <div className="space-y-6">
        {/* User Price Preference */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold" style={{color:"#5479f7"}}>Price Preference</h3>
          <RadioGroup value={user_.price_level} className="space-y-3">
            <div className="flex items-center space-x-3">
              <RadioGroupItem value="Low" id="Low" className='text-blue-500 border-blue-500 checked:bg-blue-500 checked:border-blue-500' onClick={() => {setUser((prevUser) => ({
                ...prevUser, 
                price_level: "Low",
              }));}}/>
              <Label htmlFor="Low" className="cursor-pointer">
                Low range prices
              </Label>
            </div>
            <div className="flex items-center space-x-3">
              <RadioGroupItem value="Middle" id="Middle" className='text-blue-500 border-blue-500 checked:bg-blue-500 checked:border-blue-500' onClick={() => {setUser((prevUser) => ({
                ...prevUser,
                price_level: "Middle",
              }));}}/>
              <Label htmlFor="Middle" className="cursor-pointer">
                Middle range prices
              </Label>
            </div>
            <div className="flex items-center space-x-3">
              <RadioGroupItem value="High" id="High" className='text-blue-500 border-blue-500 checked:bg-blue-500 checked:border-blue-500' onClick={() => {setUser((prevUser) => ({
                ...prevUser, 
                price_level: "High",
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
          <h3 className="text-lg font-semibold" style={{color:"#5479f7"}}>User Name</h3>
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
              <img src={user_.image || 'https://lindamood.net/wp-content/uploads/2019/09/Blank-profile-image.jpg'} alt="Profile" className="w-full h-20 object-cover mb-4" />  
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
        </div>
      </div>

      {/* Right Column (Secret Key) */}
      <div className="space-y-2">
        <h3 className="text-lg font-semibold" style={{ color: "#5479f7" }}>Secret Key</h3>
        <Button variant="outline" className="flex items-center gap-2" style={{color:"#5479f7"}} onClick={handleGenerateKey}>
          <KeyIcon className="h-5 w-5" />
          Generate New Secret Key
        </Button>
        <h3 className="text-lg font-semibold" style={{ color: "#5479f7" }}>Location</h3>
        {location ? `Lat:${location.lat}, Lng:${location.lng}` : ''}
        <Button variant="outline" className="flex items-center gap-2" style={{color:"#5479f7"}} onClick={()=>{
          setShowMap(true);
        }}>
          <MapPinIcon className="h-5 w-5" />
          Change Location
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
            <MapPicker onLocationSelect={handleMap} 
            initial={
              [user_.latitude!=""?Number(user_.latitude):7.019290329461014, user_.longitude!=""?Number(user_.longitude):80.09548187255861]
              }/>
          </div>
        </div>
      ):<></>}
    </div>
  )
}
