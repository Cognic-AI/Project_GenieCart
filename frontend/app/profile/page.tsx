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
import {  Download, MessageCircle, Settings} from 'lucide-react';
import Link from 'next/link';
import { Header } from '../components/header';
import { signOut } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import PurchasesPage from '../components/purchases-display';
import {fetchProfile, fetchHistory, fetchPurchases} from '../api/firestore.js';
 
export default function ProfilePage() {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const [purchaseTab, setPurchaseTab] = useState(false);
  const [purchases, setPurchases] = useState([]);
  const [realPurchases, setRealPurchases] = useState([]);
  const [isLoading,setIsLoading] = useState(true);
  const [user_, setUser] = useState({
    customer_id:"",
    customer_name: '',
    email: '',
    image:'',
    price_level:'',
    generated_key:'',
    country:''
  });

  const handleLoadingProfile = async () => {
    setIsLoading(true);

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
    setIsLoading(false);

  };
  const handleLoadingPurchases = async () => {
    setIsLoading(true);

    try {
      
      const res = await fetchHistory(sessionStorage.getItem('uid'));
      console.log("History recieved");

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
    setIsLoading(false);
  };

  const handleLoadingRealPurchases = async () => {
    setIsLoading(true);
    try {
      
      const res = await fetchPurchases(sessionStorage.getItem('uid'));
      console.log("Purchses recieved");

      if (Array.isArray(res)) {
        setRealPurchases(res as []);
      } else {
        console.error('Unexpected response structure:', res);
        setRealPurchases([]);
      }
      console.log('API Response:', res); // Log the response to confirm its structure
    } catch (error) {
      console.error('Error fetching purchases:', error);
    }
    setIsLoading(false);
  };
  useEffect(() => {
    if (sessionStorage.getItem('uid')) {
      handleLoadingPurchases();
      handleLoadingProfile();
      handleLoadingRealPurchases();
    }
  }, [sessionStorage.getItem('uid')]);

  if(isLoading) return (
    <div className="flex items-center justify-center h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-blue-500 border-solid border-opacity-50"></div>
    </div>
  );
  
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
      return <div className='justiy-center flex flex-col items-center w-full' style={{alignItems:'center'}}>No suggestions found</div>;
    }
    return <PurchasesPage
    folders={purchases}
    purchases={realPurchases}
    viewMode="history"
  />;
  };

  const showRealPurchases = () => {
    if (realPurchases.length === 0) {
      return <div className='justiy-center flex flex-col items-center w-full' style={{alignItems:'center'}}>No Purchases found</div>;
    }
    return <PurchasesPage
    folders={purchases}
    purchases={realPurchases} 
    viewMode="purchase"
  />;
  };

  const handleTabChange = (e) => {
    if(e=="purchase"){
      setPurchaseTab(true);
    }else{
      setPurchaseTab(false);
    }
  }
  
  return (
    <div className="min-h-screen flex flex-col bg-gray-100 w-full">
      <Header onProfileClick={() => setIsOpen(true)} />
      <main className="flex-grow flex flex-col">
        <div className="flex flex-row gap-5 items-center" style={{marginTop:80,marginBottom:0,alignSelf:'start', paddingLeft:20, paddingBottom:0}}>
          <Button key="purchase" name='purchase' variant="outline" className="flex items-center gap-2" style={{color:(purchaseTab?"#ffffff":"#5479f7"),backgroundColor:(purchaseTab?"#5479f7":"#ffffff")}} onClick={()=>{handleTabChange("purchase")}}>
            <Download className="h-5 w-5" />
              Purchses
          </Button>
          <Button name='suggestions' variant="outline" className="flex items-center gap-2" style={{color:(!purchaseTab?"#ffffff":"#5479f7"),backgroundColor:(!purchaseTab?"#5479f7":"#ffffff")}} onClick={()=>{handleTabChange("suggestions")}}>
            <MessageCircle className="h-5 w-5" />
              Suggestions
          </Button>
        </div>
        <div className="p-4 flex flex-col" style={{marginTop:0,paddingTop:0}}>
          <div className="flex flex-col">  
            {purchaseTab?showRealPurchases():showPurchases()}
          </div>
        </div>
      </main>
      <Drawer open={isOpen} onOpenChange={setIsOpen}>
        <DrawerContent  className="w-[300px] sm:w-[400px]">
          <DrawerHeader className="text-left">
            <DrawerTitle color='#5479f7'>User Profile</DrawerTitle>
          </DrawerHeader>
          <div className="px-4 py-2 flex flex-col items-center">
          <img style={{borderRadius:30}} src={user_.image||"https://lindamood.net/wp-content/uploads/2019/09/Blank-profile-image.jpg"} alt={user_.customer_name} className="w-full h-40 object-cover mb-4" />   
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
