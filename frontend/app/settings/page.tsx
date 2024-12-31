'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar"
import { Pencil, Check } from 'lucide-react'

export default function SettingsPage() {
  const [isEditing, setIsEditing] = useState(false)
  const [userName, setUserName] = useState('John Doe')
  const [tempUserName, setTempUserName] = useState(userName)
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [avatarSrc, setAvatarSrc] = useState(""); // Avatar image source
  const [newAvatarLink, setNewAvatarLink] = useState(""); // For the input link

  const handleAvatarChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setAvatarSrc(URL.createObjectURL(file));
    }
  };

  const handleEditClick = () => {
    setIsEditingProfile(true);
  };

  const handleSubmitClick = () => {
    setAvatarSrc(newAvatarLink); // Update avatarSrc with the new link
    setIsEditingProfile(false); // Exit edit mode
  };

  const handleEditToggle = () => {
    if (isEditing) {
      setUserName(tempUserName)
    } else {
      setTempUserName(userName)
    }
    setIsEditing(!isEditing)
  }

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
        <RadioGroup defaultValue="middle" className="space-y-3">
          <div className="flex items-center space-x-3">
            <RadioGroupItem value="low" id="low" className='text-blue-500 border-blue-500 checked:bg-blue-500 checked:border-blue-500'/>
            <Label htmlFor="low" className="cursor-pointer">
              Low range prices
            </Label>
          </div>
          <div className="flex items-center space-x-3">
            <RadioGroupItem value="middle" id="middle" className='text-blue-500 border-blue-500 checked:bg-blue-500 checked:border-blue-500'/>
            <Label htmlFor="middle" className="cursor-pointer">
              Middle range prices
            </Label>
          </div>
          <div className="flex items-center space-x-3">
            <RadioGroupItem value="high" id="high" className='text-blue-500 border-blue-500 checked:bg-blue-500 checked:border-blue-500'/>
            <Label htmlFor="high" className="cursor-pointer">
              High range prices
            </Label>
          </div>
        </RadioGroup>
          </div>

          {/* User Name Change */}
          <div className="space-y-2">
            <h3 className="text-lg font-semibold"  style={{color:"#5479f7"}}>User Name</h3>
            <div className="flex items-center space-x-2">
              {isEditing ? (
                <Input 
                  value={tempUserName} 
                  onChange={(e) => setTempUserName(e.target.value)}
                  className="flex-grow"
                />
              ) : (
                <span className="text-lg">{userName}</span>
              )}
              <Button onClick={handleEditToggle} size="icon"style={{color:"#5479f7", background:'white'}}>
                {isEditing ? <Check className="h-4 w-4"  /> : <Pencil className="h-4 w-4" />}
              </Button>
            </div>
          </div>

          {/* User Profile Change */}
          <div className="space-y-2">
      <h3 className="text-lg font-semibold" style={{ color: "#5479f7" }}>Profile Picture</h3>
      <div className="flex items-center space-x-4">
      <Avatar className="h-24 w-24">
      <img src={avatarSrc || 'https://m.media-amazon.com/images/M/MV5BOGQ5YWFjYjItODE5OC00ZDQxLTk5ZmYtNzY0YzM4NjIyMWFlXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg'} alt="Profile" className="w-full h-40 object-cover mb-4" />  
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
                Submit
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
        </CardContent>
      </Card>
    </div>
    </div>
  )
}

