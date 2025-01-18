'use client';

import { useState, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
} from "@/components/ui/drawer";
import { Settings } from 'lucide-react';
import Link from 'next/link';
import { Header } from '../components/header';
import { signOut } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import PurchasesPage from '../components/purchases-display';
import {fetchProfile, fetchHistory} from '../api/firestore.js';
 
export default function ProfilePage() {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const [purchases, setPurchases] = useState([]);
  const [user_, setUser] = useState({
    customer_id:"",
    customer_name: '',
    email: '',
    image:'',
    price_level:'',
    generated_key:'',
    country:''
  });


  // const handleLoadingPurchases = async () => {
  //   try {
  //     const response = await fetch('/api/profile/history', {
  //       method: 'POST',
  //       headers: { 'Content-Type': 'application/json' },
  //       body: JSON.stringify({ key: user?.id }),
  //     });

  //     if (!response.ok) {
  //       throw new Error('Failed to fetch purchases');
  //     }

  //     const data = await response.json();

  //     // Ensure the response is an array
  //     if (Array.isArray(data)) {
  //       setPurchases(data as []);
  //     } else {
  //       console.error('Unexpected response structure:', data, data.type);
  //       setPurchases([]);
  //     }
  //     console.log('API Response:', data); // Log the response to confirm its structure
  //   } catch (error) {
  //     console.error('Error fetching purchases:', error);
  //   }
  // };

  // const handleLoadingProfile = async () => {
  //   try {
  //     const response = await fetch('/api/profile/profile', {
  //       method: 'POST',
  //       headers: { 'Content-Type': 'application/json' },
  //       body: JSON.stringify({ key: user?.id }),
  //     });

  //     if (!response.ok) {
  //       throw new Error('Failed to fetch purchases');
  //     }

  //     const data = await response.json();

  //     if (Array.isArray(data)) {
  //       setUser((data)[0]);
  //     } else {
  //       console.error('Unexpected response structure:', data, data.type);
  //     }
  //     console.log('API Response:', data); // Log the response to confirm its structure
  //   } catch (error) {
  //     console.error('Error fetching purchases:', error);
  //   }
  // };

  const handleLoadingProfile = async () => {
    try {
      const profile = await fetchProfile("customer",sessionStorage.getItem("uid"));
      if (profile) {
        setUser({
          customer_id: sessionStorage.getItem("uid"),
          customer_name: profile.name, // Access the 'name' property from the fetched profile
          email: profile.email || "", // Handle undefined fields gracefully
          image: profile.image || "",
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
  const handleLoadingPurchases = async () => {
    try {
      
      const res = await fetchHistory(sessionStorage.getItem('uid'));

      if (Array.isArray(res)) {
        setPurchases(res as []);
      } else {
        console.error('Unexpected response structure:', res);
        setPurchases([]);
      }
      console.log('API Response:', res); // Log the response to confirm its structure
    } catch (error) {
      console.error('Error fetching purchases:', error);
    }
  };

  useEffect(() => {
    if (sessionStorage.getItem('uid')) {
      handleLoadingPurchases();
      handleLoadingProfile();
    }
  }, [sessionStorage.getItem('uid')]);

  
  if (!sessionStorage.getItem('uid')) return <div>Not authenticated</div>;

  const handleSignOut = async () => {
    try {
      sessionStorage.removeItem('uid');
      await signOut({ 
        callbackUrl: '/',
        redirect: true
      });
    } catch (error) {
      console.error('Error signing out:', error);
      router.replace('/');
    }
  };

  const showPurchases = () => {
    if (purchases.length === 0) {
      return <div>No suggestions found</div>;
    }
    return PurchasesPage(purchases);
  };
  
  return (
    <div className="min-h-screen flex flex-col bg-gray-100 w-full">
      <Header onProfileClick={() => setIsOpen(true)} />
      <main className="flex-grow flex items-center justify-center">
        <div className="p-4 flex flex-col items-center justify-center">
          <div className="flex flex-col items-center justify-center">  
            {showPurchases()}
          </div>
        </div>
      </main>
      <Drawer open={isOpen} onOpenChange={setIsOpen}>
        <DrawerContent  className="w-[300px] sm:w-[400px]">
          <DrawerHeader className="text-left">
            <DrawerTitle color='#5479f7'>User Profile</DrawerTitle>
          </DrawerHeader>
          <div className="px-4 py-2 flex flex-col items-center">
          <img style={{borderRadius:30}} src={user_.image||"https://m.media-amazon.com/images/M/MV5BOGQ5YWFjYjItODE5OC00ZDQxLTk5ZmYtNzY0YzM4NjIyMWFlXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg"} alt={user_.customer_name} className="w-full h-40 object-cover mb-4" />   
          <div className="space-y-4 w-full">
              <div>
                <h3 className="font-medium" style={{color:"#5479f7"}}>Name</h3>
                <p className="text-sm text-gray-500">{user_.customer_name}</p>
              </div>
              <div>
                <h3 className="font-medium" style={{color:"#5479f7"}}>Email</h3>
                <p className="text-sm text-gray-500">{user_.email}</p>
              </div>
              <div>
                <h3 className="font-medium" style={{color:"#5479f7"}}>Country</h3>
                <p className="text-sm text-gray-500">{user_.country}</p>
              </div>
            </div>
          </div>
          <div className="px-4 py-2">
            <nav className="space-y-2" style={{color:"#5479f7"}}>
              <Link href="/settings" className="flex items-center gap-2 p-2 rounded-md hover:bg-gray-100">
                <Settings className="h-5 w-5" />
                <span>Settings</span>
              </Link>
            </nav>
          </div>
          <DrawerFooter>
            <Button variant="destructive" className="w-full" onClick={handleSignOut} style={{backgroundColor:"#5479f7",color:'white'}}>Sign Out</Button>
            <DrawerClose asChild>
              <Button variant="outline">Close</Button>
            </DrawerClose>
          </DrawerFooter>
        </DrawerContent>
      </Drawer>
    </div>
  )
}
