'use client';

import { useState, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
} from "@/components/ui/drawer";
import { Settings, HelpCircle } from 'lucide-react';
import Link from 'next/link';
import { Header } from '../components/header';
import { signOut, useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import PurchasesPage from '../components/purchases-display';

export default function ProfilePage() {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const [purchases, setPurchases] = useState([]);
  const { data: session, status } = useSession();
  const user = session?.user;

  const handleLoadingPurchases = async () => {
    try {
      const response = await fetch('/api/profile/history', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key: user?.id }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch purchases');
      }

      const data = await response.json();

      // Ensure the response is an array
      if (Array.isArray(data)) {
        setPurchases(data as []);
      } else {
        console.error('Unexpected response structure:', data, data.type);
        setPurchases([]);
      }
      console.log('API Response:', data); // Log the response to confirm its structure
    } catch (error) {
      console.error('Error fetching purchases:', error);
    }
  };

  useEffect(() => {
    if (user) {
      handleLoadingPurchases();
    }
  }, [user]);

  if (status === 'loading') return <div>Loading...</div>;
  if (!user) return <div>Not authenticated</div>;

  const handleSignOut = async () => {
    await signOut();
    router.replace('/'); // Use `replace` to prevent going forward
  };

  const showPurchases = () => {
    if (purchases.length === 0) {
      return <div>No purchases found</div>;
    }
    return PurchasesPage(purchases);
  };
  
  return (
    <div className="min-h-screen flex flex-col bg-gray-100 w-full">
      <Header onProfileClick={() => setIsOpen(true)} />
      <main className="flex-grow flex items-center justify-center w-full">
        <div className="p-4 flex flex-col items-center justify-center w-full">
          <div className="flex flex-col items-center justify-center">  
            {showPurchases()}
          </div>
        </div>
      </main>
      <Drawer open={isOpen} onOpenChange={setIsOpen}>
        <DrawerContent  className="w-[300px] sm:w-[400px]">
          <DrawerHeader className="text-left">
            <DrawerTitle>User Profile</DrawerTitle>
            <DrawerDescription>View your profile details here.</DrawerDescription>
          </DrawerHeader>
          <div className="px-4 py-2 flex flex-col items-center">
            <img src={user.image || "/placeholder.svg"} alt={user.name} className="w-full h-40 object-cover mb-4" /> 
            <div className="space-y-4 w-full">
              <div>
                <h3 className="font-medium">Name</h3>
                <p className="text-sm text-gray-500">{user.name}</p>
              </div>
              <div>
                <h3 className="font-medium">Email</h3>
                <p className="text-sm text-gray-500">{user.email}</p>
              </div>
              <div>
                <h3 className="font-medium">Secret Key</h3>
                <p className="text-sm text-gray-500">{user.generated_key}</p>
              </div>
            </div>
          </div>
          <div className="px-4 py-2">
            <nav className="space-y-2">
              <Link href="/settings" className="flex items-center gap-2 p-2 rounded-md hover:bg-gray-100">
                <Settings className="h-5 w-5" />
                <span>Settings</span>
              </Link>
              <Link href="/help" className="flex items-center gap-2 p-2 rounded-md hover:bg-gray-100">
                <HelpCircle className="h-5 w-5" />
                <span>Help</span>
              </Link>
            </nav>
          </div>
          <DrawerFooter>
            <Button variant="destructive" className="w-full" onClick={handleSignOut}>Sign Out</Button>
            <DrawerClose asChild>
              <Button variant="outline">Close</Button>
            </DrawerClose>
          </DrawerFooter>
        </DrawerContent>
      </Drawer>
    </div>
  )
}

