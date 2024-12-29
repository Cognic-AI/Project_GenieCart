import { Button } from "@/components/ui/button"
import { UserCircle } from 'lucide-react'

interface HeaderProps {
  onProfileClick: () => void;
}

export function Header({ onProfileClick }: HeaderProps) {
  return (
    <header className="bg-white shadow-sm w-full fixed top-0 z-50" style={{backgroundColor:'#5479f7'}}>
        <div className="max-w-screen mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center w-full">
            <h1 className="text-2xl font-bold text-white">GenieCart 1.0</h1>
            <Button variant="outline" className="flex items-center gap-2" style={{color:"#5479f7"}} onClick={onProfileClick}>
                <UserCircle className="h-5 w-5" />
                View Profile
            </Button>
        </div>
    </header>
  )
}

